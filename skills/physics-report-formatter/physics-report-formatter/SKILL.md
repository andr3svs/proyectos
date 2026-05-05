---
name: physics-report-formatter
description: Specialized skill for generating standardized LaTeX laboratory reports for physics experiments. Use when a data_provenance.md file exists and needs to be formatted into a full report following university guidelines and reference structures.
---

# Physics Report Formatter

## Overview
This skill transforms structured measurement data (from `data_provenance.md`) and university guidelines (Guiones) into a professionally formatted LaTeX report. It strictly follows the reference structures seen in experiments like M3bis2.

## Workflow

### 1. Structural Analysis
- **Identify Experiment**: Determine the base name (e.g., `m3bis`).
- **Load Guidelines**: Read the university "Guion" (found in PDF or Markdown fallback like `m3bis2pdf.md`) to identify required sections and physical objectives.
- **Reference Template**: Use `m3bis2_example.tex` as the authoritative structure for preamble, abstract, and sections.

### 2. Document Construction
- **Preamble**: Set up `siunitx`, `booktabs`, and metadata macros (`\experimentTitle`, `\authorName`).
- **Abstract**: Generate a qualitative 4-6 sentence summary. **No numerical data**. Focus on objective, method, and significance.
- **Data & Results**: 
  - Convert Markdown tables from `data_provenance.md` into LaTeX `tabular` environments.
  - Use `siunitx` for all numbers (e.g., `$3.2 \pm 0.8$ \unit{m/s}`).
  - Insert figures found in the folder with descriptive captions.
- **Placeholders**: Leave **Discussion** and **Conclusions** empty for the human author. Use a clear marker like `% [HUMAN AUTHOR: WRITE DISCUSSION HERE]`.

### 3. Quality Control
- **Formatting**: Use `booktabs` for clean tables (`\toprule`, `\midrule`, `\bottomrule`).
- **Units**: Strictly use `\unit{}` and `\SI{}{}`.
- **Cross-References**: Ensure all figures and tables are labeled and referenced in text.

### 4. Compilation & Validation
- **Build**: Execute `latexmk -pdf [filename].tex`.
- **Verify**: Ensure the build completes without errors and includes all data from the provenance file.

## Quality Standards
- **English Only**: The entire report must be in English.
- **Template Maker Only**: The agent NEVER writes physical interpretations or conclusions.
- **Deterministic**: Every number in the report must match the `data_provenance.md` file exactly.

## Resources

### references/
- `m3bis2_example.tex`: Reference LaTeX structure from the M3bis2 experiment.
