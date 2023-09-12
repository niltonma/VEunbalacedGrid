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
        mv_bus_voltage_dict[bus] = dss.bus_kv_base()

percent = 0.8


selected_buses =random.sample(mv_buses, int(percent * len(mv_buses)))
selected_buses = sorted(set(selected_buses))

for bus in selected_buses:
    #carga =funcoes.create_load_shape()
    dss.text("New LoadShape.Semana npts=24  interval=1  mult=(0 0 0 0 0 0 0 0 0 0 0 0 -0.4352945582710477 -0.4599901380457315 -0.47928261720234 -0.6324155092982278 0 0.2238169525946716 0.8234655360471604 0.5631497375909773 0.9349134637001743 0 0 1)")
    dss.text(f"New Load.{bus} Bus1={bus}  Phases=3 daily=Semana Conn=Wye   Model=1 kV=2.4   kW=20.0  kvar=10.0")
    print(f"New Load.{bus} Bus1={bus}  Phases=3 daily=Semana Conn=Wye   Model=1 kV=2.4   kW=20.0  kvar=10.0")
    #dss.text(f"New LoadShape.Semana npts=[{24}]  interval=[{1}]  mult=[{carga}]")
    #funcoes.define_3ph_EV(bus,24,1, carga) nao funciona, nao sei pq 

dss.text("Interpolate")
dss.solution_solve()
dss.text("plot profile phases=all")
print("here2")