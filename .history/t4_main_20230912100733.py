import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os

random.seed(114)

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 

circuit_pu = 1.045
load_variation1 = 0.8
percent = 0.2
p_step = 1
kva_to_kw = 1
location = 114
pf =1


dss.text(f"Compile [{dss_file}]")
dss.text(f"edit Vsource.Source pu ={circuit_pu}")
dss.solution_solve()
dss.text("plot profile")

dss.text("edit TRANSFORMER.REG1A XHL=0.0000000001")
dss.text(f"edit Vsource.Source pu ={circuit_pu}")

dss.solution_solve()
dss.text("plot profile")