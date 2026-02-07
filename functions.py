'''
File Types:
Documents => ['.doc', '.docx', '.pdf', '.txt']
Image => ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
Audio => ['.mp3', '.wav', '.aac', '.flac', '.ogg']
Video => ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
Compressed => ['.zip', '.rar', '.tar', '.gz', '.7z']
'''

# Decompression of files logic
# Imports
import gzip, shutil, patoolib, os, warnings

# Function to decompress files and save the output
def decompress_file(input_file_type, input_file, output_folder):
    # Check if the input file type is supported for decompression
    if input_file_type not in ['.zip', '.rar', '.tar', '.gz', '.7z']:
        raise ValueError("Unsupported file type for decompression.")
    # Check for types and decompress with the library that supports it
    elif input_file_type in ['.zip','.rar', '.tar', '.7z']:
        shutil.unpack_archive(input_file, output_folder)
    elif input_file_type == '.rar':
        patoolib.extract_archive(input_file, outdir=output_folder)
    else: #input_file_type as '.gz'
        with gzip.open(input_file, 'rb') as f_in:
            with open(output_folder, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # Print a message indicating successful decompression
    print(f"File decompressed successfully to {output_folder}")

# Imports for all conversion functions
# Documents related imports
from docx import Document as DocxDocument
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
# Image related imports
from PIL import Image
# Audio related imports
import ffmpeg
from pydub import AudioSegment
# Video related imports
# Import of ffmpeg done above

# Documents conversion logic
def convert_document(input_file, input_file_type, output_file_type, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Generate output file path
    output_path = output_folder+output_file_type
    
    # DOC/DOCX to other formats
    if input_file_type in ['.doc', '.docx']:
        if output_file_type == '.txt':
            docx_to_txt(input_file, output_path)
        elif output_file_type == '.pdf':
            docx_to_pdf(input_file, output_path)
        else:
            raise ValueError(f"Unsupported output file type '{output_file_type}' for document conversion.")
    
    # PDF to other formats
    elif input_file_type == '.pdf':
        if output_file_type in ['.doc', '.docx']:
            pdf_to_docx(input_file, output_path)
        elif output_file_type == '.txt':
            pdf_to_txt(input_file, output_path)
        else:
            raise ValueError(f"Unsupported output file type '{output_file_type}' for PDF conversion.")
    
    # TXT to other formats
    elif input_file_type == '.txt':
        if output_file_type in ['.doc', '.docx']:
            txt_to_docx(input_file, output_path)
        elif output_file_type == '.pdf':
            txt_to_pdf(input_file, output_path)
        else:
            raise ValueError(f"Unsupported output file type '{output_file_type}' for text conversion.")
    
    else:
        raise ValueError(f"Unsupported input file type '{input_file_type}' for document conversion.")
    
    return output_path

def docx_to_txt(input_file, output_path):
    """Convert DOCX to plain text"""
    try:
        doc = DocxDocument(input_file)
        text_content = []
        for paragraph in doc.paragraphs:
            text_content.append(paragraph.text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_content))
    except Exception as e:
        raise Exception(f"Error converting DOCX to TXT: {str(e)}")

def docx_to_pdf(input_file, output_path):
    """Convert DOCX to PDF using reportlab (basic conversion)"""
    warnings.warn("DOCX to PDF conversion is basic. For complex formatting, consider using libreoffice/unoconv or python-docx2pdf", UserWarning)
    
    try:
        doc = DocxDocument(input_file)
        c = canvas.Canvas(output_path, pagesize=letter)
        
        y_position = 750  # Start position from top
        line_height = 14
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Skip empty paragraphs
                # Simple text wrapping (basic implementation)
                lines = wrap_text(paragraph.text, 80)
                for line in lines:
                    if y_position < 50:  # New page if near bottom
                        c.showPage()
                        y_position = 750
                    c.drawString(50, y_position, line)
                    y_position -= line_height
        
        c.save()
    except Exception as e:
        raise Exception(f"Error converting DOCX to PDF: {str(e)}")

def pdf_to_txt(input_file, output_path):
    """Convert PDF to plain text"""
    try:
        with open(input_file, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text_content = []
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content.append(page.extract_text())
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(text_content))
    except Exception as e:
        raise Exception(f"Error converting PDF to TXT: {str(e)}")

def pdf_to_docx(input_file, output_path):
    """Convert PDF to DOCX (basic conversion - text only)"""
    warnings.warn("PDF to DOCX conversion only extracts text. Formatting and images are not preserved.", UserWarning)
    
    try:
        # Extract text from PDF
        with open(input_file, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text_content = []
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content.append(page.extract_text())
        
        # Create DOCX with extracted text
        doc = DocxDocument()
        
        for page_text in text_content:
            if page_text.strip():
                doc.add_paragraph(page_text)
        
        doc.save(output_path)
    except Exception as e:
        raise Exception(f"Error converting PDF to DOCX: {str(e)}")

def txt_to_docx(input_file, output_path):
    """Convert TXT to DOCX"""
    try:
        with open(input_file, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read()
        
        doc = DocxDocument()
        doc.add_paragraph(content)
        doc.save(output_path)
    except Exception as e:
        raise Exception(f"Error converting TXT to DOCX: {str(e)}")

def txt_to_pdf(input_file, output_path):
    """Convert TXT to PDF"""
    try:
        with open(input_file, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read()
        
        c = canvas.Canvas(output_path, pagesize=letter)
        
        y_position = 750  # Start position from top
        line_height = 14
        
        # Simple text wrapping
        lines = wrap_text(content, 80)
        
        for line in lines:
            if y_position < 50:  # New page if near bottom
                c.showPage()
                y_position = 750
            c.drawString(50, y_position, line)
            y_position -= line_height
        
        c.save()
    except Exception as e:
        raise Exception(f"Error converting TXT to PDF: {str(e)}")

def wrap_text(text, max_line_length):
    """Simple text wrapping function"""
    lines = []
    words = text.split()
    
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_line_length:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Image conversion logic
def convert_image(input_file, output_file_type, output_folder):    
    # Create output path with same name, new extension
    output_file = output_folder+output_file_type
    
    # Convert image using PIL
    try:
        # Open the image
        with Image.open(input_file) as img:
            # Convert RGBA to RGB for JPEG (JPEG doesn't support transparency)
            if output_file_type.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                else:  # LA mode
                    background.paste(img, mask=img.split()[0])
                img = background
            
            # Save with explicit format (strip the dot from extension)
            img.save(output_file, format=output_file_type[1:].upper())
    
    except Exception as e:
        print(f"Error converting image {input_file}: {str(e)}")

# Audio conversion logic
def convert_audio(input_file, input_file_type, output_file_type, output_folder):
    # Create output path with same name, new extension
    output_file = output_folder+output_file_type
    
    # Convert audio (strip the dot from format)
    audio = AudioSegment.from_file(input_file, format=input_file_type[1:].lower())
    audio.export(output_file, format=output_file_type[1:].lower())
    
    print(f"Converted: {os.path.basename(input_file)} -> {os.path.basename(output_file)}")
    return output_file

# Video conversion logic  
def convert_video(input_file, output_file_type, output_folder):    
    # Create output path with same name, new extension
    output_file = output_folder+output_file_type
    
    # Convert video using ffmpeg
    try:
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        print(f"Converted: {os.path.basename(input_file)} -> {os.path.basename(output_file)}")
        return output_file
    except ffmpeg.Error as e:
        print(f"Error converting video: {e.stderr.decode()}")
        return None