---
name: physics-table-styler
description: Ensures LaTeX tables in physics reports have professional, even formatting and consistent alignment. Use to polish tables after they have been generated or modified.
---

# Physics Table Styler

## Overview
This skill focuses on the aesthetic and structural "evenness" of LaTeX tables. It ensures that tables are not only data-complete but also visually balanced and free of formatting artifacts.

## Workflow

### 1. Structural Symmetry Audit
- **Column Alignment**: Every numeric column MUST use the `S` column type from `siunitx`. Ensure `table-format` is specified (e.g., `S[table-format=3.2(2)]`) to prevent jagged alignment.
- **Header Balancing**: Use `\multicolumn{1}{c}{Header}` for headers over `S` columns to ensure they are perfectly centered.
- **Rule Consistency**: Verify the presence of `\toprule`, `\midrule`, and `\bottomrule`. NO vertical lines (`|`) are allowed.

### 2. "Even Text" & Spacing Check
- **Overfull Hboxes**: Check the LaTeX log for "Overfull \hbox" warnings. If a table is too wide, reduce font size locally using `\small` or `\footnotesize` inside the table environment.
- **Row Padding**: Ensure `\renewcommand{\arraystretch}{1.2}` is used if rows look cramped.
- **Longtable Continuity**: Verify that `longtable` headers repeat on every page and that the "Continued on next page" footer is right-aligned and visually distinct.

### 3. Visual Polish
- **Units in Headers**: Units should be in the header, not in the data rows, using `\unit{}` or `\qty{}{}` syntax.
- **Caption Centering**: Ensure captions are centered and have consistent padding from the table body.
- **Math Mode Balance**: Ensure all `\pm` symbols are properly padded with spaces and enclosed in a single math environment or handled by `siunitx`.

## Quality Standards
- **Aesthetic Perfection**: Tables must look "even"—no mismatched column widths or weird gaps.
- **Zero Warnings**: No overfull/underfull box warnings related to tables.
- **Consistent Scaling**: Multiple tables in the same report should use the same font size and stretch factor.
