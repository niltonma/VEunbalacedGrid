import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes


random.seed(114)

dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 
#dss = py_dss_interface.DSSDLL(r"C:\Program Files\OpenDSS")

dss.text(f"Compile [{dss_file}]")

dss.text("plot profile")

print('oi')