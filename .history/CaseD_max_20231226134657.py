import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes
import numpy as np


circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
#dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface
dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1_pm element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2_pm element=Line.632633  terminal=1")
dss.text("New monitor.powers1_comb_pm action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1")
dss.text("New monitor.powers2_comb_pm action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2_pm action=Save element=Line.632633  terminal=1 ppolar=no mode=1")

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")

#cria loadshape 7.5 horas de carga (primeiras horas do dia)
n_pontos_curva = 96 #24* 4 
pontos_inicias = int(4*7.5)
ls = [-1 for i in range(7*4)]
ls2 = [ 1 for i in range(17*4)]
LSf1 = ls + ls2


dss.text(f"New LoadShape.comb_v2_pm npts={n_pontos_curva}  interval={0.25}  mult={LSf1}")
# dss.text(f"New LoadShape.comb_f23 npts={n_pontos_curva}  interval={0.25}  mult={ls_f23}")

#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-252   kvar=0 daily=comb_v2_pm")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=comb_v2_pm")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=comb_v2_pm")
dss.text("plot Loadshape Object=comb_v2_pm") 
#print(dss.Cicruit.LoadShapes.Mult)
# dss.text("calcv")
dss.solution.solve()
#dss.text("plot Loadshape Object=DEFAULT")
dss.text("plot Loadshape Object=comb_v2_pm")
#dss.text("plot Loadshape Object=comb_f23")
#dss.text("plot monitor object=powers2 labels=Yes")

dss.text("plot monitor object=powers1_comb_pm") # para salvar as potencias
print('plotado para salvar dados')
resultados = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS1_COMB_PM-ch1-ch3-ch5.DSV')
print("potencias: ", resultados)

#dss.text("export monitor object=powers1_comb") #salva em uma pasta temp

dss.text("plot monitor object=powers2_comb_pm") # para salvar as tensões
tensao = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS2_COMB_PM-ch1-ch3-ch5.DSV')
base = 2400 #volts
tensao_pu = [i/base for i in tensao]
print("tensao_pu: ", tensao_pu)

### get voltage in each fase

time = np.arange(0.0, 24.0, 0.25)
time = list(time)

list_of_voltage_in_fases = functions.get_voltage_fases('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS2_COMB_PM-ch1-ch3-ch5.DSV')
color = 'tab:red'
plt.xlabel('Horas')
plt.ylabel('V [pu]', color=color)
plt.plot(time,[i/base for i in  list_of_voltage_in_fases[0]],color = "green", label = "Fase_1")
plt.plot(time,[i/base for i in  list_of_voltage_in_fases[1]],color = "red", label = "Fase_2")
plt.plot(time,[i/base for i in  list_of_voltage_in_fases[2]],color = "blue", label = "Fase_3")
plt.legend()
plt.show()



dss.text("plot monitor object=powers2_comb_pm channel=[15]")  # verificar corrente de neutro
resultados_corrente_neutro = functions.read_file_montior_neutral_current('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS2_COMB_PM-ch15.DSV')
print("Max neutral current:", resultados_corrente_neutro[0], " Min neutral current:", resultados_corrente_neutro[1])



# dss.text("Show Voltages LN Nodes ")
# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")

print('Loading')
