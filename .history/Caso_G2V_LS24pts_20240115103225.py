import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes
import numpy as np


circuit_pu = 1.045

random.seed(114) # mantém os valores "aleatorios" iguais.
#dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface
dss = py_dss_interface.DSS(r"C:\Program Files\OpenDSS")


dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"

dss.text(f"Compile [{dss_file}]")
