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
dss.text("New monitor.powers1_g2v action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1")
dss.text("New monitor.Current1_g2v action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=1 ppolar=no mode=1")

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")

#cria loadshape 7.5 horas de carga (primeiras horas do dia)
n_pontos_curva = 96 #24* 4 
pontos_inicias = int(4*7.5)

ls = [0.0, 0.00, 0.0450, 0.0450, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
    0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
    0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# ls_f2 = [0.000571, 0.000571, 0.1021, 0.1021, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
#     0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
#     0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#ajusta loadshape das fases 2 e 3
# path_machine = "C:\\Users\\alves"
# path_opendss_exports = "\\AppData\\Local\\OpenDSS"
# file_name = "\\IEEE13Nodeckt_Mon_powers1_g2v_1.csv"
# file_exported_to_read = path_machine +path_opendss_exports+file_name
# ls_f2_v2 = functions.create_custom_ls_g2v(file_exported_to_read,'C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_g2v_f23.csv',ls)

ls_f2_v2 = [0.05302457142857146, 0.05302857142857143, 0.12039028571428567, 0.12042857142857144, 0.12040857142857146, 0.15697142857142854, 0.17413714285714285, 0.17413714285714285, 0.17413714285714285, 0.17985142857142855, 0.19183199999999995, 0.19298285714285712, 0.19308400000000003, 0.211028, 0.21104, 0.21104, 0.21104, 0.20989714285714284, 0.2119657142857143, 0.21196800000000002, 0.21196800000000002, 0.19038628571428567, 0.19037714285714283, 0.19037714285714283, 0.17323428571428567, 0.17323428571428567, 0.1347297142857143, 0.13454171428571426, 0.13474457142857138, 0.08753542857142861, 0.08728971428571429, 0.08729142857142855, 0.1101485714285714, 0.1101485714285714, 0.05134285714285714, 0.05189142857142859, 0.05189142857142859, 0.01709142857142857, 0.017588571428571446, 0.05758857142857145, 0.05758857142857145, 0.05758857142857145, 0.04837142857142859, 0.04837142857142859, 0.04837142857142859, 0.013080000000000008, 0.013074285714285696, 0.013074285714285696, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03423542857142853, 0.03423371428571426, 0.03423371428571426, 0.058727428571428555, 0.05874285714285715, 0.05874285714285715]
# TESTE PARA VERIFICAR INFLUENCIA DO AUMENTO DO CONSUMO NA TENSAO
# ls_f2_v2 = [0.805302457142857146, 0.805302857142857143, 0.812039028571428567, 0.812042857142857144, 0.812040857142857146, 0.815697142857142854, 0.817413714285714285, 0.817413714285714285, 0.817413714285714285, 0.817985142857142855, 0.819183199999999995, 0.819298285714285712, 0.819308400000000003, 0.8211028, 0.21104, 0.21104, 0.21104, 0.20989714285714284, 0.2119657142857143, 0.21196800000000002, 0.21196800000000002, 0.19038628571428567, 0.19037714285714283, 0.19037714285714283, 0.17323428571428567, 0.17323428571428567, 0.1347297142857143, 0.13454171428571426, 0.13474457142857138, 0.08753542857142861, 0.08728971428571429, 0.08729142857142855, 0.1101485714285714, 0.1101485714285714, 0.05134285714285714, 0.05189142857142859, 0.05189142857142859, 0.01709142857142857, 0.017588571428571446, 0.05758857142857145, 0.05758857142857145, 0.05758857142857145, 0.04837142857142859, 0.04837142857142859, 0.04837142857142859, 0.013080000000000008, 0.013074285714285696, 0.013074285714285696, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03423542857142853, 0.03423371428571426, 0.03423371428571426, 0.058727428571428555, 0.05874285714285715, 0.05874285714285715]

plt.plot(ls_f2_v2)
plt.show()


dss.text(f"New LoadShape.G2V npts={n_pontos_curva}  interval={0.25}  mult={ls}")
dss.text(f"New LoadShape.G2V_f2_v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=252   kvar=0 daily=G2V")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V_f2_v2")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V_f2_v2") 
#print(dss.Cicruit.LoadShapes.Mult)



dss.solution.solve()
dss.text("Show Losses            ")
#dss.text("show voltages")
#dss.text("plot profile")  #tensao em pu
#dss.text("plot Loadshape Object=DEFAULT")
dss.text("plot Loadshape Object=G2V")
dss.text("plot Loadshape Object=G2V_f2_v2")
#dss.text("plot Loadshape Object=G2V_f2_v2")
#dss.text("plot monitor object=powers2 labels=Yes")
dss.text("plot monitor object=powers1_g2v")
print('plotado para salvar dados')
resultados = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-POWERS1_G2V-ch1-ch3-ch5.DSV')

dss.text("plot monitor object=Current1_g2v")
tensao = functions.read_file_montior('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-Current1_G2V-ch1-ch3-ch5.DSV')
base = 2400 #volts
tensao_pu = [i/base for i in tensao]
print("tensao_pu: ", tensao_pu)



dss.text("plot monitor object=Current1_g2v channel=[15]")  # verificar corrente de neutro
resultados_corrente_neutro = functions.read_file_montior_neutral_current('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_MONITOR-Current1_G2V-ch15.DSV')
print("Max neutral current:", resultados_corrente_neutro[0], " Min neutral current:", resultados_corrente_neutro[1])


#dss.text("export monitor object=powers1_g2v") #salva em uma pasta temp
#dss.text("plot monitor object=Current1 channel=[15 16] ")

#dss.text("plot monitor object=Current1 channel=[1 3 5] ")


# ## plotagem de todos os monitors: positivo - consumo; negativo - geração
# monitors_names = dss.monitors_all_names()
# n_monitors = len(monitors_names)

# z=dss.monitors_first()

# for i in range(n_monitors):
#     dss.monitors_read_element()
#     z=dss.monitors_next()
#     for h in range(7):
#         plt.plot(dss.monitors_channel(h))
# dss.monitors_count()
# plt.show()

# ls_f2_v2 = functions.create_custom_ls('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_1_v2.csv',ls_f2)

# dss.text(f"New LoadShape.G2V_f2v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
# dss.text("edit Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=G2V_f2v2")
# dss.solution_solve()

# dss.text("plot Loadshape Object=G2V_f2v2")
# dss.text("plot monitor object=powers1")


# dss.text("Show Voltages LN Nodes ")
# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
# dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")

print('Loading')