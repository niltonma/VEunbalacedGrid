import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes


circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
#dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface
# dss = py_dss_interface.DSS.DSSDLL(r"C:\Program Files\OpenDSS")
dss = py_dss_interface.DSS()


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")


dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")
dss.text("New monitor.powers1_V2G action=Save element=Transformer.XFM1  terminal=2 ppolar=no mode=1")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=no mode=1")


#INSERIR MEDIDOR NA BARRA RG60 PARA VERIFICAR QUAL MOMENTO OCORRE A VIOLACAO DE TENSAO
#BARRA RG60 ESTA NA LINHA Line.650632
dss.text("New monitor.tensao action=Save element=Line.650632  terminal=2 ppolar=no mode=0") # mode=0 (monitoramento de tensões e corrente)

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-160   kvar=-110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")

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

## transforma a loadshape de 96 pontos para 24 pontos, pois nao consegui simular com 96
# n_pontos_curva = 24
# temp = list()
# for indice, value in enumerate(ls):
#     if indice == 0 or indice %4  == 0:
#         # print(indice, value)
#         temp.append(value)
# ls = temp
# print(len(ls))
# ls_f2 = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0020, 0.0026, 0.06, 0.060,
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



#comentado para verificar e fazer ajustes se precisar
#ls_f2_v2 = functions.create_custom_ls_v2g('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_v2g_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_v2g.csv',ls_f2)

#print(ls_f2_v2)

ls_f2_v2 = [-0.00024685714285721717, -0.00024685714285713596, 0.0008108571428571817, 0.0007897142857142723, 0.0029445714285714075, 0.0030337142857143006, 0.0037022857142857543, 0.0036920000000000234, 0.0036920000000000234, 0.003916571428571436, 0.003987999999999943, 0.0040320000000000225, 0.00393885714285716, 0.004108571428571476, 0.004108571428571395, 0.004108571428571395, 0.004108571428571395, 0.004065142857142844, 0.0041474285714285285, 0.004147428571428609, 0.004147428571428609, 0.003927428571428615, 0.003933142857142847, 0.003933142857142847, 0.003258857142857161, 0.0032748571428571236, 0.0029017142857143035, 0.003055428571428576, 0.0028691428571428496, -0.054729142857142796, -0.05454800000000002, -0.05455371428571425, -0.05221942857142856, -0.051619428571428566, 0.0035857142857142685, 0.0032994285714285504, 0.005299428571428552, 0.03507028571428572, 0.03482914285714282, 0.035249714285714245, 0.03324971428571432, 0.03325028571428577, 0.06819485714285714, 0.07319428571428571, 0.07319428571428571, 0.10291885714285709, 0.10292457142857148, 0.10292457142857148, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.11085714285714288, 0.11085714285714288, 0.11085714285714288, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.06785714285714287, 0.06785714285714287, 0.06785714285714287, 0.05285714285714286, 0.05285714285714286, 0.05385714285714286, 0.05385714285714286, 0.05435714285714286, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.0003782857142857199, 0.0003782857142857199, 0.0003782857142857199, -0.016674285714285753, -0.016689714285714266, -0.016689714285714266]
ls_f2_v2 = [ 0.00000000000000000000,  0.00000000000000000000, 0.0008108571428571817, 0.0007897142857142723, 0.0029445714285714075, 0.0030337142857143006, 0.0037022857142857543, 0.0036920000000000234, 0.0036920000000000234, 0.003916571428571436, 0.003987999999999943, 0.0040320000000000225, 0.00393885714285716, 0.004108571428571476, 0.004108571428571395, 0.004108571428571395, 0.004108571428571395, 0.004065142857142844, 0.0041474285714285285, 0.004147428571428609, 0.004147428571428609, 0.003927428571428615, 0.003933142857142847, 0.003933142857142847, 0.003258857142857161, 0.0032748571428571236, 0.0029017142857143035, 0.003055428571428576, 0.0028691428571428496,  0.000000000000000000,  0.00000000000000000,  0.00000000000000000,  0.00000000000000000,  0.000000000000000000, 0.0035857142857142685, 0.0032994285714285504, 0.005299428571428552, 0.03507028571428572, 0.03482914285714282, 0.035249714285714245, 0.03324971428571432, 0.03325028571428577, 0.06819485714285714, 0.07319428571428571, 0.07319428571428571, 0.10291885714285709, 0.10292457142857148, 0.10292457142857148, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.11085714285714288, 0.11085714285714288, 0.11085714285714288, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.10785714285714287, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.06785714285714287, 0.06785714285714287, 0.06785714285714287, 0.05285714285714286, 0.05285714285714286, 0.05385714285714286, 0.05385714285714286, 0.05435714285714286, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.0003782857142857199, 0.0003782857142857199, 0.0003782857142857199,  0.000000000000000000,  0.000000000000000000,  0.000000000000000000]

