import py_dss_interface
import random
import  functions
circuit_pu = 1.045
random.seed(114) # mantém os valores "aleatorios" iguais.
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")

dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
dss.text("New EnergyMeter.medidor1 element=Transformer.XFM1 terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")
dss.text("New monitor.powers1_g2v action=Save element=Transformer.XFM1  terminal=2 ppolar=no mode=1")
dss.text("New monitor.Current1 action=Save element=Transformer.XFM1  terminal=2 ppolar=no mode=0")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=no mode=1")

#carga original, caso base - CASE A:
dss.text("edit Load.634a Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-160   kvar=-110 daily=DEFAULT")
dss.text("edit Load.634b Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")
dss.text("edit Load.634c Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-120   kvar=-90  daily=DEFAULT")

#cria loadshape 7.5 horas de carga (primeiras horas do dia)
n_pontos_curva = 96 #24* 4 
pontos_inicias = int(4*7.5)
#i1 = int(4*3)
# i11 = int(4)
# i12 = int(4)
# i13 = int(4)
# i2 = int(4*3)
# #i3 = int(4*1.5)
# i31 = int(2*1.5)
# i32 = int(2*1.5)
# ls = []
# for i in range(i11):
#     ls.append(0.05)
# for i in range(i12):
#     ls.append(0.10)
# for i in range(i13):
#     ls.append(0.15)    
# for i in range(i2):
#     ls.append(0.15)
# for i in range(i31):
#     ls.append(0.12)
# for i in range(i32):
#     ls.append(0.06)    
# for i in range(n_pontos_curva-(i11+i12+i13+i2+i31+i32)):
#     ls.append(0)    
# print(ls)

ls = [0.0, 0.00, 0.0450, 0.0450, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
    0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
    0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# ls_f2 = [0.000571, 0.000571, 0.1021, 0.1021, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
#     0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
#     0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#ajusta loadshape das fases 2 e 3
ls_f2_v2 = functions.create_custom_ls_g2v('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_g2v_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_g2v_f23.csv',ls)


dss.text(f"New LoadShape.G2V npts={n_pontos_curva}  interval={0.25}  mult={ls}")
dss.text(f"New LoadShape.G2V_f2_v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
#case C (G2V): adicionar carga à carga original
#valores à adicionar:
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-252   kvar=0 daily=G2V")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=G2V_f2_v2")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=G2V_f2_v2") 
#print(dss.Cicruit.LoadShapes.Mult)



dss.solution_solve()
#dss.text("show voltages")
#dss.text("plot profile")  #tensao em pu
#dss.text("plot Loadshape Object=DEFAULT")
dss.text("plot Loadshape Object=G2V")
dss.text("plot Loadshape Object=G2V_f2_v2")
#dss.text("plot Loadshape Object=G2V_f2_v2")
#dss.text("plot monitor object=powers2 labels=Yes")
dss.text("plot monitor object=powers1_g2v")
#dss.text("export monitor object=powers1_g2v") #salva em uma pasta temp
#dss.text("plot monitor object=Current1 channel=[15 16] ")

#dss.text("plot monitor object=Current1 channel=[1 3 5] ")


# ## plotagem de todos os monitors: positivo - consumo; negativo - geração
# monitors_names = dss.monitors_all_names()
# n_monitors = len(monitors_names)

# z=dss.monitors_first()

# for i in range(n_monitors):
#     dss.monitors_read_element()
#     z=dss.monitors_next()
#     for h in range(7):
#         plt.plot(dss.monitors_channel(h))
# dss.monitors_count()
# plt.show()

# ls_f2_v2 = functions.create_custom_ls('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_1_v2.csv',ls_f2)

# dss.text(f"New LoadShape.G2V_f2v2 npts={n_pontos_curva}  interval={0.25}  mult={ls_f2_v2}")
# dss.text("edit Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=-168   kvar=0 daily=G2V_f2v2")
# dss.solution_solve()

# dss.text("plot Loadshape Object=G2V_f2v2")
# dss.text("plot monitor object=powers1")


print('Loading')