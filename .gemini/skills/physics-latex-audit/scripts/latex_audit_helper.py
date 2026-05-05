import pandas as pd
import re
import sys
import os

def extract_latex_tables(tex_path):
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find tabular and longtable environments
    tables = []
    # Simplified regex for extracting rows from tables
    pattern = re.compile(r'\\begin\{(?:tabular|longtable)\}.*?\\midrule(.*?)\\bottomrule', re.DOTALL)
    
    matches = pattern.finditer(content)
    for i, match in enumerate(matches):
        table_content = match.group(1).strip()
        rows = []
        for line in table_content.split('\\\\'):
            line = line.strip()
            if not line: continue
            # Remove LaTeX comments
            line = re.sub(r'%.*$', '', line).strip()
            if not line: continue
            
            cells = [c.strip() for c in line.split('&')]
            rows.append(cells)
        tables.append({'id': i, 'rows': rows})
    
    return tables

def audit_tables(tex_path, excel_path):
    if not os.path.exists(tex_path):
        print(f"Error: LaTeX file not found at {tex_path}")
        return
    if not os.path.exists(excel_path):
        print(f"Error: Excel file not found at {excel_path}")
        return

    print(f"Auditing {tex_path} against {excel_path}...")
    
    tex_tables = extract_latex_tables(tex_path)
    print(f"Found {len(tex_tables)} tables in LaTeX file.")
    
    xls = pd.ExcelFile(excel_path)
    print(f"Sheets in Excel: {xls.sheet_names}")
    
    for i, table in enumerate(tex_tables):
        print(f"\n--- LaTeX Table {i} ---")
        print(f"Rows: {len(table['rows'])}")
        if table['rows']:
            print(f"Columns: {len(table['rows'][0])}")
            print(f"First row: {table['rows'][0]}")
        
    print("\nManual verification recommended for row content match.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python latex_audit_helper.py <file.tex> <file.xlsx>")
    else:
        audit_tables(sys.argv[1], sys.argv[2])
