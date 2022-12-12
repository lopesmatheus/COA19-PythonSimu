import numpy as np

# THIS FUNCTION DISCRETIZE A GIVEN VECTOR WITH STEP dt.
# The second option is almost twice as fast as the first, but has not been extensively tested
def discretize(t,fun,dt,opt):
    n = int(t[len(t)-1]/dt)+1
    ret = np.zeros(n)
    if opt==1:
        for i in range(0,n):
            for k in range(1,len(t)):
                if t[k-1]<=i*dt and i*dt<t[k]:
                    break
            x_interp = np.array([fun[k-1],fun[k]])
            t_interp = np.array([t[k-1],t[k]])
            ret[i] = np.interp(i*dt,t_interp,x_interp)
    elif opt==2:
        ret[0] = fun[0]
        count_t = 1
        for k in range(1,len(fun)):
            x_interp = np.array([fun[k-1],fun[k]])
            t_interp = np.array([t[k-1],t[k]])
            ns = int(round((t[k]-t[k-1])/dt))+1
            for i in range(1,ns):
                ret[count_t] = np.interp(count_t*dt,t_interp,x_interp)
                count_t+=1
    return ret


class TestCase:

    def __init__(self,dt):
        self._Tsimu = 0
        self._Tend = 0
        self._time = np.linspace(0,self._Tsimu,int(self._Tsimu/dt)+1)

        self._MACH = []
        self._ZA_FT = []
        self._Patm_mbar = []

        self._T_FAN_degC = []
        self._P_FAN_barg = []
        self._OPV_FLOW_kg_min = []
        self._OPV_TEMP_degC = []
        self._TPRV_degC = []
        self._PPRV_barg = []
        self._T_tgt_C = []

        self._order = []
        self._constants = []

    def setInputOrder(self,order_list):
        self._order = order_list
    
    def getConstants(self):
        return self._constants

    def getAll(self,vr,ind):
        if vr==858:
            return self._MACH[ind]
        elif vr==859:
            return self._ZA_FT[ind]
        elif vr==860:
            return self._OPV_FLOW_kg_min[ind]
        elif vr==861:
            return self._OPV_TEMP_degC[ind]
        elif vr==862:
            return self._TPRV_degC[ind]
        elif vr==863:
            return self._PPRV_barg[ind]
        elif vr==864:
            return self._T_FAN_degC[ind]
        elif vr==865:
            return self._P_FAN_barg[ind]
        elif vr==866:
            return self._Patm_mbar[ind]

    def getTsimu(self):
        return self._Tsimu

    def getTime(self):
        return self._time

    def getMach(self):
        return self._MACH
    
    def getZA_FT(self):
        return self._ZA_FT

    def getPatm_mbar(self):
        return self._Patm_mbar

    def getT_FAN_degC(self):
        return self._T_FAN_degC

    def getP_FAN_barg(self):
        return self._P_FAN_barg

    def getOPV_FLOW_kg_min(self):
        return self._OPV_FLOW_kg_min

    def getOPV_TEMP_degC(self):
        return self._OPV_TEMP_degC

    def getTPRV_degC(self):
        return self._TPRV_degC

    def getPPRV_barg(self):
        return self._PPRV_barg

    def getT_tgt_C(self):
        return self._T_tgt_C
        
    def getTend(self):
        return self._Tend
