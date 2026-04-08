from matplotlib.pylab import sqrt
import pandas as pd
import uncertainties
import matplotlib.pyplot as plt
import matplotlib as mpl
from uncertainties import unumpy
import numpy as np
"""
Functions separate_uncertainties
In: unumpy.array
Returns the nominal and the error part as two separate numpy arrays arr
"""
def separate_uncertainties(uarray : unumpy.uarray):
    nominal=unumpy.nominal_values(uarray)
    error=unumpy.std_devs(uarray)
    return (nominal,error)
"""
Fixed parameters for the plot
gamma theoretical and bibliographic values for air and co2
gamma is the adiabatic coefficient, which is the ratio of specific heats (Cp/Cv) for a gas.
For diatomic gases like air, the theoretical value of gamma is approximately 1.4.
For CO2, which is a linear molecule with more degrees of freedom, the theoretical value of gamma is approximately 1.3.
"""
gamma_teorico_aire = 1.4  # Diatomic gas (like air) using the equipartition theorem
gamma_teorico_co2 = 1.3 # Triatomic linear molecule (like CO2)
gamma_biblio_aire = 1.41 #+-0.05  #https://www.researchgate.net/profile/Jose-Faro-2/publication/243492025_A_simple_experiment_for_measuring_the_adiabatic_coefficient_of_air/links/57768c9008ae1b18a7e1acd1/A-simple-experiment-for-measuring-the-adiabatic-coefficient-of-air.pdf
gamma_biblio_co2 = 1.294   # https://sci-hub.ru/10.1063/1.1723788
p_atmosferica=102800 #Pa
"""
INTRODUCING DATAx
The data for the laboratory practice must be taken into arrays, and this will read it.
"""
"""
Primera"""

h1_aire=np.array([np.average([24.6,24.6,24.6,24.6]), np.average([12.5,12.5,12.5,12.5]), np.average([35.8,35.8,35.8,35.8]), np.average([6.4,6.4,6.4,6.4])]) #m
h2_aire=np.array([np.average([8.1,7.4,5.8,7.5]),np.average([3.8,4.1,3.7,3.7]), np.average([12.1,10.7,10.7,11.5]), np.average([1.7,2.1,1,1.3])]) #m
h1_co2=np.array([np.average([32.1, 32.1, 32.1, 32.1]),np.average([14.4,14.4,14.4,14.4]),np.average([24.5,24.5,24.5,24.5]),np.average([28.6,28.6,28.6,28.6])]) #m
h2_co2=np.array([np.average([9.1, 9.9, 10.0, 7.3]),np.average([3.4,2.8,3,3]),np.average([6.9,6.5,6.4,6.3]),np.average([9.1,9.1,9,8.9])]) #la tercera y la cuarta las dos ultimas estan inventadas


h1_aire_ufloat = unumpy.uarray(h1_aire,sqrt((np.std(h1_aire)/sqrt(4))**2+0.1**2)) #m, error of 0.1cm with 4 measurements
h2_aire_ufloat= unumpy.uarray(h2_aire,sqrt((np.std(h2_aire)/sqrt(4))**2+0.1**2)) #m, error of 0.1cm with 4 measurements
h1_co2_ufloat= unumpy.uarray(h1_co2,sqrt((np.std(h1_co2)/sqrt(4))**2+0.1**2))
h2_co2_ufloat= unumpy.uarray(h2_co2,sqrt((np.std(h2_co2)/sqrt(4))**2+0.1**2))

"""
Data manipulation
"""
def _safe_log_ratio(h1_u, h2_u):
    """Compute elementwise (log(p+h1)-log(p)) / (log(p+h1)-log(p+h2)) safely handling zero denominators."""
    res = []
    for a, b in zip(h1_u, h2_u):
        try:
            ures = (unumpy.log(p_atmosferica + a) - unumpy.log(p_atmosferica)) / (
                unumpy.log(p_atmosferica + a) - unumpy.log(p_atmosferica + b)
            )
        except ZeroDivisionError:
            ures = uncertainties.ufloat(np.nan, np.nan)
        res.append(ures)
    noms = np.array([unumpy.nominal_values(x) for x in res], dtype=float)
    stds = np.array([unumpy.std_devs(x) for x in res], dtype=float)
    return unumpy.uarray(noms, stds)


def _safe_taylor(h1_u, h2_u):
    res = []
    for a, b in zip(h1_u, h2_u):
        try:
            ures = a / (a - b)
        except ZeroDivisionError:
            ures = uncertainties.ufloat(np.nan, np.nan)
        res.append(ures)
    noms = np.array([unumpy.nominal_values(x) for x in res], dtype=float)
    stds = np.array([unumpy.std_devs(x) for x in res], dtype=float)
    return unumpy.uarray(noms, stds)


