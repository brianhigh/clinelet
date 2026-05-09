import os
import re
import sys

# Constants
RAW_DIR = "raw"
SPACE_DIR = "wiki"
STATE_DIR = ".clinelet"
MANIFEST_PATH = os.path.join(STATE_DIR, "processed_files.txt")

def load_manifest():
    """Loads processed filenames and ensures state directory exists."""
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)
        
    if not os.path.exists(MANIFEST_PATH):
        # Create the file if it doesn't exist
        open(MANIFEST_PATH, 'a').close()
        return set()

    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"Error reading manifest: {e}")
        return set()

def save_to_manifest(filename):
    """Appends a filename to the manifest file."""
    try:
        if not os.path.exists(STATE_DIR):
            os.makedirs(STATE_DIR)
            
        with open(MANIFEST_PATH, 'a', encoding='utf-8') as f:
            f.write(filename + "\n")
    except Exception as e:
        print(f"Warning: Could not update manifest: {e}")

def to_snake_case(filename):
    """Converts filename to snake_case and ensures it ends in .md"""
    name = os.path.splitext(filename)[0]
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
    """Extracts text and saves to markdown. Returns False if skipped/failed."""
    new_filename = to_snake_case(filename)
    target_path = get_unique_path(SPACE_DIR, new_filename)
    
    ext = os.path.splitext(filename)[1].lower()
    content = ""
    
    try:
        if ext in [".md", ".txt"]:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

        elif ext == ".html":
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                html = f.read()
            content = re.sub(r'<[^>]+>', '', html)

        elif ext == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(file_path)
                content = "\n".join([page.extract_text() or "" for page in reader.pages]).strip()
                if not content:
                    print(f"[!] Skipped: {filename} (PDF has no text layer/is image-based)")
                    return False
            except ImportError:
                print(f"[-] Missing 'pypdf'. Skipping: {filename}")
                return False

        elif ext == ".docx":
            try:
                import docx
                doc = docx.Document(file_path)
                content = "\n".join([p.text for p in doc.paragraphs]).strip()
            except ImportError:
                print(f"[-] Missing 'python-docx'. Skipping: {filename}")
                return False

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
                print(f"[-] Missing 'openpyxl'. Skipping: {filename}")
                return False

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
                print(f"[-] Missing 'python-pptx'. Skipping: {filename}")
                return False

        else:
            print(f"[!] Unsupported format: {ext} ({filename})")
            return False

        # Final check: If content is still empty after processing
        if not content.strip():
            print(f"[!] Skipped: {filename} (No content extracted)")
            return False

        # Final write to markdown
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True

    except Exception as e:
        print(f"[ERROR] Critical error processing {filename}: {e}")
        return False

def main():
    # Verify source
    if not os.path.exists(RAW_DIR):
        print(f"Error: Source directory '{RAW_DIR}' not found.")
        return
    
    # Ensure destination directories exist
    for d in [SPACE_DIR, STATE_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

    processed_files = load_manifest()
    
    to_process = [f for f in os.listdir(RAW_DIR) 
                  if f not in processed_files and not f.startswith('.')]

    if not to_process:
        print("No new files to process.")
        return

    print(f"Found {len(to_process)} candidate files...")

    for filename in to_process:
        file_path = os.path.join(RAW_DIR, filename)
        
        if os.path.isfile(file_path):
            if process_file(file_path, filename):
                save_to_manifest(filename)
                print(f"[SUCCESS] Integrated: {filename}")

if __name__ == "__main__":
    main()

