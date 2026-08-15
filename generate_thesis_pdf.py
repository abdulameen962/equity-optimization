import os
import sys
sys.path.insert(0, '.')

from pypdf import PdfWriter, PdfReader
from src.generate_chapters import generate_chapters_pdf

def compile_complete_thesis_pdf():
    """
    Merges original Abdulameen Chapter 1 -3.pdf with newly generated Chapters_4_and_5.pdf
    into a single, consolidated publication-ready document: Abdulameen_Complete_Thesis_Chapters_1_5.pdf.
    Preserves Abdulameen Chapter 1 -3.pdf completely untouched.
    """
    ch1_3_path = "Abdulameen Chapter 1 -3.pdf"
    ch4_5_path = "output/pdf/Chapters_4_and_5.pdf"
    output_pdf_path = "Abdulameen_Complete_Thesis_Chapters_1_5.pdf"
    
    if not os.path.exists(ch1_3_path):
        raise FileNotFoundError(f"Source file not found: {ch1_3_path}")
        
    # Ensure Chapters 4 & 5 PDF is generated
    generate_chapters_pdf(ch4_5_path)
    
    writer = PdfWriter()
    
    # Append Chapters 1 - 3
    reader1 = PdfReader(ch1_3_path)
    print(f"Adding Chapters 1-3 ({len(reader1.pages)} pages)...")
    for page in reader1.pages:
        writer.add_page(page)
        
    # Append Chapters 4 & 5
    reader2 = PdfReader(ch4_5_path)
    print(f"Adding Chapters 4-5 ({len(reader2.pages)} pages)...")
    for page in reader2.pages:
        writer.add_page(page)
        
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
        
    print(f"\n========================================================")
    print(f"SUCCESS: Complete Thesis PDF compiled!")
    print(f"Final Document: {output_pdf_path}")
    print(f"Total Pages: {len(writer.pages)}")
    print(f"========================================================")

if __name__ == '__main__':
    compile_complete_thesis_pdf()
