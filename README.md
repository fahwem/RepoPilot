<div align="center">

# RepoPilot

**A local, privacy-first AI agent that reads and explains any GitHub repository — 100% offline.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Runs%20on-Ollama-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![smolagents](https://img.shields.io/badge/Framework-smolagents-orange)](https://github.com/huggingface/smolagents)
[![Gradio](https://img.shields.io/badge/UI-Gradio-FF7C00?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[Overview](#overview) • [Features](#features) • [Screenshots](#screenshots) • [Demo Video](#demo-video) • [Getting Started](#getting-started) • [Usage](#usage-example) • [Project Structure](#project-structure) • [Roadmap](#roadmap)

</div>

---

## Overview

**RepoPilot** is an open-source AI agent that analyzes GitHub repositories for you. Give it any public repo URL and it will:

- Inspect the file and folder structure
- Read and reason about the source code
- Explain backend logic in plain language
- Identify the languages, frameworks, and technologies used
- Answer follow-up questions about the codebase, with full conversation memory

Everything runs **locally on your machine** — no code, prompts, or execution logs are ever sent to a third-party cloud API.

### Why I Built This

Navigating large, unfamiliar, or poorly documented repositories takes time. RepoPilot was built to instantly read a codebase, summarize what it does, and answer targeted technical questions — without shipping your code or context off your machine.

---

## Features

| Feature | Description |
|---|---|
| **Repo Analysis** | Point it at any public GitHub URL and get an instant structural + functional breakdown |
| **Conversational Follow-ups** | Ask follow-up questions — RepoPilot remembers the context of the current repo |
| **Fully Local** | Powered by [Ollama](https://ollama.com/) running `qwen2.5-coder:7b` — no API keys, no cloud, no cost |
| **Agentic Reasoning** | Built on Hugging Face's [smolagents](https://github.com/huggingface/smolagents) for tool-calling and step-by-step reasoning |
| **Simple Web UI** | Clean [Gradio](https://www.gradio.app/) interface with real-time reasoning logs |
| **Language & Tech Detection** | Automatically identifies the main languages and frameworks used in a repo |

---

## Screenshots

> Replace the placeholders below with your own screenshots. Drop your image files into `docs/screenshots/` and update the paths to match.

<table>
  <tr>
    <td width="50%" align="center">
      <img src="docs/screenshots/01_interface_overview.png" alt="Screenshot 1 — App interface" width="100%" /><br/>
      <sub><b>1. App interface</b> — the main Gradio dashboard</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/screenshots/02_followup_execution.png" alt="Screenshot 2 — Follow-up question" width="100%" /><br/>
      <sub><b>2. Follow-up reasoning</b> — the agent answering a follow-up question</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="docs/screenshots/03_placeholder.png" alt="Screenshot 3 — Add your image" width="100%" /><br/>
      <sub><b>3. Add screenshot</b> — e.g. repo structure inspection</sub>
    </td>
    <td width="50%" align="center">
      <img src="docs/screenshots/04_placeholder.png" alt="Screenshot 4 — Add your image" width="100%" /><br/>
      <sub><b>4. Add screenshot</b> — e.g. tech-stack detection output</sub>
    </td>
  </tr>
</table>

---

## Demo Video

> Replace the thumbnail and file path with your own recording. Put your video in `docs/demo/` (`.mp4` is best for autoplay support on the web; GitHub will render `.mov` too, but only as a downloadable/clickable link).

<div align="center">

[![Watch the demo](docs/screenshots/video_thumbnail.png)](docs/demo/demo.mp4)

*Click the thumbnail above to watch a full walkthrough: terminal setup, Gradio UI, and live repository analysis.*

</div>

---

##  How It Works

RepoPilot combines a local LLM with lightweight local tooling:

1. **Framework** — Uses Hugging Face's `smolagents` for tool-calling and agentic reasoning.
2. **Local Model** — Runs `qwen2.5-coder:7b` through Ollama, entirely on your own hardware.
3. **Interface** — A Gradio web UI provides an interactive chat experience with visible reasoning steps.
4. **Analysis Engine** — Custom Python utilities inspect the repo's directory structure, count files/folders, and parse source files in real time to feed context to the model.

---

## Getting Started

Follow these steps to get RepoPilot running on your own machine.

### Step 1 — Install Prerequisites

1. Make sure **Python 3.10+** is installed:
   ```bash
   python --version
   ```
2. Install **Ollama** from [ollama.com](https://ollama.com/).
3. Pull the model RepoPilot uses:
   ```bash
   ollama pull qwen2.5-coder:7b
   ```

### Step 2 — Clone the Repository

```bash
git clone https://github.com/fahwem/RepoPilot.git
cd RepoPilot
```

### Step 3 — Create a Virtual Environment (recommended)

```bash
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Make Sure Ollama Is Running

In a separate terminal, start the Ollama service (if it isn't already running in the background):

```bash
ollama serve
```

### Step 6 — Launch RepoPilot

```bash
python app.py
```

Gradio will print a local URL in your terminal, typically:

```
Running on local URL:  http://127.0.0.1:7860
```

Open that link in your browser to start using RepoPilot.

### Step 7 — Analyze a Repository

1. Paste a public GitHub repository URL into the input box.
2. Ask a question, e.g. *"Explain this repo in short"* or *"Which language does it use?"*
3. Read the agent's step-by-step reasoning and final answer.
4. Ask follow-up questions — the conversation context is preserved.

---

## Usage Example

```
Input Repository: https://github.com/fahwem/Audio-filtering---Fourier-Transform
User Query:        "explain to me this repo in short"

Agent Output:
- Detects file structure (README.md, audiofilter_app.m)
- Identifies MATLAB as the main language
- Summarizes the Fourier audio filtering GUI
```

---

## Project Structure

```
RepoPilot/
├── tools/            # Custom tools used by the agent (repo inspection, parsing, etc.)
├── docs/
│   ├── screenshots/   # README images
│   └── demo/          # Demo video
├── Gradio_UI.py       # Gradio web interface logic
├── app.py             # Application entry point
├── agent.json         # Agent configuration
├── prompts.yaml       # System / task prompts for the agent
├── requirements.txt   # Python dependencies
└── README.md
```

---

##  Tech Stack

- **Language:** Python 3.10+
- **Agent Framework:** [smolagents](https://github.com/huggingface/smolagents)
- **Local LLM Runtime:** [Ollama](https://ollama.com/) (`qwen2.5-coder:7b`)
- **UI:** [Gradio](https://www.gradio.app/)
- **Other Dependencies:** `markdownify`, `requests`, `duckduckgo_search`, `pandas`

---

##  Roadmap

- [ ] Support for private repositories (via auth token)
- [ ] Streaming responses in the UI
- [ ] Support for additional local models
- [ ] Exportable analysis reports (Markdown / PDF)

---

## Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
Built for developers who want a codebase explained without sending it to the cloud.
</div>
