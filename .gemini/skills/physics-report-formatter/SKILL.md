---
name: physics-report-formatter
description: Specialized skill for generating standardized LaTeX laboratory reports for physics experiments. Use when a data_provenance.md file exists and needs to be formatted into a full report following university guidelines and reference structures.
---

# Physics Report Formatter

## Overview
This skill transforms structured measurement data (from `data_provenance.md`) and university guidelines (Guiones) into a professionally formatted LaTeX report. It strictly follows the reference structures seen in experiments like M3bis2.
DO NOT ADD ANY REASONAMENT; CHECK TWICE TO NOT MESS UP THE NOMENCLATURE OF THE VARIABLES, TABLES, FIGURES, ETC. DO NOT INTERPRET THE DATA IN ANY WAY. DO NOT WRITE ANY DISCUSSION OR CONCLUSIONS. ONLY FOCUS ON FORMATTING THE DATA AND STRUCTURE.
## Workflow

### 1. Structural Analysis
- **Identify Experiment**: Determine the base name (e.g., `m3bis`).
- **Load Guidelines**: Read the university "Guion" (found in PDF or Markdown fallback like `m3bis2pdf.md`) to identify required sections and physical objectives.
- **Reference Template**: Use `m3bis2_example.tex` as the authoritative structure for preamble, abstract, and sections.

### 2. Document Construction
- **Preamble**: Set up `siunitx`, `booktabs`, `longtable` (if needed), and metadata macros (`\experimentTitle`, `\authorName`).
- **Abstract**: Generate a qualitative 4-6 sentence summary. **No numerical data**. Focus on objective, method, and significance.
- **Data & Results**: 
  - **Full Dataset**: Convert ALL Markdown tables from `data_provenance.md` into LaTeX. Do NOT use samples; include every single data point.
  - **Table Choice**: Use `tabular` for small datasets and `longtable` for any dataset exceeding 10 rows to ensure proper page breaks.
  - **Formatting**: Use `siunitx` for all numbers (e.g., `$3.2 \pm 0.8$ \unit{m/s}`).
  - **Figures**: Insert figures found in the folder with descriptive captions.
- **Strictly Data-Driven**: NEVER include "Discussion", "Conclusions", or "Questions/Cuestiones" content. Leave these sections entirely to the human author with clear comment markers like `% [HUMAN AUTHOR: WRITE DISCUSSION/CONCLUSIONS/QUESTIONS HERE]`.

### 3. Quality Control
- **Formatting**: Use `booktabs` for clean tables (`\toprule`, `\midrule`, `\bottomrule`).
- **Units**: Strictly use `\unit{}` and `\qty{}{}` (siunitx v3).
- **Cross-References**: Ensure all figures and tables are labeled and referenced in text.

### 4. Compilation & Validation
- **Build**: Execute `latexmk -pdf [filename].tex`.
- **Verify**: Ensure the build completes without errors and includes the COMPLETE dataset from the provenance file.

## Quality Standards
- **English Only**: The entire report must be in English.
- **No Interpretation**: The agent NEVER writes physical interpretations, reasoning, or answers to experimental questions.
- **Complete Tables**: Every row in the source data must be present in the LaTeX output.
- **Deterministic**: Every number in the report must match the `data_provenance.md` file exactly.

## Resources

### references/
#### LaTeX Templates & Examples (.tex)
- `m3bis2_example.tex`: Reference LaTeX structure from the M3bis2 experiment.
- `Mecanica_m12bis_mecanica_m12bis.tex`: Reference for Mechanics M12bis.
- `Mecanica_m3bis_article_4.tex`: Article template for Mechanics M3bis.
- `Mecanica_m3bis_m3bis2.tex`: Reference for Mechanics M3bis2.
- `Mecanica_m3bis_m3bis_style_template.tex`: Style template for Mechanics M3bis.
- `Mecanica_m3bis_structure.tex`: Structure definitions for Mechanics M3bis.
- `Termodinamica_p12_termodinamica_latex_p12.tex`: Reference for Thermodynamics P12.
- `Termodinamica_p12_termodinamica_termo_p12.tex`: Alternative reference for Thermodynamics P12.
- `Termodinamica_p5_termodinamica_latex_p5.tex`: Reference for Thermodynamics P5.
- `Termodinamica_p5_termodinamica_latex_tabla_con_errores.tex`: Table template with errors for Thermodynamics P5.
- `Termodinamica_p5_termodinamica_latex_termo_p05.tex`: Alternative reference for Thermodynamics P5.
- `Termodinamica_p5_termodinamica_tabla_resultados.tex`: Results table template for Thermodynamics P5.
- `Termodinamica_p7_termodinamica_p7.tex`: Reference for Thermodynamics P7.
- `medioambiente_analisis_incertidumbre_logaritmo.tex`: Uncertainty analysis reference for Environment reports.
- `medioambiente_tabla_flujos_kcal.tex`: Flow table template for Environment reports.
- `medioambiente_table_uncertainties.tex`: Uncertainty table template for Environment reports.

#### Markdown Guidelines & Fallbacks (.md)
- `Mecanica_m3bis_m3bis2pdf.md`: Markdown version of the M3bis2 guidelines.
