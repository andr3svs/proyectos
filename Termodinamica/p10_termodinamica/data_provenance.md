# Data Provenance - P10 Thermistor

## Metadata
- **Experiment**: P10 - Resistance-Temperature Relation of a Thermistor
- **Source**: `Termodinamica\p10_termodinamica\p10.py`, `p10.xlsx`
- **Timestamp**: 2026-05-10

## Parameters & Constants
| Quantity | Symbol | Value | Uncertainty | Unit | Source |
|----------|--------|-------|-------------|------|--------|
| High Temp Reference | $T_1$ | 353.15 | 0.10 | K | p10.py line 53 |
| Low Temp Reference | $T_2$ | 273.25 | 0.10 | K | p10.py line 52 |
| Resistance at $T_1$ | $R_1$ | 1.25 | 0.22 | k$\Omega$ | p10.py line 55 |
| Resistance at $T_2$ | $R_2$ | 31.5 | 0.58 | k$\Omega$ | p10.py line 54 |

## Experimental Data
| Celsius | Temperature (T) | $u_T$ | Resistance (R) | $u_R$ | Unit (T/R) |
|---------|-----------------|-------|----------------|-------|------------|
| 5.0 | 278.15 | 0.10 | 25.25 | 0.50 | K / k$\Omega$ |
| 20.0 | 293.15 | 0.10 | 12.26 | 0.35 | K / k$\Omega$ |
| 25.0 | 298.15 | 0.10 | 9.81 | 0.32 | K / k$\Omega$ |
| 30.0 | 303.15 | 0.10 | 7.80 | 0.29 | K / k$\Omega$ |
| 35.0 | 308.15 | 0.10 | 6.32 | 0.28 | K / k$\Omega$ |
| 40.0 | 313.15 | 0.10 | 5.13 | 0.26 | K / k$\Omega$ |
| 45.0 | 318.15 | 0.10 | 4.20 | 0.25 | K / k$\Omega$ |
| 50.0 | 323.15 | 0.10 | 3.46 | 0.24 | K / k$\Omega$ |

## Fit Results
### Two-Point Analytical Solution
- **A**: $2.0 \times 10^{-5} \pm 1.6 \times 10^{-5}$
- **B**: $3890 \pm 210$ K
- **Provenance**: `resultados.txt` lines 2-3

### ODR Nonlinear Fit ($R = A e^{B/T}$)
- **A**: $1.59 \times 10^{-5} \pm 7.6 \times 10^{-7}$
- **B**: $3973 \pm 14$ K
- **$R^2$**: 0.999876
- **Provenance**: `resultados.txt` lines 6-8

## Figures
- **File**: `logvst.png`
- **Description**: Plot of $\ln(R)$ vs $1/T$.
