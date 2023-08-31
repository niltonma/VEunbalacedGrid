import py_dss_interface
import pandas as pd


def read_save_loads(dss, path_to_save_df):

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
        #energy_kva = dss.loads_read_kva()
        name = dss.loads_read_name()
        list_energy_kw.append(energy_kw)
        list_energy_kvar.append(energy_kvar)
        list_energy_name.append(name)
        print(energy_kw, energy_kvar)

        dss.loads_next()
    # save 
    # df1 = pd.DataFrame([1, 2, 3], index=["a", "b", "c"], columns=["x"])
    df_p_kw = pd.DataFrame(list_energy_kw, index=all_names, columns=["P_Kw"])
    df_q_kvar= pd.DataFrame(list_energy_kvar, index=all_names, columns=["Q_Kvar"])
    df_p_kw.to_csv(path_to_save_df+'\df_p_kw.csv')
    df_q_kvar.to_csv(path_to_save_df+'\df_p_kvar.csv')

  
