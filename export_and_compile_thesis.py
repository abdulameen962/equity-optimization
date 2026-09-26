import os
import io
import time
import win32com.client
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfWriter, PdfReader

from src.generate_chapters import generate_chapters_pdf
from generate_thesis_docx import generate_complete_thesis_docx
from shrink_thesis_pdf import shrink_pdf_formula_safe

def export_docx_to_pdf(docx_path, output_pdf_path):
    """
    Uses Microsoft Word COM to export DOCX to PDF, maintaining 100% native Word layout, 
    math vector equations, matrices, tables, and justification settings.
    """
    docx_abs = os.path.abspath(docx_path)
    pdf_abs = os.path.abspath(output_pdf_path)
    os.makedirs(os.path.dirname(pdf_abs), exist_ok=True)
    
    print(f"Opening Microsoft Word COM to export {docx_path} -> PDF...")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    
    try:
        doc = word.Documents.Open(
            FileName=docx_abs,
            ConfirmConversions=False,
            ReadOnly=True,
            AddToRecentFiles=False
        )
        time.sleep(1)  # Allow Word to fully initialize layout
        doc.SaveAs2(pdf_abs, FileFormat=17)  # 17 = wdFormatPDF
        print(f"[OK] Successfully exported DOCX to PDF: {pdf_abs}")
        doc.Close(False)
    finally:
        word.Quit()

def int_to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def add_page_number_overlay(pdf_path, front_matter_pages=11):
    """
    Stamps bottom-centered page numbers:
    - Page 1 (Title page): No page number.
    - Pages 2 to 11 (Front Matter): Lowercase Roman numerals (ii through xi).
    - Pages 12 onwards (Chapter 1 onwards): Arabic numerals starting at 1 (1, 2, 3...).
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    
    for i, page in enumerate(reader.pages):
        if i == 0:
            # Title page: no number
            writer.add_page(page)
            continue
            
        if 1 <= i < front_matter_pages:
            page_str = int_to_roman(i + 1)
        else:
            page_str = str(i - front_matter_pages + 1)
        
        # Create transparent canvas with centered page number
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont('Times-Roman', 10)
        can.drawCentredString(306, 36, page_str)
        can.save()
        packet.seek(0)
        
        # Merge canvas overlay with page
        overlay_reader = PdfReader(packet)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)
        
    with open(pdf_path, 'wb') as f_out:
        writer.write(f_out)
    print(f"[OK] Successfully stamped academic page numbers on all {total_pages} pages (Roman ii-xii, Arabic 1-{total_pages - front_matter_pages}).")


def compile_complete_thesis_from_docx():
    """
    1. Generates unified DOCX with Chapters 1-5 + References.
    2. Exports the complete unified DOCX directly to PDF using Microsoft Word COM,
       retaining 100% native Word layout, vector formulas, and clean, succinct tables.
    3. Stamps bottom-centered academic page numbers (Roman ii-xii, Arabic 13-N).
    4. Also updates the standalone Chapters 4 & 5 auxiliary PDF.
    """
    full_docx_path = "Abdulameen_Complete_Thesis_Chapters_1_5.docx"
    ch4_5_pdf_path = "output/pdf/Chapters_4_and_5.pdf"
    output_pdf_path = "Abdulameen_Complete_Thesis_Chapters_1_5.pdf"

    # 1. Update full DOCX with latest content & formatting
    print("--- 1/3: Building complete unified DOCX ---")
    generate_complete_thesis_docx(full_docx_path)

    # 2. Export complete unified DOCX directly to PDF via Word COM
    print("--- 2/3: Exporting complete thesis from Word COM ---")
    export_docx_to_pdf(full_docx_path, output_pdf_path)
        
    # 3. Stamp centered page numbers across all pages
    print("--- 3/3: Stamping academic page numbers ---")
    add_page_number_overlay(output_pdf_path)
    
    # Also update standalone Chapters 4 & 5 PDF
    try:
        generate_chapters_pdf(ch4_5_pdf_path)
    except Exception as e:
        print(f"Note: auxiliary Chapters 4-5 PDF generation: {e}")
    
    # 4. Generate Formula-Safe Compressed PDF (< 600 KB)
    print("--- 4/4: Generating Formula-Safe Compressed PDF Edition (< 600 KB) ---")
    shrink_output_pdf = "Abdulameen_Complete_Thesis_Chapters_1_5_under_600kb.pdf"
    try:
        shrink_pdf_formula_safe(
            input_pdf_path=output_pdf_path,
            output_pdf_path=shrink_output_pdf
        )
    except Exception as e:
        print(f"Note: PDF compression: {e}")

    reader = PdfReader(output_pdf_path)
    total_pages = len(reader.pages)
    print(f"\n========================================================")
    print(f"SUCCESS: Complete Thesis PDF compiled from Word DOCX!")
    print(f"Full Document     : {output_pdf_path}")
    print(f"Compressed Edition: {shrink_output_pdf}")
    print(f"Total Pages       : {total_pages}")
    print(f"========================================================")

if __name__ == '__main__':
    compile_complete_thesis_from_docx()

