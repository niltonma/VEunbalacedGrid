import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd

random.seed(114)
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS") # usa versao da maquina
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 

dss.text(f"Compile [{dss_file}]")
dss.text("Buscoords  BusCoords.dat")
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
# dss.text("plot profile phases=1")
# dss.text("plot profile phases=2")
# dss.text("plot profile phases=3")
# dss.text("dump Line.L1 debug ")

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

dss.text("plot circuit Power max=2800 n n C1=$08FF0000")

#start read loads
dss.loads_first()
#read save and change loads

## read all bus
n_loads = dss.loads_count()
list_energy_kw =[]
list_energy_kvar =[]
list_energy_name =[]
all_names = dss.loads_all_names()
for i in range(n_loads):
    energy_kw = dss.loads_read_kw()
    energy_kvar = dss.loads_read_kvar()
    name = dss.loads_read_name()
    list_energy_kw.append(energy_kw)
    list_energy_kvar.append(energy_kvar)
    list_energy_name.append(name)
    print(energy_kw, energy_kvar)

    dss.loads_next()




# df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"], columns=["x"])
df_p_kw = pd.DataFrame(list_energy_kw, index=all_names, columns=["P_Kw"])
df_q_kvar= pd.DataFrame(list_energy_kvar, index=all_names, columns=["Q_Kvar"])
for i in range(n_loads):
    dss.loads_write_kw()
    dss.loads_write_kva()



print('here')