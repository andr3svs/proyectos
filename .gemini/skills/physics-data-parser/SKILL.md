---
name: physics-data-parser
description: Specialized skill for extracting and normalizing physics laboratory data from Python scripts or Excel workbooks. Use when data needs to be parsed into a structured Markdown format for reporting. Enforces strict uncertainty tracking and rounding to 2 significant figures.
---

# Physics Data Parser

## Overview
This skill extracts raw measurement data and analysis results from human-provided sources (Python scripts or Excel) and converts them into a structured "Data Provenance" Markdown file. This Markdown file serves as the single source of truth for downstream report generation.

## Workflow

### 1. Identify Data Source
- **Python-First**: Ask the user: "Do you have a Python analysis script? (Yes/No)". 
  - If yes, look for a `""" LATEX GENERATION """` block.
- **Excel-Fallback**: If no script, locate `m[XX]bis.xlsx` or similar. Use the `read_excel.py` script to inspect contents.

### 2. Extraction & Normalization
- **Quantities**: Extract all measured values, parameters, and their associated uncertainties.
- **Significant Figures**: Round all numerical values and uncertainties to **2 significant figures** before storage.
- **Uncertainty Mapping**: Pair every value with its uncertainty. If missing, mark as `TODO_UNCERTAINTY`.
- **Fit Quality**: Extract **reduced chi-squared (χ²_red)** values. Do not use R².

### 3. Generate Data Provenance Markdown
Produce a file named `data_provenance.md` in the experiment directory with the following structure:

#### Metadata
- **Experiment**: [Name/ID]
- **Source**: [Script Path / Excel Path]
- **Timestamp**: [ISO Date]

#### Parameters & Constants
| Quantity | Symbol | Value | Uncertainty | Unit | Source |
|----------|--------|-------|-------------|------|--------|
| ...      | ...    | ...   | ...         | ...  | ...    |

#### Experimental Data (Tables)
[Generate Markdown tables for each measured series]

#### Fit Results
- **Parameter**: [Value ± Uncertainty]
- **χ²_red**: [Value]
- **Provenance**: [Line number in script or Sheet/Column in Excel]

## Quality Standards
- **English Only**: All data labels and descriptions must be in English.
- **Traceability**: Every value must include its exact source (provenance).
- **No Interpretation**: This skill only parses data; it does not analyze physical meaning.

## Resources

### scripts/
- `read_excel.py`: Tool for inspecting Excel sheets and columns.