## transforma a loadshape de 96 pontos para 24 pontos, pois nao consegui simular com 96
# temp = list()
# for indice, value in enumerate(ls_f2_v2):
#     if indice == 0 or indice %4  == 0:
#         # print(indice, value)
#         temp.append(value)
# ls_f2_v2 = temp
# print(len(ls_f2_v2))
# #ls_f2_v2[20:24] = [0.75385714285714286, 0.729857142857142853, 0.7298571428571429, 0.5003782857142858]    
# print(ls_f2_v2[20:24])
# plt.plot(ls_f2_v2)
# plt.show()

dss.text(f"New LoadShape.G2V npts={n_pontos_curva}  interval={0.25}  mult={ls}")
dss.text(f"New LoadShape.G2V_f2_v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
dss.text(f"New LoadShape.G2V_f3 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=252   kvar=0 daily=G2V")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V_f2_v2")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0 daily=G2V_f2_v2") 

#######  Arthur ########

# v_mag_EOL= dict()
# v_mag_EOL_pu= dict()

x_inf = [i/4 for i in range(1, 97)]
# x_inf = [i for i in range(0, 24)]

x_min = [i for i in range(0, 1440, 15)]
dss.text("set mode=daily")
#dss.text("set number=96")
#dss.text("set stepsize=0.25h")
nodes_names = dss.circuit.nodes_names
v_mag_pu = pd.DataFrame(index=nodes_names, columns=range(n_pontos_curva))
v_mag = pd.DataFrame(index=nodes_names, columns=range(n_pontos_curva))
losses_kw = list()
for h in range(n_pontos_curva):  #96 pontos
# for h in x_min:  #96 pontos
    dss.text("set stepsize=15m")
    dss.text("set number=1")  #numero de interações
    dss.text(f"set hour={(h+1)/4}")
    dss.text("solve")
    # v_mag[h,:] = dss.circuit.buses_vmag
    v_mag[h]= dss.circuit.buses_vmag
    v_mag_pu[h] = dss.circuit.buses_vmag_pu
    losses_kw   = dss.circuit.losses[0]/1000  #perdas em kw

fig, ax1 = plt.subplots()


color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('exp', color=color)




# plt.axhline(y = 1.05, color = "orange", label = "limite superior adequada", ls = '--', lw = 2.5)
# plt.axhline(y = 0.95, color = "red", label = "limite inferior adequada", ls = '--', lw = 2.5)
ax1.plot(x_inf, v_mag_pu.loc["rg60.1",:],color = "green", label = "RG60",  lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.1",:],color = "Blue", label = "634.1",  lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.2",:],color = "black", label = "634.2", lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.3",:],color = "purple", label = "634.3",  lw = 1.5)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'

ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
ax2.plot(x_inf,ls_f2_v2,color = "yellow", label = "LoadShape",  lw = 2.0)

plt.legend()
# plt.ylabel("V [pu]")
# plt.xlabel("Horas")
# plt.show()

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

