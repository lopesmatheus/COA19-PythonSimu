import numpy as np
from TestCases import TestCase, discretize
import matplotlib.pyplot as plt

class A_T03b(TestCase):

    def __init__(self,dt):
        self._Tsimu = 4000
        self._Tend = 2000
        self._time = np.linspace(0,self._Tsimu,int(self._Tsimu/dt)+1)
        self._order = []
        self._constants = [2,3,4,5,7,8,9,10]

        self._MACH = [0.55]
        self._ZA_FT = [17000.0]
        self._Patm_mbar = [0.179]

        self._T_FAN_degC = [1.0]
        self._P_FAN_barg = [0.15]
        self._OPV_FLOW_kg_min = [103.2]
        self._OPV_TEMP_degC = [253]
        self._PPRV_barg = [7.3]
        self._T_tgt_C = [199]
        
        TPRV_degC = 190
        TPRV_Max_degC = 225
        Xtime = (TPRV_Max_degC - TPRV_degC)*5.5

        TPRV_t = np.array([0,self._Tsimu/6,self._Tsimu/5+Xtime,self._Tsimu/5+Xtime+600,self._Tsimu/5+2*Xtime+600,self._Tsimu])
        TPRV_fun = np.array([TPRV_degC,TPRV_degC,TPRV_Max_degC,TPRV_Max_degC,TPRV_degC,TPRV_degC])

        self._TPRV_degC = discretize(TPRV_t,TPRV_fun,dt,2)
