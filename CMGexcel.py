# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 23:23:28 2022

@author: PZuloaga
"""

import pandas as pd
import os
# import datetime


def excel_to_prd(excel_input, txt_output):
    df = pd.read_excel(excel_input)
    os.remove(txt_output)
    # toma los encabezados de excel como nombres de columnas
    df.columns = df.iloc[3]
    # crea lista a partir de las celdas que tienen nombres de pozos
    # y borra columnas que no se usan
    well_list = df.iloc[3][2:]
    df = df.drop([0, 1, 2, 3])
    df = df.drop(columns=["Time (day)"])
    df = df.reset_index(drop=True)
    Date = df["Date"]
    prd = []
    for i in [j for j in range(0, len(well_list))]:
        Well_ID = pd.Series(well_list[(i)] for x in range(len(df.index)))
        Rate = df.iloc[:, (i+1)]
        prd = pd.DataFrame({"Well_ID": Well_ID,
                            "Date": Date,
                            "Gas_Rate": Rate})
        # se exporta todos los pz con encabezado
        prd.to_csv(txt_output, sep='\t', index=False, mode='a')
    editPRD = pd.read_csv(txt_output, sep='\t')
    # se vuelve a importar para sacar encbz
    editPRD = editPRD.drop(editPRD[editPRD.Well_ID == "Well_ID"].index)
    # agregar edit para que borre fechas mayores al pronostico
    # edit = edit.drop(edit[edit.Date > "Well_ID"].index)
    # edit para convertir caudales menores de 1 a 0
    editPRD.Gas_Rate[editPRD.Gas_Rate.astype(float) < 1] = 0
    os.remove(txt_output)
    editPRD.to_csv(txt_output, sep='\t', index=False, mode='a')


excel_to_prd('cmg_prd.xlsx', 'prd.txt')
excel_to_prd('cmg_iny.xlsx', 'iny.txt')
