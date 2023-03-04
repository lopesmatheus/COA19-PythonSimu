import numpy as np
from TestCases import TestCase, discretize

class C_T02(TestCase):

    def __init__(self,dt):
        self._Tsimu = 4000
        self._Tend = 1800
        self._time = np.linspace(0,self._Tsimu,int(self._Tsimu/dt)+1)
        self._order = []
        self._constants_inputs = [2,3,5,6,7,8,9,10]
        self._variables_inputs = [4]

        self._MACH = [0.55]
        self._ZA_FT = [0.0]
        self._Patm_mbar = [0.179]
        
        self._T_FAN_degC = [15.0]
        self._P_FAN_barg = [0.7]
        self._OPV_TEMP_degC = [253]
        self._TPRV_degC  = [250]
        self._PPRV_barg = [8.0]

        OPV_FLOW__kg_min =100.0
        _OPV_FLOW_kg_min_t=np.array([0,self._Tsimu/8,self._Tsimu/8+20,self._Tsimu/8+200,self._Tsimu/8+260,self._Tsimu/8+460,self._Tsimu/8+660,self._Tsimu/8+860,self._Tsimu/8+1060,self._Tsimu/8+1260,self._Tsimu/8+1320 ,self._Tsimu/8+1520 ,self._Tsimu/8+1540 ,self._Tsimu])
        _OPV_FLOW_kg_min_fun=np.array([OPV_FLOW__kg_min,OPV_FLOW__kg_min,OPV_FLOW__kg_min-10,OPV_FLOW__kg_min-10,OPV_FLOW__kg_min+20,OPV_FLOW__kg_min+20,OPV_FLOW__kg_min-80,OPV_FLOW__kg_min-80,OPV_FLOW__kg_min+20,OPV_FLOW__kg_min+20,OPV_FLOW__kg_min-10,OPV_FLOW__kg_min-10,OPV_FLOW__kg_min,OPV_FLOW__kg_min])
        self._OPV_FLOW_kg_min = discretize(_OPV_FLOW_kg_min_t,_OPV_FLOW_kg_min_fun,dt,2)
        
        T_tgt_C_t=np.array([0,self._Tsimu/8+200,self._Tsimu/8+200.001,self._Tsimu/8+460,self._Tsimu/8+460.001,self._Tsimu/8+860,self._Tsimu/8+860.001,self._Tsimu/8+1260,self._Tsimu/8+1260.001,self._Tsimu])
        T_tgt_C_fun=[199.00,199.00,230.00,230.00,199.00,199.00,230.00,230.00,199.00,199.00]
        self._T_tgt_C = discretize(T_tgt_C_t,T_tgt_C_fun,dt,2)