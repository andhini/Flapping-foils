#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Note:
# Enter Fluid and Body files directories. The cell/point numbers should be the same.
# Fluid files can be from several files. Q level contour  is set to 1% of max Q level (line 134).
# The more Q level close to zero (positives values), the more structures will show.
# Contor pressure=0 represent foil body.
# The colors are based on vorticity-z set to -0.5 to 0.5 of Vorticity_z*C/U.
# Filetypes (*.pvd etc) should be the same.

# FluidFile=['F:\\research\\swept\\R_G30_HiA\\roll_g30_HiA\\fluid.vtr.pvd'] #single fluid data
FluidFile=['F:\\research\\swept\\R_G30_HiA\\roll_g30_HiA\\Ave_1.vtr.pvd',
            'F:\\research\\swept\\R_G30_HiA\\roll_g30_HiA\\Ave_2.vtr.pvd',
            'F:\\research\\swept\\R_G30_HiA\\roll_g30_HiA\\Ave_3.vtr.pvd',
            'F:\\research\\swept\\R_G30_HiA\\roll_g30_HiA\\Ave_4.vtr.pvd']
BodyFile='F:\\research\\swept\\R_G30_HiA\\roll_g30_HiA\\bodyF.vtr.pvd'

# create a new 'PVD Reader'
bodyFvtipvd = PVDReader(FileName=BodyFile)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
bodyFvtipvdDisplay = Show(bodyFvtipvd, renderView1)

