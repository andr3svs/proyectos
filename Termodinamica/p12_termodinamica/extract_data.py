import pandas as pd

df = pd.read_excel('p12.xlsx')
with open('data_table.md', 'w') as f:
    f.write('| tiempo (s) | u_tiempo (s) | theta1 (°C) | u_theta1 (°C) | theta2 (°C) | u_theta2 (°C) |\n')
    f.write('|---|---|---|---|---|---|\n')
    for index, row in df.iterrows():
        f.write(f"| {row['tiempo']:.2f} | 0.10 | {row['theta1']:.2f} | 0.10 | {row['theta2']:.2f} | 0.10 |\n")
