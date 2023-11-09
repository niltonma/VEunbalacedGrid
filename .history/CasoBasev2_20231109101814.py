import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes
# https://dss-extensions.org/dss_properties.html
circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
dss = py_dss_interface.DSS()

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")


dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")

dss.text("New monitor.powers1 action=Save element=Transformer.XFM1  terminal=2 ppolar=no mode=1") # mode= 1 medir Potencia ativa
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=1 ppolar=no mode=1")
dss.text("New monitor.Current1 action=Save element=Transformer.XFM1 terminal=1 ppolar=no mode=0")

# dss.text("New monitor.powers1 action=Save element=Transformer.XFM1  terminal=2 ppolar=yes mode=0") # mode= 0 medir tensao
# dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=yes mode=0")

default_loadShape = [ 0.677, 0.6256, 0.6087, 0.5833, 0.58028, 0.6025, 0.657, 0.7477, 0.832, 0.88, 0.94, 0.989, 0.985, 0.98, 0.9898, 0.999, 1, 0.958, 0.936, 0.913, 0.876, 0.876, 0.828, 0.756]

plt.plot(default_loadShape)
plt.show()
dss.text("New LoadShape.G2V_f3 npts=96  interval=0.25  mult=DEFAULT")

dss.text("plot Loadshape Object=DEFAULT")
dss.text("export Loadshape Object=DEFAULT")
dss.text("plot Loadshape Object=G2V")
dss.text("export Loadshape Object=G2V")
#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-160   kvar=-110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")


x_inf = [i/4 for i in range(1, 97)]

n_pontos_curva = 96 #24* 4 

dss.text("set mode=daily")
nodes_names = dss.circuit.nodes_names
v_mag_pu = pd.DataFrame(index=nodes_names, columns=range(n_pontos_curva))
v_mag = pd.DataFrame(index=nodes_names, columns=range(n_pontos_curva))
losses_kw = list()
for h in range(n_pontos_curva):  #96 pontos
    dss.text("set stepsize=15m")
    dss.text("set number=1")  #numero de interações
    dss.text(f"set hour={(h+1)/4}") # hora de inicio da simulacao
    dss.text("solve")
    v_mag[h]= dss.circuit.buses_vmag
    v_mag_pu[h] = dss.circuit.buses_vmag_pu
    losses_kw   = dss.circuit.losses[0]/1000  #perdas em kw

fig, ax1 = plt.subplots()


color = 'tab:red'
ax1.set_xlabel('Horas')
ax1.set_ylabel('V [pu]', color=color)




plt.axhline(y = 1.05, color = "orange", label = "limite superior adequada", ls = '--', lw = 2.5)
ax1.plot(x_inf, v_mag_pu.loc["rg60.1",:],color = "green", label = "RG60",  lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.1",:],color = "Blue", label = "634.1",  lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.2",:],color = "black", label = "634.2", lw = 1.5)
ax1.plot(x_inf,v_mag_pu.loc["634.3",:],color = "purple", label = "634.3",  lw = 1.5)
plt.legend()


ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('pu', color=color)  # we already handled the x-label with ax1
ax2.plot(x_inf,ls_f2_v2,color = "red", label = "LoadShape_Bus1=634.2_Bus1=634.3",  lw = 2.0)

plt.legend()
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()



# dss.text("plot Loadshape Object=DEFAULT")
#dss.text("plot monitor object=powers2")
dss.text("plot monitor object=powers1")
dss.text("plot monitor object=Current1 channel=[15]")
dss.text("plot EnergyMeter object=medidor1")
dss.text("Show Voltages LN Nodes ")
# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")

print("\n================================")
