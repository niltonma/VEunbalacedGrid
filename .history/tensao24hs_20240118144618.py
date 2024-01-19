import py_dss_interface # biblioteca do OpenDSS versão 2.0.2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, functions, funcoes

mode =0 #0: caso base, 1: com carregamento
num_H = 24
dss = py_dss_interface.DSS()
arquivo_dss = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt"






if mode == 0: ##  caso base
    dss.text("clear")
    dss.text("compile [{}]".format(arquivo_dss))
    dss.dssinterface.allow_forms = 0 # 0 - bloqueia os pop-ups do OpenDSS // 1 - permite os pop-ups do OpenDSS
    
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

    dss.text(f"New LoadShape.comb_v2_pm npts={24}  interval={1}  mult={ls_24pts_v1}")

    ## Medidor em todas as linhas para medir tensao
    linhas =[650632, 632670, 670671, 671680, 632633, 632645, 645646, 692675, 671684, 684611, 684652]
    for index, elem in enumerate(linhas):
        print(f"New monitor.Tensao{index} action=Save element=Line.{elem}  terminal=1 ppolar=no mode=0")
        dss.text(f"New monitor.Tensao{index} action=Save element=Line.{elem}  terminal=1 ppolar=no mode=0")
        

    dss.text("calcv")
    dss.text("set mode=daily")
    node_list = dss.circuit.nodes_names #nome dos nós
    n_node_list = len(node_list) #número de nós

    Losses = np.zeros(num_H)
    v_mag = np.zeros((num_H, n_node_list))
    v_mag_pu = np.zeros((num_H, n_node_list))
    for h in range(num_H):
        dss.text("set stepsize=1h") # passo de 1h
        dss.text("set number=1")    # número de iterações
        dss.text(f"set hour={h}")   # hora do dia
        dss.text("solve")           # resolve o circuito
        v_mag[h,:] = dss.circuit.buses_vmag #tensão em módulo
        v_mag_pu[h,:] = dss.circuit.buses_vmag_pu #tensão em módulo pu
        Losses[h] = (dss.circuit.losses[0]/1000) #perdas em kW
        if h == 13 :
            dss.dssinterface.allow_forms = 1
            dss.text("Plot Profile Phases=All")
            dss.dssinterface.allow_forms = 0
    dss.text("export monitor carga")
    dss.text("export monitor linha")
    print("oi")