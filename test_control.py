from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from A_T01a import A_T01a
import numpy as np
import shutil
import pandas as pd
import matplotlib.pyplot as plt

# define the model name and simulation parameters
fmu_plant_filename = 'PLANT_v3_mac.fmu'
fmu_controller_filename = 'CTRL_v3_mac.fmu'
step_size = 10**(-3)
CaseTest = A_T01a(step_size)
Tend = CaseTest.getTsimu()

# read the model description
plant_description = read_model_description(fmu_plant_filename)
controller_description = read_model_description(fmu_controller_filename)

# collect the value references
plant_vrs = {}
for variable in plant_description.modelVariables:
    plant_vrs[variable.name] = variable.valueReference

controller_vrs = {}
for variable in controller_description.modelVariables:
    controller_vrs[variable.name] = variable.valueReference


## get the value references for the variables we want to get/set
inputs_plant = [v for v in plant_description.modelVariables if v.causality == 'input']
outputs_plant = [v for v in plant_description.modelVariables if v.causality == 'output']

inputs_control = [v for v in controller_description.modelVariables if v.causality == 'input']
outputs_control = [v for v in controller_description.modelVariables if v.causality == 'output']

input_plant_order = []

for v in inputs_plant:
    input_plant_order.append(v.valueReference)

CaseTest.setInputOrder(input_plant_order)

# extract the FMU
unzipdir_plant = extract(fmu_plant_filename)

fmu_plant = FMU2Slave(guid=plant_description.guid,
                unzipDirectory=unzipdir_plant,
                modelIdentifier=plant_description.coSimulation.modelIdentifier,
                instanceName='instance1')

# initialize
fmu_plant.instantiate()
fmu_plant.setupExperiment(startTime=0)
fmu_plant.enterInitializationMode()
fmu_plant.exitInitializationMode()

# extract the FMU
unzipdir_controller = extract(fmu_controller_filename)

fmu_controller = FMU2Slave(guid=controller_description.guid,
                unzipDirectory=unzipdir_controller,
                modelIdentifier=controller_description.coSimulation.modelIdentifier,
                instanceName='instance1')

# initialize
fmu_controller.instantiate()
fmu_controller.setupExperiment(startTime=0)
fmu_controller.enterInitializationMode()
fmu_controller.exitInitializationMode()

# %% - Simulation loop

time = 0

rows = []  # list to record the results


# SET CASE CONSTANTS INPUTS

fmu_plant.setReal([inputs_plant[1].valueReference], [2.0])       # HYSTERESIS 
for cst in CaseTest.getConstants():
    vr = inputs_plant[cst].valueReference
    fmu_plant.setReal([vr], [CaseTest.getAll(vr,0)])

fmu_controller.setReal([inputs_control[0].valueReference], CaseTest.getZA_FT())
fmu_controller.setReal([inputs_control[1].valueReference], CaseTest.getT_tgt_C())

# GAINS
fmu_controller.setReal([inputs_control[3].valueReference], [-959240])
fmu_controller.setReal([inputs_control[4].valueReference], [-738570])
fmu_controller.setReal([inputs_control[5].valueReference], [-217670])
fmu_controller.setReal([inputs_control[6].valueReference], [152])

count = 0

time_vect = []
TBAS_SENSOR = []
FAV_POSITION_DEG = []
SW_FAV_CTRL_CMD = []

# SETTING INITIAL CONDITIONS
time_vect.append(0)
TBAS_SENSOR.append(0)
FAV_POSITION_DEG.append(0)
SW_FAV_CTRL_CMD.append(0)

# simulation loop
while time < Tend:

    # NOTE: the FMU.get*() and FMU.set*() functions take lists of
    # value references as arguments and return lists of values
    fmu_controller.setReal([inputs_control[2].valueReference], [TBAS_SENSOR[count]])

    vr6 = inputs_plant[6].valueReference
    fmu_plant.setReal([vr6], [CaseTest.getAll(vr6,count)])
    fmu_plant.setReal([inputs_plant[0].valueReference], [SW_FAV_CTRL_CMD[count]])

    # perform one step
    fmu_controller.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)
    fmu_plant.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)

    # get the values for 'inputs' and 'outputs'
    
    time += step_size
    count += 1
    TBAS_SENSOR.append(fmu_plant.getReal([outputs_plant[4].valueReference])[0])
    FAV_POSITION_DEG.append(fmu_plant.getReal([outputs_plant[0].valueReference])[0])
    SW_FAV_CTRL_CMD.append(fmu_controller.getReal([outputs_control[0].valueReference])[0])
    time_vect.append(time)

fmu_plant.terminate()
fmu_plant.freeInstance()

fmu_controller.terminate()
fmu_controller.freeInstance()

# clean up
shutil.rmtree(unzipdir_plant, ignore_errors=True)
shutil.rmtree(unzipdir_controller, ignore_errors=True)


''' # Export data for validation
data_dic = {'time': time_vect, 'TBAS_SENSOR': TBAS_SENSOR, 'FAV_POSITION_DEG': FAV_POSITION_DEG, 'SW_FAV_CTRL_CMD': SW_FAV_CTRL_CMD}
data_end = pd.DataFrame(data=data_dic)

data_end.to_csv('Validation_python.csv',index=False)
'''

# plot the results
#plt.figure()
#plt.plot(time_vect,TBAS_SENSOR)

#plt.figure()
#plt.plot(time_vect,FAV_POSITION_DEG)

#plt.show()