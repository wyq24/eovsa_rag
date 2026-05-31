#!/usr/bin/env python3
"""
Wiki Documentation Scraper
Scrapes wiki pages and saves them as markdown files for the LLM agent
"""

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import html2text
import time
import urllib.parse
from typing import List, Dict
import json

class WikiScraper:
    """Scrape wiki documentation and save as markdown files"""
    
    def __init__(self, base_url: str, output_dir: str = "data/raw/wiki"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure html2text converter
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = False
        self.converter.ignore_emphasis = False
        self.converter.body_width = 0  # Don't wrap lines
        
        # Track scraped URLs to avoid duplicates
        self.scraped_urls = set()
        self.failed_urls = []
        
    def clean_filename(self, title: str) -> str:
        """Clean title to create valid filename"""
        # Remove/replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '_')
        
        # Remove extra whitespace and limit length
        title = '_'.join(title.split())
        return title[:100]  # Limit to 100 characters
    
    def scrape_page(self, url: str, max_retries: int = 3) -> Dict:
        """Scrape a single wiki page"""
        
        if url in self.scraped_urls:
            return {'status': 'skipped', 'reason': 'already_scraped'}
        
        for attempt in range(max_retries):
            try:
                print(f"Scraping: {url} (attempt {attempt + 1})")
                
                # Add delay to be respectful
                time.sleep(1)
                
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_elem = soup.find('title')
                title = title_elem.text.strip() if title_elem else 'Untitled'
                
                # Try to find main content area (common wiki selectors)
                content_selectors = [
                    '#content',           # MediaWiki
                    '.wiki-content',      # Confluence  
                    '.page-content',      # Generic
                    '.main-content',      # Generic
                    'main',               # HTML5
                    '.content'            # Generic
                ]
                
                content_elem = None
                for selector in content_selectors:
                    content_elem = soup.select_one(selector)
                    if content_elem:
                        break
                
                # If no content area found, use body
                if not content_elem:
                    content_elem = soup.find('body')
                
                if not content_elem:
                    return {'status': 'error', 'reason': 'no_content_found'}
                
                # Remove navigation, sidebar, footer elements
                for unwanted in content_elem.select('nav, .navigation, .sidebar, footer, .footer, .toc, .edit-section'):
                    unwanted.decompose()
                
                # Convert HTML to markdown
                html_content = str(content_elem)
                markdown_content = self.converter.handle(html_content)
                
                # Clean up the markdown
                markdown_content = self.clean_markdown(markdown_content)
                
                # Save to file
                filename = self.clean_filename(title) + '.md'
                filepath = self.output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\n")
                    f.write(f"**Source:** {url}\n")
                    f.write(f"**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write(markdown_content)
                
                self.scraped_urls.add(url)
                
                return {
                    'status': 'success',
                    'title': title,
                    'filename': str(filepath),
                    'size': len(markdown_content)
                }
                
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    self.failed_urls.append({'url': url, 'error': str(e)})
                    return {'status': 'error', 'reason': str(e)}
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.failed_urls.append({'url': url, 'error': str(e)})
                return {'status': 'error', 'reason': str(e)}
    
    def clean_markdown(self, markdown: str) -> str:
        """Clean up markdown content"""
        lines = markdown.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove excessive blank lines
            if line.strip() == '' and len(cleaned_lines) > 0 and cleaned_lines[-1].strip() == '':
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def scrape_sitemap(self, sitemap_url: str) -> List[str]:
        """Extract URLs from sitemap.xml"""
        try:
            response = requests.get(sitemap_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
            
            print(f"Found {len(urls)} URLs in sitemap")
            return urls
            
        except Exception as e:
            print(f"Error reading sitemap: {e}")
            return []
    
    def discover_pages(self, start_url: str, max_pages: int = 50) -> List[str]:
        """Discover wiki pages by following links"""
        
        discovered_urls = set()
        to_visit = [start_url]
        visited = set()
        
        while to_visit and len(discovered_urls) < max_pages:
            current_url = to_visit.pop(0)
            
            if current_url in visited:
                continue
                
            visited.add(current_url)
            
            try:
                response = requests.get(current_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    
                    # Convert relative URLs to absolute
                    full_url = urllib.parse.urljoin(current_url, href)
                    
                    # Only include URLs from the same domain
                    if full_url.startswith(self.base_url):
                        discovered_urls.add(full_url)
                        
                        # Add to visit queue if it looks like a wiki page
                        if any(pattern in full_url.lower() for pattern in ['wiki/', 'page/', 'doc/']):
                            if full_url not in visited and full_url not in to_visit:
                                to_visit.append(full_url)
                
                time.sleep(1)  # Be respectful
                
            except Exception as e:
                print(f"Error discovering pages from {current_url}: {e}")
        
        return list(discovered_urls)
    
    def scrape_multiple_pages(self, urls: List[str]) -> Dict:
        """Scrape multiple pages"""
        
        results = {
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'total_size': 0,
            'files': []
        }
        
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing {i}/{len(urls)}: {url}")
            
            result = self.scrape_page(url)
            
            if result['status'] == 'success':
                results['successful'] += 1
                results['total_size'] += result['size']
                results['files'].append(result['filename'])
            elif result['status'] == 'skipped':
                results['skipped'] += 1
            else:
                results['failed'] += 1
        
        return results
    
    def save_log(self):
        """Save scraping log"""
        log_data = {
            'scraped_urls': list(self.scraped_urls),
            'failed_urls': self.failed_urls,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        log_file = self.output_dir / 'scraping_log.json'
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)

# Usage examples
def main():
    """Example usage of the wiki scraper"""
    
    # Example 1: MediaWiki site
    scraper = WikiScraper("https://your-wiki-site.com")
    
    # Method 1: Scrape specific pages
    specific_pages = [
        "https://your-wiki-site.com/wiki/Telescope_Operations",
        "https://your-wiki-site.com/wiki/Maintenance_Procedures",
        "https://your-wiki-site.com/wiki/Troubleshooting_Guide"
    ]
    
    print("Scraping specific pages...")
    results = scraper.scrape_multiple_pages(specific_pages)
    
    # Method 2: Auto-discover pages
    print("\nAuto-discovering pages...")
    discovered_urls = scraper.discover_pages("https://your-wiki-site.com/wiki/Main_Page", max_pages=20)
    results_discovered = scraper.scrape_multiple_pages(discovered_urls)
    
    # Method 3: Use sitemap (if available)
    sitemap_urls = scraper.scrape_sitemap("https://your-wiki-site.com/sitemap.xml")
    if sitemap_urls:
        print(f"\nScraping from sitemap ({len(sitemap_urls)} pages)...")
        results_sitemap = scraper.scrape_multiple_pages(sitemap_urls[:50])  # Limit to first 50
    
    # Save log
    scraper.save_log()
    
    print(f"\nScraping completed!")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Files saved to: {scraper.output_dir}")

if __name__ == "__main__":
    # Interactive mode
    print("Wiki Documentation Scraper")
    print("=" * 30)
    
    base_url = input("Enter your wiki base URL (e.g., https://wiki.example.com): ").strip()
    
    if not base_url:
        print("No URL provided, using example...")
        main()
    else:
        scraper = WikiScraper(base_url)
        
        choice = input("\nChoose method:\n1. Enter specific URLs\n2. Auto-discover from start page\n3. Use sitemap\nChoice (1-3): ")
        
        if choice == "1":
            print("Enter URLs one per line (empty line to finish):")
            urls = []
            while True:
                url = input().strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                results = scraper.scrape_multiple_pages(urls)
                print(f"Scraped {results['successful']} pages successfully")
        
        elif choice == "2":
            start_page = input("Enter starting page URL: ").strip()
            max_pages = int(input("Maximum pages to discover (default 20): ") or "20")
            
            discovered = scraper.discover_pages(start_page, max_pages)
            print(f"Discovered {len(discovered)} pages")
            
            if discovered:
                results = scraper.scrape_multiple_pages(discovered)
                print(f"Scraped {results['successful']} pages successfully")
        
        elif choice == "3":
            sitemap_url = input("Enter sitemap URL (or press enter for /sitemap.xml): ").strip()
            if not sitemap_url:
                sitemap_url = base_url + "/sitemap.xml"
            
            urls = scraper.scrape_sitemap(sitemap_url)
            if urls:
                max_pages = int(input(f"Found {len(urls)} URLs. How many to scrape? (default 50): ") or "50")
                results = scraper.scrape_multiple_pages(urls[:max_pages])
                print(f"Scraped {results['successful']} pages successfully")
        
        scraper.save_log()
        print(f"Files saved to: {scraper.output_dir}")
        print("Scraping log saved to: scraping_log.json")