from fmpy import read_model_description, extract
from fmpy.fmi2 import FMU2Slave
from A_T01a import A_T01a
import numpy as np
import shutil
import pandas as pd
import matplotlib.pyplot as plt

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


# define the model name and simulation parameters
fmu_filename = 'PLANT_v3.fmu'
step_size = 10**(-3)
CaseTest = A_T01a(step_size)

# read the model description
model_description = read_model_description(fmu_filename)

# collect the value references
vrs = {}
for variable in model_description.modelVariables:
    vrs[variable.name] = variable.valueReference

#print(vrs)

## get the value references for the variables we want to get/set
inputs = [v for v in model_description.modelVariables if v.causality == 'input']
outputs = [v for v in model_description.modelVariables if v.causality == 'output']


input_order = []
for v in inputs:
    input_order.append(v.valueReference)
    print(v.name)
    print(v.valueReference)
#    print(v.type)
#    print(type(v.valueReference))

print(CaseTest.getAll(858,0))

CaseTest.setInputOrder(input_order)

#for variable in model_description.modelVariables:
 #   print(variable.valueReference)

# extract the FMU
unzipdir = extract(fmu_filename)

fmu = FMU2Slave(guid=model_description.guid,
                unzipDirectory=unzipdir,
                modelIdentifier=model_description.coSimulation.modelIdentifier,
                instanceName='instance1')

# initialize
fmu.instantiate()
fmu.setupExperiment(startTime=0)
fmu.enterInitializationMode()
fmu.exitInitializationMode()

# %% - Simulation loop

time = 0

rows = []  # list to record the results


# SET CASE CONSTANTS INPUT
fmu.setReal([inputs[1].valueReference], [2.0])       # HYSTERESIS 
for cst in CaseTest.getConstants():
    vr = inputs[cst].valueReference
    fmu.setReal([vr], [CaseTest.getAll(vr,0)])

vet_TPRV_degC = CaseTest.getTPRV_degC()

count = 0

# simulation loop
while time < CaseTest.getTsimu():

    # NOTE: the FMU.get*() and FMU.set*() functions take lists of
    # value references as arguments and return lists of values

        
    fmu.setReal([inputs[6].valueReference], [vet_TPRV_degC[count]])
    fmu.setReal([inputs[0].valueReference], [0.0 if time < 200 else 200 ])
    # perform one step
    fmu.doStep(currentCommunicationPoint=time, communicationStepSize=step_size)

    # get the values for 'inputs' and 'outputs'
    val_inputs = {}
    for v in inputs:
        val_inputs[v.name] = fmu.getReal([v.valueReference])[0]

    val_outputs = {}
    for v in outputs:
        val_outputs[v.name] = fmu.getReal([v.valueReference])[0]
    
    val_time = {}
    val_time['time'] = time
    # append the results
    rowsDict = Merge(Merge(val_time,val_inputs),val_outputs)
    rows.append(rowsDict)

#    print(time)
    # advance the time
    time += step_size
    count += 1

fmu.terminate()
fmu.freeInstance()

# clean up
shutil.rmtree(unzipdir, ignore_errors=True)

# %% - Plot Results
# convert the results to a structured NumPy array
result = pd.DataFrame(rows)

# plot the results
plt.plot(result['time'],result['T_BAS_DEGC'])
plt.show()