# -*- coding: utf-8 -*-
# @Time    : 3/24/2021 8:22 PM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : functions.py
# @Software: PyCharm

import pandas as pd



# df = pd.read_csv('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_1.csv')
# df2 = pd.read_csv('C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_1_v2.csv')
# #print(df)
# #calcular o erro
# #lista dos pontos desejados
# # print(df[' P2 (kW)'] -df2['meta'])
# # print((df[' P2 (kW)'] -df2['meta'])/1.75)
# type((df[' P2 (kW)'] -df2['meta'])/1.75)

# df['new'] = (df[' P2 (kW)'] -df2['meta'])/0.175
# #df['meta']
# df['new'].values.tolist()
# #df.values.tolist()


# ls_f2 = [0.0571, 0.0571, 0.1021, 0.1021, 0.04450, 0.0780, 0.0780, 0.0780, 0.0780, 0.0780, 0.0880, 0.0880, 0.09050, 0.10400, 
#     0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.10400, 0.08800, 0.08800, 0.08800, 0.08800, 0.08800, 0.05900,
#     0.055, 0.06, 0.005, 0, 0, 0.000, 0, 0, 0.02, 0.02, 0, 0.02, 0.02, 0.02, 0.02, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# df['ls_old'] = ls_f2
# df['ls_new'] = df['ls_old'] +df['new']
def create_custom_ls(power, power_goal, ls_old):
    """receves the power goal df exportes from opendss read power_goal_df 
    and creates the loadshape to achieve the power_goal"""
    df = pd.read_csv(power)
    df2 = pd.read_csv(power_goal)
    df['new'] = (df[' P2 (kW)'] -df2['meta'])*(0.1 /1.75)
    df['ls_old'] = ls_old
    df['ls_new'] = df['ls_old'] +df['new']
    loadshape  = df['ls_new'].values.tolist()

    return loadshape

# ll = create_custom_ls('C:\\Users\\alves\\AppData\\Local\\OpenDSS\\IEEE13Nodeckt_Mon_powers1_1.csv','C:\\Users\\alves\\Downloads\\IEEE13Nodeckt_Mon_powers1_1_v2.csv')


# df['ls_old'] = ls_f2
def define_3ph_pvsystem(dss, bus, kv, kva, pmpp):

    dss.text("New XYCurve.MyPvsT npts=4  xarray=[0  25  75  100]  yarray=[1 1 1 1]")
    dss.text("New XYCurve.MyEff npts=4  xarray=[.1  .2  .4  1.0]  yarray=[1 1 1 1]")

    dss.text("New PVSystem.PV_{} phases=3 conn=wye  bus1={} kV={} kVA={} Pmpp={} pf=1"
             " effcurve=Myeff  P-TCurve=MyPvsT vmaxpu=2 vminpu=0.5".format(bus, bus, kv * 1.73, kva, pmpp))

def add_bus_marker(dss, bus, color, size_marker=8, code=15):
    dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus, color, size_marker, code))

def volt_var(dss):
    x_vv_curve = "[0.5 0.92 0.98 1.0 1.02 1.08 1.5]"
    y_vv_curve = "[1 1 0 0 0 -1 -1]"
    dss.text(f"new XYcurve.volt-var_catb_curve npts=7 yarray={y_vv_curve} xarray={x_vv_curve}")
    dss.text("new invcontrol.inv mode=voltvar voltage_curvex_ref=rated vvc_curve1=volt-var_catb_curve RefReactivePower=VARMAX")

def define_opendss_object(dss, opendss_class, name, **kwargs):

    command = "New {}.{}".format(opendss_class, name)

    for property, value in kwargs.items():
        command = command + " {}={}".format(property, value)

    dss.text(command)


def get_powerflow_results(dss):
    total_p_feederhead = -1 * dss.circuit_total_power()[0]
    total_q_feederhead = -1 * dss.circuit_total_power()[1]
    voltages = dss.circuit_all_bus_vmag_pu()
    voltage_min = min(voltages)
    voltage_max = max(voltages)

    return total_p_feederhead, total_q_feederhead, voltage_min, voltage_max

def increment_pv_size(dss, p_step, kva_to_kw, pf, i):
    dss.pvsystems_first()
    for _ in range(dss.pvsystems_count()):
        dss.text(f"edit pvsystem.{dss.pvsystems_read_name()} pmpp={p_step * i} kva={kva_to_kw * p_step * i} pf={pf} pfpriority=yes")
        dss.pvsystems_next()
    dss.solution_solve()


def get_total_pv_powers(dss):
    total_pv_p_list = list()
    total_pv_q_list = list()
    dss.pvsystems_first()
    for _ in range(dss.pvsystems_count()):
        dss.circuit_set_active_element(f"PVsystem.{dss.pvsystems_read_name()}")
        total_pv_p_list.append(-1 * sum(dss.cktelement_powers()[0:6:2]))
        total_pv_q_list.append(-1 * sum(dss.cktelement_powers()[1:6:2]))
        dss.pvsystems_next()
    total_pv_p = sum(total_pv_p_list)
    total_pv_q = sum(total_pv_q_list)

    return total_pv_p, total_pv_q