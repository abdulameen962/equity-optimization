import os
import io
import time
import win32com.client
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader

from src.generate_chapters import generate_chapters_pdf

def export_docx_to_pdf(docx_path, output_pdf_path):
    """
    Uses Microsoft Word COM to export DOCX to PDF, maintaining 100% native Word layout, 
    math vector equations, matrices, tables, and justification settings.
    """
    docx_abs = os.path.abspath(docx_path)
    pdf_abs = os.path.abspath(output_pdf_path)
    os.makedirs(os.path.dirname(pdf_abs), exist_ok=True)
    
    print(f"Opening Microsoft Word COM to export {docx_path} -> PDF...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    try:
        doc = word.Documents.Open(docx_abs)
        time.sleep(2)  # Allow Word to fully initialize layout
        doc.SaveAs2(pdf_abs, FileFormat=17)  # 17 = wdFormatPDF
        print(f"[OK] Successfully exported DOCX to PDF: {pdf_abs}")
        doc.Close(False)
    finally:
        word.Quit()

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

def compile_complete_thesis_from_docx():
    """
    1. Converts 'Abdulameen Chapter 1 -3.docx' directly to PDF using Word COM.
    2. Generates Chapters 4 & 5 + References PDF.
    3. Merges Chapters 1-3 (from Word) + Chapters 4-5.
    4. Stamps bottom-centered page numbers across all pages.
    """
    docx_path = "Abdulameen Chapter 1 -3.docx"
    ch1_3_pdf_path = "output/pdf/Ch1_3_from_word.pdf"
    ch4_5_pdf_path = "output/pdf/Chapters_4_and_5.pdf"
    output_pdf_path = "Abdulameen_Complete_Thesis_Chapters_1_5.pdf"
    
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Source file not found: {docx_path}")

    # 1. Export Word DOCX to PDF
    export_docx_to_pdf(docx_path, ch1_3_pdf_path)
    
    # 2. Generate Chapters 4 & 5 PDF
    generate_chapters_pdf(ch4_5_pdf_path)
    
    # 3. Merge Chapters 1-3 (Word export) + Chapters 4-5
    writer = PdfWriter()
    
    reader_ch1_3 = PdfReader(ch1_3_pdf_path)
    print(f"Loading Word-exported Chapters 1-3 ({len(reader_ch1_3.pages)} pages)...")
    for page in reader_ch1_3.pages:
        writer.add_page(page)
        
    reader_ch4_5 = PdfReader(ch4_5_pdf_path)
    print(f"Loading Chapters 4-5 ({len(reader_ch4_5.pages)} pages)...")
    for page in reader_ch4_5.pages:
        writer.add_page(page)
        
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
        
    # 4. Stamp centered page numbers across all pages
    add_page_number_overlay(output_pdf_path)
    
    print(f"\n========================================================")
    print(f"SUCCESS: Complete Thesis PDF compiled from Word DOCX!")
    print(f"Final Document: {output_pdf_path}")
    print(f"Total Pages: {len(writer.pages)}")
    print(f"========================================================")

if __name__ == '__main__':
    compile_complete_thesis_from_docx()
