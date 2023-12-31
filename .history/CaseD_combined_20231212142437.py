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
dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=1")
dss.text("New monitor.powers1_comb action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1")
dss.text("New monitor.powers2_comb action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=1 ppolar=no mode=1")

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")

#cria loadshape 7.5 horas de carga (primeiras horas do dia)
n_pontos_curva = 96 #24* 4 
pontos_inicias = int(4*7.5)



# ls = [ 0.0, 0.00, 0, 0, 0, 0, 0, -0.0780, -0.0780, -0.0780,-0.0880, -0.0880, -0.09050, -0.10400, 
#     -0.10400, -0.10400, -0.10400, -0.10400, -0.10400,-0.10400,-0.10400, -0.08800, -0.08800, -0.08800, -0.08800, -0.08800, -0.05900,
#     -0.055, -0.06, -0.005, 0, 0, 0.0020, 0.0026, 0.06, 0.060,
#        0.0620, 0.0920, 0.092, 0.092 ,
#        0.09, 0.09, 0.125, 0.13, 0.13, 0.16, 0.160, 0.160, 0.160, 
#        0.160, 0.160, 0.160, 0.160, 0.160,
#        0.160, 0.160, 0.160, 0.160,
#          0.160, 0.160, 0.160, 0.160, 0.1680, 0.1680, 0.1680,
#        0.165, 0.1650, 0.1650, 0.1650,
#          0.140, 0.140, 0.140,
#          0.140, 0.140, 0.1250, 0.1250, 0.1250, 0.110,
#            0.110,
#          0.11100, 0.11100,
#     0.1115, 0.0870, 0.0870, 0.0870, 0.0870, 0.0870, 0.0870,
#       0.0870, 0.0870, 0.0570, 0.057, 0.057, 0.01, 0.01, 0.01 ]

ls_comb = [ 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0020, 0.0026, 0.06, 0.060,
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

ls_f1 = functions.create_custom_ls_comb_f1('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_comb_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_comb.csv',ls_comb)

ls_f23 = functions.create_custom_ls_comb_f23('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_comb_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_comb_f23.csv',ls_comb)
x_inf = [i/4 for i in range(1, 97)]

plt.plot(x_inf,ls_f1)
plt.plot(x_inf, ls_f23)
plt.show()

dss.text(f"New LoadShape.comb_v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f1}")
dss.text(f"New LoadShape.comb_f23 npts={n_pontos_curva}  interval={0.25}  mult={ls_f23}")

#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-252   kvar=0 daily=comb_v2")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=comb_f23")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=comb_f23") 
#print(dss.Cicruit.LoadShapes.Mult)
dss.solution.solve()
#dss.text("plot Loadshape Object=DEFAULT")
#dss.text("plot Loadshape Object=comb_v2")
#dss.text("plot Loadshape Object=comb_f23")
#dss.text("plot monitor object=powers2 labels=Yes")

dss.text("plot monitor object=powers1_comb") # para salvar as potencias
print('plotado para salvar dados')
resultados = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS1_COMB-ch1-ch3-ch5.DSV')
print("potencias: ", resultados)

#dss.text("export monitor object=powers1_comb") #salva em uma pasta temp

dss.text("plot monitor object=powers2_comb") # para salvar as tensões

dss.text("plot monitor object=powers2_comb")
# dss.text("Show Voltages LN Nodes ")
# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")

print('Loading')