# reset view to fit data
renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(bodyFvtipvdDisplay, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
bodyFvtipvdDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

# set active source
SetActiveSource(bodyFvtipvd)

# create a new 'Contour'
contour1 = Contour(Input=bodyFvtipvd)
contour1.ContourBy = ['POINTS', 'Pressure']
contour1.Isosurfaces = [0.0]
contour1.PointMergeMethod = 'Uniform Binning'

# Properties modified on contour1
contour1.ComputeNormals = 0
contour1.ComputeScalars = 1
contour1.GenerateTriangles = 0

# get color transfer function/color map for 'Pressure'
pressureLUT = GetColorTransferFunction('Pressure')

# show data in view
contour1Display = Show(contour1, renderView1)

# show color bar/color legend
contour1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

for i in range(len(FluidFile)):
    # create a new 'PVD Reader'
    ave_1vtipvd = PVDReader(FileName=FluidFile[i])

    # get animation scene
    animationScene1 = GetAnimationScene()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    # show data in view
    ave_1vtipvdDisplay = Show(ave_1vtipvd, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    # set active source
    SetActiveSource(ave_1vtipvd)

    # create a new 'Gradient Of Unstructured DataSet'
    gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=ave_1vtipvd)
    gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'Pressure']

    # Properties modified on gradientOfUnstructuredDataSet1
    gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'Velocity']
    gradientOfUnstructuredDataSet1.ComputeGradient = 0
    gradientOfUnstructuredDataSet1.ComputeVorticity = 1
    gradientOfUnstructuredDataSet1.ComputeQCriterion = 1

    # show data in view
    gradientOfUnstructuredDataSet1Display = Show(gradientOfUnstructuredDataSet1, renderView1)

    # hide data in view
    Hide(ave_1vtipvd, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Calculator'
    calculator1 = Calculator(Input=gradientOfUnstructuredDataSet1)
    calculator1.Function = ''

    # Properties modified on calculator1
    calculator1.ResultArrayName = 'Q'
    calculator1.Function = 'Q-criterion'

    #get max Q data
    calculator1.UpdatePipeline()
    dataRange=calculator1.PointData.GetArray('Q').GetRange()
    print('1% of max Q data'+str(i)+'=',dataRange[1])

    # show data in view
    calculator1Display = Show(calculator1, renderView1)

    # hide data in view
    Hide(gradientOfUnstructuredDataSet1, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    # create a new 'Contour'
    contour2 = Contour(Input=calculator1)
    contour2.ContourBy = ['POINTS', 'Q']
    contour2.Isosurfaces = [0.01*dataRange[1]] #1% of max Q data
    contour2.PointMergeMethod = 'Uniform Binning'

    # Properties modified on contour2
    contour2.ComputeNormals = 0
    contour2.ComputeScalars = 1
    contour2.GenerateTriangles = 0

    # get color transfer function/color map for 'Q'
    qLUT = GetColorTransferFunction('Q')

    # show data in view
    contour2Display = Show(contour2, renderView1)

    # show color bar/color legend
    contour2Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(contour2Display, ('POINTS', 'Vorticity', 'Magnitude'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(qLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    contour2Display.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    contour2Display.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'Vorticity'
    vorticityLUT = GetColorTransferFunction('Vorticity')

    # set scalar coloring
    ColorBy(contour2Display, ('POINTS', 'Vorticity', 'Z'))

    # rescale color and/or opacity maps used to exactly fit the current data range
    contour2Display.RescaleTransferFunctionToDataRange(False, False)

    # Update a scalar bar component title.
    UpdateScalarBarsComponentTitle(vorticityLUT, contour2Display)

    # hide color bar/color legend
    contour2Display.SetScalarBarVisibility(renderView1, False)

    # hide data in view
    Hide(calculator1, renderView1)

    # set active source
    SetActiveSource(contour1)

    # hide color bar/color legend
    contour1Display.SetScalarBarVisibility(renderView1, False)

    # set active source
    SetActiveSource(contour2)

    # show color bar/color legend
    contour2Display.SetScalarBarVisibility(renderView1, True)

    # get color legend/bar for vorticityLUT in view renderView1
    vorticityLUTColorBar = GetScalarBar(vorticityLUT, renderView1)

    # find source
    contour2 = FindSource('Contour2')

    # set active source
    SetActiveSource(contour2)

    # get color transfer function/color map for 'Vorticity'
    vorticityLUT = GetColorTransferFunction('Vorticity')

    # get opacity transfer function/opacity map for 'Vorticity'
    vorticityPWF = GetOpacityTransferFunction('Vorticity')

    # Rescale transfer function
    vorticityLUT.RescaleTransferFunction(-0.5, 0.5)

    # Rescale transfer function
    vorticityPWF.RescaleTransferFunction(-0.5, 0.5)
    # find source
    contour2 = FindSource('Contour2')

    # set active source
    SetActiveSource(contour2)

    # get color transfer function/color map for 'Vorticity'
    vorticityLUT = GetColorTransferFunction('Vorticity')

    # get opacity transfer function/opacity map for 'Vorticity'
    vorticityPWF = GetOpacityTransferFunction('Vorticity')

    # Properties modified on vorticityLUT
    vorticityLUT.EnableOpacityMapping = 0

    # get display properties
    contour2Display = GetDisplayProperties(contour2, view=renderView1)

    # hide color bar/color legend
    contour2Display.SetScalarBarVisibility(renderView1, False)


# change scalar bar placement
vorticityLUTColorBar.WindowLocation = 'AnyLocation'
vorticityLUTColorBar.Position = [0.013117283950617245, 0.4092664092664092]
vorticityLUTColorBar.ScalarBarLength = 0.33000000000000007
# find source
pVDReader1 = FindSource('PVDReader1')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# hide data in view
Hide(pVDReader1, renderView1)

# find source
contour1 = FindSource('Contour1')

# set active source
SetActiveSource(contour1)

# get color transfer function/color map for 'Pressure'
pressureLUT = GetColorTransferFunction('Pressure')

# get opacity transfer function/opacity map for 'Pressure'
pressurePWF = GetOpacityTransferFunction('Pressure')

# get display properties
contour1Display = GetDisplayProperties(contour1, view=renderView1)

# turn off scalar coloring
ColorBy(contour1Display, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pressureLUT, renderView1)

LoadPalette(paletteName='WhiteBackground')


#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [193.0, 0.5, 1506.6927577990632]
renderView1.CameraFocalPoint = [193.0, 0.5, 166.5]
renderView1.CameraParallelScale = 346.8674098268674
