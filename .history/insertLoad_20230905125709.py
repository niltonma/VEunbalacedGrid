import py_dss_interface
import random
#import matplotlib.pyplot as plt
import pandas as pd
import os
import funcoes

path_to_save_df = r'C:\Users\alves\Documents\OpenDSS\replicar_artigos'

random.seed(114)
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS") # usa versao da maquina
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 

dss.text(f"Compile [{dss_file}]")
dss.text("Buscoords  BusCoords.dat")
dss.text("New EnergyMeter.Feeder Line.L115 1")
dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")

dss.solution_solve()
dss.text("plot profile phases=all")
print("here")

buses = dss.circuit_all_bus_names()

mv_buses = list()
mv_bus_voltage_dict = dict()

for bus in buses:
    dss.circuit_set_active_bus(bus)
    num_phases = len(dss.bus_nodes())

    if num_phases == 3:
        mv_buses.append(bus)
        mv_bus_voltage_dict[bus] = dss.bus_voltage()

percent = 0.1
selected_buses =random.sample(mv_buses, int(percent * len(mv_buses)))
print("here")