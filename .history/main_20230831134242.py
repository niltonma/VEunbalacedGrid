<<<<<<< HEAD
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
dss.text("set mode=daily")
dss.text("set number=24")
dss.text("set stepsize=1h")
# dss.text("Set Maxiterations=100")
# dss.text("set maxcontrolit=100")
# dss.text("edit Reactor.MDV_SUB_1_HSB x=0.0000001")
# dss.text("edit Transformer.MDV_SUB_1 %loadloss=0.0000001 xhl=0.00000001")
# dss.text("edit vsource.source pu=1.045")

# Ex 1
# a) Voltage profile at peak load and at offpeak load

#! Define bus coordinates

# dss.text(f"batchedit load..* mode=1")
# dss.text("set loadmult=0.2")
dss.solution_solve()

dss.meters_write_name("feeder")
# dss.text("plot profile phases=1")
# dss.text("plot profile phases=2")
# dss.text("plot profile phases=3")
# dss.text("dump Line.L1 debug ")
energ_base_kwh   = 100000
energ_base_kvarh = 100000
# names
energ_kwh = dss.meters_register_names()[0]
losses_kwh = dss.meters_register_names()[12]
#values 
energ_cal_kwh = dss.meters_register_values()[0]
energ_cal_kvarh = dss.meters_register_values()[1]
losses_cal_kwh = dss.meters_register_values()[12]

dss.meters_reset()


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
    # dss.text("plot circuit Power max=2800 n n C1=$08FF0000")
# Obtenha o nome da imagem de plot
    plot_image_name = f"PowerPlot_{i}.png"
    # dss.text(f"PowerPlot_{i}.png")
    # Salve o plot como uma imagem
    # dssText.Command = f"set pane=1 bitmap={plot_image_name}"
    # dss.text(f"set bitmap={plot_image_name}")
# dss.text("Save circuit dir='C:\\Users\\alves\\Documents\\OpenDSS\\replicar_artigos\\ImpUnbGrid'")

#print graph
#dss.text("plot circuit Power max=2800 n n C1=$08FF0000")





#read_save_loads(dss,path_to_save_df, True)

# #start read loads
# dss.loads_first()



# #read save and change loads

# ## read all bus
# n_loads = dss.loads_count()
# list_energy_kw =[]
# list_energy_kvar =[]
# list_energy_name =[]
# all_names = dss.loads_all_names()
# for i in range(n_loads):
#     energy_kw = dss.loads_read_kw()
#     energy_kvar = dss.loads_read_kvar()
#     #energy_kva = dss.loads_read_kva()
#     name = dss.loads_read_name()
#     list_energy_kw.append(energy_kw)
#     list_energy_kvar.append(energy_kvar)
#     list_energy_name.append(name)
#     print(energy_kw, energy_kvar)

#     dss.loads_next()
# # save 
# # df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"], columns=["x"])
# df_p_kw = pd.DataFrame(list_energy_kw, index=all_names, columns=["P_Kw"])
# df_q_kvar= pd.DataFrame(list_energy_kvar, index=all_names, columns=["Q_Kvar"])
# df_p_kw.to_csv(path_to_save_df+'\df_p_kw.csv')
# df_q_kvar.to_csv(path_to_save_df+'\df_p_kvar.csv')
n_loads = dss.loads_count()
dss.loads_first()

#need to prepare to write in specifics buses
for i in range(n_loads):
    dss.loads_write_kw(dss.loads_read_kw() * (1+energ_factor_kwh)) # qdo aumenta P aumenta Q autmatically
    dss.loads_write_kvar(dss.loads_read_kvar()* (1+energ_factor_kvarh)) # qdo aumenta Q nao aumenta P autmatically
    dss.loads_next()    

dss.solution_solve()
read_save_loads(dss,path_to_save_df, False)


energ_cal_kwh = dss.meters_register_values()[0]
energ_cal_kvarh = dss.meters_register_values()[1]
losses_cal_kwh = dss.meters_register_values()[12]
