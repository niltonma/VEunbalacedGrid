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
dss.text("set number=24")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1_pm element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2_pm element=Line.632633  terminal=1")
dss.text("New monitor.powers1_comb_pm action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1")
dss.text("New monitor.powers2_comb_pm action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2_pm action=Save element=Line.632633  terminal=1 ppolar=no mode=1")


ls = [0.0, 0.00, 0.0450, 0.0450, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
    0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
    0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ls_24pts_v1 = functions.ls_96_to_24(ls)

print(ls_24pts_v1)

# ls_24pts_v1 = list()
# count = 0
# for i in ls:
#     if count == 0:
#         ls_24pts_v1.append(i)
#     count += 1
#     if count == 4:
#         count = 0
         
print("oi")        

plt.plot(ls_24pts_v1)
plt.show()
ls_f2_v2 = [0.05302457142857146, 0.05302857142857143, 0.12039028571428567, 0.12042857142857144, 0.12040857142857146, 0.15697142857142854, 0.17413714285714285, 0.17413714285714285, 0.17413714285714285, 0.17985142857142855, 0.19183199999999995, 0.19298285714285712, 0.19308400000000003, 0.211028, 0.21104, 0.21104, 0.21104, 0.20989714285714284, 0.2119657142857143, 0.21196800000000002, 0.21196800000000002, 0.19038628571428567, 0.19037714285714283, 0.19037714285714283, 0.17323428571428567, 0.17323428571428567, 0.1347297142857143, 0.13454171428571426, 0.13474457142857138, 0.08753542857142861, 0.08728971428571429, 0.08729142857142855, 0.1101485714285714, 0.1101485714285714, 0.05134285714285714, 0.05189142857142859, 0.05189142857142859, 0.01709142857142857, 0.017588571428571446, 0.05758857142857145, 0.05758857142857145, 0.05758857142857145, 0.04837142857142859, 0.04837142857142859, 0.04837142857142859, 0.013080000000000008, 0.013074285714285696, 0.013074285714285696, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03423542857142853, 0.03423371428571426, 0.03423371428571426, 0.058727428571428555, 0.05874285714285715, 0.05874285714285715]


ls_24pts_v23 = list()
count = 0
for i in ls_f2_v2:
    if count == 0:
        ls_24pts_v23.append(i)
    count += 1
    if count == 4:
        count = 0


plt.plot(ls_24pts_v23)
plt.show()
print("oi")