import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes
# https://dss-extensions.org/dss_properties.html
circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
dss = py_dss_interface.DSS() # usa versao fornecida por py_dss_interface
# dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

# dss.text("set mode=daily")
# dss.text("set number=96")
# dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")

dss.text("New monitor.powers1 action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1") # mode= 1 medir Potencia ativa
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=1 ppolar=no mode=1")
dss.text("New monitor.Current1 action=Save element=Transformer.XFM1 terminal=1 ppolar=no mode=0")

lsDEF96pts1 = [0.677,0.677                 , 0.677                ,0.677, 0.6256,0.6256,0.6256,0.6256, 0.6087,0.6087,0.6087,0.6087, 0.5833,0.5833,0.5833,0.5833, 0.58028,0.58028,0.58028,0.58028, 0.6025, 0.6025, 0.6025, 0.6025, 0.657,0.657,0.657,0.657, 0.7477,0.7477,0.7477,0.7477, 0.832,0.832,0.832,0.832, 0.88,0.88,0.88,0.88, 0.94,0.94,0.94,0.94, 0.989,0.989,0.989,0.989, 0.985, 0.985, 0.985, 0.985, 0.98,0.98,0.98,0.98, 0.9898,0.9898,0.9898,0.9898, 0.999,0.999,0.999,0.999, 1,1,1,1, 0.958,0.958,0.958,0.958, 0.936,0.936,0.936,0.936, 0.913,0.913,0.913,0.913, 0.876,0.876,0.876,0.876, 0.876,0.876,0.876,0.876, 0.828,0.828,0.828,0.828, 0.756, 0.756, 0.756, 0.756]
lsDEF96pts2 = [1,1,1,1,1,1,1,1, 1,1,1,1, 0.5833,0.5833,0.5833,0.5833, 0.58028,0.58028,0.58028,0.58028, 0.6025, 0.6025, 0.6025, 0.6025, 0.657,0.657,0.657,0.657, 0.7477,0.7477,0.7477,0.7477, 0.832,0.832,0.832,0.832, 0.88,0.88,0.88,0.88, 0.94,0.94,0.94,0.94, 0.989,0.989,0.989,0.989, 0.985, 0.985, 0.985, 0.985, 0.98,0.98,0.98,0.98, 0.9898,0.9898,0.9898,0.9898, 0.999,0.999,0.999,0.999, 1,1,1,1, 0.958,0.958,0.958,0.958, 0.936,0.936,0.936,0.936, 0.913,0.913,0.913,0.913, 0.876,0.876,0.876,0.876, 0.876,0.876,0.876,0.876, 0.828,0.828,0.828,0.828, 0.756, 0.756, 0.756, 0.756]

# loadShape mais intensa
ls_f2_v2   = [ 0.00000000000000000000,  0.00000000000000000000, 0.0008108571428571817, 0.0007897142857142723, 0.0029445714285714075, 0.0030337142857143006, 0.0037022857142857543, 0.0036920000000000234, 0.0036920000000000234, 0.003916571428571436, 0.003987999999999943, 0.0040320000000000225, 0.00393885714285716, 0.004108571428571476, 0.004108571428571395, 0.004108571428571395, 0.004108571428571395, 0.004065142857142844, 0.0041474285714285285, 0.004147428571428609, 0.004147428571428609, 0.003927428571428615, 0.003933142857142847, 0.003933142857142847, 0.003258857142857161, 0.0032748571428571236, 0.0029017142857143035, 0.003055428571428576, 0.0028691428571428496,  0.000000000000000000,  0.00000000000000000,  0.00000000000000000,  0.00000000000000000,  0.000000000000000000, 0.0035857142857142685, 0.0032994285714285504, 0.005299428571428552, 0.03507028571428572, 0.03482914285714282, 0.035249714285714245, 0.03324971428571432, 0.03325028571428577, 0.06819485714285714, 0.07319428571428571, 0.07319428571428571, 0.10291885714285709, 0.10292457142857148, 0.10292457142857148, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.10285714285714287, 0.910285714285714287, 0.910285714285714287, 0.910285714285714287, 0.910285714285714287, 0.910285714285714287, 0.911085714285714288, 0.911085714285714288, 0.911085714285714288, 0.910785714285714287, 0.910785714285714287, 0.910785714285714287, 0.910785714285714287, 0.908285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.08285714285714288, 0.06785714285714287, 0.06785714285714287, 0.06785714285714287, 0.05285714285714286, 0.05285714285714286, 0.05385714285714286, 0.05385714285714286, 0.05435714285714286, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.029857142857142853, 0.0003782857142857199, 0.0003782857142857199, 0.0003782857142857199,  0.000000000000000000,  0.000000000000000000,  0.000000000000000000]

# plt.plot(ls_f2_v2)
# plt.plot(lsDEF96pts2)
# plt.show()

n_pontos_curva = 96 #24* 4 

dss.text(f"New LoadShape.G2V_f2_v2 npts={n_pontos_curva}  interval={0.25}  mult={lsDEF96pts2}")


#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=G2V_f2_v2")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=G2V_f2_v2")

# dss.solution.solve()


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
ax1.set_xlabel('Horas')
ax1.set_ylabel('V [pu]', color=color)




plt.axhline(y = 1.05, color = "orange", label = "limite superior adequada", ls = '--', lw = 2.5)
# plt.axhline(y = 0.95, color = "red", label = "limite inferior adequada", ls = '--', lw = 2.5)
ax1.plot(x_inf, v_mag_pu.loc["rg60.1",:],color = "green", label = "RG60",  lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.1",:],color = "Blue", label = "634.1",  lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.2",:],color = "black", label = "634.2", lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.3",:],color = "purple", label = "634.3",  lw = 1.5)
plt.legend()


ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'

ax2.set_ylabel('pu', color=color)  # we already handled the x-label with ax1
ax2.plot(x_inf,lsDEF96pts2,color = "red", label = "LoadShape_Bus1=634.2_Bus1=634.3",  lw = 2.0)

plt.legend()
plt.ylabel("V [pu]")
plt.xlabel("Horas")
plt.show()

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

print(v_mag_pu.transpose().sort_values(by="634.2", ascending=False).head())
print(v_mag_pu.transpose().describe())
print(v_mag_pu.transpose().describe()["634.2"])

# df[(df["Churn"] == 0) & (df["International plan"] == "No")]["Total intl minutes"].max()
# df[(v_mag_pu["Churn"] == 0) & (df["International plan"] == "No")]["Total intl minutes"].max()
# v_mag_pu[v_mag_pu > 1.05]
print(v_mag_pu[v_mag_pu > 1.05])







dss.text("plot Loadshape Object=DEFAULT")
#dss.text("plot monitor object=powers2")
dss.text("plot monitor object=powers1")
dss.text("plot monitor object=Current1 channel=[15]")
# dss.text("plot EnergyMeter object=medidor1")
dss.text("Show Voltages LN Nodes ")
# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")





print("\n================================")
