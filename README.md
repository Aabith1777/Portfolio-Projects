# PromptVault — Your Personal AI Prompt Library

A premium, production-quality offline-first desktop-style web application to browse, search, organize, bookmark, and copy high-performance AI prompt templates. Designed for freelancers, developer professionals, and managers who want an elegant interface that runs completely offline with no network dependencies.

## Key Features

- **🚀 100% Offline Compatible**: Works instantly by double-clicking `index.html` via the `file://` protocol. No complex server installations or Node setups needed.
- **✨ Premium Dark & Light Aesthetics**: Sleek modern interface inspired by Notion, Linear, and Raycast. Glassmorphism styling, clean animations, and responsive panels.
- **🔍 Advanced Search Engine**: Search through titles, categories, tags, and template content instantly with relevance scoring and highlight matching.
- **⚡ Command Palette (`Ctrl + K`)**: Keyboard-navigable quick command hub to jump between prompts, toggle theme, export data, or open settings.
- **📁 Local Caching & Sync**: Favorites, pinned items, custom ratings, recently viewed lists, and preferences are saved locally in the browser.
- **📤 Export & Import Backups**: Download your configurations and favorites as a single JSON file and restore it on any device.
- **📈 Stats & Daily Widget**: Interactive real-time metrics dashboard and rotation of expert prompt tips.
- **📄 Print / Export PDF**: Built-in stylesheet templates to print clean prompt sheets directly using standard browser print configurations.

## Project Structure

```text
PromptVault/
│
├── index.html            # Main markup shell (links script sequentially to bypass CORS blocks)
│
├── css/
│   └── style.css         # Design tokens, variables, typography, layouts & print targets
│
├── js/
│   ├── app.js            # Orchestration engine, filters, state triggers & shortcuts
│   ├── ui.js             # SVG rendering dictionary, DOM builders & modal toggles
│   ├── search.js         # Client-side weighted keyword matching & regex text highlighting
│   ├── favorites.js      # Bookmark state manager
│   ├── theme.js          # Dark/Light system config
│   └── storage.js        # LocalStorage persistence & JSON importer/exporter
│
├── data/
│   ├── categories.json   # Base category metadata definitions
│   ├── categories.js     # Global categories variable export (Offline fallback)
│   ├── prompts.json      # Master list of 100 premium prompt templates
│   └── prompts.js        # Global prompts variable export (Offline fallback)
│
├── assets/
│   ├── logo.svg          # Brand vector logo
│   └── icons/            # SVG vector assets
│
├── README.md             # Product documentation guide
└── LICENSE.txt           # MIT licensing terms
```

## Getting Started

1. Download the `PromptVault` project folder.
2. Double-click [index.html](file:///c:/Users/aabit/.gemini/antigravity-ide/scratch/PromptVault/index.html) to open the application in any modern web browser (Chrome, Edge, Firefox, Safari).
3. (Optional) If you are running a local development server, you can host the files using `npm install -g http-server && http-server .` and visit the server port.

## Keyboard Hotkeys

| Shortcut | Action |
| --- | --- |
| `Ctrl + F` | Focus and select search bar inputs |
| `Ctrl + K` | Open/Close command palette |
| `Ctrl + D` | Toggle between Light and Dark themes |
| `ArrowUp` | Move selection to previous prompt in the listing |
| `ArrowDown` | Move selection to next prompt in the listing |
| `Esc` | Clear search query, exit focused inputs, or close modals |

## Customization & Adding Prompts

To add, edit, or customize prompt templates:

1. Open [prompts.json](file:///c:/Users/aabit/.gemini/antigravity-ide/scratch/PromptVault/data/prompts.json) inside your code editor and append your new object. Each prompt has this format:
   ```json
   {
     "id": "uniq-id",
     "title": "Clear Prompt Name",
     "category": "resume",
     "difficulty": "Intermediate",
     "description": "Short summary explaining target application.",
     "tags": ["Tag1", "Tag2"],
     "prompt": "Write your template content here with [PLACEHOLDERS] in brackets.",
     "exampleInput": "Sample parameters variables data.",
     "exampleOutput": "What the AI response looks like.",
     "tips": ["Tip list", "Another advice"],
     "createdDate": "2026-07-20"
   }
   ```
2. Mirror the changes in [prompts.js](file:///c:/Users/aabit/.gemini/antigravity-ide/scratch/PromptVault/data/prompts.js) by appending the object to the `window.PROMPTS_DATA` array to guarantee offline support on `file://`.
3. (Alternatively) If you have Python installed, you can modify the generator script [generate_prompts.py](file:///c:/Users/aabit/.gemini/antigravity-ide/scratch/PromptVault/scratch/generate_prompts.py) inside the `scratch/` folder, run `python generate_prompts.py`, and it will automatically synchronize both `.json` and `.js` files for you.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
