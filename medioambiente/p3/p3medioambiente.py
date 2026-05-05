import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, ScalarFormatter
from uncertainties import unumpy

db_Raw = np.array([
    58.6, 56.4, 55.4, 56.4, 57.3, 58.0, 57.9, 55.7, 58.4, 56.3, 60.1, 63.1, 55.6, 59.7, 56.4, 55.2, 58.2, 59.2, 57.6, 58.5,
    60.4, 59.3, 58.6, 54.5, 56.6, 57.8, 59.5, 57.7, 57.2, 54.1, 55.6, 65.8, 54.4, 56.3, 55.9, 55.5, 56.1, 55.8, 57.5, 55.5,
    58.3, 58.3, 58.0, 55.4, 59.0, 60.2, 54.6, 57.0, 55.7, 57.3, 60.0, 57.6, 58.4, 63.8, 58.4, 60.9, 62.1, 56.1, 57.2, 58.1,
    59.6, 63.6, 63.9, 59.0, 59.4, 59.2, 60.4, 57.6, 57.2, 60.2, 59.7, 56.7, 60.3, 62.8, 59.5, 59.7, 59.7, 62.0, 60.5, 60.2,
    54.8, 63.9, 65.5, 61.3, 54.0, 58.2, 56.6, 57.9, 58.5, 56.2, 61.0, 58.1, 56.8, 55.0, 55.2, 57.5, 55.3, 56.1, 54.7, 56.8,
    54.8, 55.2, 55.4, 55.1, 54.1, 58.9, 57.8, 56.6, 56.8, 58.9, 53.5, 55.5, 56.3, 56.6, 56.4, 54.9, 54.3, 55.6, 57.8, 53.2,
    55.1, 56.6, 57.0, 55.3, 55.1, 57.4, 54.8, 56.8, 56.0, 57.8, 59.7, 59.6, 59.1, 57.1, 57.8, 57.7, 57.8, 56.9, 56.7, 58.2,
    55.7, 57.1, 57.1, 58.6, 56.5, 55.3, 55.9, 63.7, 56.4, 54.7, 58.7, 57.7, 59.0, 55.8, 58.3, 61.4, 55.6, 61.1, 58.9, 56.5,
    55.9, 56.8, 55.9, 57.8, 58.4, 58.4, 58.3, 59.9, 58.0, 56.8, 57.7, 58.0, 63.0, 60.9, 59.9, 60.6, 61.8, 59.1, 60.5, 59.8,
])

ld_gobierno = 60
tiempo = np.arange(1, db_Raw.size + 1)
tiempo_unc = unumpy.uarray(tiempo*10, 0.001)
db_Raw_unc = unumpy.uarray(db_Raw, 1.5)
medida_app = 59.4
l = unumpy.pow(10, db_Raw_unc / 10)
Laeq = 10 * unumpy.log10((1 / 180) * np.sum(l))

# Cálculo de percentiles en magnitud lineal y conversión a dB
percentiles_linear = np.percentile(unumpy.nominal_values(l), [10, 50, 90])
percentiles_db = 10 * np.log10(percentiles_linear)
print("Percentiles (10th, 50th, 90th) [dB]:", percentiles_db)

# MEDIA LAEQ PARA COMPARAR
print(f"Laeq = {unumpy.nominal_values(Laeq):.6f} +/- {unumpy.std_devs(Laeq):.6f} dB")
diferencia_gobierno = Laeq - ld_gobierno
print(
    f"diferencia con el límite de gobierno: "
    f"{unumpy.nominal_values(diferencia_gobierno):.6f} +/- {unumpy.std_devs(diferencia_gobierno):.6f} dB"
)
diferencia_app = Laeq - medida_app
print(
    f"diferencia con la medida de aplicación: "
    f"{unumpy.nominal_values(diferencia_app):.6f} +/- {unumpy.std_devs(diferencia_app):.6f} dB"
)

# Plotting configuration
mpl.rcParams.update({
    "figure.figsize": (11, 5),
    "figure.dpi": 120,
    "axes.facecolor": "#F7F8FA",
    "axes.edgecolor": "#3A3A3A",
    "axes.labelcolor": "#1F1F1F",
    "axes.grid": True,
    "grid.color": "#D5D9E0",
    "grid.alpha": 0.8,
    "grid.linewidth": 0.8,
    "grid.linestyle": "--",
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
    "xtick.color": "#222222",
    "ytick.color": "#222222",
    "legend.frameon": True,
    "legend.edgecolor": "#A7A7A7",
    "legend.facecolor": "#FFFFFF",
})

tiempo_nom = unumpy.nominal_values(tiempo_unc)

lin_unc = unumpy.pow(10, db_Raw_unc / 10)
lin_nom = unumpy.nominal_values(lin_unc)
lin_std = unumpy.std_devs(lin_unc)

db_nom = unumpy.nominal_values(db_Raw_unc)
db_std = unumpy.std_devs(db_Raw_unc)

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, ScalarFormatter

# ... (Todo tu código previo de arrays y cálculos) ...

# ----------------- GRÁFICA 1: Magnitud lineal (10^(L/10)) -----------------
fig1, ax1 = plt.subplots()
ax1.plot(tiempo_nom, lin_nom, color="#12355B", linewidth=1.8, label="$10^{L/10}$")
ax1.fill_between(
    tiempo_nom,
    lin_nom - lin_std,
    lin_nom + lin_std,
    color="#2A6F97",
    alpha=0.25,
    label="Incertidumbre",
)

# Nombres correctos: Relación de presión cuadrática
ax1.set_title("Evolución Temporal de la Relación de Presión Cuadrática", fontsize=13, fontweight="bold")
ax1.set_xlabel("Tiempo $t$ (s)")
ax1.set_ylabel("Relación $P^2/P_0^2$")
ax1.legend(loc="upper left")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Notación científica
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0, 0))
ax1.yaxis.set_major_formatter(formatter)

# ----------------- GRÁFICA 2: Decibelios en bruto -----------------
fig2, ax2 = plt.subplots()
ax2.errorbar(
    tiempo_nom,
    db_nom,
    yerr=db_std,
    fmt="o",
    markersize=4,
    color="#6B2D5C",
    ecolor="#A64D79",
    elinewidth=1,
    capsize=3,
    alpha=0.9,
    label="Valores Medidos",
)
ax2.plot(tiempo_nom, db_nom, color="#2F4858", linewidth=1.2, alpha=0.7)
ax2.axhline(ld_gobierno, color="#D72631", linestyle="--", linewidth=1.5, label="Límite de Gobierno (60 dB)")
ax2.axhline(percentiles_db[0], color="green", linestyle=":", linewidth=1.5, label="$L_{90}$ ")
ax2.axhline(percentiles_db[1], color="blue", linestyle=":", linewidth=1.5, label="$L_{50}$ ")
ax2.axhline(percentiles_db[2], color="red", linestyle=":", linewidth=1.5, label="$L_{10}$ ")   

# Nombres correctos: Nivel de Presión Sonora
ax2.set_title("Evolución Temporal del Nivel de Presión Sonora", fontsize=13, fontweight="bold")
ax2.set_xlabel("Tiempo $t$ (s)")
ax2.set_ylabel("Nivel de Presión Sonora $L_A$ (dBA)") 
ax2.legend(loc="upper left")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

plt.show()