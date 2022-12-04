import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

valid_python = pd.read_csv('Validation_python.csv')
valid_matlab = pd.read_csv('Validation_MATLAB.csv',names=['time','TBAS_SENSOR','FAV_POSITION_DEG'])

print(valid_python)

print(valid_matlab)

plt.figure()
plt.plot(valid_python['time'],valid_python['TBAS_SENSOR'],label='Python')
plt.plot(valid_matlab['time'],valid_matlab['TBAS_SENSOR'],'--r',label='MATLAB')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('TBAS_SENSOR [ºC]')
plt.title('Validation')
plt.axis([0,3500,-60,240])
plt.savefig('Validation_TBAS.png')

plt.figure()
plt.plot(valid_python['time'],valid_python['FAV_POSITION_DEG'],label='Python')
plt.plot(valid_matlab['time'],valid_matlab['FAV_POSITION_DEG'],'--r',label='MATLAB')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('FAV_POSITION_DEG [º]')
plt.title('Validation')
plt.axis([0,3500,0,80])
plt.savefig('Validation_FAVPOS.png')


plt.show()