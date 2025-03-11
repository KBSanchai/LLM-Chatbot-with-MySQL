<h1>💬 SQL Chatbot App with LangChain, Ollama, Streamlit & MySQL</h1>

<p>
An intelligent, full-stack chatbot app built using <strong>LangChain</strong>, <strong>Ollama</strong>, <strong>Streamlit</strong>, and <strong>MySQL</strong>. This app allows users to interact with their MySQL database using natural language. It includes user authentication and uses an LLM (LLaMA 3 via Ollama) to convert user queries into SQL, execute them, and summarize the results.
</p>

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
  <li><strong>Frontend</strong>: Streamlit</li>
  <li><strong>Backend</strong>: Python, LangChain</li>
  <li><strong>LLM</strong>: LLaMA 3 (via Ollama)</li>
  <li><strong>Database</strong>: MySQL (userdatabase & portfolio)</li>
  <li><strong>Auth</strong>: Custom login/signup with hashed passwords</li>
</ul>

<h2>⚙️ Setup Instructions</h2>

<ol>
  <li>🧱 <strong>Prerequisites</strong></li>
  <ul>
    <li>Python 3.10+</li>
    <li>MySQL Server</li>
    <li>Ollama installed locally</li>
    <li>LLaMA 3 model pulled via Ollama</li>
  </ul>
</ol>

<h2>📸 Screenshots</h2>

<h4>🔌 Connect to MySQL Database & Chat</h4>
<img src="screenshots/Screenshot 2025-03-11 200040.png" alt="Chatbot Interface with MySQL Connection" width="800"/>

<h4>🔐 Login / Signup Page</h4>
<img src="screenshots/Screenshot 2025-03-11 195838.png" alt="Login and Signup Page" width="800"/>

<h4>🧩 Database Schema (ER Diagram)</h4>
<img src="screenshots/dbms er.png" alt="MySQL ER Diagram" width="800"/>

<h2>📂 Database Tables Used</h2>
<p>
This chatbot interacts with the following tables inside the <code>portfolio</code> MySQL database:
</p>
<ul>
  <li><code>company_price</code></li>
  <li><code>company_profile</code></li>
  <li><code>dividend_history</code></li>
  <li><code>fundamental_averaged</code></li>
  <li><code>fundamental_report</code></li>
  <li><code>holdings_view</code></li>
  <li><code>news</code></li>
  <li><code>suggested_improvements</code></li>
  <li><code>technical_signals</code></li>
  <li><code>transaction_history</code></li>
  <li><code>user_profile</code></li>
  <li><code>watchlist</code></li>
</ul>

<p>
These tables support a wide range of financial operations, from tracking company performance to generating investment insights.
</p>


