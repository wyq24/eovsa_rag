# Antenna Position - EOVSA Wiki

**Source:** https://www.ovsa.njit.edu/wiki/index.php/Antenna_Position
**Scraped:** 2025-08-05 09:13:22

# Antenna Position

From EOVSA Wiki

Jump to navigation Jump to search

## Fundamentals

A synthesis imaging radio instrument consists of a number of radio elements (radio dishes, dipoles, or other collectors of radio emission), which represent measurement points in _u,v,w_ space. We need to describe how to convert an array of dishes on the ground to a set of points in _u,v,w_ space. 

### _E, N, U_ coordinates to _x, y, z_

The first step is to determine a consistent coordinate system. Antennas are typically measured in units such as meters along the ground. We will use a right-handed coordinate system of _**East**_ , _**North**_ , and _**Up**_ _**(E, N, U)**_. These coordinates are relative to the local horizon, however, and will change depending on where we are on the spherical Earth. It is convenient in astronomy to use a coordinate system aligned with the Earth's rotational axis, for which we will use coordinates _**(x, y, z)**_ as shown in **Figure 1**. Conversion from _(E, N, U)_ to _(x, y, z)_ is done via a simple rotation matrix: 

[![](/wiki/images/0/02/Coords_Antenna_position_wiki_fig1.gif)](/wiki/index.php/File:Coords_Antenna_position_wiki_fig1.gif)

[](/wiki/index.php/File:Coords_Antenna_position_wiki_fig1.gif "Enlarge")

