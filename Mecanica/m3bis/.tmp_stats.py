import pandas as pd, numpy as np
xls=pd.ExcelFile('C:/Users/Andres/Practicas-Fisica/Mecanica/m3bis/m3bis2.xlsx')

# helper

def trials_from_row(df, cols):
    vals=[]
    for c in cols:
        v=df.loc[0,c]
        if pd.notna(v): vals.append(float(v))
    return np.array(vals,float)

wsd=pd.read_excel(xls,'wsderecha')
wsi=pd.read_excel(xls,'wsizquierda')
wad=pd.read_excel(xls,'waderecha')
wai=pd.read_excel(xls,'waizquierda')
md=pd.read_excel(xls,'minderecho')

ws_trials=np.concatenate([
    trials_from_row(wsd,['Unnamed: 3','Unnamed: 7','Unnamed: 11']),
    trials_from_row(wsi,['Unnamed: 3','Unnamed: 7','Unnamed: 11'])
])
wa_trials=np.concatenate([
    trials_from_row(wad,['Unnamed: 3','Unnamed: 7','Unnamed: 11']),
    trials_from_row(wai,['Unnamed: 3','Unnamed: 7','Unnamed: 11'])
])

wmin_trials=trials_from_row(md,['f_max','Unnamed: 7','Unnamed: 11'])*2*np.pi
wmax_trials=trials_from_row(md,['f_max_small','Unnamed: 6','Unnamed: 10'])*2*np.pi

print('ws mean,std',ws_trials.mean(),ws_trials.std(ddof=1))
print('wa mean,std',wa_trials.mean(),wa_trials.std(ddof=1))
print('wmin mean,std',wmin_trials.mean(),wmin_trials.std(ddof=1))
print('wmax mean,std',wmax_trials.mean(),wmax_trials.std(ddof=1))
