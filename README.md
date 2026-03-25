### AI PDF Assistant
AI PDF Assistant is a streamlined Streamlit application designed to turn your static PDF documents into interactive conversation partners. By leveraging Large Language Models (LLMs), this agent allows you to upload a document and extract specific insights, summaries, or data points simply by asking questions in plain English.

## Features
1. Instant Analysis: Upload any PDF and start querying immediately.
2. Context-Aware Chat: The agent understands the content of your specific file to provide accurate answers.
3. Chat History: All previous exchanges are neatly tucked away in an expandable section to keep your workspace clean but accessible.
4. Secure API Handling: Input your OpenAI API key directly through the UI (it is not hardcoded).

## Installation
1. Clone the repository (or navigate to the project folder): git clone https://github.com/alvin66tsang/ai-pdf-assistant.git
2. cd ./ai-pdf-assistant
3. pip install -r ./requirement.txt in the terminal

## How to Use
1. Start the application: run "streamlit run main.py"
2. Configure your session:
   1. Enter your OpenAI API Key in the sidebar/input field provided.
   2. Upload your target PDF file.
3. Start Chatting

## Technology Stack
1. Frontend: Streamlit
2. LLM Integration: OpenAI
3. LangChain Framework