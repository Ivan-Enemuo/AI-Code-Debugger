# 🔍 AI Code Debugger

A Streamlit web application that leverages Google GenAI to analyze code, identify bugs, and suggest fixes. Whether you have a screenshot of a broken code snippet or you want to paste the code directly, this tool will act as your expert programming debugger.

## ✨ Features

* **Multi-Modal Input:** Upload screenshots of code or paste raw text directly into the app.
* **Real-Time Streaming:** Watch the AI's analysis and code corrections stream in real-time.
* **Model Selection:** Choose between different Google GenAI models (e.g., `gemini-2.0-flash`, `gemma-4-26b-a4b-it`) to suit your needs.
* **Custom Instructions:** Add specific prompts (e.g., "Rewrite this in Python 3.12" or "Optimize for performance").
* **Stop Generation:** A dedicated stop button to halt the analysis stream immediately if you already have the answer you need.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.8 or higher
* A valid [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## 📦 Installation

1. **Clone the repository** (or download the source code):
   ```bash
   git clone [https://github.com/yourusername/ai-code-debugger.git](https://github.com/yourusername/ai-code-debugger.git)
   cd ai-code-debugger