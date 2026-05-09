# 🐸 clinelet

`clinelet` provides a set of specialized [Cline Rules](https://docs.cline.bot/customization/cline-claude-rules) designed to transform the [VS Code Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) into a powerful, automated "Living LLM Wiki" curator agent. The wiki it builds will be optimized for browsing with the [SilverBullet](https://silverbullet.md/) wiki app.

Following the organizational principles of Andrej Karpathy, this setup enables you to ingest raw documents and transform them into a dense, interlinked, and searchable knowledge base.

This short YouTube video introduces the concept and demostrates an implementation with a different toolset (Clause Code and Obsidian wiki):

[![Watch a video on LLM Wikis](https://img.youtube.com/vi/iXd0t60YmMw/0.jpg)](https://www.youtube.com/watch?v=iXd0t60YmMw)

So why use VS Code, Cline, and SilverBullet? VS Code with Cline gives you the ability to use other LLMs, especially locally-hosted models via, e.g., Ollama or LM Studio. You can easily restrict Cline's actions (read/write workspace files, only execute safe commands, no web or MCP access, etc.). SilverBullet supports Lua scripting and and is open source. However, you can also use [Obsidian](https://obsidian.md) with this setup if you want to. And if you prefer the open source version of VS Code, you can use [VSCodium](https://vscodium.com).

## 🚀 Key Features

- **Automated Ingestion**: Use `scripts/wiki_integrator.py` to process various file formats (.txt, .md, .pdf, .docx, etc.) and generate structured wiki pages.
- **Knowledge Management**: Implements a "Living LLM Wiki" approach with interlinked pages for easy discovery.
- **Productivity Focused**: Integrates Brian Tracy's [Eat That Frog!](https://www.briantracy.com/blog/time-management/the-truth-about-frogs/) methodology for task prioritization.
- **Automated Maintenance**: Includes capabilities for "linting" the wiki to identify orphaned pages, broken links, and missing concepts.

**Note:** Currently the included text extraction script does not support OCR for image-based content (scanned PDFs, etc.), but if you need that, ask the agent (Cline) to build that for you.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- [Git](https://git-scm.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) for VS Code
- [SilverBullet+ App](https://silverbullet.plus/)
- [Python 3.x](https://www.python.org/) (Miniconda is recommended)

To support processing non-text filetypes such as pdf, docx, xlsx, and pptx, you will also need some additional Python packages, which you can install from your Terminal with:

```bash
pip install pypdf python-docx openpyxl python-pptx
```

Or you can let the agent (Cline) do this for you if it realizes they are missing. Cline should do this automatically, prompting you for approval.

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brianhigh/clinelet.git
   ```
   This will create a folder `clinelet` which contains the files from this repository.

2. **Set up your workspace:**
   Create a new directory for your wiki (e.g., `my_wiki`). Within this directory, you must structure it as follows:
   ```text
   my_wiki/
   ├── .clinerules/        <-- Copy from clinelet/.clinerules/
   ├── scripts/            <-- Copy from clinelet/scripts/
   ├── raw/                <-- Place your source documents here
   └── wiki/               <-- Your generated knowledge base will live here
   ```

3. **Copy core components:**
   Copy the `.clinerules` and `scripts` folders from this repository into your new workspace directory.

## 🛠️ Configuration

1. **Configure Cline:** 
   - Set up your preferred LLM in the Cline extension.
     - Use a context size of at least 64k for local models (the more the better).
     - Ensure the model supports **tool use**
       - A local model like qwen3.5:9b works okay, but use a larger model like gemma4:26b if you can
       - If your model is running too slowly, try a smaller model (e.g., qwen3.5:4b) with a larger context size (e.g., 128k).
   - For Auto-approve, enable: 
     - [x] Read project files
     - [x] Edit project files
     - [x] Execute safe commands 
2. **Customize Rules (Optional):** Review and edit `.clinerules/personal_agent.md` and `.clinerules/project_guidelines.md` to better align with your specific workflow or professional needs.
3. **Initialize Wiki:** 
   - Opening your empty `wiki/` folder with SilverBullet will automatically create the `index.md` file.
   - If this does not create `index.md`, or if it is rather bare, you can copy the one included here into `wiki/`.
   - Copy `eat_that_frog.md` into your `wiki/` folder so Cline will reference that when creating "todo" lists.

## 📖 Usage

### 1. Ingesting Data
Place your source documents (`.txt`, `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, etc.) into the `raw/` folder. Then, in VS Code, open your LLM Wiki project folder, e.g., "my_wiki". Select the Cline extension from the left-side navigation bar. In the Cline chat box, instruct Cline to run the integration script (in Act mode):

> process @/raw with @/scripts/wiki_integrator.py

Or simply:

> process raw

And after processing, if the new pages lack formatting (sections, lists, tables, links, etc.):

> improve the markdown formatting of the new pages, condense long pages, and interlink with other pages

Cline will:
- Extract text from your files.
- Create new, formatted Markdown pages in `wiki/`.
- Establish links between related concepts.
- Log all operations in `wiki/log.md`.

If you wish to discuss the document or how you want it integrated into the wiki, use Plan mode first.

### 2. Managing the Wiki
- **Reviewing Content:** Open the `wiki/` folder in the SilverBullet+ app to browse your interlinked knowledge base.
- **Auditing:** Ask Cline to "lint the wiki" to find broken links, orphans, or formatting errors.
- **Iterating:** If the extraction isn't perfect, simply ask Cline to improve the `wiki_integrator.py` script.

## 📄 License

[MIT License](LICENSE)
