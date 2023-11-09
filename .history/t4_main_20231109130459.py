import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes


random.seed(114)

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"
dss = py_dss_interface.DSS() # usa versao fornecida por py_dss_interface 
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")
circuit_pu = 1.045
load_variation1 = 0.8
percent = 0.2
p_step = 1
kva_to_kw = 1
location = 114
pf =1


dss.text(f"Compile [{dss_file}]")
dss.text("Buscoords  BusCoords.dat")
dss.text(f"edit Vsource.Source pu ={circuit_pu}")
dss.text("edit TRANSFORMER.REG1A XHL=0.0000000001")
dss.text(f"edit Vsource.Source pu ={circuit_pu}") # PQ linha 22 e 24 sao iguais?

dss.text("New energyMeter.M1 element=TRANSFORMER.REG1A terminal=1")

dss.text("New monitor.powers action=Save element=TRANSFORMER.REG1A terminal=1 ppolar=no mode=0")
dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")

dss.solution.solve()
dss.text("show voltages")
dss.text("plot profile")
#dss.text("plot monitor object=powers")

load_variation1 = 1
all_nodes_names_v_min= dict()
all_nodes_names_v_max= dict()
for i in range(3):
    

    dss.text(f"set Loadmult = {load_variation1}")

    dss.solution_solve()
    #dss.text("plot profile")

    #PArte 1-B

    voltages = dss.circuit_all_bus_vmag_pu()
    v_max = max(voltages)
    index_v_max = voltages.index(v_max)
    v_min = min(voltages)
    index_v_min = voltages.index(v_min)
    all_nodes_names = dss.circuit_all_node_names()
    
    node_v_max = all_nodes_names[index_v_max]
    all_nodes_names_v_max[node_v_max] = v_max

    node_v_min = all_nodes_names[index_v_min]
    all_nodes_names_v_min[node_v_min] = v_min
    # temp_v_max = funcoes.find_bus(v_min, dss)
    print("node_v_max: ", node_v_max, "node_v_min: ",node_v_min)
    
    print("v_max: ", v_max,"index_v_max: ", index_v_max, "v_min: ", v_min,"index_v_min: ",index_v_min, 'load_variation1: ',load_variation1)
    load_variation1 = load_variation1 * 1.05

#dss.solution_solve()
dss.text("plot monitor object=powers")
#Parte 1-C

power = dss.circuit_total_power()

print('Power is:', power)




for bus in all_nodes_names_v_max:
    b =  bus.split('.')[0] #descratar as fases
    functions.add_bus_marker(dss, b, "green", 5)


for bus in all_nodes_names_v_min:
    b =  bus.split('.')[0] #descratar as fases
    functions.add_bus_marker(dss, b, "red", 5)



# feederhead_kw=-1*dss.circuit_total_power()[0]
# feederhead_kvar=-1*dss.circuit_total_power()[1]

# #Parte 2-A
# # Encontrar barras trifásicas
# mv_buses = list()
# # Mapear as tensões na barra por um dicionário
# bus_voltage_dict = dict()

# # Retorna o nome de cada barra
# buses = dss.circuit_all_bus_names()

# # Encontrar número e identificar barras

# for bus in buses:
#     # Ativar pela interface circuit para pegar número de nós
#     dss.circuit_set_active_bus(bus)
#     kv_bus = dss.bus_kv_base() #LN voltage
#     # Comando len Retorna o número de fases
#     num_phases =len(dss.bus_nodes())

#     if kv_bus > 1.0 and num_phases == 3 and bus != '150' and bus != '150r' and bus != '149':

#         # Adiciona elementos na barra selecionada
#         mv_buses.append(bus)

#         # Associa tensão a variável bus_voltage_dict
#         bus_voltage_dict[bus] = kv_bus
#         bus_voltage_dict[bus] = kv_bus

# cont3f = len(mv_buses)


# #Parte 2-B
#   # Pacote random para escolher aleatoriamente número de barras (importar pacote random)
#   # seed fixa a semente usada para simular os números aleatórios
# random.seed(location)

# # Seleciona um percentual das barras selecionadas
# selected_buses = random.sample(mv_buses, int(percent*len(mv_buses)))

# # Função para ativar pv system nas barras selecionadas e marca-las no diagrama
# # Para fazer isto deve-se ativar a função functions
# #bus_voltage_dict[bus] permite acessar a tensão pelo dicionário

# for bus in selected_buses:
#     # p_step (Altera potência ativa no hc)
#     functions.define_3ph_pvsystem(dss, bus, bus_voltage_dict[bus], kva_to_kw*p_step, p_step)
#     functions.add_bus_marker(dss, bus, "red", 5)

# # Calcular fluxo de potência
#dss.solution_solve()

# Plotar circuito com pvs marcados
dss.text("plot circuit Power max=2000 n n C1=$00FF0000")
print("here")


# #Parte 3-A - Avaliar violações de tensão e potência (Método de HC)
# ov_violation = False
# thermal_violation = False

# i=0

# #Quando existe violação do while, o processo para
# while not ov_violation and not thermal_violation and i<1000:
#     i+=1
#     functions.increment_pv_size(dss, p_step, kva_to_kw,pf, i)

#     # Resolve o fluxo de potência
#     dss.solution_solve()
#     # Obtem as tensões das barras
#     voltages = dss.circuit_all_bus_vmag_pu()
#     # Cálcula o Vmax
#     v_max = max(voltages)
#     # Testa violação de tensão
#     if v_max > 1.05:
#         ov_violation = True

#     # Obtem as correntes

#     dss.lines_first()

#     # Obtendo as correntes
#     for _ in range(dss.lines_count()):
#         dss.circuit_set_active_element(f"line.{dss.lines_read_name}")
#         current = dss.cktelement_currents_mag_ang()
#         rating_current = dss.lines_read_norm_amps()
#         # Elementos de corrente com módulos (3) ângulos (3) entrada e saída (12 elmentos)
#         # [0: 12: 2]  - Varre de 0 até 12 e pega de 2 em 2
#         if max(current[0:12:2]) > rating_current:
#             thermal_violation = True
#             break
# # Quando violar volta um ponto e se encontra o HC 
# functions.increment_pv_size(dss, p_step, kva_to_kw,pf, i-1)
