import sidrapy
import pandas as pd
import time
from threading import Thread, active_count
from datetime import datetime

MUN_FRAME = pd.read_excel("assets/municipios.xls")[["codmunisu", "nome_municipio"]]

def get_sidra(segment : str = "territorial", frames : list = [], iWasTheFirst : bool = True, **kwargs) -> pd.DataFrame:
    try:
        sidraFrame = sidrapy.get_table(**kwargs)
        for col in sidraFrame.columns:
            sidraFrame.rename(columns={col:sidraFrame.at[0, col]}, inplace=True)
        sidraFrame.drop(0, inplace=True)
    except ValueError as vError:
        print(vError)
        if "excedeu o limite" in str(vError):
            requestedVal = str(vError).split(": ")[1].split(' ')[0]
            print("--Requisição execedeu o limite. (Requisitado: "+requestedVal+", limite: 100000)")
        if "all" in kwargs["ibge_territorial_code"]:
            total = 5570
            halfA = total//2
            halfB = total-halfA
            if halfA*2 != total:
                halfA += 1
            argsA, argsB = kwargs.copy(), kwargs.copy()
            argsA["ibge_territorial_code"], argsB["ibge_territorial_code"] = '', ''
            print(halfA, halfB)
            for i in range(halfA):
                argsA["ibge_territorial_code"] += str(MUN_FRAME.at[i, "codmunisu"])+','
            for i in range(halfB, total):
                argsB["ibge_territorial_code"] += str(MUN_FRAME.at[i, "codmunisu"])+','
            argsA["ibge_territorial_code"] = argsA["ibge_territorial_code"][:len(argsA["ibge_territorial_code"])-1]
            argsB["ibge_territorial_code"] = argsB["ibge_territorial_code"][:len(argsB["ibge_territorial_code"])-1]
            threadA = Thread(target=get_sidra, args=(segment, frames, False), kwargs=argsA)
            threadB = Thread(target=get_sidra, args=(segment, frames, False), kwargs=argsB)
            threadA.run()
            threadB.run()
            print("--splitting request...")
        else:
            codes = kwargs["ibge_territorial_code"]
            total = len(codes.split(','))
            halfA = total//2
            halfB = total-halfA
            if halfA*2 != total:
                halfA += 1
            argsA, argsB = kwargs.copy(), kwargs.copy()
            argsA["ibge_territorial_code"], argsB["ibge_territorial_code"] = '', ''
            print(halfA, halfB)
            for i in range(halfA):
                argsA["ibge_territorial_code"] += str(MUN_FRAME.at[i, "codmunisu"])+','
            for i in range(halfB, total):
                argsB["ibge_territorial_code"] += str(MUN_FRAME.at[i, "codmunisu"])+','
            argsA["ibge_territorial_code"] = argsA["ibge_territorial_code"][:len(argsA["ibge_territorial_code"])-1]
            argsB["ibge_territorial_code"] = argsB["ibge_territorial_code"][:len(argsB["ibge_territorial_code"])-1]
            threadA = Thread(target=get_sidra, args=(segment, frames, False), kwargs=argsA)
            threadB = Thread(target=get_sidra, args=(segment, frames, False), kwargs=argsB)
            threadA.run()
            threadB.run()
            print("--splitting request...")
    else:
        frames.append(sidraFrame)
        print(sidraFrame)
    print("Hello")
    if iWasTheFirst:
        while active_count() > 1:
            time.sleep(1)
            print("Number of threads:", active_count())
            pass
        theTrueFrame = frames[0]
        if len(frames) > 1:
            for i, frame in enumerate(frames):
                if i > 0:
                    theTrueFrame = pd.concat([theTrueFrame, frame])
            return theTrueFrame
        else:
            return theTrueFrame

beginLap = datetime.now()
sidraFrame = get_sidra(table_code="5457", territorial_level='6', ibge_territorial_code="all", variable="8331", classifications={"782":"all"}, period="all", header='y')
endLap = datetime.now()

print("Started at:",beginLap)
print("Finished at:", endLap)

#print(MUN_FRAME)
print(sidraFrame)
sidraFrame.to_csv("tester.csv", sep=';')