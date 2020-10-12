# This is code calculate Lift force (PN) for a slice/section on a flapping finite wing.
# Input sources from fluid and body separately, so timestep for both can be different.
# Controlling body timestep from 'no', and the slice position from 'Slice_no'.
# Here, Slice_no is a combination of AD=2A/D (flapping peak-to-peak amplitude
# per foil thickness) and if span length is  sl*3C.
# PN = integrate (Pressure*Normal); PN is located in the spreadsheet.
# X, Y components are for thrust and lift forces. CL= X/(0.5*rho*U*C), rho=U=1.

#### import the simple module from the paraview
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()


##--------- change input here -----------##
no=3 # timestep for body, change manually
AD=3. ## 2A/D amplitude per
sl=1. # 1 for span length=3C, 2 for 6C
Slice_no= AD*128.*0.8*sl # C/delta_x=128

FluidFile = 'C:\\Users\\andhini\\Documents\\research_data\\finite_span3_twistroll\\twistroll_6\\fluid.vti.pvd'
BodyFile = 'C:\\Users\\andhini\\Documents\\research_data\\finite_span3_twistroll\\twistroll_6body\\bodyF.vti.pvd'
##------------end of input --------------##

# create a new 'PVD Reader'
ave_3vtipvd = PVDReader(FileName=FluidFile)
ave_3vtipvd.PointArrays = ['Velocity', 'Pressure']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
ave_3vtipvdDisplay = Show(ave_3vtipvd, renderView1)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'PVD Reader'
bodyFvtipvd = PVDReader(FileName=BodyFile)
bodyFvtipvd.PointArrays = ['Velocity', 'Pressure']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# show data in view
bodyFvtipvdDisplay = Show(bodyFvtipvd, renderView1)

# update the view to ensure updated data information
renderView1.Update()

#----------------timestep changed for body --------------------#
# create a new 'Extract Time Steps'
extractTimeSteps1 = ExtractTimeSteps(Input=bodyFvtipvd)
extractTimeSteps1.TimeStepIndices = [no-1]
extractTimeSteps1.TimeStepRange = [0, 4]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
extractTimeSteps1Display = Hide(extractTimeSteps1, renderView1)
#---------------------------------------------------------------#

# create a new 'Contour'
contour1 = Contour(Input=extractTimeSteps1)
contour1.ContourBy = ['POINTS', 'Pressure']
contour1.PointMergeMethod = 'Uniform Binning'
contour1.ComputeScalars = 1
contour1.GenerateTriangles = 0
contour1.Isosurfaces = [1.0]

# show data in view
contour1Display = Show(contour1, renderView1)

# turn off scalar coloring
ColorBy(contour1Display, None)

# get color transfer function/color map for 'Pressure'
pressureLUT = GetColorTransferFunction('Pressure')

# get opacity transfer function/opacity map for 'Pressure'
pressurePWF = GetOpacityTransferFunction('Pressure')

# Properties modified on contour1Display
contour1Display.Opacity = 0.4

LoadPalette(paletteName='WhiteBackground')

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(Input=ave_3vtipvd,
    Source=contour1)
resampleWithDataset1.CellLocator = 'Static Cell Locator'

# Properties modified on resampleWithDataset1
resampleWithDataset1.PassPointArrays = 1

# show data in view
resampleWithDataset1Display = Show(resampleWithDataset1, renderView1)

# hide data in view
Hide(ave_3vtipvd, renderView1)


# create a new 'Calculator'
calculator1 = Calculator(Input=resampleWithDataset1)
calculator1.ResultArrayName = 'PN'
calculator1.Function = 'Pressure*Normals'

# show data in view
calculator1Display = Show(calculator1, renderView1)

# hide data in view
Hide(resampleWithDataset1, renderView1)

# hide data in view
Hide(bodyFvtipvd, renderView1)

# set active source
SetActiveSource(contour1)

# show data in view
contour1Display = Show(contour1, renderView1)

# set active source
SetActiveSource(calculator1)

# create a new 'Slice'
slice1 = Slice(Input=calculator1)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [0.0, 0.0, Slice_no]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1)

# hide data in view
Hide(calculator1, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(Input=slice1)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L
# uncomment following to set a specific view size
# spreadSheetView1.ViewSize = [400, 400]

# get layout
layout1 = GetLayout()

# place view in the layout
layout1.AssignView(2, spreadSheetView1)

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1)

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
spreadSheetView1.Update()

## -------------- glyph --------------#

# set active source
SetActiveSource(slice1)

# create a new 'Glyph'
glyph1 = Glyph(Input=slice1,
    GlyphType='Arrow')
glyph1.OrientationArray = ['POINTS', 'PN']
glyph1.ScaleArray = ['POINTS', 'PN']
glyph1.ScaleFactor = 1.
glyph1.GlyphTransform = 'Transform2'

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on glyph1.GlyphType
glyph1.GlyphType.Invert = 1

# show data in view
glyph1Display = Show(glyph1, renderView1)

# show color bar/color legend
glyph1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on pressureLUT
pressureLUT.EnableOpacityMapping = 0

# set active source
SetActiveSource(slice1)

# get display properties
slice1Display = GetDisplayProperties(slice1, view=renderView1)

# turn off scalar coloring
ColorBy(slice1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pressureLUT, renderView1)



# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-44.666954370924984, 410.55503694463084, 1173.2307598959674]
renderView1.CameraFocalPoint = [130.1275677239374, -110.5530155390882, 9.860220936085648]
renderView1.CameraViewUp = [0.19230162407032608, 0.9060497614989441, -0.37695346538746854]
renderView1.CameraParallelScale = 333.01651610693426
