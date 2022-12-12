import numpy as np
from TestCases import TestCase, discretize
import matplotlib.pyplot as plt

class C_T01_m(TestCase):

    def __init__(self,dt):
        self._Tsimu = 4000
        self._Tend = 1800
        self._time = np.linspace(0,self._Tsimu,int(self._Tsimu/dt)+1)
        self._order = []
        self._constants = [2,3,4,5,7,8,9,10]

        self._MACH = [0.0]
        self._ZA_FT = [0.0]
        self._Patm_mbar = [0.179]

        self._T_FAN_degC = [15.0]
        self._P_FAN_barg = [0.15]
        self._OPV_FLOW_kg_min = [100.0]
        self._OPV_TEMP_degC = [253]
        self._PPRV_barg = [8.0]
        self._T_tgt_C = [200.0]
        
        TPRV_degC = 230
        TPRV_Max_degC = 290
        Xtime = (TPRV_Max_degC - TPRV_degC)*5.5

        TPRV_t = np.array([0,self._Tsimu/4,self._Tsimu/4+1,self._Tsimu])
        TPRV_fun = np.array([TPRV_degC,TPRV_degC,TPRV_Max_degC,TPRV_Max_degC])
        
        _OPV_FLOW_kg_min_t=np.array([0,self._Tsimu/8,self._Tsimu/8+20,self._Tsimu/8+200,self._Tsimu/8+260,self._Tsimu/8+460,self._Tsimu/8+470,self._Tsimu/8+1050,self._Tsimu/8+1060,self._Tsimu/8+1260,self._Tsimu/8+1320 ,self._Tsimu/8+1520 ,self._Tsimu/8+1540 ,self._Tsimu])
        _OPV_FLOW_kg_min_fun=np.array([self._OPV_FLOW_kg_min,self._OPV_FLOW_kg_min,self._OPV_FLOW_kg_min-10,self._OPV_FLOW_kg_min-10,self._OPV_FLOW_kg_min+20,self._OPV_FLOW_kg_min+20,self._OPV_FLOW_kg_min-80,self._OPV_FLOW_kg_min-80,self._OPV_FLOW_kg_min+20,self._OPV_FLOW_kg_min+20,self._OPV_FLOW_kg_min-10,self._OPV_FLOW_kg_min-10,self._OPV_FLOW_kg_min,self._OPV_FLOW_kg_min ])
        T_tgt_C_t=np.array([0,self._Tsimu/8+200,self._Tsimu/8+200.001,self._Tsimu/8+460,self._Tsimu/8+460.001,self._Tsimu/8+1050,self._Tsimu/8+1050.001,self._Tsimu/8+1260,self._Tsimu/8+1260.001,self._Tsimu])
        T_tgt_C_fun=[199.00,199.00,230.00,230.00,199.00,199.00,230.00,230.00,199.00]
        self._TPRV_degC = discretize(TPRV_t,TPRV_fun,dt,2)