**Fig. 1:** The relationship between _E, N, U_ coordinates and _x, y, z_ coordinates, for a latitude  λ {\displaystyle \lambda } ![{\\displaystyle \\lambda }](https://wikimedia.org/api/rest_v1/media/math/render/svg/b43d0ea3c9c025af1be9128e62a18fa74bedda2a). The direction of _z_ is parallel to the direction to the celestial pole. The directions _y_ and _E_ are the same direction.

[ x y z ] = [ 0 − sin ⁡ λ cos ⁡ λ 1 0 0 0 cos ⁡ λ sin ⁡ λ ] [ E N U ] {\displaystyle {\begin{bmatrix}x\\\y\\\z\\\\\end{bmatrix}}={\begin{bmatrix}0&-\sin \lambda &\cos \lambda \\\1&0&0\\\0&\cos \lambda &\sin \lambda \\\\\end{bmatrix}}{\begin{bmatrix}E\\\N\\\U\\\\\end{bmatrix}}} ![{\\displaystyle {\\begin{bmatrix}x\\\\y\\\\z\\\\\\end{bmatrix}}={\\begin{bmatrix}0&-\\sin \\lambda &\\cos \\lambda \\\\1&0&0\\\\0&\\cos \\lambda &\\sin \\lambda \\\\\\end{bmatrix}}{\\begin{bmatrix}E\\\\N\\\\U\\\\\\end{bmatrix}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/15c787355b4bb1653f1146834b1af58a8bc7406f)

which yields the relations: 

x = − N sin ⁡ λ + U cos ⁡ λ y = E z = N cos ⁡ λ + U sin ⁡ λ {\displaystyle {\begin{aligned}x&=-N\sin \lambda +U\cos \lambda \\\y&=E\\\z&=N\cos \lambda +U\sin \lambda \end{aligned}}} ![{\\displaystyle {\\begin{aligned}x&=-N\\sin \\lambda +U\\cos \\lambda \\\\y&=E\\\\z&=N\\cos \\lambda +U\\sin \\lambda \\end{aligned}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/5591675c75147e28bcc7a2118bc2d1d43443c8b8)

### Baselines and Spatial Frequencies

Note that the baselines are differences of coordinates, i.e. for the baseline between two antennas we have a vector: 

[![](/wiki/images/3/34/Interferometer3_Antenna_position_wiki_fig2.gif)](/wiki/index.php/File:Interferometer3_Antenna_position_wiki_fig2.gif)

[](/wiki/index.php/File:Interferometer3_Antenna_position_wiki_fig2.gif "Enlarge")

**Fig. 2:** Geometry of an interferometer baseline where a delay  τ {\displaystyle \tau } ![{\\displaystyle \\tau }](https://wikimedia.org/api/rest_v1/media/math/render/svg/38a7dcde9730ef0853809fefc18d88771f95206c) is inserted in one antenna, in order to steer the phase center to a direction  θ o {\displaystyle \theta _{o}} ![{\\displaystyle \\theta _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2645aeefe20a7318a6baffa7ee02bd25f5ad22c6) from the vertical  λ {\displaystyle \lambda } ![{\\displaystyle \\lambda }](https://wikimedia.org/api/rest_v1/media/math/render/svg/b43d0ea3c9c025af1be9128e62a18fa74bedda2a).

B → = ( B x , B y , B z ) = ( x 2 − x 1 , y 2 − y 1 , z 2 − z 1 ) {\displaystyle {\vec {B}}=(B_{x},B_{y},B_{z})=(x_{2}-x_{1},y_{2}-y_{1},z_{2}-z_{1})} ![{\\displaystyle {\\vec {B}}=\(B_{x},B_{y},B_{z}\)=\(x_{2}-x_{1},y_{2}-y_{1},z_{2}-z_{1}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/5b693a84eb6c149e89190ea7701171cd9fa1fbd0)

This vector difference in positions can point in any direction in space, but the part of the baseline that matters in calculating _u,v,w_ is the component perpendicular to the direction  θ o {\displaystyle \theta _{o}} ![{\\displaystyle \\theta _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2645aeefe20a7318a6baffa7ee02bd25f5ad22c6) (the phase center direction), which we called  B p r o j {\displaystyle B_{proj}} ![{\\displaystyle B_{proj}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/1f377807439feffbe7e6245ae5540087f23622d3) in **Figure 2**. Let us express the phase center direction as a unit vector ** s o → {\displaystyle {\vec {s_{o}}}} ![{\\displaystyle {\\vec {s_{o}}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/b6eb35ace6d8c09cf325886aaed573e2f9b1bf3d)** = ( h o , δ o ) {\displaystyle =(h_{o},\delta _{o})} ![{\\displaystyle =\(h_{o},\\delta _{o}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f3db5fcc175425014bd7657138f9c01b7c9cff54), where  h o {\displaystyle h_{o}} ![{\\displaystyle h_{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/061fe3db70e941c0ab1da72710043d669ef38b9a) is the hour angle (relative to the local meridian) and  δ o {\displaystyle \delta _{o}} ![{\\displaystyle \\delta _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/5224006dbcb2d7dbdca72b259f28313961ea2000) is the declination (relative to the celestial equator). Then  B p r o j = B → ⋅ s o → = B cos ⁡ θ o {\displaystyle B_{proj}={\vec {B}}\cdot {\vec {s_{o}}}=B\cos \theta _{o}} ![{\\displaystyle B_{proj}={\\vec {B}}\\cdot {\\vec {s_{o}}}=B\\cos \\theta _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/45bf6616fdd35c24d6b2476b532d056289fd6916). 

Recall that the spatial frequencies _u,v,w_ are just the distances expressed in wavelength units, so we can get the _u,v,w_ coordinates from the baseline length expressed in wavelength units from the following coordinate transformation ([see Thompson 1999 for details](http://adsabs.harvard.edu/abs/1999ASPC..180...11T)): 

[ u v w ] = B λ → ⋅ s o → = ( 1 / λ ) [ sin ⁡ h o cos ⁡ h o 0 − sin ⁡ δ o cos ⁡ h o sin ⁡ δ o sin ⁡ h o cos ⁡ δ o cos ⁡ δ o cos ⁡ h o − cos ⁡ δ o sin ⁡ h o sin ⁡ δ o ] [ B x B y B z ] {\displaystyle {\begin{bmatrix}u\\\v\\\w\\\\\end{bmatrix}}={\vec {B_{\lambda }}}\cdot {\vec {s_{o}}}=(1/\lambda ){\begin{bmatrix}\sin h_{o}&\cos h_{o}&0\\\\-\sin \delta _{o}\cos h_{o}&\sin \delta _{o}\sin h_{o}&\cos \delta _{o}\\\\\cos \delta _{o}\cos h_{o}&-\cos \delta _{o}\sin h_{o}&\sin \delta _{o}\\\\\end{bmatrix}}{\begin{bmatrix}B_{x}\\\B_{y}\\\B_{z}\end{bmatrix}}} ![{\\displaystyle {\\begin{bmatrix}u\\\\v\\\\w\\\\\\end{bmatrix}}={\\vec {B_{\\lambda }}}\\cdot {\\vec {s_{o}}}=\(1/\\lambda \){\\begin{bmatrix}\\sin h_{o}&\\cos h_{o}&0\\\\-\\sin \\delta _{o}\\cos h_{o}&\\sin \\delta _{o}\\sin h_{o}&\\cos \\delta _{o}\\\\\\cos \\delta _{o}\\cos h_{o}&-\\cos \\delta _{o}\\sin h_{o}&\\sin \\delta _{o}\\\\\\end{bmatrix}}{\\begin{bmatrix}B_{x}\\\\B_{y}\\\\B_{z}\\end{bmatrix}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/16d0bd062fc69f368e9f2972257f279910287be1) ( 1 ) {\displaystyle (1)} ![{\\displaystyle \(1\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/a25115739469707c4758b189fe310a750092a80a)

### How baseline errors can contribute to the error in phase

The geometric phase difference at the phase center ( w {\displaystyle w} ![{\\displaystyle w}](https://wikimedia.org/api/rest_v1/media/math/render/svg/88b1e0c8e1be5ebe69d18a8010676fa42d7961e6) term in (1)) is: 

ϕ g = 2 π τ g ν = ( 2 π / λ ) [ B x cos ⁡ δ o cos ⁡ h o − B y cos ⁡ δ o sin ⁡ h o + B z sin ⁡ δ o ] {\displaystyle \phi _{g}=2\pi \tau _{g}\nu =(2\pi /\lambda )[B_{x}\cos \delta _{o}\cos h_{o}-B_{y}\cos \delta _{o}\sin h_{o}+B_{z}\sin \delta _{o}]} ![{\\displaystyle \\phi _{g}=2\\pi \\tau _{g}\\nu =\(2\\pi /\\lambda \)\[B_{x}\\cos \\delta _{o}\\cos h_{o}-B_{y}\\cos \\delta _{o}\\sin h_{o}+B_{z}\\sin \\delta _{o}\]}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2b74473ae701f4c967fd59333b0fcfa3988aea64)

where  τ g = B → ⋅ s → / c {\displaystyle \tau _{g}={\vec {B}}\cdot {\vec {s}}/c} ![{\\displaystyle \\tau _{g}={\\vec {B}}\\cdot {\\vec {s}}/c}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0f6ef67f5122d6aad3af1328352884dcda95cf96), geometric delay. We can see what can affect the geometric phase by taking the differential of this expression: 

d ϕ g = 2 π ν d τ g = ( 2 π / λ ) [ d B x cos ⁡ δ o cos ⁡ h o − d B y cos ⁡ δ o sin ⁡ h o + d B z sin ⁡ δ o + d α o cos ⁡ δ o ( B x sin ⁡ h o + B y cos ⁡ h o ) + d δ o ( − B x cos ⁡ h o sin ⁡ δ o + B y sin ⁡ h o sin ⁡ δ o + B z cos ⁡ δ o ) ] {\displaystyle {\begin{aligned}d\phi _{g}=2\pi \nu d\tau _{g}=(2\pi /\lambda )[&dB_{x}\cos \delta _{o}\cos h_{o}-dB_{y}\cos \delta _{o}\sin h_{o}+dB_{z}\sin \delta _{o}\\\\+\ &d\alpha _{o}\cos \delta _{o}(B_{x}\sin h_{o}+B_{y}\cos h_{o})\\\\+\ &d\delta _{o}(-B_{x}\cos h_{o}\sin \delta _{o}+B_{y}\sin h_{o}\sin \delta _{o}+B_{z}\cos \delta _{o})]\end{aligned}}} ![{\\displaystyle {\\begin{aligned}d\\phi _{g}=2\\pi \\nu d\\tau _{g}=\(2\\pi /\\lambda \)\[&dB_{x}\\cos \\delta _{o}\\cos h_{o}-dB_{y}\\cos \\delta _{o}\\sin h_{o}+dB_{z}\\sin \\delta _{o}\\\\+\\ &d\\alpha _{o}\\cos \\delta _{o}\(B_{x}\\sin h_{o}+B_{y}\\cos h_{o}\)\\\\+\\ &d\\delta _{o}\(-B_{x}\\cos h_{o}\\sin \\delta _{o}+B_{y}\\sin h_{o}\\sin \\delta _{o}+B_{z}\\cos \\delta _{o}\)\]\\end{aligned}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/210ab11a3cb2bcba431a38f77cca793fe73fe3ab) ( 2 ) {\displaystyle (2)} ![{\\displaystyle \(2\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/43f88fdd4acbb57a291f9eb9f23ae23a1e492b30)

where we have used the relation between right ascension and hour angle:  h o = L S T − α o {\displaystyle h_{o}=LST-\alpha _{o}} ![{\\displaystyle h_{o}=LST-\\alpha _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e83c5e107d0aabee428b7f9089556d4436a5fe11), so  d h o = − d α o {\displaystyle dh_{o}=-d\alpha _{o}} ![{\\displaystyle dh_{o}=-d\\alpha _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/be8a5831851457487be23aef23144a60a2b9f67e). Equation (2) shows how baseline errors  ( d B x , d B y , d B z ) {\displaystyle (dB_{x},dB_{y},dB_{z})} ![{\\displaystyle \(dB_{x},dB_{y},dB_{z}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2e140451dfd3afdcfd2775635dcfafa6c36c3dd5) and source position errors ( α o {\displaystyle \alpha _{o}} ![{\\displaystyle \\alpha _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/6b97ca5af177111e7be85910a51bf682ed2225fa),  δ o {\displaystyle \delta _{o}} ![{\\displaystyle \\delta _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/5224006dbcb2d7dbdca72b259f28313961ea2000)) will affect the error in group delay  d τ g {\displaystyle d\tau _{g}} ![{\\displaystyle d\\tau _{g}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/85f6d2e69cfc482ecad98bde1721f838f3180110) (or yield an error in phase  d ϕ g {\displaystyle d\phi _{g}} ![{\\displaystyle d\\phi _{g}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/57ece57c598d9829a24e8102525ba0d07584e42a)). Note that a clock error is equivalent to a source position error  d α o {\displaystyle d\alpha _{o}} ![{\\displaystyle d\\alpha _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0ba7cf44951e23944858ab8d15e47983f7814d7f). 

If we have a source whose position is known, we can use Equation (2) to find the location of the antennas (this is called _**baseline determination**_). The error in antenna position is largely independent of the baseline lengths. For example, say that we can measure  d ϕ g {\displaystyle d\phi _{g}} ![{\\displaystyle d\\phi _{g}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/57ece57c598d9829a24e8102525ba0d07584e42a) to within 1 degree at 5 GHz ( λ {\displaystyle \lambda } ![{\\displaystyle \\lambda }](https://wikimedia.org/api/rest_v1/media/math/render/svg/b43d0ea3c9c025af1be9128e62a18fa74bedda2a) = 6 cm). Then we can measure  d B x {\displaystyle dB_{x}} ![{\\displaystyle dB_{x}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7644579cc01fb880811e48120dd324d371c41c45),  d B y {\displaystyle dB_{y}} ![{\\displaystyle dB_{y}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/cb5026327c62f1df18757ab259b2282a42829bfc) and  d B z {\displaystyle dB_{z}} ![{\\displaystyle dB_{z}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/b24fc3277e8ff4b4ebb0555c4db74cb1c749008b) to a precision of order (1 / 360) 6 cm ~ 1 / 60 cm even though  B = ( B x 2 + B y 2 + B z 2 ) 1 / 2 {\displaystyle B=(B_{x}^{2}+B_{y}^{2}+B_{z}^{2})^{1/2}} ![{\\displaystyle B=\(B_{x}^{2}+B_{y}^{2}+B_{z}^{2}\)^{1/2}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/9c7eb062150e72efa4623c9baf7a9a7972a5606f) = 5000 km or more (VLBI). 

The time of day and location of the antennas must be known to relatively high accuracy -- needed for determining the geometric delay. A clock error of 1 s, or a baseline error of a few cm, will cause a serious phase shift of the source over, say, 10 minutes. At OVRO, using a GPS clock and measuring baselines with cosmic source calibration, we get a time accuracy of << 1 ms, and baseline errors of about 3 mm. Therefore, these effects are not serious over a short time interval, but may still be problematic over 8 hours. This is one reason that we do phase calibration observations every ~ 2 hours. 

## EOVSA Antenna Position Calibration

The positions of EOVSA antennas are determined using observations by the 27-m (Ant 14) low-frequency receiver (S and C band) of celestial radio sources during several observation runs in fall 2016. This document describes the procedure followed and the final? calibrated antenna positions. 

For calibrator sources with locations with sufficient accuracy (we use caibrators from the [VLA Calibrator Manual](http://www.aoc.nrao.edu/~gtaylor/csource.html)), and a good time-keeping accuracy at EOVSA (what is our time-keeping accuracy? --[Bchen](/wiki/index.php?title=User:Bchen&action=edit&redlink=1 "User:Bchen \(page does not exist\)") 19 November 2016) ,  d α o {\displaystyle d\alpha _{o}} ![{\\displaystyle d\\alpha _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0ba7cf44951e23944858ab8d15e47983f7814d7f) and  d δ o {\displaystyle d\delta _{o}} ![{\\displaystyle d\\delta _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2670710a4e9f4e053bdc2fde504b987be79a6779) in Eq. 2 can be neglected. Hence Eq. 2 can be simplified to: 

ϕ g = ϕ o + ( 2 π / λ ) ( d B x cos ⁡ δ cos ⁡ h − d B y cos ⁡ δ sin ⁡ h + d B z sin ⁡ δ ) {\displaystyle \phi _{g}=\phi _{o}+(2\pi /\lambda )(dB_{x}\cos \delta \cos h-dB_{y}\cos \delta \sin h+dB_{z}\sin \delta )} ![{\\displaystyle \\phi _{g}=\\phi _{o}+\(2\\pi /\\lambda \)\(dB_{x}\\cos \\delta \\cos h-dB_{y}\\cos \\delta \\sin h+dB_{z}\\sin \\delta \)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/69ada7aec4f345a9e53c5a46b7d5326bcc3950e2), (3) 

where  ϕ o {\displaystyle \phi _{o}} ![{\\displaystyle \\phi _{o}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f1147b75ad0a7d963189e1187a38a7b48ce3ec7a) is the intrinsic instrumental phase at the given baseline. 

We use a two-step calibration to solve for the EOVSA baseline error as following: 

### 1\. Determine baseline errors in X and Y

Observing one strong and point-like calibrator for a sufficiently long time (at least several hours). Note it is important to observe for a long time in order to have sufficient variation of the phase vs. hour angle curve as determined by sin(h) and cos(h). We use a function of the following form to fit the observed phases at a baseline involving antenna i and j: 

ϕ i j = ( 2 π / λ ) ( c 0 + c 1 cos ⁡ h + c 2 sin ⁡ h ) {\displaystyle \phi _{ij}=(2\pi /\lambda )(c_{0}+c_{1}\cos h+c_{2}\sin h)} ![{\\displaystyle \\phi _{ij}=\(2\\pi /\\lambda \)\(c_{0}+c_{1}\\cos h+c_{2}\\sin h\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f5eef7957bb368aa25e95a369823e447ed6c620c)

where 

c 0 = ϕ o i j / ( 2 π / λ ) + sin ⁡ δ ( d B z i − d B z j ) c 1 = cos ⁡ δ ( d B x i − d B x j ) c 2 = − cos ⁡ δ ( d B y i − d B y j ) {\displaystyle {\begin{aligned}c_{0}&=\phi _{oij}/(2\pi /\lambda )+\sin \delta (dB_{zi}-dB_{zj})\\\c_{1}&=\cos \delta (dB_{xi}-dB_{xj})\\\c_{2}&=-\cos \delta (dB_{yi}-dB_{yj})\end{aligned}}} ![{\\displaystyle {\\begin{aligned}c_{0}&=\\phi _{oij}/\(2\\pi /\\lambda \)+\\sin \\delta \(dB_{zi}-dB_{zj}\)\\\\c_{1}&=\\cos \\delta \(dB_{xi}-dB_{xj}\)\\\\c_{2}&=-\\cos \\delta \(dB_{yi}-dB_{yj}\)\\end{aligned}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/327ed5145bfd7f7cecb059a1bd656d12ae28f436) (4) 

In a usual case, visibilities are measured at many baselines (e.g., for N antennas one would normally have N(N-1)/2 unique baselines). In that case, one can solve for the antenna-based phase  ϕ i {\displaystyle \phi _{i}} ![{\\displaystyle \\phi _{i}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0182dbf29b54844c92fd9b0311778a02a38398ec) as a function of hour angle for each antenna i. The resulted fit parameters c1 and c2 then only involve the absolute position error dBi for antenna i. For EOVSA, we only have one 27-m antenna in the array, so we have to use the 13 baseline-based phases  ϕ i − 14 {\displaystyle \phi _{i-14}} ![{\\displaystyle \\phi _{i-14}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/3e6f8e8f387ca8887ed729ff6101e8cb41399293) to solve for  d B ( x , y , z ) i − d B ( x , y , z ) 14 {\displaystyle dB_{(x,y,z)i}-dB_{(x,y,z)14}} ![{\\displaystyle dB_{\(x,y,z\)i}-dB_{\(x,y,z\)14}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/9fbea1a30dd5ee35db4570eb46354bd6fdf89956). For simplification, I will omit the subscripts (i-14) In the following discussions. 

For each antenna i-14 baseline pair, we have two unique polarization measurements. To take advantage of both polarization measurements, we fit the following equations separately: 

ϕ X X + ϕ Y Y = ( 2 π / λ ) ( c 0 X X + c 0 Y Y + 2 c 1 cos ⁡ h + 2 c 2 sin ⁡ h ) ϕ X X − ϕ Y Y = ( 2 π / λ ) ( c 0 X X − c 0 Y Y ) {\displaystyle {\begin{aligned}\phi _{XX}+\phi _{YY}&=(2\pi /\lambda )(c_{0XX}+c_{0YY}+2c_{1}\cos h+2c_{2}\sin h)\\\\\phi _{XX}-\phi _{YY}&=(2\pi /\lambda )(c_{0XX}-c_{0YY})\end{aligned}}} ![{\\displaystyle {\\begin{aligned}\\phi _{XX}+\\phi _{YY}&=\(2\\pi /\\lambda \)\(c_{0XX}+c_{0YY}+2c_{1}\\cos h+2c_{2}\\sin h\)\\\\\\phi _{XX}-\\phi _{YY}&=\(2\\pi /\\lambda \)\(c_{0XX}-c_{0YY}\)\\end{aligned}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/80cfa8071823cdb23234ce02a8f3516b0575745c) (5) 

and obtain the four parameters  c 0 X X {\displaystyle c_{0XX}} ![{\\displaystyle c_{0XX}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/77a1a084a739a732e2dedb655981e7cc41a10c13),  c 0 Y Y {\displaystyle c_{0YY}} ![{\\displaystyle c_{0YY}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/c96df0350e9c8ca24cddd6f4bc32cfd7ff38f2b9),  c 1 {\displaystyle c_{1}} ![{\\displaystyle c_{1}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/77b7dc6d279091d354e0b90889b463bfa7eb7247), and  c 2 {\displaystyle c_{2}} ![{\\displaystyle c_{2}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0b30ba1b247fb8d334580cec68561e749d24aff2). The baseline error for antenna i (relative to antenna 14) is then: 

d B x = c 1 cos ⁡ δ d B y = − c 2 cos ⁡ δ {\displaystyle {\begin{aligned}dB_{x}&={\frac {c_{1}}{\cos \delta }}\\\dB_{y}&=-{\frac {c_{2}}{\cos \delta }}\\\\\end{aligned}}} ![{\\displaystyle {\\begin{aligned}dB_{x}&={\\frac {c_{1}}{\\cos \\delta }}\\\\dB_{y}&=-{\\frac {c_{2}}{\\cos \\delta }}\\\\\\end{aligned}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/ae0a2a58c000363c918c0478d29622d7ce68bf20) (6) 

An example is given in Fig. 3 based on a 5.5-hr observation on 3C84 made on 2016 Sep 7 using EOVSA band 5 only (7 usable science channels). 

[![](/wiki/images/e/e3/Pha_vs_ha_0319%2B415_20160907.png)](/wiki/index.php/File:Pha_vs_ha_0319%2B415_20160907.png)

[](/wiki/index.php/File:Pha_vs_ha_0319%2B415_20160907.png "Enlarge")

**Fig. 3:** Phase vs. hour angle for Antennas 9, 10, 11, 13 w.r.t. Antenna 14 at both XX and YY polarizations. This is based on a ~5.5 hour observation of 3C84 on 2016 Sep 7. Circular symbols are measured phases and curves are the corresponding sinusoidal curves. Different colors represent measurements/fits at different frequency channels.

After  d B x , d B y {\displaystyle dB_{x},dB_{y}} ![{\\displaystyle dB_{x},dB_{y}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e2aeeee3872bb60b344bf548ed47c2cc0e65f00e) are determined, they can be applied to the visibility date to correct for the sinusoidal variation of the phase vs. hour angle. I use CASA's task "gencal" to generate the calibration table for antenna position correction (use mode="antpos"). However, the task requires corrections of the antenna positions in the ITRF (International Terrestrial Reference Frame) coordinate system (see [gencal help page](https://casa.nrao.edu/docs/taskref/gencal-task.html) for details). The X-axis of this system points to prime meridian, i.e., the big circle along zero longitude, while the X-axis of our local Cartesian x, y, z system points to the local central meridian. Therefore we have to rotate the derived  d B x , d B y {\displaystyle dB_{x},dB_{y}} ![{\\displaystyle dB_{x},dB_{y}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e2aeeee3872bb60b344bf548ed47c2cc0e65f00e) by EOVSA's longitude (118.287° west, or -118.287°) to get the new  d B x ′ , d B y ′ {\displaystyle dB_{x}',dB_{y}'} ![{\\displaystyle dB_{x}',dB_{y}'}](https://wikimedia.org/api/rest_v1/media/math/render/svg/897514584ed4f9b815ed1c4831201c42a32fe96b) in the ITRF system: 

d B x ′ = d B x cos ⁡ ( l ) − d B y sin ⁡ ( l ) d B y ′ = d B x sin ⁡ ( l ) + d B y cos ⁡ ( l ) {\displaystyle {\begin{aligned}dB_{x'}&=dB_{x}\cos(l)-dB_{y}\sin(l)\\\dB_{y'}&=dB_{x}\sin(l)+dB_{y}\cos(l)\\\\\end{aligned}}} ![{\\displaystyle {\\begin{aligned}dB_{x'}&=dB_{x}\\cos\(l\)-dB_{y}\\sin\(l\)\\\\dB_{y'}&=dB_{x}\\sin\(l\)+dB_{y}\\cos\(l\)\\\\\\end{aligned}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/eea7b6a762c01d46a08c01875c3e58719e860b73) (7) 

Each antenna should have three inputs in "parameter":  d B x ′ , d B y ′ , d B z ′ {\displaystyle dB_{x}',dB_{y}',dB_{z}'} ![{\\displaystyle dB_{x}',dB_{y}',dB_{z}'}](https://wikimedia.org/api/rest_v1/media/math/render/svg/b1dd90e19af0a70f7666253f2d09d941da7ea9e3). For now we set  d B z ′ {\displaystyle dB_{z}'} ![{\\displaystyle dB_{z}'}](https://wikimedia.org/api/rest_v1/media/math/render/svg/c26209f49b919cc74826506ad7d525fc5a03e9a0) to be 0, which will be determined in the next step. An example of generating a calibration table and apply the corrections for the positions of antenna IDs 8 and 9 (that is, Ant 9 and 10): 
    
    gencal(vis=your_ms_visibility,caltable='caltb.antpos',caltype='antpos',
                antenna='8, 9', parameter=[dBx'_9, dBy'_9, 0, dBx'_10, dBy'_10, 0])
    applycal(vis=your_ms_visibility,gaintable='caltb.antpos')
    
The results after applying the Bx and By correction are shown in Fig. 4: 

[![](/wiki/images/1/13/Pha_vs_ha_0319%2B415_20160907_corrected.png)](/wiki/index.php/File:Pha_vs_ha_0319%2B415_20160907_corrected.png)

[](/wiki/index.php/File:Pha_vs_ha_0319%2B415_20160907_corrected.png "Enlarge")

**Fig. 4:** Corrected phase vs. hour angle for Antennas 9, 10, 11, 13 w.r.t. Antenna 14 at both XX and YY polarizations. This is based on a ~5.5 hour observation of 3C84 on 2016 Sep 7. Different colors represent measurements/fits at different frequency channels.

Each frequency channel has an independent measurement of the correlated phases (note the wavelength λ in Eq. 3 is different). But they should return the same answer of dBx and dBy. Previously I selected 6 channels in Band 5 and fit them independently, and took the average of the resulted dBx and dBy to be the answer. This worked pretty well for the 2016 Sep 7 observation on 3C84, which is a very strong calibrator source (23 Jy in C band) and we observed band 5 in a sit-and-stare mode, hence the signal-to-noise was excellent at all channels (results are shown in Figs. 3 and 4). However, for calibrators that are not so strong and/or the array in a fast-frequency-tuning mode, the signal-to-noise is not so good. Fitting all channels independently would result in different answers, especially for those with small baseline errors. An example is shown in Fig. 5 for an observation on 2016 Oct 9 on 2253+161 using the fast frequency-sweeping mode. It is desired to take data from all channels and fit for the same c1 and c2 (which are determined by dBx and dBy respectively), but different c0 parameter in Eq. 4 (because different channels have different phase offsets). I have implemented such a technique using [SciPy's "leastsq" function](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.leastsq.html). I applied this method to an observation of 2136+006 (9.9 Jy at C band) and 2253+161 (10 Jy at C band) on 2016 Sep 7 under the fast frequency-sweeping mode of the 27-m low-frequency receiver. The results are shown in Fig. 6. 

  * [![](/wiki/images/f/f5/Pha_vs_ha_2253%2B161_20161009_independent_fits.png)](/wiki/index.php/File:Pha_vs_ha_2253%2B161_20161009_independent_fits.png)

Phase vs. hour angle for Antennas 9, 10, 11, 13 w.r.t. Antenna 14 at both XX and YY polarizations. Fits are done on each channel independently. 

  * [![](/wiki/images/e/ee/Pha_vs_ha_2253%2B161_20161009_one_fit.png)](/wiki/index.php/File:Pha_vs_ha_2253%2B161_20161009_one_fit.png)

Phase vs. hour angle for Antennas 9, 10, 11, 13 w.r.t. Antenna 14 at both XX and YY polarizations. Fits are done on all channels simultaneously. 

Table 1: Calculated Baseline Corrections in X and Y   
---  
Antenna  | dBx (m)  | dBy (m)   
3C84 | 2136+006 | 2153+161 | 3C84 | 2136+006 | 2153+161   
2016/09/07 | 2016/10/09 | 2016/10/09 | 2016/09/07 | 2016/10/09 | 2016/10/09   
eo09 | -0.075 | -0.061 | -0.064 | 0.018 | 0.019 | 0.018   
eo10 | -0/006 | 0.003 | 0.003 | 0.004 | 0.001 | -0.001   
eo11 | 0.028 | \-- | 0.030 | -0.011 | \-- | -0.006   
eo13 | -0.029 | -0.049 | -0.047 | 0.013 | 0.024 | 0.020   
  
### 2\. Determine baseline errors in Z

Once the Bx and By coordinates have been determined, there should not be significant phase change as a function of time. The remaining error is in Bz, which results in different phases for sources at different declinations. From Eq. 3 we now have: 

ϕ g = ϕ o + ( 2 π / λ ) d B z sin ⁡ δ {\displaystyle \phi _{g}=\phi _{o}+(2\pi /\lambda )dB_{z}\sin \delta } ![{\\displaystyle \\phi _{g}=\\phi _{o}+\(2\\pi /\\lambda \)dB_{z}\\sin \\delta }](https://wikimedia.org/api/rest_v1/media/math/render/svg/1846177e4fe750dc167f07eee7f4d83313eb1d58) (8) 

We can now observe several calibrator sources at different declinations δ, and fit a function to the observed phases as below: 

ϕ = ( 2 π / λ ) ( c 3 + c 4 sin ⁡ δ ) , {\displaystyle \phi =(2\pi /\lambda )(c_{3}+c_{4}\sin \delta ),} ![{\\displaystyle \\phi =\(2\\pi /\\lambda \)\(c_{3}+c_{4}\\sin \\delta \),}](https://wikimedia.org/api/rest_v1/media/math/render/svg/18d3a76b5d0520124f33266d0ebecdebf096d195) (9) 

where  c 4 = d B z {\displaystyle c_{4}=dB_{z}} ![{\\displaystyle c_{4}=dB_{z}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/55aac6cf98382ae4751cd02dede186e2b1fe6c8e) is the resulted baseline error in Z. We had an observation on 2016 Oct 9 on two calibrator sources at different declinations (2136+006 and 2153+161), which is used to determine a rough value of dBz. However, it is desired to make an observation on many more sources to fit the sinusoidal curve to improve the accuracy. Our calibrator survey performed on 2016 Oct 14 would be a good database to do this. We need to firstly apply the Bx and By corrections to the visibility data, and then fit the phases at different declinations. 

## Source Coordinates

The source catalog uses the framework provided by the aipy (astronomical imaging in python) package, which in turn is based on the pyephem package. Source coordinates in pyephem are available in three systems: 

  * a_ra, a_dec — Astrometric Geocentric Position in J2000 (or ICRF) coordinates (or another epoch if specified)
  * g_ra, g_dec — Apparent Geocentric Position for the epoch-of-date
  * ra, dec — Apparent Topocentric Position for the epoch-of-date

Unfortunately, CASA wants the source Astrometric Topocentric Position in J2000 coordinates, which is none of the above. However, it is sufficient to calculate the difference between apparent topocentric and apparent geocentric coordinates, and then add it to the astrometric geocentric coordinates, i.e. 

  * ra_j2000 = (src.ra - src.g_ra) + src.a_ra
  * dec_j2000 = (src.dec - src.g_dec) + src.a_dec

Of course, for very distant sources this correction is unnecessary. 

For moving sources, such as the Sun, the RA and Dec coordinates are continually changing. For that reason, it is necessary to know the time for which the coordinates are valid. EOVSA Miriad files use the start time of the scan. 

Retrieved from "[http://ovsa.njit.edu//wiki/index.php?title=Antenna_Position&oldid=1504](http://ovsa.njit.edu//wiki/index.php?title=Antenna_Position&oldid=1504)"
