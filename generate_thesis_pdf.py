import os
import sys
sys.path.insert(0, '.')

from pypdf import PdfWriter, PdfReader
from src.generate_chapters import generate_chapters_pdf
from src.generate_section_3_3_6 import generate_section_3_3_6_pdf

def compile_complete_thesis_pdf():
    """
    Merges original 53-page 'Abdulameen Chapter 1 -3.pdf' completely UNTOUCHED,
    inserts the newly formatted Section 3.3.6 page right after Page 47,
    and appends Chapters 4-5 ('output/pdf/Chapters_4_and_5.pdf') into
    'Abdulameen_Complete_Thesis_Chapters_1_5.pdf'.
    """
    ch1_3_path = "Abdulameen Chapter 1 -3.pdf"
    sec336_path = "output/pdf/section_3_3_6.pdf"
    ch4_5_path = "output/pdf/Chapters_4_and_5.pdf"
    output_pdf_path = "Abdulameen_Complete_Thesis_Chapters_1_5.pdf"
    
    if not os.path.exists(ch1_3_path):
        raise FileNotFoundError(f"Source file not found: {ch1_3_path}")
        
    # 1. Generate standalone Section 3.3.6 page
    generate_section_3_3_6_pdf(sec336_path)
    
    # 2. Generate Chapters 4 & 5 PDF
    generate_chapters_pdf(ch4_5_path)
    
    writer = PdfWriter()
    
    # Read original Chapters 1-3
    reader1 = PdfReader(ch1_3_path)
    print(f"Loading original Chapters 1-3 ({len(reader1.pages)} pages)...")
    
    # Insert Pages 1 to 47 of Chapters 1-3
    for i in range(min(47, len(reader1.pages))):
        writer.add_page(reader1.pages[i])
        
    # Insert Section 3.3.6 page
    reader_sec = PdfReader(sec336_path)
    print("Inserting Section 3.3.6 (Hypothesis Testing Framework)...")
    for page in reader_sec.pages:
        writer.add_page(page)
        
    # Append remaining pages of Chapters 1-3 (Pages 48 to end)
    for i in range(47, len(reader1.pages)):
        writer.add_page(reader1.pages[i])
        
    # Append Chapters 4 & 5
    reader2 = PdfReader(ch4_5_path)
    print(f"Adding Chapters 4-5 ({len(reader2.pages)} pages)...")
    for page in reader2.pages:
        writer.add_page(page)
        
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
        
    print(f"\n========================================================")
    print(f"SUCCESS: Complete Thesis PDF compiled successfully!")
    print(f"Final Document: {output_pdf_path}")
    print(f"Total Pages: {len(writer.pages)}")
    print(f"========================================================")

if __name__ == '__main__':
    compile_complete_thesis_pdf()
