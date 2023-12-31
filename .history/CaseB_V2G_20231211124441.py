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
# dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")
dss = py_dss_interface.DSS()

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=1")
dss.text("New monitor.powers1_V2G action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=1 ppolar=no mode=1")


#INSERIR MEDIDOR NA BARRA RG60 PARA VERIFICAR QUAL MOMENTO OCORRE A VIOLACAO DE TENSAO
#BARRA RG60 ESTA NA LINHA Line.650632
dss.text("New monitor.tensao action=Save element=Line.650632  terminal=1 ppolar=no mode=0") # mode=0 (monitoramento de tensões e corrente)
dss.text("New monitor.tensao_v2 action=Save element=Transformer.XFM1 terminal=1 ppolar=no mode=0")
#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")

#cria loadshape 7.5 horas de carga (primeiras horas do dia)
n_pontos_curva = 96 #24* 4 
pontos_inicias = int(4*7.5)


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



#comentado para verificar e fazer ajustes se precisar
#ls_f2_v2 = functions.create_custom_ls_v2g('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_v2g_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_v2g.csv',ls_f2)

#print(ls_f2_v2)

ls_f2_v2 = [-0.00024685714285721717, -0.00024685714285713596, 0.0008108571428571817, 0.0007897142857142723, 0.0029445714285714075, 0.0030337142857143006, 0.0037022857142857543, 0.0036920000000000234, 0.0036920000000000234, 0.003916571428571436, 0.003987999999999943, 0.0040320000000000225, 0.00393885714285716, 0.004108571428571476, 0.004108571428571395, 0.004108571428571395, 0.004108571428571395, 0.004065142857142844, 0.0041474285714285285, 0.004147428571428609, 0.004147428571428609, 0.003927428571428615, 0.003933142857142847, 0.003933142857142847, 0.003258857142857161, 0.0032748571428571236, 0.0029017142857143035, 0.003055428571428576, 0.0028691428571428496, -0.054729142857142796, -0.05454800000000002, -0.05455371428571425, -0.05221942857142856, -0.051619428571428566, 0.0035857142857142685, 0.0032994285714285504, 0.005299428571428552, 0.03507028571428572, 0.03482914285714282, 0.035249714285714245, 0.03324971428571432, 0.03325028571428577, 0.06819485714285714, 0.07319428571428571, 0.07319428571428571, 0.10291885714285709, 0.10292457142857148, 0.10292457142857148, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.11085714285714288, 0.11085714285714288, 0.11085714285714288, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.06785714285714287, 0.06785714285714287, 0.06785714285714287, 0.05285714285714286, 0.05285714285714286, 0.05385714285714286, 0.05385714285714286, 0.05435714285714286, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.0003782857142857199, 0.0003782857142857199, 0.0003782857142857199, -0.016674285714285753, -0.016689714285714266, -0.016689714285714266]
ls_f2_v2 = [ 0.00000000000000000000,  0.00000000000000000000, 0.0008108571428571817, 0.0007897142857142723, 0.0029445714285714075, 0.0030337142857143006, 0.0037022857142857543, 0.0036920000000000234, 0.0036920000000000234, 0.003916571428571436, 0.003987999999999943, 0.0040320000000000225, 0.00393885714285716, 0.004108571428571476, 0.004108571428571395, 0.004108571428571395, 0.004108571428571395, 0.004065142857142844, 0.0041474285714285285, 0.004147428571428609, 0.004147428571428609, 0.003927428571428615, 0.003933142857142847, 0.003933142857142847, 0.003258857142857161, 0.0032748571428571236, 0.0029017142857143035, 0.003055428571428576, 0.0028691428571428496,  0.000000000000000000,  0.00000000000000000,  0.00000000000000000,  0.00000000000000000,  0.000000000000000000, 0.0035857142857142685, 0.0032994285714285504, 0.005299428571428552, 0.03507028571428572, 0.03482914285714282, 0.035249714285714245, 0.03324971428571432, 0.03325028571428577, 0.06819485714285714, 0.07319428571428571, 0.07319428571428571, 0.10291885714285709, 0.10292457142857148, 0.10292457142857148, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.11085714285714288, 0.11085714285714288, 0.11085714285714288, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.06785714285714287, 0.06785714285714287, 0.06785714285714287, 0.05285714285714286, 0.05285714285714286, 0.05385714285714286, 0.05385714285714286, 0.05435714285714286, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.0003782857142857199, 0.0003782857142857199, 0.0003782857142857199,  0.000000000000000000,  0.000000000000000000,  0.000000000000000000]

plt.plot(ls_f2_v2)
plt.show()

dss.text(f"New LoadShape.G2V npts={n_pontos_curva}  interval={0.25}  mult={ls}")
dss.text(f"New LoadShape.G2V_f2_v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
dss.text(f"New LoadShape.G2V_f3 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-252   kvar=0 daily=G2V")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=G2V_f2_v2")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=G2V_f2_v2") 
#print(dss.Cicruit.LoadShapes.Mult)
dss.solution.solve()
#dss.text("plot Loadshape Object=DEFAULT")

#dss.text("plot Loadshape Object=G2V")
#dss.text("plot Loadshape Object=G2V_f2_v2")
#dss.text("plot monitor object=powers2 labels=Yes")
dss.text("plot monitor object=powers1_V2G")
print('plotado para salvar dados')
resultados = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS1_V2G-ch1-ch3-ch5.DSV')

# dss.text("plot monitor object=tensao")
dss.text("plot monitor object=tensao_v2")
tensao = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-TENSAO_V2-ch1-ch3-ch5.DSV')
base = 2400 #volts
tensao_pu = [i/base for i in tensao]
print("tensao_pu: ", tensao_pu)

# dss.text("export monitor object=powers1_V2G") #salva em uma pasta temp

dss.text("Show Voltages LN Nodes ")

dss.text("plot monitor object=tensao_v2 channel=[15]")  # verificar corrente de neutro
resultados_corrente_neutro = functions.read_file_montior_neutral_current('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-TENSAO_V2-ch15.DSV')
print("Max neutral current:", resultados_corrente_neutro[0], " Min neutral current:", resultados_corrente_neutro[1])


# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
# dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")

## plotagem de todos os monitors: positivo - consumo; negativo - geração
monitors_names = dss.monitors_all_names()
print("monitors_names is: ", monitors_names)
n_monitors = len(monitors_names)

z=dss.monitors_first()

for i in range(n_monitors):
    dss.monitors_read_element()
    z=dss.monitors_next()
    for h in range(7):
        plt.plot(dss.monitors_channel(h))
dss.monitors_count()
plt.show()


print('Loading')
