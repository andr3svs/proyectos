import pandas as pd
xls = pd.ExcelFile('C:/Users/Andres/Practicas-Fisica/Mecanica/m3bis/m3bis2.xlsx')
for s in ['w0','wsderecha','wsizquierda','waderecha','waizquierda','minderecho','minizquierdo']:
    df=pd.read_excel(xls,s)
    print('\n===',s,'===')
    print(df.columns.tolist())
    print(df.head(1).to_string(index=False))
