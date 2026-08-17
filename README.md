# RepoPilot

RepoPilot is an open-source, local AI agent designed to analyze GitHub repositories. Give it any public repository URL, and it inspects file structures, analyzes source code, explains backend logic, identifies technologies, and answers specific questions—all running 100% locally on your machine.

---

## Why I Built This

Navigating large, unfamiliar, or poorly documented GitHub repositories takes time. I wanted an AI tool that can instantly read a codebase, summarize its contents, and answer targeted technical queries without sending private local execution logs or code contexts to cloud APIs.

---

## How It Works

RepoPilot works by combining lightweight local AI execution with local runtime tools:

* Framework: Built using Hugging Face's smolagents framework for tool-calling and agentic reasoning.
* Local Model Execution: Uses Ollama running qwen2.5-coder:7b locally on PC hardware to ensure privacy and zero API costs.
* User Interface: Powered by Gradio for a seamless web UI and interactive chat interface.
* Repository Analysis Engine: Leverages custom Python utilities to inspect directory structures, count files/folders, inspect backend files, and parse source code in real time.

---

## Media and Demos

### Web Interface and Live Execution
The Gradio dashboard allows interactive queries while showing real-time step-by-step agent reasoning logs.

![RepoPilot Interface](./docs/screenshots/01_interface_overview.png)

> **Execution Example:**
> * Input Repository: `https://github.com/fahwem/Audio-filtering---Fourier-Transform`
> * User Query: "explain to me this repo in short"
> * Agent Output: Detects file structure (`README.md`, `audiofilter_app.m`), identifies MATLAB as the main language, and summarizes the Fourier audio filtering GUI.

---

### Step-by-Step Reasoning and Follow-Ups
RepoPilot preserves chat context for follow-up questions, evaluating codebase extensions on the fly.

![RepoPilot Execution Logs](./docs/screenshots/02_followup_execution.png)

> **Follow-Up Query:** "tell me which language it uses"  
> **Agent Thought:** Inspects file extensions and repo metadata  
> **Final Output:** "The language used in the repository is MATLAB."

---

### Video Demonstration
For a full walk-through of the terminal setup, Gradio UI, and real-time query parsing, watch the demonstration video:

[![Watch Demo Video](./docs/screenshots/video_thumbnail.png)](./docs/demo/0817.mov)

*(Click thumbnail to play 0817.mov)*

---

## How to Run RepoPilot Locally

Follow these steps to run RepoPilot on your own PC.

### Step 1: Install Prerequisites
1. Ensure Python 3.10 or higher is installed on your system.
2. Download and install Ollama from https://ollama.com/
3. Open your terminal or command prompt and run the following command to pull the required AI model:
   ```bash
   ollama pull qwen2.5-coder:7b
