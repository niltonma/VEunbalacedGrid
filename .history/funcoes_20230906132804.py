import py_dss_interface
import pandas as pd
import random

def define_3ph_EV(dss, npts, interval, mult):
    """"npts = 24 (no ptos of load) interval = 1 mult = (0.69 0.50 ... 0.89) --> 24 point """
    dss.text(f"New LoadShape.Semana npts=[{npts}]  interval=[{interval}]  mult=[{mult}]")
    #dss.text(f"New LoadShape.Semana npts=[{24}]  interval=[{1}]  mult=[{carga}]")

def create_load_shape():
    charge1 = -1 * random.random()
    charge2 = -1 * random.random()
    charge3 = -1 * random.random()
    charge4 = -1 * random.random()
    d1 = -1 * random.random()
    d2 = -1 * random.random()
    d3 = -1 * random.random()
    d4 = -1 * random.random()

    mult = f"(0 0 0 0 0 0 0 0 0 0 0 0 {charge1} {charge2} {charge3} {charge4} 0 {d1} {d2} {d3} {d4} 0 0 0)" 
    return mult

def read_save_loads(dss, path_to_save_df, save: bool):


    #read save and change loads

    ## read all bus
    n_loads = dss.loads_count()
    list_energy_kw =[]
    list_energy_kvar =[]
    list_energy_name =[]
    all_names = dss.loads_all_names()
    #start read loads
    dss.loads_first()
    for i in range(n_loads):
        energy_kw = dss.loads_read_kw()
        energy_kvar = dss.loads_read_kvar()
        #energy_kva = dss.loads_read_kva()
        name = dss.loads_read_name()
        list_energy_kw.append(energy_kw)
        list_energy_kvar.append(energy_kvar)
        list_energy_name.append(name)
        print(energy_kw, energy_kvar, dss.loads_read_name())

        dss.loads_next()
    # save 
    # df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"], columns=["x"])
    if save == True:
    
        df_p_kw = pd.DataFrame(list_energy_kw, index=all_names, columns=["P_Kw"])
        df_q_kvar= pd.DataFrame(list_energy_kvar, index=all_names, columns=["Q_Kvar"])
        df_p_kw.to_csv(path_to_save_df+'\df_p_kw.csv')
        df_q_kvar.to_csv(path_to_save_df+'\df_p_kvar.csv')
