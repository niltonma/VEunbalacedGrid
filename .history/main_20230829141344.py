import py_dss_interface
import random

random.seed(114)
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Master.dss"

dss = py_dss_interface.DSSDLL()

dss.text(f"Compile [{dss_file}]")
dss.text("Set Maxiterations=100")
dss.text("set maxcontrolit=100")
dss.text("edit Reactor.MDV_SUB_1_HSB x=0.0000001")
dss.text("edit Transformer.MDV_SUB_1 %loadloss=0.0000001 xhl=0.00000001")
dss.text("edit vsource.source pu=1.045")

# Ex 1
# a) Voltage profile at peak load and at offpeak load

#! Define bus coordinates
dss.text("Buscoords  BusCoords.dat")
dss.text(f"batchedit load..* mode=1")
dss.text("set loadmult=0.2")
dss.solution_solve()
dss.text("plot profile phases=all")

dss.text("dump Line.L1 debug ")