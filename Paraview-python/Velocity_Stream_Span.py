## This script produce 2 types of vector velocity i.e. VSpan and VStream of wing slices.
## Both VSpan and VStream are vector field of velocity on skin (1  cell above body skin)
## VSpan is each skin velocity projected to perpendicular direction to freestream.
## Vstream is each skin velocity projected to parallel of freestream & body contour.
## Positive Vspan is towards the tip. Positive Vstream is towards downstream.
## Caution: coarse simulation causes high error of projected vectors on corner/tip.

#### import the simple module from the paraview
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

## ----------------------input -----------------------##
BodyFile = 'C:\\Users\\andhini\\Documents\\research_data\\finite_span3_twistroll\\twistroll_6body\\bodyF.vti.pvd'
Ave1File = 'C:\\Users\\andhini\\Documents\\research_data\\finite_span3_twistroll\\twistroll_6\\fluid.vti.pvd'

AD = 3.0 # AD=2A/D where D=0.16C foil thickness of NACA16
sl= 3.0/3.0 #sl=1 for span-length=3c and 2 for 6c
##---------------------End of input -----------------##

LoadPalette(paletteName='WhiteBackground')

# create a new 'PVD Reader'
bodyFvtipvd = PVDReader(FileName=BodyFile)
bodyFvtipvd.PointArrays = ['Velocity', 'Pressure']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# create a new 'PVD Reader'
ave_1vtipvd = PVDReader(FileName=Ave1File)
ave_1vtipvd.PointArrays = ['Velocity', 'Pressure']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
bodyFvtipvdDisplay = Show(bodyFvtipvd, renderView1)

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show data in view
ave_1vtipvdDisplay = Show(ave_1vtipvd, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(bodyFvtipvd)

# create a new 'Extract Time Steps'
extractTimeSteps1 = ExtractTimeSteps(Input=bodyFvtipvd)
extractTimeSteps1.TimeStepIndices = [0]
extractTimeSteps1.TimeStepRange = [0, 4]

# show data in view
extractTimeSteps1Display = Show(extractTimeSteps1, renderView1)

# hide data in view
Hide(bodyFvtipvd, renderView1)

# create a new 'Contour'
contour1 = Contour(Input=extractTimeSteps1)
contour1.ContourBy = ['POINTS', 'Pressure']
contour1.Isosurfaces = [120.67470455169678]
contour1.PointMergeMethod = 'Uniform Binning'

# Properties modified on contour1
contour1.ComputeScalars = 1
contour1.GenerateTriangles = 0
contour1.Isosurfaces = [1.0]

# show data in view
contour1Display = Show(contour1, renderView1)

# get color transfer function/color map for 'Pressure'
pressureLUT = GetColorTransferFunction('Pressure')

# get opacity transfer function/opacity map for 'Pressure'
pressurePWF = GetOpacityTransferFunction('Pressure')

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(Input=ave_1vtipvd,
    Source=contour1)
resampleWithDataset1.CellLocator = 'Static Cell Locator'

# hide data in view
Hide(contour1, renderView1)

# Properties modified on resampleWithDataset1
resampleWithDataset1.PassPointArrays = 1

# show data in view
resampleWithDataset1Display = Show(resampleWithDataset1, renderView1)

# hide data in view
Hide(ave_1vtipvd, renderView1)

# hide data in view
Hide(contour1, renderView1)

# show color bar/color legend
resampleWithDataset1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# hide data in view
Hide(extractTimeSteps1, renderView1)

# hide data in view
Hide(resampleWithDataset1, renderView1)

# set active source
SetActiveSource(resampleWithDataset1)

# create a new 'Slice'
slice1 = Slice(Input=resampleWithDataset1)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]
slice1.SliceType.Origin = [0.0, 0.0, AD*0.8*128*sl]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# set active source
SetActiveSource(slice1)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# show data in view
slice1Display = Show(slice1, renderView1)

# hide data in view
Hide(resampleWithDataset1, renderView1)

# set active source
SetActiveSource(slice1)

