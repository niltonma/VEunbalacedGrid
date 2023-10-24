import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes


from py_dss_interface.models.LoadShapes.LoadShapesF import LoadShapesF
from py_dss_interface.models.LoadShapes.LoadShapesI import LoadShapesI
from py_dss_interface.models.LoadShapes.LoadShapesS import LoadShapesS
from py_dss_interface.models.LoadShapes.LoadShapesV import LoadShapesV
from typing import List



circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
#dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface
dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")
dss.text("New monitor.powers1 action=Save element=Transformer.XFM1  terminal=2 ppolar=no mode=1")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=no mode=1")

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-160   kvar=-110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")

#cria loadshape 7.5 horas de carga (primeiras horas do dia)
n_pontos_curva = 96 #24* 4 
pontos_inicias = int(4*7.5)
#i1 = int(4*3)
# i11 = int(4)
# i12 = int(4)
# i13 = int(4)
# i2 = int(4*3)
# #i3 = int(4*1.5)
# i31 = int(2*1.5)
# i32 = int(2*1.5)
# ls = []
# for i in range(i11):
#     ls.append(0.05)
# for i in range(i12):
#     ls.append(0.10)
# for i in range(i13):
#     ls.append(0.15)    
# for i in range(i2):
#     ls.append(0.15)
# for i in range(i31):
#     ls.append(0.12)
# for i in range(i32):
#     ls.append(0.06)    
# for i in range(n_pontos_curva-(i11+i12+i13+i2+i31+i32)):
#     ls.append(0)    
# print(ls)


ls = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0020, 0.0026, 0.06, 0.060,
       0.0620, 0.0920, 0.092, 0.092 ,
       0.09, 0.09, 0.125, 0.13, 0.13, 0.16, 0.160, 0.160, 0.160, 
       0.160, 0.160, 0.160, 0.160, 0.160,
       0.160, 0.160, 0.160, 0.160,
         0.160, 0.160, 0.160, 0.160, 0.1680, 0.1680, 0.1680,
       0.165, 0.1650, 0.1650, 0.1650,
         0.140, 0.140, 0.140,
         0.140, 0.140, 0.140, 0.140, 0.140, 0.240, 0.1680,
         0.08800, 0.05900,
    0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02 ]
dss.text(f"New LoadShape.G2V npts={n_pontos_curva}  interval={0.25}  mult={ls}")
#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=252   kvar=0 daily=G2V")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V") 
#print(dss.Cicruit.LoadShapes.Mult)
dss.solution_solve()
#dss.text("plot Loadshape Object=DEFAULT")
#dss.text("plot Loadshape Object=G2V")
#dss.text("plot monitor object=powers2 labels=Yes")
dss.text("plot monitor object=powers1")
print('Loading')
