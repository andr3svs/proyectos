---
name: physics-latex-audit
description: Revises LaTeX physics reports, ensures successful compilation, validates table data against Excel sources, and implements longtable for large datasets. Use this skill after generating or modifying a LaTeX report to ensure it meets academic standards and contains all experimental data.
---

# Physics LaTeX Audit

## Overview
This skill provides a rigorous validation workflow for physics laboratory reports. It ensures the document is technically sound (compiles), factually accurate (matches Excel source), and correctly formatted for large data series.

## Workflow

### 1. Compilation Verification
- **Build Command**: Always attempt to compile using `latexmk -pdf [filename].tex`.
- **Error Diagnosis**: If it fails, search for common LaTeX errors:
  - Missing packages (e.g., `siunitx`, `booktabs`, `longtable`).
  - Unescaped special characters (e.g., `_`, `%`, `&`).
  - Undefined control sequences.
- **Validation**: A successful build producing a PDF is mandatory.

### 2. Data Integrity Audit (Excel vs. LaTeX)
- **Identify Source**: Locate the `.xlsx` file used to populate the report.
- **Data Coverage**: Verify that tables in LaTeX contain 100% of the data points from the relevant Excel sheets. NO samples allowed.
- **GUM Significant Figures Check**: Ensure ALL numbers follow the GUM (Guide to the Expression of Uncertainty in Measurement) rules:
  1. **Uncertainty**: MUST be rounded to exactly **2 significant figures**. (e.g., $0.1 \rightarrow 0.10$, $0.00567 \rightarrow 0.0057$).
  2. **Nominal Value**: MUST be rounded to the same decimal place as the last significant figure of the uncertainty. (e.g., $12.345 \pm 0.1$ becomes $12.35 \pm 0.10$ if uncertainty sig figs dictate).
  3. **LaTeX Implementation**: Use `\qty[round-mode = uncertainty, round-precision = 2]{val \pm err}{unit}` in `siunitx` v3 for automatic compliance.
- **Spot Check**: Compare at least 10% of the data points directly between Excel and the PDF.

### 3. Structural & Formatting Audit
- **Table Length**: If a table contains more than 10 rows, it must use the `longtable` environment.
- **Units**: Verify all physical quantities use `\unit{}` or `\qty{}{}` from the `siunitx` v3 package.
- **Captions & Labels**: Every table and figure must have a descriptive caption and a unique label for cross-referencing.
- **Abstract Check**: Ensure the abstract contains NO numerical data and summarizes objective, method, and qualitative findings.

## Quality Standards
- **GUM Compliance**: Zero tolerance for incorrect significant figure rounding. Uncertainties MUST show exactly 2 sig figs.
- **Traceability**: If data is missing or doesn't match, explicitly list the discrepancies for correction.