print(v_mag_pu.transpose().sort_values(by="634.1", ascending=False).head())
print(v_mag_pu.transpose().describe())
print(v_mag_pu.transpose().describe()["634.1"])

# df[(df["Churn"] == 0) & (df["International plan"] == "No")]["Total intl minutes"].max()
# df[(v_mag_pu["Churn"] == 0) & (df["International plan"] == "No")]["Total intl minutes"].max()
# v_mag_pu[v_mag_pu > 1.05]
print(v_mag_pu[v_mag_pu > 1.05])

print("done")
#############################3

# https://repositorio.ufu.br/bitstream/123456789/34549/1/Sobretens%C3%B5esCircuitosSecund%C3%A1rios.pdf

# dss.text("set mode=daily")

# maximos = list()
# minimos = list()
# medias = list()
# nodes_vpu_list = list()

# for i in range(24):
#     nodes_vpu_list = []
#     dss.text("Set hour = {}".format(i))
#     dss.text("Set number = 1")
#     dss.text("solve")
#     for node in range(len(dss.circuit.nodes_names[3:])):
#         if ".4" in dss.circuit.nodes_names[3:][node]:
#             continue
#         else:
#             nodes_vpu_list.append(dss.circuit.buses_vmag_pu[3:][node])
#     maximos.append(max(nodes_vpu_list))
#     minimos.append(min(nodes_vpu_list))
#     medias.append(sum(nodes_vpu_list)/len(nodes_vpu_list))

# plt.axhline(y = 1.059, color = "r", label = "limite superior precária", ls = ':', lw = 2.5)
# plt.axhline(y = 1.05, color = "orange", label = "limite superior adequada", ls = '--', lw = 2.5)
# # plt.axhline(y = 1.0, color = "k", label = "tensão de referência", lw = 2.5)
# plt.axhline(y = 0.91, color = "orange", label = "limite inferior adequada", ls = '--', lw = 2.5)
# plt.axhline(y = 0.86, color = "r", label = "limite inferior precária", ls = ':', lw = 2.5)
# plt.plot(range(len(maximos)), maximos, "k", ls = '--', label="Máximo", lw = 2)
# plt.plot(range(len(minimos)), minimos, "k", ls = ':', label="Mínimo", lw = 2)
# plt.plot(range(len(medias)), medias, "k", label="Média", lw = 2.5)
# plt.title("Perfil das Tensões do Circuito nos dias de Domingo com 35 Conexões Fotovoltaicas e Ajuste de Tap no Transformador.")
# plt.legend()
# plt.ylabel("V [pu]")
# plt.xlabel("Horas")

###############################3



# dss.solution_solve()
#dss.text("plot Loadshape Object=DEFAULT")

#dss.text("plot Loadshape Object=G2V")
#dss.text("plot monitor object=powers2 labels=Yes")
# dss.text("plot monitor object=powers1_V2G")
# # dss.text("plot monitor object=tensao")
# dss.text("plot monitor object=tensao channel=[5]")
# # dss.text("export monitor object=powers1_V2G") #salva em uma pasta temp

# dss.text("Show Voltages LN Nodes ")
# # dss.text("Show Currents Elem     ")
# # dss.text("Show Powers kVA Elem   ")
# # dss.text("Show Losses            ")
# # dss.text("Show Taps              ")

# dss.text("Show Currents residual=yes Elements")

## plotagem de todos os monitors: positivo - consumo; negativo - geração
# monitors_names = list()
# monitors_names = dss.monitors.names
# print("monitors_names is: ", monitors_names)
# n_monitors = len(monitors_names)

# z=dss.monitors._first()

# for i in range(n_monitors):
#     dss.monitors._element_read()
#     z=dss.monitors.next()
#     for h in range(7):
#         plt.plot(dss.monitors._channel(h))
# dss.monitors._count()
# plt.show()


print('Loading')
