import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes
import numpy as np


circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
dss = py_dss_interface.DSS() # usa versao fornecida por py_dss_interface
#dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")
dss.text("New EnergyMeter.medidor1_pm1 element=Transformer.Sub terminal=1")
dss.text("New EnergyMeter.medidor1_pm element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2_pm element=Line.632633  terminal=1")
dss.text("New monitor.powers1_comb_pm action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=1")
dss.text("New monitor.powers2_comb_pm action=Save element=Transformer.XFM1  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2_pm action=Save element=Line.632633  terminal=1 ppolar=no mode=1")

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=160   kvar=110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=120   kvar=90  daily=DEFAULT")


ls = [0.0, 0.00, 0.0450, 0.0450, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
    0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
    0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

ls_24pts_v1 = functions.ls_96_to_24(ls)

print(ls_24pts_v1)
# para testar energymeter no inicio da linha
# for index, elem in enumerate(ls_24pts_v1):
#     ls_24pts_v1[index] = elem * 500
hr =  range(0, len(ls_24pts_v1))
# plt.plot(hr, ls_24pts_v1)
# plt.show()
# print('oi')
#ls_f2_v2 = [0.05302457142857146, 0.05302857142857143, 0.12039028571428567, 0.12042857142857144, 0.12040857142857146, 0.15697142857142854, 0.17413714285714285, 0.17413714285714285, 0.17413714285714285, 0.17985142857142855, 0.19183199999999995, 0.19298285714285712, 0.19308400000000003, 0.211028, 0.21104, 0.21104, 0.21104, 0.20989714285714284, 0.2119657142857143, 0.21196800000000002, 0.21196800000000002, 0.19038628571428567, 0.19037714285714283, 0.19037714285714283, 0.17323428571428567, 0.17323428571428567, 0.1347297142857143, 0.13454171428571426, 0.13474457142857138, 0.08753542857142861, 0.08728971428571429, 0.08729142857142855, 0.1101485714285714, 0.1101485714285714, 0.05134285714285714, 0.05189142857142859, 0.05189142857142859, 0.01709142857142857, 0.017588571428571446, 0.05758857142857145, 0.05758857142857145, 0.05758857142857145, 0.04837142857142859, 0.04837142857142859, 0.04837142857142859, 0.013080000000000008, 0.013074285714285696, 0.013074285714285696, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.03423542857142853, 0.03423371428571426, 0.03423371428571426, 0.058727428571428555, 0.05874285714285715, 0.05874285714285715]

# ls_24pts_v23 = functions.ls_96_to_24(ls_f2_v2)

# plt.plot(ls_24pts_v23)
# plt.show()
print("oi")

dss.text(f"New LoadShape.comb_v2_pm npts={24}  interval={1}  mult={ls_24pts_v1}")

# dss.text("plot Loadshape Object=DEFAULT")

#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-252   kvar=0 daily=comb_v2_pm")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=comb_v2_pm")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=comb_v2_pm")

# dss.text("plot Loadshape Object=comb_v2_pm")

dss.solution.solve()
# dss.text("plot monitor object=powers1_comb_pm") # para salvar as potencias
print('plotado para salvar dados')

buses =  dss.circuit.buses_names
mv_buses = list()
mv_bus_voltage_dict = dict()

for bus in buses:
    dss.circuit.set_active_bus(bus)
    num_phases = len(dss.bus.nodes)
    print(num_phases)
    if num_phases == 3:
        mv_buses.append(bus)
        mv_bus_voltage_dict[bus] = dss.bus.kv_base

percent = 0.95

selected_buses =random.sample(mv_buses, int(percent * len(mv_buses)))
selected_buses = sorted(set(selected_buses))
# selected_buses = ['632', '633', '634', '650', '670', '671', '675', '680', '692', 'sourcebus']
carga =ls_24pts_v1

for index, elem in enumerate(carga):
    carga[index] = elem * 50000 #50
color = 'tab:red'
plt.xlabel('Horas')
plt.ylabel('V [pu]', color=color)
plt.plot(hr,carga)
plt.show()

for bus in selected_buses:
    print(f"New LoadShape.Semana npts={24}  interval={1}  mult={carga}\n")
    dss.text(f"New LoadShape.Semana npts={24}  interval={1}  mult={carga}")
    print(f"New Load.{bus}abc Bus1={bus}  Phases=3 daily=Semana\n")
    dss.text(f"New Load.{bus}abc Bus1={bus}  Phases=3 daily=Semana")


dss.text("Interpolate")
dss.solution.solve()
dss.text("plot profile phases=all")
print("here2")

register_names = dss.meters.register_names 
register_values = dss.meters.register_values

#############################################

# List with elements starting from Line.684652 back to the Vsource.source
element_list = list()

dss.topology._branch_name_write("Line.684652")
element_list.append(dss.topology._branch_name_read())

while dss.topology._backward_branch():
    active_element = dss.topology._branch_name_read()
    element_list.append(active_element)

    # Need power flow results
    cktelement_name = dss.cktelement._name()  # I tested and it name is the active_element
    v = dss.cktelement._powers()

    # Need read/write data (line example)
    if active_element.split(".")[0].lower() == "line":
        line_name = dss.lines._name_read()  # I tested and it name is the active_element
        rmatrix = dss.lines._rmatrix_read()
    else:
        line_name = None

    print(f"Topology: {active_element}, cktelement: {cktelement_name}, line: {line_name}")

print(element_list)

print("here2")


