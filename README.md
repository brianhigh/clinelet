# 🐷 clinelet

`clinelet` provides a set of specialized [Cline Rules](https://docs.cline.bot/customization/cline-claude-rules) designed to transform the [VS Code Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) into a powerful, automated "Living LLM Wiki" using [SilverBullet](https://silverbullet.md/).

Following the organizational principles of Andrej Karpathy, this setup enables you to ingest raw documents and transform them into a dense, interlinked, and searchable knowledge base.

[![Watch a video on LLM Wikis](https://img.youtube.com/vi/iXd0t60YmMw/0.jpg)](https://www.youtube.com/watch?v=iXd0t60YmMw)

## 🚀 Key Features

- **Automated Ingestion**: Use `scripts/wiki_integrator.py` to process various file formats (.txt, .md, .pdf, .docx, etc.) and generate structured wiki pages.
- **Knowledge Management**: Implements a "Living LLM Wiki" approach with interlinked pages for easy discovery.
- **Productivity Focused**: Integrates Brian Tracy's [Eat That Frog!](https://www.briantracy.com/blog/time-management/the-truth-about-frogs/) methodology for task prioritization.
- **Automated Maintenance**: Includes capabilities for "linting" the wiki to identify orphaned pages, broken links, and missing concepts.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- [Git](https://git-scm.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) for VS Code
- [SilverBullet+ App](https://silverbullet.plus/)
- [Python 3.x](https://www.python.org/) (Miniconda is recommended)

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/brianhigh/clinelet.git
   cd clinelet
   ```

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

1. **Configure Cline:** Set up your preferred LLM in the Cline extension. Ensure the model supports **tool use** (e.g., Claude 3.5 Sonnet).
2. **Customize Rules (Optional):** Review and edit `.clinerules/personal_agent.md` and `.clinerules/project_guidelines.md` to better align with your specific workflow or professional needs.
3. **Initialize Wiki:** Opening your empty `wiki/` folder with SilverBullet will automatically create the `index.md` file.

## 📖 Usage

### 1. Ingesting Data
Place your source documents (`.txt`, `.md`, `.pdf`, `.docx`, `.xlsx`, `.pptx`, etc.) into the `raw/` folder. Then, instruct Cline to run the integration script:

> "Cline, please use `scripts/wiki_integrator.py` to process the documents in my `raw/` folder."

Cline will:
- Extract text from your files.
- Create new, formatted Markdown pages in `wiki/`.
- Establish links between related concepts.
- Log all operations in `wiki/log.md`.

### 2. Managing the Wiki
- **Reviewing Content:** Open the `wiki/` folder in the [SilverBullet+ app] to browse your interlinked knowledge base.
- **Auditing:** Ask Cline to "lint the wiki" to find broken links, orphans, or formatting errors.
- **Iterating:** If the extraction isn't perfect, simply ask Cline to improve the `wiki_integrator.py` script.

## 📄 License

[MIT License](LICENSE)
