---
name: mecanica-mxbis-latex
description: "Use when: modifying, populating, or structuring LaTeX documents in Mecanica/m[XX] or m[XX]bis experiment folders. First ask if a Python script exists; if yes, use arrays under \"\"\" LATEX GENERATION \"\"\". If no script exists, read Excel. In all cases, map PDF-required columns and store uncertainty-aware values with the uncertainties module. Follows m11bis/M3bis2 reference patterns for consistency."
applyTo: "Mecanica/m[0-9]*/**/*.tex"
---

# Physics Practice - Mechanics Experiment (mXX/mXXbis) LaTeX Structure Guide

## Overview
Documents in the `Mecanica/m[XX]/` or `Mecanica/m[XX]bis*/` folders follow a standardized structure for laboratory reports. The workflow is deterministic: always ask the user first whether they already have a Python script. If they do, locate a `""" LATEX GENERATION """` section and use the arrays defined there for report population. If they do not, extract from Excel. Then analyze the reference PDF to determine required outputs, store uncertainty-aware values using the `uncertainties` module (`ufloat`/`unumpy`), and write a debug TXT log with all used data and provenance.

---

## Quality Requirements (Non-Negotiable)

All reports must meet the following requirements:

### **CRITICAL: Agent is a Template Maker Only**
🔴 **Agent NEVER writes Discussion or Conclusions**
- Discussion is reserved for human interpretation
- Conclusions must be written by human investigator
- Agent only populates: Data, Results, Tables, Figures, Abstract
- Agent leaves Discussion/Conclusions sections **empty or with placeholders** for human to complete

### **CRITICAL: No Autonomous Fitting or Value Derivation**
🔴 **Agent NEVER runs fits, regressions, optimizations, or uncertainty estimation on its own**
- Use only human-provided values and uncertainties from approved sources (Python `""" LATEX GENERATION """` arrays or Excel fields prepared by human)
- Do not run `curve_fit`, chi-squared minimization, or any derived-parameter computation unless explicit human-provided results already exist
- If a value or uncertainty is missing, ambiguous, or method is unclear, insert a clear placeholder instead of inferring
- Preferred placeholder format: `TODO_VALUE`, `TODO_UNCERTAINTY`, or table cell `-- (pending human value)`

### **Data Presentation**
1. **Significant figures**: Present all numerical results with **2 significant figures only**
   - Example: `$3.2 \pm 0.8$ \unit{m/s}` ✓
   - Example: `$3.214 \pm 0.819$` ✗ (too many digits)

2. **Uncertainty integrity (mandatory)**: Never invent, assume, or round in an uncertainty value unless the source and method are verified.
   - If uncertainty is not explicitly provided by source data, do not fabricate `\pm` values.
   - If a value is uncertain in provenance, mark it as pending and ask the user before inserting.
   - Any inserted uncertainty must state its source (sheet/column/script output) and method (e.g., standard deviation).
   
3. **Uncertainty explanation**: Every time an uncertainty is mentioned or shown, **briefly explain what it represents**
   - Use 1-2 sentences in caption or text
   - Example: "The uncertainty represents the standard error of the fit (χ²_red ≈ 1)"
   - Example: "Values shown with uncertainties estimated from residual analysis"
   
4. **Goodness of fit**: Use **reduced chi-squared (χ²_red)** instead of R²
   - ✓ Mention: "The model fits well with χ²_red ≈ 1"
   - ✗ Avoid: "The model fits well with R² = 0.95"
   - Explain briefly in Results Interpretation section what χ²_red ≈ 1 means
   - Do not create scripts for fits on your own, use the data under #LATEX SECTION.

### **Figure Management**
1. **Placeholder comments**: When a figure should be inserted, add a clear comment
   - Example: `% [FIGURE: Insert trajectory_1.png here - experimental data visualization]`
   - Example: `% [FIGURE: Fitted curve overlay on experimental points - goodness of fit illustration]`
   
2. **Automatic inclusion**: If figure files are found in the experiment folder, include them with proper captions
   - Match filenames from Excel "Figure References" or Python-generated files
   - Add descriptive caption explaining what is shown and what it demonstrates
   
3. **Caption requirements**: Every figure caption must include:
   - What is being shown (axes, markers, lines)
   - Physical meaning or context
   - Reference to supporting text (e.g., "See Section 2.1 for analysis")

### **Abstract Generation**
1. **No numerical data** (unless explicitly requested)
   - ✓ "The experiment measured the scattering angles using trajectory analysis"
   - ✗ "The experiment measured angles ranging from 102° to 111°"
   
2. **Structure**: Brief summary of:
   - Experiment objective (what was studied)
   - Methodology (how it was done)
   - Qualitative conclusion (what was found, without numbers)
   - Physical significance (why it matters)
   
3. **Concise language**: Keep abstract to 4-6 sentences maximum

### **Language & Style**
- ✓ **Always use English**
- ✓ **Concise, direct language** — avoid wordiness
- ✓ **Technical terminology is appropriate** — use it accurately
- ✓ **Active voice** where possible
- ✗ Avoid Spanish, mixed languages, verbose explanations

---

## Examples Folder Reference

Before making any modifications, check the `Mecanica/examples/` or similar reference folder for:
- Complete examples of properly formatted `.tex` documents
- Reference PDF documents showing expected structure
- Excel files demonstrating data organization
- Examples of how figures should be integrated
- Sample abstracts and figure captions

**If you find discrepancies between these instructions and examples, the examples take precedence** — report the discrepancy for instructions update.

---

## Workflow: Ask Script First, Then Python-or-Excel, PDF-Guided Columns

### **Step 0: Ask User for Existing Python Script** (Mandatory First Interaction)

Before modifying the `.tex` file, ask this exact question first:

> **"Do you already have a Python analysis script for this experiment? (Yes/No)"**

Routing rules:
1. If **Yes**: locate that script and search for a section labeled `""" LATEX GENERATION """`.
2. If the section exists: use arrays/variables from that section as the primary report data source.
3. If the section is missing: ask one follow-up whether to use the rest of the script outputs or fallback to Excel.
4. If **No**: use Excel as source of values.

If uncertainty values are missing in either source, do not estimate them.

Use this prompt instead:

> **"Some uncertainties are missing or unclear. I will leave placeholders unless you provide the exact values and source. Continue? (Yes/No)"**

### **Step 1A: Python Path (When User Has Script)**

Required behavior:
1. Locate script with experiment base name (for example `m3bis.py`, `p12_mecanica.py`).
2. Parse/inspect `""" LATEX GENERATION """` block.
3. Extract arrays used for tables/results exactly as defined there.
4. Keep a mapping record: `report_quantity -> script_variable`.

### **Step 1B: Excel Path (When User Has No Script)**

Required behavior:
1. Locate Excel file with experiment base name (for example `m3bis2.xlsx`).
2. Read all relevant sheets and normalize column names.
3. Produce a column inventory (sheet, column name, units if available).
4. Build mapping record: `report_quantity -> sheet.column`.

### **Step 2: Identify and Analyze Reference PDF**

After selecting and loading the data source, analyze the PDF (or text/markdown fallback) to determine required report outputs.

When I begin work on a `.tex` file, I will:
1. Identify the experiment folder base name (for example `m3bis`, `m12`, `m12bis`).
2. Search for reference PDF (`M[XX]bis[N]*.pdf` or `m[XX]bis*.pdf`).
3. If PDF cannot be read, use a same-name markdown/text fallback.
4. Extract required sections, tables, figures, and numerical outputs.

### **Step 3: Map PDF Requirements to Source Data and Store Uncertainties**

Using the selected source from Step 1A or Step 1B and the PDF-required outputs from Step 2:
1. Build an explicit mapping from required PDF quantities to source fields (script arrays or Excel columns).
2. For each measured quantity, pair value and uncertainty fields.
3. Store uncertainty-aware values using `uncertainties` module types:
   - Scalar values: `ufloat(value, sigma)`
   - Arrays/series: `uncertainties.unumpy.uarray(values, sigmas)`
4. Keep mapped uncertainty-aware data in named structures (for example dictionaries/DataFrames) that can be consumed by `.tex` table generation.
5. Ensure each uncertainty has traceable provenance (sheet/column and method).
6. If any value/uncertainty is not explicitly present in the source, write a placeholder and mark provenance as pending human confirmation.

### **Step 4: Mandatory Debug TXT Export (Data + Provenance)**

Before populating `.tex`, write a debug text file in the experiment folder (for example `debug_data_provenance.txt`) containing:
1. Timestamp and selected data source (Python script or Excel).
2. For every value used in the report:
   - Report quantity name.
   - Numeric value and uncertainty.
   - Provenance:
     - Python path: script filename + variable/array name + `""" LATEX GENERATION """` reference.
     - Excel path: workbook + sheet + column (+ row/index when applicable).
   - Uncertainty method (explicit source, stdev, propagated, etc.).
3. A final summary block with counts of quantities, direct-source uncertainties, and computed uncertainties.

Important policy for this debug file:
- Computed uncertainties count should be `0` unless values were explicitly provided by human as computed outputs.
- Add a `PENDING_PLACEHOLDERS` section listing every unresolved quantity.

Also print one debug line to console when file is generated, for example:
`DEBUG: wrote debug_data_provenance.txt with N mapped quantities`.

### **Step 5: Populate `.tex` with Processed Values**

1. Insert tables/results according to the PDF structure.
2. Format numbers with 2 significant figures and proper `siunitx` units.
3. Preserve explanatory text unless the user requests wording edits.

### **Reference Folder Structure**
```
Mecanica/m3bis/
├── M3bis2. Oscilaciones acopladas.pdf  (structure contract)
├── m3bis2.xlsx                         (source data)
├── read_m3bis2.py                      (mandatory preprocessing script)
├── m3bis2.tex                          (target report)
└── references.bib
```

### **Step 6: Final Compile Validation of the `.tex` File** (Mandatory Before Finish)

Before considering the task complete, I must ensure the generated `.tex` file compiles successfully.

Required checks:
1. Run a LaTeX build command in the experiment folder (for example: `latexmk -pdf <file>.tex`, or equivalent configured command).
2. If compilation fails, fix LaTeX errors related to the generated content and compile again.
3. Only finish when compilation succeeds, or explicitly report a blocker (missing tool/package/environment issue).
4. Report compile status clearly to the user as the final step.

---

## Document Structure (Following m11bis/M3bis2 Reference)

### 1. **Preamble & Metadata** (Lines 1-40)
**Purpose**: Setup LaTeX environment and document information.

**Required Elements**:
- `\newcommand{\experimentTitle}{...}` — Brief experiment name
- `\newcommand{\experimentDate}{...}` — Date of experiment
- `\newcommand{\authorName}{...}` — Author(s) name
- `\newcommand{\groupNumber}{...}` — Group identifier

**Guidelines**:
- Use `\usepackage{booktabs}` for table formatting (cleaner lines)
- Include `\usepackage{siunitx}` for proper unit formatting (e.g., `\unit{m/s}`, `\SI{5}{\percent}`)
- Configure biblatex with `\addbibresource{references.bib}`

### 2. **Abstract** (After `\maketitle`)
**Purpose**: One-paragraph summary of experiment objectives, methodology, and key findings.

**Placement rule (mandatory)**:
- The abstract must appear on the **first page**, immediately after `\maketitle`.
- Do not place `\section` content before the abstract.
- Do not insert page breaks (`\newpage`, `\clearpage`) between `\maketitle` and the abstract.

**Structure**:
1. What was tested/studied
2. How it was done (method/apparatus)
3. Key results or discoveries
4. Physical significance

**Data Integration**: Extract only from human-provided outputs (Python `""" LATEX GENERATION """` arrays or Excel fields).

### 3. **Introduction and Objectives**
**Purpose**: Establish physics context and experiment goals.

**Required Subsections**:
- Theoretical background (Newton's laws, central forces, scattering theory, etc.)
- Model being tested
- Specific objectives for your experiment
- Link between theory and the physical system being studied

**Guidelines**:
- Reference the actual form of potential/equation used in analysis
- Explain measurement approach (Tracker software, trajectory analysis, etc.)
- Mention any assumptions or constraints

### 4. **Results and Data Analysis** (Main Content Section)

#### **4.1 Subsection: First Analysis (e.g., "Analysis of the Hill Scattering")**

##### **4.1.1 Experimental Data** (subsubsection)
**Purpose**: Present measured trajectories, show raw/processed experimental observations.

**Required Elements**:
- **Figure(s)**: Experimental trajectories or raw plots
  - Populate from: `[Analysis Python file]` generates `trayectorias_experimentales_*.png`
  - Caption must identify what measurement is shown (e.g., "h represents initial ramp height; axes centered on center of forces")
  
- **Data Table**: Summary of key measurements for each trial
  - Columns: velocities (`v_0`), scattering angles (`θ`), heights (`h`), or other measured quantities
  - Include uncertainties using `±` format with consistent decimal places
  - Use `\unit{}` from siunitx for units
  - Example row: `$0.317 \pm 0.029$ & $108.400 \pm 0.029$ \\`

**Auto-Population Checklist**:
- [ ] Read human-provided script outputs (`""" LATEX GENERATION """`) or Excel fields
- [ ] Copy generated tables with `\unit{}` formatting
- [ ] Place figures in `Mecanica/m[X]bis_mecanica/` directory
- [ ] Reference with `\label{fig:...}` and `\ref{fig:...}`

##### **4.1.2 Theoretical Model and Fitting Process** (subsubsection)
**Purpose**: Document the mathematical model and fitting methodology.

**Required Elements**:
- **Physics Equation(s)**: Display the theoretical model
  - Example: `$b = \cos\left(\frac{\theta}{2}\right) \left[ \frac{k}{m v_0^2 \sin\left(\frac{\theta}{2}\right)} - r_0 \right]$`
  
- **Parameter Definitions**: Describe what each symbol means
  - `k` = interaction constant
  - `m` = mass
  - `v_0` = initial velocity
  - `θ` = scattering angle
  - `r_0` = center of forces offset
  
- **Fitting Method**: Report only the fitting method description already provided by the human source; do not execute or infer fitting steps.

- **Key Assumption**: Document fixed parameters
  - Example: "We have taken `b = 4.75 cm` in all cases" (impact parameter, adjusted per experiment)

**Auto-Population from Source**:
- Extract equation/fit summaries only if explicitly present in source fields
- Pull chi-squared reduced value only if explicitly provided
- If absent, leave placeholders and mark pending human input

##### **4.1.3 Results Interpretation** (subsubsection)
**Purpose**: Analyze fitted parameters and their physical meaning.

**Required Elements**:
- **Parameter Results Table**:
  ```latex
  \begin{table}[H]
      \centering
      \begin{tabular}{lcc}
          \toprule
          Parameter & Symbol & Value \\
          \midrule
          Interaction Constant & $k$ & $(1.17 \pm 0.54) \times 10^{-3}$ \unit{kg.m^3/s^2} \\
          Center of Forces Offset & $r_0$ & $(0.00 \pm 0.05)$ \unit{m} \\
          \bottomrule
      \end{tabular}
      \caption{Parameters obtained from fitting.}
      \label{tab:fit_results}
  \end{table}
  ```

- **Physical Interpretation**:
  - Compare fitted values to expected ranges
  - Discuss uncertainties and what they imply
  - Address any discrepancies with theory
  - Mention systematic errors or experimental limitations (friction, surface bumps, etc.)

- **Validation Check**:
  - Reconstruct a derived quantity from fitted parameters
  - Compare with theoretical or measured value
  - Example: "Using k = 1.17 × 10⁻³, the predicted hill height at r = 1 cm is 12 ± 5 cm, consistent with laboratory setup"

**Auto-Population from Source**:
- Extract fitted parameters with uncertainties only when explicitly present in source data
- Include chi-squared or residual metrics only when explicitly provided
- Otherwise use placeholders and add pending notes

#### **4.2 Subsection: Second Analysis (e.g., "Potential Well Analysis")**

Follow same structure as 4.1:
- **Experimental Data**: Trajectories or observations
- **Theoretical Model**: Expected behavior (energy-dependent orbit types)
- **Results/Classification**: Categorize trajectories (open vs. closed orbits, energy analysis)

**For Qualitative Analysis** (when fitting data is not provided):
- Describe trajectories visually with reference to theory
- Classify by energy regime (high E → open, low E → bound/precessing)
- Note observable effects (orbital decay, precession, friction)

---

## Excel File Format & Data Extraction

### **Expected Excel Structure**

When using PDF + Excel approach, the `.xlsx` file should follow this pattern:

#### **Sheet: Experimental Data**
| Measurement | Symbol | Value | Unit | Uncertainty |
|-----------|--------|-------|------|------------|
| Initial Velocity | $v_0$ | 0.317 | m/s | 0.029 |
| Scattering Angle | $θ$ | 108.4 | deg | 0.029 |

**For LaTeX population**: Convert to → `$0.317 \pm 0.029$ \unit{m/s}`

#### **Sheet: Fitted Parameters**
| Parameter Name | Symbol | Value | Exponent | Unit | Uncertainty |
|---|---|---|---|---|---|
| Interaction Constant | $k$ | 1.17 | -3 | kg.m³/s² | 0.54 |
| Center Offset | $r_0$ | 0.00 | 0 | m | 0.05 |

**For LaTeX population**: Convert to → `$(1.17 \pm 0.54) \times 10^{-3}$ \unit{kg.m^3/s^2}`

#### **Sheet: Figure References**
| Figure Name | Filename | Caption |
|---|---|---|
| Trajectories 1 | trayectorias_experimentales_1.png | Experimental trajectories, h represents initial height... |
| Trajectories 2 | trayectorias_experimentales_2.png | Additional trajectories showing scattering pattern... |

**For LaTeX population**: Insert as → `\includegraphics[width=1\textwidth]{trayectorias_experimentales_1.png}`

### **How I Extract From Excel**

When using the Excel path:

1. **Open** `m[X]bis*.xlsx` (matching base name of instructions file)
2. **Read sheet names** to find: "Experimental Data", "Fitted Results", "Figure References", etc.
3. **Extract rows** from each sheet with complete data
4. **Format values** with uncertainties using siunitx syntax
5. **Match** rows to corresponding `.tex` table placeholders
6. **Preserve** existing table structure and captions (only replace data rows)
7. **Do not derive missing values**; keep placeholders for missing/uncertain entries

---

## To-Populate Checklist Before Running Agent

### **If Using Excel Path**:
- [ ] **PDF reference identified**: `M3bis2. Oscilaciones acopladas.pdf` or similar
  - Confirms document structure and section order
  - Provides reference formatting examples
  - **If PDF unreadable**: Check for alternate formats
    - Look for `.md`, `.txt`, or `.markdown` version with similar base name
    - Use markdown/text file as structure reference instead
  
- [ ] **Excel file found**: Look for `m[X]bis*.xlsx` in experiment folder
  - Contains: tables, parameters, computed values
  - Rows match data measurements
  - Cells labeled with headers (Name, Symbol, Value, Unit, Uncertainty)

- [ ] **.tex template ready**: `Template.tex` or `m[X]bis.tex`
  - Has stub sections with `\begin{table}[H]` and `\includegraphics{}`
  - Lacks numerical data (placeholders only)

### **If Using Python Approach**:
- [ ] **Python source prepared by human**: `""" LATEX GENERATION """` section exists
   - Contains: tables/arrays/values already prepared for LaTeX population
   - Agent reads only, does not run new fitting computations

- [ ] **Figures present** in the experiment folder:
  - `trayectorias_experimentales_*.png` (trajectory plots)
  - Any derived plots (e.g., fitted curves, comparisons)

- [ ] **Identify placeholder patterns**:
  - Marked tables with `\begin{table}[H]` (some may be hardcoded examples)
  - Marked figures with `\includegraphics[width=...]{...}`
  - Math expressions in `\begin{equation}`

- [ ] **Confirm m11bis/M3bis2 reference structure**:
  - Abstract: physics context + methods + results summary
  - Intro: theory and modeling approach
  - Results: organized by analysis type with data → model → interpretation flow
  - Discussion: physical implications and agreement with theory
  - Conclusions: summary and future improvements

---

## Common Task Patterns

### **When to Populate a Table**
1. Data source confirmed (PDF+Excel or Python output)
2. Table caption and label already exist in `.tex` file
3. Rows should be extracted from Excel sheet or Python dataframe
4. Use `siunitx` format: `$value \pm uncertainty$ & \unit{unit}`

### **When to Insert a Figure**
1. Source approach confirmed:
   - **PDF+Excel**: Figure filename listed in "Figure References" sheet
   - **Python**: Python generates `.png` file in the experiment directory
2. `.tex` file has `\includegraphics{...}` stub with filename
3. Add appropriate caption describing axes, markers, and physical meaning
4. Reference: `\label{fig:...}` for cross-referencing

### **When to Update Results Section**
1. Human-provided source includes fitted parameters
2. Results Interpretation subsection has a parameter table
3. Extract parameter names, values, uncertainties, units
4. Format using `\times 10^{n}` for scientific notation when needed

### **When to Validate Against m11bis**
- Check section naming and order match m11bis.pdf structure
- Verify table formatting (booktabs: `\toprule`, `\midrule`, `\bottomrule`)
- Confirm figure captions are descriptive and link to physics concepts
- Ensure equations are properly defined in Theoretical Model section

---

## Formatting Guidelines

### **Units & Values**
```latex
% CORRECT (using siunitx)
\SI{5}{\percent}              % 5%
\unit{m/s}                    % m/s
$1.17 \times 10^{-3}$         % scientific notation
$0.317 \pm 0.029$            % value with uncertainty

% AVOID
5% (unformatted percentage)
m/s (plain text)
1.17e-3 (not in LaTeX math mode)
```

### **Table Format** (booktabs style)
```latex
\begin{table}[H]
    \centering
    \begin{tabular}{lcc}        % l=left, c=center
        \toprule              % Top line
        Column 1 & Column 2 & Column 3 \\
        \midrule              % Middle line
        data & data & data \\
        \bottomrule           % Bottom line
    \end{tabular}
    \caption{Descriptive caption.}
    \label{tab:unique_identifier}
\end{table}
```

### **Cross-References**
```latex
See Figure~\ref{fig:trajectory_1} and Table~\ref{tab:experimental_data}.
% Use ~ for non-breaking space before references
```

---

## Agent Instructions

### **What Agent DOES (Template Population Only)**

✅ **PERMITTED OPERATIONS**:
- Populate Preamble & Metadata
- Generate Abstract (no numbers)
- Populate Introduction (if template has placeholders)
- Extract and insert Experimental Data (tables, figures)
- Extract and insert Results (measured values, fitted parameters)
- Insert Figure placeholders with comments for where they belong
- Format all numerical values and uncertainties

❌ **STRICTLY FORBIDDEN**:
- **NEVER write Discussion sections** — leave empty or with marker
- **NEVER write Conclusions** — leave empty or with marker
- **NEVER interpret results** — data only
- **NEVER evaluate significance** — facts only
- **NEVER explain physical implications** — human's role

### **Sections Responsibility Assignment**

| Section | Agent Does | Human Does |
|---------|-----------|-----------|
| Preamble | ✅ Populate metadata | - |
| Abstract | ✅ Generate (no numbers) | Revise if needed |
| Introduction | ✅ Populate from template | Add/refine physics context |
| Results & Data | ✅ Extract & insert values | - |
| Figures | ✅ Include/comment location | Add figures if missing |
| Discussion | ❌ Leave empty | ✅ Write full interpretation |
| Conclusions | ❌ Leave empty | ✅ Write summary & implications |

---

### **Before Any Work: Check Examples Folder**

1. **Locate examples**: Look for `Mecanica/examples/` or similar reference folder
2. **Review structure**: Examine completed `.tex` files to understand expected quality
3. **Note formatting**: Observe how tables, figures, abstracts, and captions are formatted
4. **Cross-check instructions**: If examples differ from instructions, examples are authoritative

### **Initial Workflow: PDF-First Analysis**

**When I begin work on a `.tex` file, I will:**

1. **Identify the experiment folder** (e.g., `Mecanica/m3bis/`, `Mecanica/m12bis_mecanica/`)
   - Extract base name pattern: `m[XX]` or `m[XX]bis` (bis is optional)
   
2. **Search for reference PDF**:
   - Look for any `.pdf` file in the experiment folder with a descriptive title
   - Example patterns: `M3bis2. Oscilaciones acopladas.pdf`, `m11bis.pdf`, `m4bis_oscilaciones.pdf`
   - The PDF is the authoritative guide for document structure and content
   
3. **Analyze PDF structure**:
   - Identify all sections and subsections
   - Note which results/parameters/tables are presented
   - Understand the logical flow and connections between sections
   - Extract formatting patterns (how tables are labeled, how figures are captioned, etc.)

4. **Check examples folder** (if available):
   - Compare PDF structure to examples
   - Note any formatting differences in tables, captions, abstracts
   - Verify expected quality standards

5. **Map PDF to `.tex` template**:
   - Ensure your `.tex` file follows the same logical structure as the PDF
   - Identify what numerical/table content is explicitly shown in PDF
   - Create stubs or verify placeholders exist for each result section

6. **Ask for data source**:
   > **"Now that I understand the PDF structure, how would you like me to extract the required results?**  
   > **A)** From Excel file `m[XX]bis[N].xlsx`?  
   > **B)** From Python script `p[XX]*.py`, regenerating from raw data?"**

### **If You Choose Option A (Excel)**:
1. **Locate Excel file**: `m[XX]bis[N].xlsx` with matching base name
2. **Extract data from sheets** to match PDF-identified sections
3. **Format with quality requirements**:
   - Round to **2 significant figures only**
   - Include uncertainty explanation in captions/text
   - Use χ²_red instead of R² for fit quality
4. **Insert figures**: Check folder for referenced files, include with captions
5. **Generate abstract**: No numbers, focus on objective/method/significance
6. **Populate `.tex`** preserving structure

### **If You Choose Option B (Python)**:
1. **Locate and execute Python script**: `p[XX]_*.py`
2. **Extract targeted results** that PDF structure requires
3. **Format with quality requirements**:
   - Round to **2 significant figures only**
   - Document χ²_red values, avoid R²
   - Explain where uncertainties come from
4. **Collect generated figures**: Include with descriptive captions
5. **Generate abstract**: No numerical data, descriptive only
6. **Format with siunitx** and insert into `.tex` file

### **During Population: Quality Checklist**:

**Agent Verifies** ✅:
- [ ] All numerical values: 2 significant figures only
- [ ] Uncertainties: Every one has brief explanation (1-2 sentences)
- [ ] Figures: Placeholders marked with comments or actual files included
- [ ] Figure captions: Describe what's shown + physical meaning + section reference
- [ ] Goodness of fit: χ²_red documented, NOT R²
- [ ] Abstract: No numerical data, 4-6 sentences, qualitative only
- [ ] Language: English only, concise and direct
- [ ] Follows PDF structure: Organization matches reference document
- [ ] Examples comparison: Format matches examples folder quality
- [ ] Discussion section: **LEFT EMPTY for human** (marked with placeholder)
- [ ] Conclusions section: **LEFT EMPTY for human** (marked with placeholder)

**Human Completes** ✍️:
- [ ] Discussion: Write full interpretation and physical implications
- [ ] Conclusions: Summarize findings and significance
- [ ] Review Abstract: Refine if needed
- [ ] Add any missing context or nuance

### **Final Validation**:
1. **Follow PDF as authoritative**: The PDF structure is the contract for data sections
2. **Preserve explanatory text**: Only replace stub/placeholder numerical content
3. **Match formatting**: Use booktabs, siunitx, and cross-references as shown in PDF
4. **Validate completeness**: Ensure all DATA visible in PDF is present in `.tex`
5. **Quality review**: Verify all requirements met before completion
6. **Discussion & Conclusions empty**: Both sections left blank with clear markers for human to fill
7. **Delivery checklist**: 
   - ✅ Preamble populated
   - ✅ Abstract generated
   - ✅ Data & Results filled
   - ✅ Figures included/commented
   - ❌ Discussion empty (human's task)
   - ❌ Conclusions empty (human's task)

---

## File Organization Reference

### **Naming Convention**
- Experiment folders: `m[XX]` or `m[XX]bis` (bis is optional, always lowercase)
- Reference PDFs: `M[XX]bis[N]. [Description].pdf` or `m[XX]bis.pdf`
- Excel files: `m[XX]bis[N].xlsx` (must match PDF base name)
- Python files: `p[XX]_mecanica.py` or `p[XX]bis.py` or `p[XX].py`
- LaTeX files: `m[XX]bis.tex`, `Template.tex`, or `m[XX]bis_mecanica.tex`

### **PDF + Excel Structure**:
```
Mecanica/m3bis/
├── M3bis2. Oscilaciones acopladas.pdf    (← Start here: analyze structure first)
├── m3bis2.xlsx                           (extract: numerical results)
├── Template.tex                          (populate: based on PDF structure)
├── m3bis.py                              (optional: regenerates Excel data)
└── references.bib
```

### **PDF + Python Structure**:
```
Mecanica/m12bis_mecanica/
├── m11bis.pdf (or m12bis.pdf reference) (← Start here: analyze structure first)
├── p12_mecanica.py                       (extract: regenerate results)
├── m12bis.tex                            (populate: based on PDF structure)
├── references.bib
├── [raw data files: .txt, .trk, etc.]
└── [generated figures: trayectorias_*.png]
```

---

## Examples from m11bis Reference

- **Parameter uncertainty reporting**: `$(1.17 \pm 0.54) \times 10^{-3}$ \unit{kg.m^3/s^2}`
- **Table labels**: `\label{tab:fit_results}`, `\label{tab:experimental_data}`
- **Figure integration**: "Figure~\ref{fig:trajectory_1} shows..." (with `~` for non-breaking space)
- **Discussion of uncertainty**: Explain uncertainties from chi-squared fitting, residual analysis, or experimental constraints
- **Validation**: Reconstruct unfit parameters from fitted constants, compare with known values
