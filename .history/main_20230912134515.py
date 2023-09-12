import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os
from funcoes import read_save_loads

path_to_save_df = r'C:\Users\alves\Documents\OpenDSS\replicar_artigos'

random.seed(114)
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS") # usa versao da maquina
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 

dss.text(f"Compile [{dss_file}]")
dss.text("Buscoords  BusCoords.dat")
dss.text("New EnergyMeter.Feeder Line.L115 1")
dss.text("New monitor.powers element=Line.L115 terminal=1 ppolar=no mode=0")
dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")

dss.solution_solve()

dss.text("plot monitor object=powers")

dss.meters_write_name("feeder")

energ_base_kwh   = 100000
energ_base_kvarh = 100000
# names
energ_kwh = dss.meters_register_names()[0]
losses_kwh = dss.meters_register_names()[12]

energ_factor_kwh = 0

contador = 0
while (1 + energ_factor_kwh) >= 1.00:
#for j in range(10):
    #values 
    energ_cal_kwh = dss.meters_register_values()[0]
    energ_cal_kvarh = dss.meters_register_values()[1]
    losses_cal_kwh = dss.meters_register_values()[12]

    dss.meters_reset()

    contador += 1

    delta_energ_kwh = energ_base_kwh - energ_cal_kwh
    energ_factor_kwh = delta_energ_kwh / energ_base_kwh 

    delta_energ_kvarh = energ_base_kvarh - energ_cal_kvarh
    energ_factor_kvarh = delta_energ_kvarh / energ_base_kvarh 

    print('here1')

    read_save_loads(dss,path_to_save_df, False)

    for i in range(0, 5):

        bus = i
        color = "Green"
        size_marker = 2
        code = 15

        dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus, color, size_marker, code) )
    #print graph
    #dss.text("plot circuit Power max=2800 n n C1=$08FF0000")
    n_loads = dss.loads_count()

    dss.loads_first()

    #need to prepare to write in specifics buses
    for i in range(n_loads):
        dss.loads_write_kw(dss.loads_read_kw() * (1+energ_factor_kwh)) # qdo aumenta P aumenta Q autmatically
        #dss.loads_write_kvar(dss.loads_read_kvar()* (1+energ_factor_kvarh)) # qdo aumenta Q nao aumenta P autmatically
        dss.loads_next()    

    dss.solution_solve()
    read_save_loads(dss,path_to_save_df, False)


    energ_cal_kwh = dss.meters_register_values()[0]
    energ_cal_kvarh = dss.meters_register_values()[1]
    losses_cal_kwh = dss.meters_register_values()[12]
    print("losses_cal_kwh : ", losses_cal_kwh)
print(f'Valor do contador eh:  {contador}')
