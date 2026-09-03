import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader

from src.generate_chapters import generate_chapters_pdf

def add_page_number_overlay(pdf_path):
    """
    Stamps centered page numbers at the bottom middle of every single page.
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    
    for i, page in enumerate(reader.pages):
        page_num = i + 1
        
        # Create transparent canvas with centered page number
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('Times-Roman', 10)
        can.drawCentredString(306, 36, str(page_num))
        can.save()
        packet.seek(0)
        
        # Merge canvas overlay with page
        overlay_reader = PdfReader(packet)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)
        
    with open(pdf_path, 'wb') as f_out:
        writer.write(f_out)
    print(f"[OK] Successfully stamped centered page numbers on all {total_pages} pages.")

def compile_complete_thesis_pdf():
    """
    Standard Reproduction Compilation Pipeline:
    - Uses 'Abdulameen Chapter 1 -3.pdf' (derived directly from Word 'Abdulameen Chapter 1 -3.docx') as the default input for Chapters 1-3.
    - Generates Chapters 4-5 & References via ReportLab ('output/pdf/Chapters_4_and_5.pdf').
    - Merges Chapters 1-3 + Chapters 4-5 into 'Abdulameen_Complete_Thesis_Chapters_1_5.pdf'.
    - Stamps bottom-centered page numbers across all pages.
    """
    ch1_3_path = "Abdulameen Chapter 1 -3.pdf"
    ch4_5_path = "output/pdf/Chapters_4_and_5.pdf"
    output_pdf_path = "Abdulameen_Complete_Thesis_Chapters_1_5.pdf"
    
    if not os.path.exists(ch1_3_path):
        raise FileNotFoundError(f"Source file not found: {ch1_3_path}")

    # 1. Generate Chapters 4 & 5 PDF
    generate_chapters_pdf(ch4_5_path)
    
    writer = PdfWriter()
    
    # Read Chapters 1-3 (Word export baseline)
    reader1 = PdfReader(ch1_3_path)
    print(f"Loading Chapters 1-3 vector PDF ({len(reader1.pages)} pages)...")
    for page in reader1.pages:
        writer.add_page(page)
        
    # Append Chapters 4 & 5
    reader2 = PdfReader(ch4_5_path)
    print(f"Loading Chapters 4-5 ({len(reader2.pages)} pages)...")
    for page in reader2.pages:
        writer.add_page(page)
        
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
        
    # 2. Stamp centered page numbers across all pages
    add_page_number_overlay(output_pdf_path)
        
    print(f"\n========================================================")
    print(f"SUCCESS: Complete Thesis PDF compiled successfully!")
    print(f"Final Document: {output_pdf_path}")
    print(f"Total Pages: {len(writer.pages)}")
    print(f"========================================================")

if __name__ == '__main__':
    compile_complete_thesis_pdf()