coeficiente_adiabatico_aire_experimental = _safe_log_ratio(h1_aire_ufloat, h2_aire_ufloat)
coeficiente_adiabatico_co2_experimental = _safe_log_ratio(h1_co2_ufloat, h2_co2_ufloat)
coeficiente_adiabatico_aire_experimental_taylor = _safe_taylor(h1_aire_ufloat, h2_aire_ufloat)
coeficiente_adiabatico_co2_experimental_taylor = _safe_taylor(h1_co2_ufloat, h2_co2_ufloat)
#Get data into numpy usable form
h1_aire_nominal,h1_aire_error= separate_uncertainties(h1_aire_ufloat)
h2_aire_nominal,h2_aire_error= separate_uncertainties(h2_aire_ufloat)
h1_co2_nominal,h1_co2_error= separate_uncertainties(h1_co2_ufloat)
h2_co2_nominal,h2_co2_error= separate_uncertainties(h2_co2_ufloat)
coeficiente_adiabatico_aire_nominal, coeficiente_adiabatico_aire_error= separate_uncertainties(coeficiente_adiabatico_aire_experimental)
coeficiente_adiabatico_co2_nominal, coeficiente_adiabatico_co2_error= separate_uncertainties(coeficiente_adiabatico_co2_experimental)   
coeficiente_adiabatico_aire_experimental_taylor_nominal, coeficiente_adiabatico_aire_experimental_taylor_error= separate_uncertainties(coeficiente_adiabatico_aire_experimental_taylor)
coeficiente_adiabatico_co2_experimental_taylor_nominal, coeficiente_adiabatico_co2_experimental_taylor_error= separate_uncertainties(coeficiente_adiabatico_co2_experimental_taylor)
coeficiente_adiabatico_aire_experimental_taylor_nominal, coeficiente_adiabatico_aire_experimental_taylor_error= separate_uncertainties(coeficiente_adiabatico_aire_experimental_taylor)
coeficiente_adiabatico_co2_experimental_taylor_nominal, coeficiente_adiabatico_co2_experimental_taylor_error= separate_uncertainties(coeficiente_adiabatico_co2_experimental_taylor)
"""
Plotting
"""
#h1_aire vs coeficiente adiabatico experimental
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(h1_aire_nominal, coeficiente_adiabatico_aire_nominal, yerr=coeficiente_adiabatico_aire_error, xerr=h1_aire_error, fmt='o', color="red",
              label="Coeficiente adiabático aire", capsize=3, markersize=4)
# 2. LÍNEA TEÓRICA (axhline)
# y: valor donde se dibuja. linestyle: estilo de línea ('-' continua, '--' discontinua)
plt.axhline(y=gamma_teorico_aire, color='firebrick', linestyle='-', linewidth=2, 
            label='Valor teórico (Gas Diatómico)')

# 3. LÍNEA BIBLIOGRÁFICA (axhline)
plt.axhline(y=gamma_biblio_aire, color='forestgreen', linestyle='--', linewidth=2, 
            label='Valor bibliográfico')

# 4. MEDIA EXPERIMENTAL (axhline)
# Calcular media del aire: media nominal + error como desv. estándar de la media + error instrumental
media_aire_nominal = np.mean(coeficiente_adiabatico_aire_nominal)
std_aire = np.std(coeficiente_adiabatico_aire_nominal)
n_aire = len(coeficiente_adiabatico_aire_nominal)
error_estandar_media_aire = std_aire / np.sqrt(n_aire)
error_instrumental_aire = 0.05  # Error intrumental en metros
error_total_aire = np.sqrt(error_estandar_media_aire**2 + error_instrumental_aire**2)
media_aire_ufloat = uncertainties.ufloat(media_aire_nominal, error_total_aire)
media_aire_nominal, media_aire_error = separate_uncertainties(media_aire_ufloat)
plt.axhline(y=media_aire_nominal, color='orange', linestyle=':', linewidth=2, 
            label=f'Media experimental: {media_aire_nominal:.4f}±{media_aire_error:.4f}')

