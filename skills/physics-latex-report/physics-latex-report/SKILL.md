---
name: physics-latex-report
description: Specialized workflow for populating physics laboratory reports in LaTeX. Use when modifying or structuring reports in Mecanica/ folders. Handles data extraction from Excel or Python, adhering to strict scientific reporting standards (2 sig figs, chi-squared metrics, uncertainty explanations) and following reference structures.
---

# Physics LaTeX Report Builder

## Overview
This skill automates the population of standardized physics laboratory reports. It enforces a deterministic workflow: structural analysis of reference documents (PDF/Markdown) followed by precise data mapping from human-provided Python scripts or Excel workbooks.

## Workflow

### 1. Initial Assessment
- **Identify Experiment**: Determine the base name (e.g., `m12bis`).
- **Ask Script First (Mandatory)**: Ask the user: "Do you already have a Python analysis script for this experiment? (Yes/No)"
  - **If Yes**: Locate script and search for `""" LATEX GENERATION """` block. Use these arrays.
  - **If No**: Locate Excel file `m[XX]bis.xlsx` and use it as the data source.

### 2. Structural Analysis
- **Reference PDF**: Search for a reference PDF or Markdown fallback (e.g., in `agent_reports/informes_markdown`).
- **Map Structure**: Identify sections, tables, and figures required by the reference.

### 3. Data Processing & Mapping
- **Significant Figures**: Round all numerical results to **2 significant figures**.
- **Uncertainty Handling**: 
  - Never invent uncertainties. Use `TODO_UNCERTAINTY` if missing.
  - Every uncertainty must have a 1-2 sentence explanation of its source/method.
- **Goodness of Fit**: Use **reduced chi-squared (χ²_red)** instead of R².
- **Provenance**: Maintain a mapping of `report_quantity -> source_field`.

### 4. Report Population
- **Template Only**: Populate Abstract, Intro, Data, and Results.
- **Human Only**: Leave **Discussion** and **Conclusions** empty for the user.
- **LaTeX Standards**: Use `siunitx` (`\unit`, `\SI`), `booktabs` (`\toprule`, etc.), and proper cross-references (`\label`, `\ref`).

### 5. Validation & Delivery
- **Debug Log**: Write `debug_data_provenance.txt` in the experiment folder.
- **Compilation**: Run `latexmk -pdf <file>.tex` and verify success.

## Quality Requirements
- **Abstract**: No numerical data. 4-6 sentences on objective, method, and significance.
- **Figures**: Include descriptive captions explaining axes and physical meaning.
- **Language**: English only, concise and technical.

## Resources

### scripts/
- `read_excel.py`: Utility to inspect Excel workbooks for data extraction.

### references/
- `m3bis2_example.tex`: Reference LaTeX structure from the M3bis2 experiment.
