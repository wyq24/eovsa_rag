# All-Day Synthesis Issues - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/All-Day_Synthesis_Issues
**Scraped:** 2025-08-05 09:12:38

# All-Day Synthesis Issues

From EOVSA Wiki

Jump to navigation Jump to search

# Correcting for Solar Rotation

Deconvolving solar images integrated over a substantial period of time presents a complex challenge due to at least two effects: 

  * _Solar rotation:_ Sources near disk center are carried from east to west at a rate of about 9 arcsec/hour. Those nearer the limb move very little in the plane of the sky. The rate of rotation is also latitude dependent due to differential solar rotation. This solar-rotation issue is made far more serious by the fact that the psf (point-spread-function, aka synthesized beam) also varies with time.
  * _Intrinsic variations versus time:_ Even without actual flaring, evolution of active region sources in shape and or brightness can occur. In applications not involving aperture synthesis, such evolution is simply averaged out in the familiar way. However, when coupled with the changing psf due to solar rotation these intrinsic variations present a more serious challenge.

One way to overcome these problems, when reasonably good uv-coverage is available, is simply to make images over a shorter time (e.g. 10 min, during which the rotation is less than 2 arcsec), then differentially rotate the images and average them in the image plane. There is some relatively minor problem in doing this, since the emission is distributed at varying heights and one must generally choose a reference height at which to do the rotation. Luckily, the emission near the limbs does not move in the plane of the sky, and so it is not a bad approximation to rotate emission on the disk and leave the emission above the limb unchanged. This "shorter-integration-time" approach is worthwhile with EOVSA when there is relatively bright active region emission that is the focus of the science study, but the fainter disk or off-limb emission is not well imaged in such short integrations. 

In cases where all of the emission is weak, long integrations with EOVSA are required, and this page describes an alternative method for improving image deconvolution in that case. This approach involves creating a spatially variable psf, and hence deconvolving model sources in various parts of the solar disk with the appropriate psf for that location. Software does not yet exist for the entire process, but some exploration is possible with the current software. 

## Description of the Problem

If solar rotation is ignored in an 8-hour integration, say, then sources near disk center will shift 72 arcsec! If the standard psf is used to clean such sources, two errors result: (1) the source is smeared in the east-west direction, appearing larger and fainter than it should, and (2) the psf sidelobes used in the deconvolution are not those created by the moving source, so much larger residuals (and possibly false sources) are left in the image. 

If the correct psf could be calculated and used, however, then applying it would reduce the residuals. Additionally the smearing of the source could be eliminated by restoring with the ideal psf core, which would also restore the true brightness. The problem, though, is that the correct psf varies with location on the solar disk. 

## Calculating the Correct PSF

No matter the shape of the source, assuming for now that it does not evolve with time, the smeared source is a convolution of the true source with an evolving psf that is created by changing uv sampling function of the array. In calculating the standard psf, the "point" in the point-spread-function is considered to be a unit amplitude point source at the phase center (amplitude 1, phase 0). If instead we consider a moving point source (amplitude 1, but shifting phase) when calculating the sythesized beam, then this would create a psf appropriate to that source. This amounts to creating a model visibility database with unit amplitudes, but properly calculated phases. 

