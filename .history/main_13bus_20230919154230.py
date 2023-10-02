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
dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")

dss.solution_solve()
dss.text("show voltages")

lista = funcoes.create_LS(96)

plt.plot(lista)
plt.ylabel('some numbers')
plt.show()
print("k")