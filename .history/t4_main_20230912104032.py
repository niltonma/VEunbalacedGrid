import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os

random.seed(114)

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 

circuit_pu = 1.045
load_variation1 = 0.8
percent = 0.2
p_step = 1
kva_to_kw = 1
location = 114
pf =1


dss.text(f"Compile [{dss_file}]")
dss.text(f"edit Vsource.Source pu ={circuit_pu}")
dss.text("edit TRANSFORMER.REG1A XHL=0.0000000001")
dss.text(f"edit Vsource.Source pu ={circuit_pu}") # PQ linha 22 e 24 sao iguais?

dss.solution_solve()
#dss.text("plot profile")

load_variation1 = 0.2

dss.text(f"set Loadmult = {load_variation1}")

dss.solution_solve()
#dss.text("plot profile")

#PArte 1-B

voltages = dss.circuit_all_bus_vmag_pu()
v_max = max(voltages)
v_min = min(voltages)


#Parte 1-C

power = dss.circuit_total_power()

print('Power is:', power)

feederhead_kw=-1*dss.circuit_total_power()[0]
feederhead_kvar=-1*dss.circuit_total_power()[1]

#Parte 2-A
# Encontrar barras trifásicas
mv_buses = list()
# Mapear as tensões na barra por um dicionário
bus_voltage_dict = dict()

# Retorna o nome de cada barra
buses = dss.circuit_all_bus_names()

# Encontrar número e identificar barras

for bus in buses:
    # Ativar pela interface circuit para pegar número de nós
    dss.circuit_set_active_bus(bus)
    kv_bus = dss.bus_kv_base() #LN voltage
    # Comando len Retorna o número de fases
    num_phases =len(dss.bus_nodes())

    if kv_bus > 1.0 and num_phases == 3 and bus != '150' and bus != '150r' and bus != '149':

        # Adiciona elementos na barra selecionada
        mv_buses.append(bus)

        # Associa tensão a variável bus_voltage_dict
        bus_voltage_dict[bus] = kv_bus
        bus_voltage_dict[bus] = kv_bus

cont3f = len(mv_buses)
