<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SQL Chatbot App</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto;">

  <h1>💬 SQL Chatbot App with LangChain, Ollama, Streamlit & MySQL</h1>
  <p>An intelligent, full-stack chatbot app built using <strong>LangChain</strong>, <strong>Ollama</strong>, <strong>Streamlit</strong>, and <strong>MySQL</strong>. This app allows users to interact with their MySQL database using natural language. It includes authentication (login/signup) and uses an LLM (LLaMA 3 via Ollama) to convert user queries into SQL, execute them, and summarize the results.</p>

  <h2>🚀 Features</h2>
  <ul>
    <li>🔐 User Login/Signup Authentication</li>
    <li>🧠 Natural Language to SQL Conversion using LLM</li>
    <li>🗃️ Query your own MySQL <code>portfolio</code> database</li>
    <li>🤖 Chatbot built with LangChain + Ollama (LLaMA 3.2)</li>
    <li>🌐 Clean and interactive Streamlit UI</li>
  </ul>

  <h2>🛠️ Tech Stack</h2>
  <ul>
    <li><strong>Frontend:</strong> Streamlit</li>
    <li><strong>Backend:</strong> Python, LangChain</li>
    <li><strong>LLM:</strong> LLaMA 3 (via Ollama)</li>
    <li><strong>Database:</strong> MySQL (<code>userdatabase</code> and <code>portfolio</code>)</li>
    <li><strong>Auth:</strong> Custom login/signup with hashed passwords</li>
  </ul>

  <h2>⚙️ Setup Instructions</h2>

  <h3>1. 🧱 Prerequisites</h3>
  <ul>
    <li>Python 3.10+</li>
    <li>MySQL Server</li>
    <li><a href="https://ollama.com/">Ollama installed</a></li>
    <li>LLaMA 3 model pulled via Ollama:</li>
  </ul>
  <pre><code>ollama pull llama3</code></pre>

</body>
</html>