Consider the case of a time-dependent shift of the point source in RA and Dec,  d α ( t ) , d δ ( t ) {\displaystyle d\alpha (t),d\delta (t)} ![{\\displaystyle d\\alpha \(t\),d\\delta \(t\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7eaeb2921fc3349612a155d27985fab88e531497). The phase shift to be applied to a uv point with coordinate  u , v {\displaystyle u,v} ![{\\displaystyle u,v}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7e66f4b32a0181923cc1337a5634f38241e5c697) is  ϕ = 2 π [ d α ( t ) u + d δ ( t ) v ] {\displaystyle \phi =2\pi [d\alpha (t)u+d\delta (t)v]} ![{\\displaystyle \\phi =2\\pi \[d\\alpha \(t\)u+d\\delta \(t\)v\]}](https://wikimedia.org/api/rest_v1/media/math/render/svg/8c97bbe9f9cd7f9911550da79b1e223d41cde478) (see [Lecture 9, eqn 3](https://web.njit.edu/~gary/728/Lecture9.html)). Thus, the visibility to be calculated is just  V ( u , v ) = e i ϕ {\displaystyle V(u,v)=e^{i\phi }} ![{\\displaystyle V\(u,v\)=e^{i\\phi }}](https://wikimedia.org/api/rest_v1/media/math/render/svg/d4fc843a0eb13487a3220195cd00a99b25ee81da). 

A complication, of course, is that the psf so calculated is valid only for a source that follows the assumed time-dependent shift, hence it varies with position on the solar disk. A full solution to this problem would be to calculate a different psf for every point in a radio image and then during each step of the cleaning process select the psf corresponding to the position of a particular clean component. An alternative that might be good enough is to divide the solar disk into a finite number of segments, identify which of a selected number of psfs is most appropriate to that location, and apply that psf. 

## An Initial Test of the Idea

At present, there is no CLEAN deconvolution software capable of applying a spatially variable psf. However, the CASA tclean task allows a parameter calcpsf=False. This will then cause tclean to use an existing psf instead of calculating it. Thus, a valid test of the idea might be to select a date when there is a rather bright active region at some heliographic latitude and longitude on the disk, calculate the time-dependent RA, Dec coordinates, and then create a model visibility database that is the same as the MS of the date, but whose visibilities are replaced by  V ( u , v ) = e i ϕ {\displaystyle V(u,v)=e^{i\phi }} ![{\\displaystyle V\(u,v\)=e^{i\\phi }}](https://wikimedia.org/api/rest_v1/media/math/render/svg/d4fc843a0eb13487a3220195cd00a99b25ee81da) with  ϕ {\displaystyle \phi } ![{\\displaystyle \\phi }](https://wikimedia.org/api/rest_v1/media/math/render/svg/72b1f30316670aee6270a28334bdf4f5072cdde4) calculated as above. An image with zero clean iterations will then form the point-spread-function required. The task tclean can then be run on the original data with calcpsf=False, and with a restoring beam specified as the unsmeared psf. 

### Selection of date

A good date that I have already explored is 2018 Jun 23, which has a relatively strong active region source at heliocentric coordinates (x, y) = (290, 103). This has to be converted to heliographic coordinates for a specific time (e.g. 2000 UT). The result (using IDL arcsec2helio procedure) is (lat, lon) = (8.169, 18.009) degrees (N and W). Then the rotation has to be calculated, which I did (using IDL track_h2a procedure) to get (once per hour): 
    
    Heliocentric X, Y offsets
     UT        X (arcsec)      Y (arcsec)
    16:00      251.60518       102.46113
    17:00      260.93304       102.47842
    18:00      270.23273       102.49959
    19:00      279.50323       102.52464
    20:00      288.74353       102.55360
    21:00      297.95264       102.58646
    22:00      307.12958       102.62324
    23:00      316.27335       102.66396
    24:00      325.38297       102.70862
    
These coordinates have to be rotated for the P-angle (354 deg on this date), which gives: 
    
    Geocentric X, Y offsets
     UT        X (arcsec)      Y (arcsec)
    16:00      239.517         128.200
    17:00      248.792         129.192
    18:00      258.038         130.185
    19:00      267.255         131.179
    20:00      276.442         132.174
    21:00      285.597         133.169
    22:00      294.720         134.165
    23:00      303.809         135.161
    24:00      312.865         136.158
    
and finally converted to  d α ( t ) , d δ ( t ) {\displaystyle d\alpha (t),d\delta (t)} ![{\\displaystyle d\\alpha \(t\),d\\delta \(t\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7eaeb2921fc3349612a155d27985fab88e531497). Note that absolute coordinates are not needed, only the relative shift vs. time. Thus, to a good approximation, this is just  d α ( t ) = − ( X ( t ) − X 0 ) / cos ⁡ ( δ 0 ) {\displaystyle d\alpha (t)=-(X(t)-X_{0})/\cos(\delta _{0})} ![{\\displaystyle d\\alpha \(t\)=-\(X\(t\)-X_{0}\)/\\cos\(\\delta _{0}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/3aba288385b474a64a85bc0ceaa82c3e8a6d5616) and  d δ ( t ) = ( Y ( t ) − Y 0 ) {\displaystyle d\delta (t)=(Y(t)-Y_{0})} ![{\\displaystyle d\\delta \(t\)=\(Y\(t\)-Y_{0}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/b55d94df23edb8047b8024746fa7de9e78fb99d2), where  ( X 0 , Y 0 ) {\displaystyle (X_{0},Y_{0})} ![{\\displaystyle \(X_{0},Y_{0}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/41a15ebbd62a57a65bbdc6aaf728011b881614e6) = (276.442,132.174) is the coordinate at 20:00 UT, and  δ 0 {\displaystyle \delta _{0}} ![{\\displaystyle \\delta _{0}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4354a8b3e95ff6fbb81492f2774dfc11b4ef2a44) = 23.42 is the declination of the Sun. This gives the following final result: 
    
    RA/Dec shifts relative to 20:00 UT
      UT        dRA         dDec
    16:00     40.1859     -3.97398
    17:00     30.0920     -2.98175
    18:00     20.0289     -1.98862
    19:00      9.9979     -0.99468
    20:00      0.0000      0.00000
    21:00     -9.9637      0.99529
    22:00    -19.8921      1.99112
    23:00    -29.7841      2.98740
    24:00    -39.6388      3.98402
    
The above hourly positions can be interpolated to finer timescales. 

### Implementation

I have written a routine to use the above table for this specific date and overwrite the data in a copy of a UDB ms with a unit source amplitude and the correct shifted phase. The two figures below show the comparison of the original psf and the smeared one. It should be noted that the smeared psf has the caustic sort of shape that looks like the residuals in the full-disk maps. 

[![](/wiki/images/e/e6/20180623_7-14_originalpsf.png)](/wiki/index.php/File:20180623_7-14_originalpsf.png)

[](/wiki/index.php/File:20180623_7-14_originalpsf.png "Enlarge")

**Fig. 1:** Original PSF for an mfs image of bands 7-14 on 2018 Jun 23 has unit amplitude and is only three pixels wide, with relatively small and symmetric sidelobes. Each cell here is 2.5".

[![](/wiki/images/4/42/20180623_7-14_smearedpsf.png)](/wiki/index.php/File:20180623_7-14_smearedpsf.png)

[](/wiki/index.php/File:20180623_7-14_smearedpsf.png "Enlarge")

**Fig. 2:** Smeared PSF for the same data as in Fig. 1 has a peak amplitude of about 0.34 and has sidelobes with a caustic pattern much like what we see in the full-disk images.

To test it, I renamed the .image file (which is the smeared psf) to have a .psf extension, and kept it and the .sumwt file, and then tried using tclean with the calcpsf parameter set to False. The entire tclean command was: 
    
    tclean(vis="/data1/eovsa/fits/UDBms_slfcaled/201806/UDB20180623.ms",selectdata=True,field="",spw="7~14",
       timerange="16:00:00~24:00:00",uvrange=">0.25Klambda",antenna="0~12",scan="",observation="",intent="",
       datacolumn="data",imagename="7-14psf-new",imsize=[1024],cell=['2.5arcsec'],phasecenter="",
       stokes="XX",projection="SIN",startmodel="",specmode="mfs",reffreq="",
       nchan=-1,start="",width="",outframe="LSRK",veltype="radio",
       restfreq=[],interpolation="linear",gridder="standard",facets=1,chanchunks=1,
       wprojplanes=1,vptable="",usepointing=False,mosweight=True,aterm=True,
       psterm=False,wbawp=True,conjbeams=False,cfcache="",computepastep=360.0,
       rotatepastep=360.0,pblimit=0.2,normtype="flatnoise",deconvolver="multiscale",scales=[0, 5, 15, 30],
       nterms=2,smallscalebias=0.6,restoration=True,restoringbeam=['10.0arcsec', '8.0arcsec', '150deg'],pbcor=False,
       outlierfile="",weighting="uniform",robust=0.5,npixels=0,uvtaper=[_],_
       niter=200,gain=0.1,threshold=0.0,nsigma=0.0,cycleniter=-1,
       cyclefactor=1.0,minpsffraction=0.05,maxpsffraction=0.8,interactive=False,usemask="auto-multithresh",
       mask="",pbmask=0.0,sidelobethreshold=3.0,noisethreshold=5.0,lownoisethreshold=1.5,
       negativethreshold=0.0,smoothfactor=1.0,minbeamfrac=0.3,cutthreshold=0.01,growiterations=75,
       dogrowprune=True,minpercentchange=-1.0,verbose=False,restart=True,savemodel="none",
       calcres=True,calcpsf=False,parallel=False)
    
Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=All-Day_Synthesis_Issues&oldid=5922](http://ovsa.njit.edu//wiki/index.php?title=All-Day_Synthesis_Issues&oldid=5922)"
