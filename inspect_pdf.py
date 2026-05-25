import os
import pypdf

pdf_path = r"d:\IITbwb\snake robot\sanke robot.pdf"
out_path = r"d:\IITbwb\snake robot\pdf_inspection.txt"

try:
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"PDF Path: {pdf_path}\n")
        f.write(f"Number of Pages: {num_pages}\n\n")
        
        # Write metadata
        f.write("--- Metadata ---\n")
        meta = reader.metadata
        if meta:
            for k, v in meta.items():
                f.write(f"{k}: {v}\n")
        else:
            f.write("No metadata found\n")
            
        f.write("\n--- Outline/TOC ---\n")
        outlines = reader.outline
        if outlines:
            for item in outlines:
                f.write(f"{item}\n")
        else:
            f.write("No outline found\n")
            
        # Extract first 5 pages and last 5 pages to compare with markdown
        f.write("\n--- FIRST 3 PAGES ---\n")
        for i in range(min(3, num_pages)):
            f.write(f"\n--- PAGE {i+1} ---\n")
            f.write(reader.pages[i].extract_text())
            
        f.write("\n--- LAST 3 PAGES ---\n")
        for i in range(max(0, num_pages-3), num_pages):
            f.write(f"\n--- PAGE {i+1} ---\n")
            f.write(reader.pages[i].extract_text())
            
    print(f"Inspection complete. Written to {out_path}")
    print(f"Total pages: {num_pages}")
except Exception as e:
    print("Error:", e)
