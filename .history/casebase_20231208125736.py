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

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 action=save element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=1")

dss.text("New monitor.powers1 action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1") # mode= 1 medir Potencia ativa
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=1 ppolar=no mode=1")
dss.text("New monitor.Current1 action=Save element=Transformer.XFM1 terminal=1 ppolar=no mode=0")

# dss.text("New monitor.powers1 action=Save element=Transformer.XFM1  terminal=2 ppolar=yes mode=0") # mode= 0 medir tensao
# dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=yes mode=0")


#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")

dss.solution.solve()

# dss.text("plot Loadshape Object=DEFAULT")
#dss.text("plot monitor object=powers2")
dss.text("plot monitor object=powers1")  # C:\Users\alves\AppData\Local\OpenDSS\
# dss.text("plot monitor object=Current1 channel=[15]") # current residual 
#dss.text("plot EnergyMeter object=medidor1") #acho q o comando esta errado
# dss.text("Visualize powers EnergyMeter.medidor1")
# dss.text("Visualize voltages EnergyMeter.medidor1")
# dss.text("Visualize currents EnergyMeter.medidor1")
dss.text("Show Voltages LN Nodes ")
# dss.text("Show Currents Elem     ")
# dss.text("Show Powers kVA Elem   ")
dss.text("Show Losses            ")
# dss.text("Show Taps              ")

dss.text("Show Currents residual=yes Elements")

print("\n================================")