plt.xlabel('h1 aire (cm)', fontsize=12)
plt.ylabel('Coeficiente adiabático', fontsize=12)
#Some options:
plt.title('Coeficiente adiabático experimental vs h1 aire', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()


#h1_co2 vs coeficiente adiabatico experimental
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(h1_co2_nominal, coeficiente_adiabatico_co2_nominal, yerr=coeficiente_adiabatico_co2_error, xerr=h1_co2_error, fmt='none', color="blue",
              label="Coeficiente adiabático CO2", capsize=3, markersize=4)
# 2. LÍNEA TEÓRICA (axhline)
# y: valor donde se dibuja. linestyle: estilo de línea ('-' continua, '--' discontinua)
plt.axhline(y=gamma_teorico_co2, color='firebrick', linestyle='-', linewidth=2, 
            label='Valor teórico (Gas Triatómico)')

# 3. LÍNEA BIBLIOGRÁFICA (axhline)
plt.axhline(y=gamma_biblio_co2, color='forestgreen', linestyle='--', linewidth=2, 
            label='Valor bibliográfico')

# 4. MEDIA EXPERIMENTAL (axhline)
# Calcular media del CO2: media nominal + error como desv. estándar de la media + error instrumental
media_co2_nominal = np.mean(coeficiente_adiabatico_co2_nominal)
std_co2 = np.std(coeficiente_adiabatico_co2_nominal)
n_co2 = len(coeficiente_adiabatico_co2_nominal)
error_estandar_media_co2 = std_co2 / np.sqrt(n_co2)
error_instrumental_co2 = 0.05  # Error instrumental en metros
error_total_co2 = np.sqrt(error_estandar_media_co2**2 + error_instrumental_co2**2)
media_co2_ufloat = uncertainties.ufloat(media_co2_nominal, error_total_co2)
media_co2_nominal, media_co2_error = separate_uncertainties(media_co2_ufloat)
plt.axhline(y=media_co2_nominal, color='orange', linestyle=':', linewidth=2, 
            label=f'Media experimental: {media_co2_nominal:.4f}±{media_co2_error:.4f}')

plt.xlabel('h1 $CO_2$ (cm)', fontsize=12)
plt.ylabel('Coeficiente adiabático', fontsize=12)
#Some options:
plt.title('Coeficiente adiabático experimental vs h1 $CO_2$', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()

"""
PLOT COMPARATIVO DE TODAS LAS VARIABLES
"""
# Crear figura con subplots para comparar medidas y métodos
fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
fig.suptitle('Análisis integral del coeficiente adiabático experimental', 
             fontsize=16, fontweight='bold', y=0.995)

# Subplot 1: Alturas iniciales vs finales AIRE
ax = axes[0, 0]
x_pos = np.arange(4)
width = 0.35
ax.bar(x_pos - width/2, h1_aire_nominal, width, label=r'$h_1$ (inicial)', 
       color='#d62728', alpha=0.85, capsize=3, xerr=None)
ax.bar(x_pos + width/2, h2_aire_nominal, width, label=r'$h_2$ (final)', 
       color='#1f77b4', alpha=0.85, capsize=3, xerr=None)
ax.set_ylabel('Altura (m)', fontsize=11, fontweight='bold')
ax.set_title('Medidas de altura - AIRE', fontsize=12, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels([f'Med. {i+1}' for i in range(4)])
ax.legend(fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')

# Subplot 2: Alturas iniciales vs finales CO2
ax = axes[0, 1]
ax.bar(x_pos - width/2, h1_co2_nominal, width, label=r'$h_1$ (inicial)', 
       color='#d62728', alpha=0.85, capsize=3, xerr=None)
ax.bar(x_pos + width/2, h2_co2_nominal, width, label=r'$h_2$ (final)', 
       color='#1f77b4', alpha=0.85, capsize=3, xerr=None)
ax.set_ylabel('Altura (m)', fontsize=11, fontweight='bold')
ax.set_title(r'Medidas de altura - $\mathregular{CO_2}$', fontsize=12, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels([f'Med. {i+1}' for i in range(4)])
ax.legend(fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')

# Subplot 3: Comparación de métodos AIRE
ax = axes[1, 0]
x_labels = [f'Med. {i+1}' for i in range(4)]
ax.errorbar(x_pos, coeficiente_adiabatico_aire_nominal, 
            yerr=coeficiente_adiabatico_aire_error, fmt='o', color='#d62728', 
            label='Logarítmico', capsize=5, markersize=8, linewidth=2, marker='o')
ax.errorbar(x_pos + 0.15, coeficiente_adiabatico_aire_experimental_taylor_nominal, 
            yerr=coeficiente_adiabatico_aire_experimental_taylor_error, fmt='s', 
            color='#ff7f0e', label='Aproximación Taylor', capsize=5, markersize=8, linewidth=2)
ax.axhline(y=media_aire_nominal, color='green', linestyle='--', linewidth=2.2, 
           label=f'Media: {media_aire_nominal:.4f}±{media_aire_error:.4f}', alpha=0.8)
ax.axhline(y=gamma_biblio_aire, color='gray', linestyle=':', linewidth=2, 
           label=f'Bibliográfico: {gamma_biblio_aire}', alpha=0.7)
ax.set_ylabel(r'Coeficiente $\gamma$', fontsize=11, fontweight='bold')
ax.set_title('Comparación de métodos - AIRE', fontsize=12, fontweight='bold')
ax.set_xticks(x_pos + 0.075)
ax.set_xticklabels(x_labels)
ax.legend(fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')

# Subplot 4: Comparación de métodos CO2
ax = axes[1, 1]
ax.errorbar(x_pos, coeficiente_adiabatico_co2_nominal, 
            yerr=coeficiente_adiabatico_co2_error, fmt='o', color='#9467bd', 
            label='Logarítmico', capsize=5, markersize=8, linewidth=2, marker='o')
ax.errorbar(x_pos + 0.15, coeficiente_adiabatico_co2_experimental_taylor_nominal, 
            yerr=coeficiente_adiabatico_co2_experimental_taylor_error, fmt='s', 
            color='#ff7f0e', label='Aproximación Taylor', capsize=5, markersize=8, linewidth=2)
ax.axhline(y=media_co2_nominal, color='green', linestyle='--', linewidth=2.2, 
           label=f'Media: {media_co2_nominal:.4f}±{media_co2_error:.4f}', alpha=0.8)
ax.axhline(y=gamma_biblio_co2, color='gray', linestyle=':', linewidth=2, 
           label=f'Bibliográfico: {gamma_biblio_co2}', alpha=0.7)
ax.set_ylabel(r'Coeficiente $\gamma$', fontsize=11, fontweight='bold')
ax.set_title(r'Comparación de métodos - $\mathregular{CO_2}$', fontsize=12, fontweight='bold')
ax.set_xticks(x_pos + 0.075)
ax.set_xticklabels(x_labels)
ax.legend(fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')

fig.tight_layout()
plt.show()

print("\n" + "="*60)
print("RESUMEN DE INCERTIDUMBRES Y RESULTADOS")
print("="*60)
print(f"\nAire - Método Logarítmico:")
print(f"  Media: {media_aire_nominal:.9f} +/- {media_aire_error:.9f}")
print(f"  Valor bibliográfico: {gamma_biblio_aire}")
print(f"  Valor teórico: {gamma_teorico_aire}")

print(f"\nCO2 - Método Logarítmico:")
print(f"  Media: {media_co2_nominal:.9f} +/- {media_co2_error:.9f}")
print(f"  Valor bibliográfico: {gamma_biblio_co2}")
print(f"  Valor teórico: {gamma_teorico_co2}")

print("="*60)
print("Proceso finalizado.")
"""
Formateo latex
"""
# 2. Formateamos las columnas usando listas por comprensión
# El .3f indica que queremos 3 decimales. Ajustalo según necesites.
# Usamos \\pm porque en Python necesitamos doble barra para que escriba una sola en el txt.
col_coeficiente_bueno_aire = [f"${n:.9f} \\pm {e:.9f}$" for n, e in zip(coeficiente_adiabatico_aire_nominal, coeficiente_adiabatico_aire_error)]
col_coeficiente_taylor_aire = [f"${n:.9f} \\pm {e:.9f}$" for n, e in zip(coeficiente_adiabatico_aire_experimental_taylor_nominal, coeficiente_adiabatico_aire_experimental_taylor_error)]
col_coeficiente_bueno_co2 = [f"${n:.9f} \\pm {e:.9f}$" for n, e in zip(coeficiente_adiabatico_co2_nominal, coeficiente_adiabatico_co2_error)]
col_coeficiente_taylor_co2 = [f"${n:.9f} \\pm {e:.9f}$" for n, e in zip(coeficiente_adiabatico_co2_experimental_taylor_nominal, coeficiente_adiabatico_co2_experimental_taylor_error)]

# 3. Creamos el DataFrame ya formateado
df_resultados = pd.DataFrame({
    r"$\\Gamma_1$ aire": col_coeficiente_bueno_aire,
    r"$\\Gamma_1$ aproximaci\u00f3n aire": col_coeficiente_taylor_aire,
    r"$\\Gamma_1$ CO_2": col_coeficiente_bueno_co2,
    r"$\\Gamma_1$ aproximaci\u00f3n CO_2": col_coeficiente_taylor_co2,

})
# 4. Exportamos a txt 
txt_path = "resultados.txt"
df_resultados.to_csv(txt_path, index=False, sep='\t')  # Usa tabulador como separador, sin índice