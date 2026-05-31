#!/usr/bin/env python3
"""Streamlit chat UI for the Enhanced Telescope LLM Agent."""

import argparse
import os
from typing import Dict, List, Optional

import streamlit as st

from llm_agent import EnhancedTelescopeLLMAgent, CHROMADB_AVAILABLE, OPENAI_AVAILABLE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Chat UI for the Enhanced Telescope LLM Agent",
        add_help=False
    )
    parser.add_argument(
        "--collection",
        default=os.getenv("CHROMA_COLLECTION", "telescope_docs"),
        help="Chroma collection name to use"
    )
    parser.add_argument(
        "--db-path",
        dest="db_path",
        default=os.getenv("DB_PATH", "data/vector_db"),
        help="Base path where chunk_metadata.json and the Chroma folder live"
    )
    parser.add_argument(
        "--chroma-path",
        dest="chroma_path",
        default=os.getenv("CHROMA_PATH"),
        help="Direct path to the Chroma directory (overrides db-path if set)"
    )
    parser.add_argument(
        "--top-k",
        dest="top_k",
        type=int,
        default=None,
        help="Maximum documents to retrieve per question"
    )
    parser.add_argument(
        "--model",
        dest="model",
        default=os.getenv("OPENAI_MODEL"),
        help="Model name for chat completions (defaults to OPENAI_MODEL env or agent default)"
    )
    return parser.parse_known_args()[0]


@st.cache_resource(show_spinner=False)
def load_agent(db_path: str, collection: str, top_k: Optional[int],
               chroma_path: Optional[str], model: Optional[str]) -> EnhancedTelescopeLLMAgent:
    if not CHROMADB_AVAILABLE:
        raise RuntimeError("ChromaDB is not available. Install chromadb to enable retrieval.")
    if not OPENAI_AVAILABLE:
        raise RuntimeError("OpenAI client is not available. Install openai to run the agent.")
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    return EnhancedTelescopeLLMAgent(
        db_path=db_path,
        collection_name=collection,
        top_k=top_k,
        chroma_path=chroma_path,
        model=model
    )


def render_sources(sources: List[Dict]) -> None:
    if not sources:
        return

    with st.expander("Sources"):
        for idx, source in enumerate(sources, start=1):
            title = source.get("title", "Unknown")
            source_type = source.get("type", "Unknown")
            st.markdown(f"**{idx}. {title}** ({source_type})")
            meta_parts = []
            if source.get("criticality"):
                meta_parts.append(f"criticality: {source['criticality']}")
            if source.get("has_code"):
                meta_parts.append("contains code")
            if source.get("has_commands"):
                meta_parts.append("commands referenced")
            if meta_parts:
                st.caption(", ".join(meta_parts))
            if source.get("summary"):
                st.markdown(source["summary"])
            if source.get("excerpt"):
                st.code(source["excerpt"])
            st.divider()


def main() -> None:
    args = parse_args()
    default_model = args.model or os.getenv("OPENAI_MODEL", "gpt-5")
    st.set_page_config(page_title="EOVSA LLM Chat", layout="wide")
    st.title("EOVSA Knowledge Chat")
    st.caption("Ask questions about telescope operations, code, and procedures. Follow-ups stay in context.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Session")
        st.write(f"Collection: `{args.collection}`")
        st.write(f"Vector DB: `{args.chroma_path or args.db_path}`")
        st.write(f"Top K: `{args.top_k or 'default'}`")
        model_input = st.text_input("Model", value=default_model)
        include_cross_refs = st.checkbox("Include cross references", value=True)
        if st.button("Reset conversation", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.get("agent"):
                st.session_state.agent.conversation_history = []
            st.rerun()

    model_name = (model_input or default_model).strip()

    try:
        agent = load_agent(
            db_path=args.db_path,
            collection=args.collection,
            top_k=args.top_k,
            chroma_path=args.chroma_path,
            model=model_name
        )
        st.session_state.agent = agent
    except Exception as exc:
        st.error(f"Could not start the agent: {exc}")
        st.info("Ensure the vector DB is built and OPENAI_API_KEY is set.")
        return

    prompt = st.chat_input("Ask about EOVSA operations or code")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                if message.get("confidence") is not None:
                    st.caption(f"Confidence: {message['confidence']:.2f} | Sources: {message.get('total_sources', 0)}")
                if message.get("safety_critical"):
                    st.warning("Safety-critical information included. Follow procedures.")
                render_sources(message.get("sources", []))

    if prompt:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = agent.ask(
                    prompt,
                    include_cross_refs=include_cross_refs,
                    use_history=True
                )
            st.markdown(response["answer"])
            if response.get("confidence") is not None:
                st.caption(f"Confidence: {response['confidence']:.2f} | Sources: {response.get('total_sources', 0)}")
            if response.get("safety_critical"):
                st.warning("Safety-critical information included. Follow procedures.")
            render_sources(response.get("sources", []))

        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"],
            "sources": response.get("sources", []),
            "confidence": response.get("confidence"),
            "total_sources": response.get("total_sources"),
            "safety_critical": response.get("safety_critical", False)
        })


if __name__ == "__main__":
    main()
