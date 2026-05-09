import os
import re
import sys

# Constants
RAW_DIR = "raw"
SPACE_DIR = "wiki"
# Fixed the path joining bug (removed os.sep)
MANIFEST_PATH = os.path.join(RAW_DIR, ".processed_files.txt")

def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        return set()
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()

def save_to_manifest(filename):
    try:
        with open(MANIFEST_PATH, 'a', encoding='utf-8') as f:
            f.write(filename + "\n")
    except Exception as e:
        print(f"Warning: Could not update manifest: {e}")

def to_snake_case(filename):
    """Converts filename to snake_case and ensures it ends in .md"""
    name = os.path.splitext(filename)[0]
    # Replace non-alphanumeric with underscore
    name = re.sub(r'[^a-zA-Z0-9]+', '_', name)
    return name.strip('_').lower() + ".md"

def get_unique_path(target_dir, filename):
    """Prevents overwriting by appending a counter if the file exists."""
    base, ext = os.path.splitext(filename)
    counter = 1
    target_path = os.path.join(target_dir, filename)
    
    while os.path.exists(target_path):
        target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
        counter += 1
    return target_path

def process_file(file_path, filename):
    new_filename = to_snake_case(filename)
    target_path = get_unique_path(SPACE_DIR, new_filename)
    
    print(f"Processing: {filename} -> {os.path.basename(target_path)}")
    
    ext = os.path.splitext(filename)[1].lower()
    content = ""
    
    try:
        if ext in [".md", ".txt"]:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

        elif ext == ".html":
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                html = f.read()
            # Simple regex strip; note: can be messy with scripts/styles
            content = re.sub(r'<[^>]+>', '', html)

        elif ext == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(file_path)
                content = "\n".join([page.extract_text() or "" for page in reader.pages]).strip()
                if not content:
                    content = "[Warning: PDF might be image-based. No text extracted.]"
            except ImportError:
                content = "[Error: pypdf library not found. Run 'pip install pypdf']"

        elif ext == ".docx":
            try:
                import docx
                doc = docx.Document(file_path)
                content = "\n".join([p.text for p in doc.paragraphs]).strip()
            except ImportError:
                content = "[Error: python-docx not found. Run 'pip install python-docx']"

        elif ext == ".xlsx":
            try:
                import openpyxl
                wb = openpyxl.load_workbook(file_path, data_only=True)
                lines = []
                for sheet in wb.worksheets:
                    lines.append(f"--- Sheet: {sheet.title} ---")
                    for row in sheet.iter_rows(values_only=True):
                        row_str = " ".join(str(c) for c in row if c is not None).strip()
                        if row_str: lines.append(row_str)
                content = "\n".join(lines)
            except ImportError:
                content = "[Error: openpyxl not found. Run 'pip install openpyxl']"

        elif ext == ".pptx":
            try:
                import pptx
                prs = pptx.Presentation(file_path)
                lines = []
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text") and shape.text.strip():
                            lines.append(shape.text.strip())
                content = "\n".join(lines)
            except ImportError:
                content = "[Error: python-pptx not found. Run 'pip install python-pptx']"

        else:
            content = f"Unsupported format: {ext}"

        # Final write
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True

    except Exception as e:
        print(f"Critical error processing {filename}: {e}")
        return False

def main():
    if not os.path.exists(RAW_DIR):
        print(f"Error: Source directory '{RAW_DIR}' not found.")
        return
    
    if not os.path.exists(SPACE_DIR):
        os.makedirs(SPACE_DIR)

    processed_files = load_manifest()
    
    # Filter out manifest itself and hidden files
    to_process = [f for f in os.listdir(RAW_DIR) 
                  if f not in processed_files and not f.startswith('.')]

    if not to_process:
        print("No new files to process.")
        return

    for filename in to_process:
        file_path = os.path.join(RAW_DIR, filename)
        
        if os.path.isfile(file_path):
            if process_file(file_path, filename):
                save_to_manifest(filename)
                print(f"Successfully integrated {filename}")

if __name__ == "__main__":
    main()
