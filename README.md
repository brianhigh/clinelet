# clinelet
This repository provides [Cline Rules](https://docs.cline.bot/customization/cline-rules) files to implement a Karpathy-style [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with the [VS Code Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) and [SilverBullet](https://silverbullet.md/) wiki [app](https://silverbullet.plus/).

## Files
- `.clinerules/personal_agent.md`: Provides work context and productivity methodology (based on Brian Tracy's [Eat that Frog!](https://www.briantracy.com/blog/time-management/the-truth-about-frogs/))
- `.clinerules/project_guidelines.md`: Provides LLM Wiki implementation guidelines (based on Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f))
- `README.md`: This file
- `scripts/wiki_integrator.py`

## Setup:
1. Install the [SilverBullet+ app](https://silverbullet.plus/).
2. Install [Visual Studio Code](https://code.visualstudio.com/download) and the [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev).
3. If your system does not have Python installed, install it. [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) is usally a good choice for that.
4. Configure the Cline extension for accessing your AI model (LLM) of choice. Make sure the model supports tool use.
5. Create a `workspace` folder for your wiki and place the `.clinerules` and `scripts` folders in it.
6. Edit the two rules files to suit your needs, or use them as-is.
7. In the `workspace` folder, create two more folders: `raw` and `wiki`.
8. Open the SilverBullet+ app and open your `workspace\wiki` folder with it.

## Usage:
1. Place some document files (.txt, .md, .html, .pdf., .docx, .xlsx., or .pptx) in the `raw` folder and ask Cline to process them using `scripts/wiki_integrator.py`.
2. If Cline says it needs you to install some dependencies like Python or Python models, consider doing so, to support running the script.
3. Cline should extract information from the `raw` files and create wiki pages in the `wiki/` folder, reate some links between them, and log what it does in `wiki/log.md`.
4. View the wiki pages in the SilverBullet+ app to confirm you are seeing the results you expect. It should look for an `index.md`, if present, and open that first.
5. If you remove a wiki page and ask Cline to "lint" the wiki, it should fix broken links.
6. If Cline is having trouble extracting text using `scripts/wiki_integrator.py`, ask Cline to improve the script.
