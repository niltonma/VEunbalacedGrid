import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes

circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
dss = py_dss_interface.DSSDLL()
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")
dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New monitor.powers1_V2G action=Save element=Transformer.XFM1  terminal=2 ppolar=no mode=1")
#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-160   kvar=-110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")
n_pontos_curva = 96 #24* 4 
ls = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0020, 0.0026, 0.06, 0.060,
       0.0620, 0.0920, 0.092, 0.092 ,
       0.09, 0.09, 0.125, 0.13, 0.13, 0.16, 0.160, 0.160, 0.160, 
       0.160, 0.160, 0.160, 0.160, 0.160,
       0.160, 0.160, 0.160, 0.160,
         0.160, 0.160, 0.160, 0.160, 0.1680, 0.1680, 0.1680,
       0.165, 0.1650, 0.1650, 0.1650,
         0.140, 0.140, 0.140,
         0.140, 0.140, 0.1250, 0.1250, 0.1250, 0.110,
           0.110,
         0.11100, 0.11100,
    0.1115, 0.0870, 0.0870, 0.0870, 0.0870, 0.0870, 0.0870,
      0.0870, 0.0870, 0.0570, 0.057, 0.057, 0.01, 0.01, 0.01 ]

ls_f2 = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0020, 0.0026, 0.06, 0.060,
       0.0620, 0.0920, 0.092, 0.092 ,
       0.09, 0.09, 0.125, 0.13, 0.13, 0.16, 0.160, 0.160, 0.160, 
       0.160, 0.160, 0.160, 0.160, 0.160,
       0.160, 0.160, 0.160, 0.160,
         0.160, 0.160, 0.160, 0.160, 0.1680, 0.1680, 0.1680,
       0.165, 0.1650, 0.1650, 0.1650,
         0.140, 0.140, 0.140,
         0.140, 0.140, 0.1250, 0.1250, 0.1250, 0.110,
           0.110,
         0.11100, 0.11100,
    0.1115, 0.0870, 0.0870, 0.0870, 0.0870, 0.0870, 0.0870,
      0.0870, 0.0870, 0.0570, 0.057, 0.057, 0.01, 0.01, 0.01 ]

ls_f2_v2 = functions.create_custom_ls_v2g('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_v2g_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_v2g.csv',ls_f2)

dss.text(f"New LoadShape.G2V npts={n_pontos_curva}  interval={0.25}  mult={ls}")
dss.text(f"New LoadShape.G2V_f2_v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
dss.text(f"New LoadShape.G2V_f3 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=252   kvar=0 daily=G2V")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V_f2_v2")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V_f2_v2") 
dss.solution_solve()
dss.text("plot Loadshape Object=G2V_f2_v2")
dss.text("plot Loadshape Object=G2V")
dss.text("plot monitor object=powers1_V2G")
# dss.text("export monitor object=powers1_V2G") #salva em uma pasta temp
print('Loading')
