import os
import re
import sys
import subprocess
import tempfile
import shutil

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

def _find_tool(name):
    """Find a tool by searching PATH first, then common installation directories.
    Returns the full path to the tool or None if not found.
    Designed to be portable across different systems.
    """
    # First try PATH
    result = shutil.which(name)
    if result:
        return result
    
    # Common Windows installation directories to search
    search_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\ProgramData",
        os.environ.get("LOCALAPPDIR", ""),
        os.environ.get("PROGRAMFILES", ""),
        os.environ.get("PROGRAMFILES(X86)", ""),
        os.environ.get("PROGRAMW6432", ""),
    ]
    
    # Filter out empty entries
    search_dirs = [d for d in search_dirs if d and os.path.isdir(d)]
    
    # Tool-specific search patterns
    tool_patterns = {
        "tesseract": [
            r"Tesseract-OCR\tesseract.exe",
        ],
        "pdftoppm": [
            r"poppler\Library\bin\pdftoppm.exe",
            r"poppler\bin\pdftoppm.exe",
            r"poppler-*/bin\pdftoppm.exe",
            r"Poppler\Library\bin\pdftoppm.exe",
            r"Poppler\bin\pdftoppm.exe",
        ],
        "pdftocairo": [
            r"poppler\Library\bin\pdftocairo.exe",
            r"poppler\bin\pdftocairo.exe",
            r"poppler-*/bin\pdftocairo.exe",
            r"Poppler\Library\bin\pdftocairo.exe",
            r"Poppler\bin\pdftocairo.exe",
        ],
    }
    
    patterns = tool_patterns.get(name, [f"{name}.exe" if os.name == 'nt' else name])
    
    for search_dir in search_dirs:
        for pattern in patterns:
            # Handle wildcard patterns like poppler-*
            if '*' in pattern:
                # Get the base directory and wildcard part
                base_subdir = pattern.split('/')[0] if '/' in pattern else pattern
                full_search = os.path.join(search_dir, base_subdir)
                if os.path.isdir(full_search):
                    for item in os.listdir(full_search):
                        candidate = os.path.join(search_dir, item, *pattern.split('/')[1:])
                        if os.path.exists(candidate):
                            return candidate
            else:
                candidate = os.path.join(search_dir, pattern)
                if os.path.exists(candidate):
                    return candidate
    
    return None

def get_tesseract_data_dir(tesseract_path):
    """Find the tessdata directory for a given tesseract installation.
    Returns the path to the tessdata directory or None.
    """
    tesseract_dir = os.path.dirname(tesseract_path)
    tessdata = os.path.join(tesseract_dir, "tessdata")
    if os.path.isdir(tessdata) and os.path.exists(os.path.join(tessdata, "eng.traineddata")):
        return tessdata
    
    # Also search parent directories
    parent = os.path.dirname(tesseract_dir)
    tessdata = os.path.join(parent, "tessdata")
    if os.path.isdir(tessdata) and os.path.exists(os.path.join(tessdata, "eng.traineddata")):
        return tessdata
    
    return None

def set_tesseract_env(tesseract_path):
    """Set TESSDATA_PREFIX environment variable for tesseract.
    Returns True if successful, False otherwise.
    """
    tessdata_dir = get_tesseract_data_dir(tesseract_path)
    if tessdata_dir:
        os.environ["TESSDATA_PREFIX"] = tessdata_dir
        return True
    print("[!] Warning: Could not find tessdata directory for tesseract")
    return False

def ocr_image(file_path):
    """OCR on an image file using tesseract, with pre-conversion to 8-bit RGB to avoid Tesseract/Leptonica issues."""
    tesseract_path = _find_tool("tesseract")
    if tesseract_path is None:
        print("[!] tesseract not found in PATH")
        return None
    
    magick_path = shutil.which("magick")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        converted_img_path = os.path.join(tmpdir, "converted_image.png")
        conversion_success = False

        # Try Pillow first
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                rgb_img = img.convert("RGB")
                rgb_img.save(converted_img_path, "PNG")
            conversion_success = True
        except Exception as e:
            print(f"[*] Pillow conversion failed for {file_path}, trying ImageMagick: {e}")
            
            # Fallback to ImageMagick
            if magick_path:
                try:
                    result = subprocess.run(
                        [magick_path, file_path, converted_img_path],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    conversion_success = True
                except subprocess.CalledProcessError as err:
                    print(f"[!] ImageMagick conversion failed for {file_path}: {err.stderr}")
            else:
                print("[!] ImageMagick (magick) not found in PATH. Cannot fallback.")

        if not conversion_success:
            print(f"[!] Failed to convert image {file_path} for OCR using both Pillow and ImageMagick.")
            return None

        base_path = os.path.join(tmpdir, "ocr_output")
        result = subprocess.run(
            [tesseract_path, converted_img_path, base_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return None
        txt_path = base_path + ".txt"
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
    return None


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
                    print(f"[*] PDF '{filename}' has no text layer. Attempting OCR...")
                    try:
                        pdftoppm_path = _find_tool("pdftoppm")
                        if pdftoppm_path is None:
                            print("[!] pdftoppm not found in PATH. Install poppler for PDF OCR support.")
                            return False

                        with tempfile.TemporaryDirectory() as tmpdir:
                            prefix = os.path.join(tmpdir, "page")
                            subprocess.run(
                                [pdftoppm_path, "-png", file_path, prefix],
                                check=True,
                                capture_output=True,
                                text=True
                            )
                            
                            # Get all png files and sort them numerically by the page number in filename
                            image_files = []
                            for f in os.listdir(tmpdir):
                                match = re.search(r'page-(\d+)\.png$', f)
                                if match:
                                    image_files.append((int(match.group(1)), f))
                            
                            image_files.sort()
                            
                            ocr_contents = []
                            for _, img_name in image_files:
                                img_path = os.path.join(tmpdir, img_name)
                                ocr_text = ocr_image(img_path)
                                ocr_contents.append(ocr_text if ocr_text else "")
                            
                            content = "\n".join(ocr_contents).strip()
                            
                            if not content:
                                print(f"[!] OCR failed to extract text from {filename}")
                                return False
                            else:
                                print(f"[+] OCR successful for {filename}")
                    except (subprocess.CalledProcessError, FileNotFoundError, Exception) as e:
                        print(f"[-] OCR failed for {filename}: {e}")
                        return False
            except ImportError:
                print(f"[-] Missing 'pypdf'. Skipping: {filename}")
                return False

        elif ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".tif", ".webp"]:
            ocr_text = ocr_image(file_path)
            if ocr_text:
                content = ocr_text
                print(f"[+] OCR successful for {filename}")
            else:
                print(f"[!] OCR failed to extract text from {filename}")
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

    # Set up tesseract environment before processing
    tesseract_path = _find_tool("tesseract")
    if tesseract_path:
        print(f"[*] Found tesseract: {tesseract_path}")
        if set_tesseract_env(tesseract_path):
            print(f"[*] TESSDATA_PREFIX set for tesseract")
    else:
        print("[!] Warning: tesseract not found. PDF/image OCR will not work.")

    pdftoppm_path = _find_tool("pdftoppm")
    if pdftoppm_path:
        print(f"[*] Found pdftoppm: {pdftoppm_path}")
    else:
        print("[!] Warning: pdftoppm not found. PDF OCR will not work.")

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

