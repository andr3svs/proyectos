#First ask the user for the path to the Excel file, then read it and print the first 99 rows of each sheet.
ruta=input("Please enter the path to the Excel file: ")
import pandas as pd
xls = pd.ExcelFile(ruta)
for sheet in xls.sheet_names:
    print(f'Sheet: {sheet}')
    df = pd.read_excel(xls, sheet_name=sheet, nrows=99)
    print(df)
# When the agent runs this then it wants to analyze each column and calculate the uncertainties.
