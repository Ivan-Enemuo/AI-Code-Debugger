🔍 AI Code Debugger

A Streamlit web application that leverages Google GenAI to analyze code, identify bugs, and suggest fixes. Whether you have a screenshot of a broken code snippet or you want to paste the code directly, this tool will act as your expert programming debugger.

✨ Features

Multi-Modal Input: Upload screenshots of code or paste raw text directly into the app.

Real-Time Streaming: Watch the AI's analysis and code corrections stream in real-time.

Model Selection: Choose between different Google GenAI models (e.g., gemini-2.0-flash, gemma-4-26b-a4b-it) to suit your needs.

Custom Instructions: Add specific prompts (e.g., "Rewrite this in Python 3.12" or "Optimize for performance").

Stop Generation: A dedicated stop button to halt the analysis stream immediately if you already have the answer you need.

🛠️ Prerequisites

Before you begin, ensure you have the following installed:

Python 3.8 or higher

A valid Google Gemini API Key

🚀 Installation & Running the App

Follow these steps to install the required dependencies and start the application.

Clone the repository (or download the source code):

git clone https://github.com/yourusername/ai-code-debugger.git
cd ai-code-debugger


Create and activate a virtual environment (highly recommended):

# On macOS/Linux:
python -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate


Install the dependencies:
You can install the required packages directly using pip:

pip install streamlit pillow google-genai


(Alternatively, if you have a requirements.txt file, run pip install -r requirements.txt)

Run the application:
Once the dependencies are installed, start the Streamlit server:

streamlit run app.py


⚙️ Configuration & Usage

Configure the app:

After running the command above, open the provided local URL (usually http://localhost:8501) in your browser.

In the left sidebar, enter your Google API Key and select your preferred model.

Analyze Code:

Use the Upload Screenshot tab to drop in an image of your code, or use the Paste Code tab for raw text.

Add any specific instructions in the text area below.

Click 🔍 Analyze Code and watch the AI transcribe, explain, and fix your code!

🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

📝 License

This project is licensed under the MIT License.
