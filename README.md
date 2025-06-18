# AI-Powered Finance Chatbot

An intelligent chatbot that extracts, summarizes, answers questions, and visualizes data from uploaded financial PDFs — powered by **LangChain**, **GPT-4o**, **Flask**, and **React**.

[![Watch Demo](https://img.youtube.com/vi/04OIAvRQmO4/0.jpg)](https://www.youtube.com/watch?v=04OIAvRQmO4)

---

## Features

- **📄 Upload PDFs** – Extract and summarize financial data.
- **💬 Ask Questions** – Chatbot answers queries using document context.
- **📊 Visualize Data** – Auto-generates bar charts for numeric insights.
- **🔗 LangChain** – Manages document context and follow-ups.
- **🐳 Dockerized** – Easy to build and run via Docker Compose.

---

## Tech Stack

- **Frontend**: React, Axios
- **Backend**: Flask, OpenAI GPT-4o, LangChain, Matplotlib, PyPDF2
- **DevOps**: Docker, Docker Compose

---

## Quick Start (Docker)

1. Add your OpenAI key to `server/.env`: 
`OPENAI_API_KEY=your-key-here `


2. Run the app:
```bash
docker-compose up --build


## Usage Instructions

### Uploading a Document:

Use the file upload option to upload a document.
Wait for the document to be processed. The bot will display a summary.

### Asking Questions:
Type a question about the document in the chat input box.
The bot will respond with answers based on the document's content.
You can also ask the bot to visualize any given numerical figures from the document.

## Troubleshooting Guide

### Front-end Errors

1. **Ensure all dependencies are installed**:  
   Run the following command in the `chatbot-ui` directory to install all required Node.js dependencies:
   ```bash
   npm install

2. **Check the browser console for any errors**:
Use your browser's developer tools to identify issues. Look for error messages in the console.

### Back-end Errors

1. **Verify Python dependencies**:
    Ensure that all Python libraries are installed by running:
    ```bash
    pip install -r requirements.txt

2. **Check if the Flask server is running:**
    Confirm that the Flask server is running. You can start the server by navigating to the server directory and running: