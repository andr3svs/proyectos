---
name: mecanica-mxbis-latex
description: "Use when: modifying, populating, or structuring LaTeX documents in Mecanica/m[XX] or m[XX]bis experiment folders. Analyzes reference PDF first to determine document structure and required results, then extracts data from either Excel or Python sources. Follows m11bis/M3bis2 reference patterns for consistency."
applyTo: "Mecanica/m[0-9]*/**/*.tex"
---

# Physics Practice - Mechanics Experiment (mXX/mXXbis) LaTeX Structure Guide

## Overview
Documents in the `Mecanica/m[XX]/` or `Mecanica/m[XX]bis*/` folders follow a standardized structure for laboratory reports. The workflow starts by asking the user if they want to use the Python analysis file. After that choice is confirmed, the **PDF reference document is always examined first** to establish the proper structure and identify what results must be extracted. Instructions then guide you to extract data from either Excel or Python sources.

---

## Quality Requirements (Non-Negotiable)

All reports must meet the following requirements:

### **CRITICAL: Agent is a Template Maker Only**
🔴 **Agent NEVER writes Discussion or Conclusions**
- Discussion is reserved for human interpretation
- Conclusions must be written by human investigator
- Agent only populates: Data, Results, Tables, Figures, Abstract
- Agent leaves Discussion/Conclusions sections **empty or with placeholders** for human to complete

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

## Workflow: PDF-First Approach

### **Step 0: Ask Data Source Preference First** (Mandatory First Interaction)

Before any extraction or edits, I will ask:

> **"Do you want me to use the Python analysis file first? (Yes/No)"**

Rules:
1. If **Yes**: proceed with Python-driven extraction as primary source.
2. If **No**: proceed with Excel/manual extracted results.
3. If unclear: ask one clarifying follow-up before proceeding.
4. If any required uncertainty is missing from the source, ask explicitly before computing it:

> **"Some uncertainties are not explicitly provided. Do you want me to compute them using sample standard deviation (stdev) from repeated trials? (Yes/No)"**

### **Step 1: Identify and Analyze Reference PDF** (Always Done After Step 0)

When I begin work on a `.tex` file, I will:

1. **Identify the experiment folder**: Extract base name (e.g., `m3bis`, `m12`, `m12bis`)
2. **Search for reference PDF**: Look for `M[XX]bis[N]*.pdf` or `m[XX]bis*.pdf` with experiment name
   - Example: `M3bis2. Oscilaciones acopladas.pdf` for `m3bis/`
   - Example: `m11bis.pdf` for `m11bis_mecanica/`
3. **If PDF cannot be read**: Search for alternate format (markdown, text, or HTML version) with similar name
   - Example: If `M3bis2. COUPLED OSCILLATIONS.pdf` is unreadable, check for `M3bis2. COUPLED OSCILLATIONS.md` or similar
   - Use the markdown/text file as the structure reference instead
   - This allows proceeding with document organization even if PDF extraction fails
4. **Analyze PDF structure**: Identify sections, subsections, tables, figures, and required results
5. **Extract structure to `.tex`**: Map PDF organization to your `.tex` template
6. **Identify data needs**: Determine exactly what numerical/table content is needed from PDF

### **Step 2: Confirm and Apply Data Source** (After PDF Structure is Clear)

Once the PDF structure is understood, I will apply the choice made in Step 0 and confirm before extraction:

> **"Confirmed source: Python or Excel. I will now extract the required results from that source."**

#### **Option A: Extract From Excel File**
**Use when**: Results are already computed and stored in `.xlsx` with matching base name.

**What I will do** (after PDF structure is analyzed):
1. Locate Excel file: `m[XX]bis[N].xlsx` (base name matching PDF)
2. Read sheets to identify available data: Experimental Data, Fitted Parameters, Figure References, etc.
3. Extract rows/tables that correspond to PDF structure sections
4. Populate `.tex` placeholders with formatted data
5. Preserve all explanatory text unchanged

**Folder structure**:
```
Mecanica/m3bis/
├── M3bis2. Oscilaciones acopladas.pdf    (← Always analyzed first)
├── m3bis2.xlsx                           (results data, if using Option A)
├── Template.tex                          (.tex file to populate)
├── m3bis.py                              (optional: if using Option B)
└── references.bib
```

**When PDF+Excel approach makes sense**:
- Results are finalized in Excel
- PDF structure clearly shows what sections/tables are needed
- Data already formatted with uncertainties
- Excel sheets organized to match PDF layout

#### **Option B: Extract From Python Script**
**Use when**: You want to regenerate results from raw data or update existing computations.

**What I will do** (after PDF structure is analyzed):
1. Locate Python script: `p[XX]_mecanica.py` or `p[XX]bis.py` in experiment folder
2. Execute script (ensuring dependencies and data files are available)
3. Extract results identified as needed by PDF structure:
   - Generated tables (DataFrames)
   - Fitted parameters with uncertainties
   - Generated plots (`.png` files)
   - Computed statistics (χ², residuals, etc.)
4. Populate `.tex` template with fresh results
5. Ensure proper siunitx formatting for all values

**Folder structure**:
```
Mecanica/m12bis_mecanica/
├── m11bis.pdf  (or similar reference)     (← Always analyzed first)
├── p12_mecanica.py                        (generates results, if using Option B)
├── m12bis.tex                             (.tex file to populate)
├── references.bib
├── [raw data files: .txt, .trk, etc.]
└── [generated figures: trayectorias_*.png]
```

**When Python approach makes sense**:
- Raw data files are available and need fresh analysis
- Results need updating due to data corrections
- You want reproducible, version-controlled results
- Excel file doesn't exist, is outdated, or you prefer computational verification

### **Step 3: Final Compile Validation of the `.tex` File** (Mandatory Before Finish)

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

**Data Integration**: Extract from Python analysis output (e.g., final fitted parameters, main conclusion)

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
- [ ] Run Python analysis script (`p[X]_mecanica.py`) to generate tables and figures
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
  
- **Fitting Method**: Explain how Python code fits data (e.g., scipy's `curve_fit`, chi-squared minimization, uncertainty estimation strategy)

- **Key Assumption**: Document fixed parameters
  - Example: "We have taken `b = 4.75 cm` in all cases" (impact parameter, adjusted per experiment)

**Auto-Population from Python**:
- Extract fitted equation from comments in `p[X]_mecanica.py`
- Pull chi-squared reduced value: `χ²_red = 1` (verify in Python output)
- Document fitting confidence threshold

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

**Auto-Population from Python**:
- Extract fitted parameters with uncertainties from Python output
- Include chi-squared checks
- Reference residual analysis or goodness-of-fit metrics

#### **4.2 Subsection: Second Analysis (e.g., "Potential Well Analysis")**

Follow same structure as 4.1:
- **Experimental Data**: Trajectories or observations
- **Theoretical Model**: Expected behavior (energy-dependent orbit types)
- **Results/Classification**: Categorize trajectories (open vs. closed orbits, energy analysis)

**For Qualitative Analysis** (when fitting is not done):
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

When you choose **Option A (PDF + Excel)**:

1. **Open** `m[X]bis*.xlsx` (matching base name of instructions file)
2. **Read sheet names** to find: "Experimental Data", "Fitted Results", "Figure References", etc.
3. **Extract rows** from each sheet with complete data
4. **Format values** with uncertainties using siunitx syntax
5. **Match** rows to corresponding `.tex` table placeholders
6. **Preserve** existing table structure and captions (only replace data rows)

---

## To-Populate Checklist Before Running Agent

### **If Using PDF + Excel Approach**:
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
- [ ] **Python analysis complete**: Run `python p[X]_mecanica.py`
  - Generates: fitted parameters, tables, plots/figures
  - Outputs stored in directory or as `.png` files

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
1. New Python analysis produces fitted parameters
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