# create a new 'Calculator'
calculator1 = Calculator(Input=slice1)
calculator1.ResultArrayName = 'VStream'
calculator1.Function = '((-Normals_Y*iHat+Normals_X*jHat).Velocity)/(mag(-Normals_Y*iHat+Normals_X*jHat)^2)*(-Normals_Y*iHat+Normals_X*jHat)'

# rename source object
RenameSource('VStream', calculator1)

# show data in view
calculator1Display = Show(calculator1, renderView1)

# hide data in view
Hide(slice1, renderView1)

# set active source
SetActiveSource(slice1)

# create a new 'Calculator'
calculator1_1 = Calculator(Input=slice1)
calculator1_1.ResultArrayName = 'VSpan'
calculator1_1.Function = '((-Normals_Z*jHat+Normals_Y*kHat).Velocity)/(mag(-Normals_Z*jHat+Normals_Y*kHat)^2)*(-Normals_Z*jHat+Normals_Y*kHat)'

# rename source object
RenameSource('VSpan', calculator1_1)

# show data in view
calculator1_1Display = Show(calculator1_1, renderView1)

# hide data in view
Hide(slice1, renderView1)

##------------------------------------glyph---------------------------------##

# set active source
SetActiveSource(slice1)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [2359, 1294]

# show data in view
slice1Display = Show(slice1, renderView1)

# find source
VStream = FindSource('VStream')

# set active source
SetActiveSource(VStream)

# create a new 'Glyph'
glyph1 = Glyph(Input=VStream,
    GlyphType='Arrow')
glyph1.OrientationArray = ['POINTS', 'VStream']
glyph1.ScaleArray = ['POINTS', 'VStream']
glyph1.ScaleFactor = 10.
glyph1.GlyphTransform = 'Transform2'

# show data in view
glyph1Display = Show(glyph1, renderView1)

# rename source object
RenameSource('Glyph_VStream', glyph1)

# find source
glyph_VStream = FindSource('Glyph_VStream')

# Properties modified on glyph_VStream
glyph_VStream.GlyphMode = 'All Points'

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(glyph1)

# turn off scalar coloring
ColorBy(glyph1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pressureLUT, renderView1)

# change solid color
glyph1Display.DiffuseColor = [0.0, 0.0, 1.0]

# find source
VSpan = FindSource('VSpan')

# set active source
SetActiveSource(VSpan)

# create a new 'Glyph'
glyph2 = Glyph(Input=VSpan,
    GlyphType='Arrow')
glyph2.OrientationArray = ['POINTS', 'VSpan']
glyph2.ScaleArray = ['POINTS', 'VSpan']
glyph2.ScaleFactor = 10.
glyph2.GlyphTransform = 'Transform2'

# show data in view
glyph2Display = Show(glyph2, renderView1)

# turn off scalar coloring
ColorBy(glyph2Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pressureLUT, renderView1)

# change solid color
glyph2Display.DiffuseColor = [1.0, 0.0, 0.0]

# rename source object
RenameSource('Glyph_VSpan', glyph2)

# find source
glyph_VSpan = FindSource('Glyph_VSpan')

# Properties modified on glyph_VSpan
glyph_VSpan.GlyphMode = 'All Points'

# reset view to fit data
renderView1.ResetCamera()

# set active source
SetActiveSource(contour1)

# show data in view
contour1Display = Show(contour1, renderView1)

# turn off scalar coloring
ColorBy(contour1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pressureLUT, renderView1)

# Properties modified on contour1Display
contour1Display.Opacity = 0.4

# set active source
SetActiveSource(slice1)

# hide color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, False)

# set active source
SetActiveSource(VStream)

# hide data in view
Hide(VStream, renderView1)

# set active source
SetActiveSource(VSpan)

# hide data in view
Hide(VSpan, renderView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [5.731461031320464, 84.72178716132407, 545.7629812412072]
renderView1.CameraFocalPoint = [5.841929499496991, 84.37102609099051, 544.8677750620376]
renderView1.CameraViewUp = [0.009614307796669271, 0.9236580608999602, -0.38309705248163484]
renderView1.CameraViewAngle = 23.679525222551927
renderView1.CameraParallelScale = 67.13543989525182

#### uncomment the following to render all views
# RenderAllViews()
