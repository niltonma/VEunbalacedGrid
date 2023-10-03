Este repositorio será utilizado para replicar o artigo:

P. Kaur and S. Kaur, "**Study of Impact of Electric Vehicle Integration in Unbalanced Distribution System**," *2022 IEEE International Power and Renewable Energy Conference (IPRECON)*, Kollam, India, 2022, pp. 1-6, doi: 10.1109/IPRECON55716.2022.10059564.



Será utilizado o OpenDSS com a biblioteca [py_dss_interface](https://pypi.org/project/py-dss-interface/)



```python
import py_dss_interface
import random
import matplotlib.pyplot as plt
import pandas as pd
import os, functions, funcoes

circuit_pu = 1.045
```



```python
random.seed(114) # mantém os valores "aleatorios" iguais.
dss = py_dss_interface.DSSDLL() # usa versao fornecida por py_dss_interface 
```

Direcionar o arquivo que será utilizado para fazer as simulações.

```python
dss_file = r"C:\Program Files\OpenDSS\IEEETestCases\13Bus\IEEE13Nodeckt.dss"
```

Compilar 

```python
dss.text(f"Compile [{dss_file}]")
```

Insere medidor e monitor nas 3 fases, nas linhas que ligam as barras 632 e 633.  Além de "setar" medição para modo diário com intervalo de 15 minutos.

```python
dss.text("New EnergyMeter.medidor1 element=Line.632633  terminal=1")
dss.text("New EnergyMeter.medidor2 element=Line.632633  terminal=2")
dss.text("New EnergyMeter.medidor3 element=Line.632633  terminal=3")
dss.text("New monitor.powers1 action=Save element=Line.632633  terminal=1 ppolar=no mode=0")
dss.text("New monitor.powers2 action=Save element=Line.632633  terminal=2 ppolar=no mode=0")
dss.text("New monitor.powers3 action=Save element=Line.632633  terminal=3 ppolar=no mode=0")
dss.text("set mode=daily")
dss.text("set number=96")
dss.text("set stepsize=0.25h")
```



Adiciona carga, para simular o ponto de carregamento do carro elétrico, conforme encontrado no artigo.

![image-20231002132239715](./img/image-20231002132239715.png?raw=true)

```python
dss.text("New Load.634a1 Bus1=634.1     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=252   kvar=0")
dss.text("New Load.634b1 Bus1=634.2     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0")
dss.text("New Load.634c1 Bus1=634.3     Phases=1 Conn=Wye  Model=1 kV=0.277  kW=168   kvar=0") 
```

Calcula o Fluxo de Potência:

```python
dss.solution_solve()
```





