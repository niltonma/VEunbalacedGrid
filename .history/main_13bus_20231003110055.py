import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes

circuit_pu = 1.045

random.seed(114)

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")

# dss.text(f"Compile [{dss_file}]")

# dss.text("New energyMeter.M1 element=TRANSFORMER.REG1A terminal=1")

# dss.text("New monitor.powers action=Save element=TRANSFORMER.REG1A terminal=1 ppolar=no mode=0")
# dss.text("set mode=daily")
# dss.text("set number=24")
# dss.text("set stepsize=1h")


 



#loadshape_name = r"C:\Users\alves\AppData\Local\OpenDSS\IEEE13Nodeckt_Loadshape_DEFAULT.DSV"
num_points = 96

# Create a list of multipliers for each 15-minute interval (e.g., 0:00, 0:15, 0:30, ...)
multipliers = [1.0] * num_points
dss.text(f"Compile [{dss_file}]")
# Set the loadshape data
# dss.loads_shape(loadshape_name, num_points, multipliers)
#dss.text("New LoadShape.diario npts=96 interval=0.25")
#  o comando "terminal" nao se refere a fase da qual vc esta inserindo o energymeter,
#  e sim em qual ponto da linha voce o colocar, ou seja, se no começo ou no final da linha,
#  por isso ele so aceita 1 e 2
#dss.text("New EnergyMeter.medidor1 element=Line.632633  terminal=1")
# https://sourceforge.net/p/electricdss/discussion/861976/thread/08d0bb5c/
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")

#dss.text("New monitor.powers1 action=Save element=Line.632633  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=no mode=0")

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")

# New EnergyMeter.medidor3 element=Transformer.XFM1 

dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=252   kvar=0")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0") 

dss.solution_solve()
# dss.text("show voltages")

#cria vetor com 96 pontos 
# carga = funcoes.create_LS(96)
# dss.text(f"New LoadShape.MyLoadShape  npts={96}  interval={0.25}  mult={carga}")
# # dss.text("export LoadShape.MyLoadShape")
# dss.text("export Loads")


# dss.text("plot Loadshape Object=DEFAULT")
# load_shape_data = dss.active_class_get("LoadShape").read()

#dss.text("set loadmult=0.3") # seta a carga com 30% da curva de carga
dss.text("New LoadShape.MyLoadShape")
dss.text("plot Loadshape Object=DEFAULT")
dss.text("plot monitor object=powers2")
# # Extract time and load values from the load shape data
# time_values = load_shape_data[0]
# load_values = load_shape_data[1]

# # Plot the load shape
# plt.plot(time_values, load_values)
# plt.title("Load Shape")
# plt.xlabel("Time (hours)")
# plt.ylabel("Load Multiplier")
# plt.grid(True)
# plt.show()


# plt.plot(carga)
# plt.ylabel('some numbers')
# plt.show()
print("k")