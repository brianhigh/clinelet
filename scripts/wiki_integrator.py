import os
import re

RAW_DIR = "raw"
SPACE_DIR = "wiki"
MANIFEST_PATH = "processed_files.txt"

def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        return set()
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()

def save_to_manifest(filename):
    with open(MANIFEST_PATH, 'a', encoding='utf-8') as f:
        f.write(filename + "\n")

def to_snake_case(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[^a-zA-Z0-9]+', '_', name)
    return name.strip('_').lower() + ".md"

def process_file(file_path, filename):
    new_filename = to_snake_case(filename)
    target_path = os.path.join(SPACE_DIR, new_filename)
    
    print(f"Processing: {filename} -> {new_filename}")
    
    ext = os.path.splitext(filename)[1].lower()
    content = ""
    
    try:
        if ext in [".md", ".txt"]:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        elif ext == ".html":
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            content = re.sub(r'<[^>]+>', '', content)
        elif ext == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                content = text.strip()
                if not content:
                    content = "[Warning: PDF parsed but no text was extracted. The PDF might be image-base.]"
            except ImportError:
                content = "[Error: pypdf library not found. Please install it using 'pip install pypdf']."
            except Exception as e:
                content = f"[Error: Failed to extract text from PDF: {e}]"
        elif ext == ".docx":
            try:
                import docx
                doc = docx.Document(file_path)
                text = [para.text for para in doc.paragraphs]
                content = "\n".join(text).strip()
            except ImportError:
                content = "[Error: python-docx library not found. Please install it using 'pip install python-docx']."
            except Exception as e:
                content = f"[Error: Failed to extract text from DOCX: {e}]"
        elif ext == ".xlsx":
            try:
                import openpyxl
                wb = openpyxl.load_workbook(file_path, data_only=True)
                text = []
                for sheet in wb.worksheets:
                    text.append(f"--- Sheet: {sheet.title} ---")
                    for row in sheet.iter_rows(values_only=True):
                        row_text = " ".join(str(cell) for cell in row if cell is not None)
                        if row_text.strip():
                            text.append(row_text)
                content = "\n".join(text).strip()
            except ImportError:
                content = "[Error: openpyxl library not found. Please install it using 'pip install openpyxl']."
            except Exception as e:
                content = f"[Error: Failed to extract text from XLSX: {e}]"
        elif ext == ".pptx":
            try:
                import pptx
                prs = pptx.Presentation(file_path)
                text = []
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text") and shape.text:
                            text.append(shape.text.strip())
                content = "\n".join(text).strip()
            except ImportError:
                content = "[Error: python-pptx library not found. Please install it using 'pip install python-pptx']."
            except Exception as e:
                content = f"[Error: Failed to extract text from PPTX: {e}]"
        else:
            content = f"Unsupported format: {ext}. Please convert to text-based format."

        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully integrated to {target_path}")
        return True
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return False

def main():
    if not os.path.exists(RAW_DIR):
        print(f"Error: {RAW_DIR} does not exist.")
        return
    
    if not os.path.exists(SPACE_DIR):
        os.makedirs(SPACE_DIR)

    processed_files = load_manifest()
    
    for filename in os.listdir(RAW_DIR):
        if filename in processed_files or filename.startswith('.'):
            continue
            
        file_path = os.path.join(RAW_DIR, filename)
        
        if os.path.isfile(file_path):
            if process_file(file_path, filename):
                save_to_manifest(filename)

if __name__ == "__main__":
    main()
