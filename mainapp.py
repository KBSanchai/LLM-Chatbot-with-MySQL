import streamlit as st
import mysql.connector
from langchain_ollama import ChatOllama
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_extraction_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate


def connectDatabase(username, port, host, password, database):
    mysql_uri = f"mysql+mysqlconnector://root:yourpassword@localhost:3306/portfolio"
    st.session_state.db = SQLDatabase.from_uri(mysql_uri)


def runQuery(query):
    return st.session_state.db.run(query) if st.session_state.db else "Please connect to database"


def getDatabaseSchema():
    return st.session_state.db.get_table_info() if st.session_state.db else "Please connect to database"


llm = ChatOllama(model="llama3.2")


def getQueryFromLLM(question):
    template = """below is the schema of MYSQL database, read the schema carefully about the table and column names. Also take care of table or column name case sensitivity.
    Finally answer user's question in the form of SQL query.

    {schema}

    please only provide the SQL query and nothing else

    for example:
    question: how many companies are in the database?
    SQL query: SELECT COUNT(*) FROM company_profile;
    question: What is the latest price of Nepal Bank Limited (NBL)?
    SQL query: SELECT LTP FROM company_price WHERE symbol = 'NBL';
    question: How many users are registered in the database?
    SQL query: SELECT COUNT(*) FROM user_profile;
    question: How many companies belong to the 'Bank' sector?
    SQL query: SELECT COUNT(*) FROM company_profile WHERE sector = 'Bank';
    question: What is the total market capitalization of all companies?
    SQL query: SELECT SUM(market_cap) FROM company_profile;
    question: How many users have added 'HEX' (Hotel Electronics) to their watchlist?
    SQl query: SELECT COUNT(*) FROM watchlist WHERE symbol = 'HEX';
    question: What companies does the user 'rewan' have in their watchlist?
    SQL query: SELECT symbol FROM watchlist WHERE username = 'rewan';
    question: what are the tables in the database.
    SQL query:show tables;
    
    
    
    your turn :
    question: {question}
    SQL query :
    please only provide the SQL query and nothing else
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "schema": getDatabaseSchema()
    })
    return response.content


def getResponseForQueryResult(question, query, result):
    template2 = """you can answer any comman question .below is the schema of MYSQL database, read the schema carefully about the table and column names of each table.
    Also look into the conversation if available
    Finally write a response in natural language by looking into the conversation and result.
    don't show like this
    Here are the responses to your questions in natural language:

    question:How many companies are in the database?
    Response:There are 10 companies in the database.

    How many users are registered in the database?
    There are 15 amazing users in the database.

    How many companies belong to the 'Bank' sector?
    There are 4 companies in the 'Bank' sector.

    What is the total market capitalization of all companies?
    The total market capitalization of all companies is 791.62 billion.

    What is the latest price of Nepal Bank Limited (NBL)?
    The latest price of Nepal Bank Limited (NBL) is 600.

    How many users have added 'HEX' (Hotel Electronics) to their watchlist?
    There are 4 users who have 'HEX' in their watchlist.

    Which users have invested in 'BIH' (Bank of Itahari)?
    The user rewan has invested in 'BIH' (Bank of Itahari).

    What is the total number of shares bought by 'rewan'?
    User rewan has bought a total of 275 shares.

    What is the latest news title related to 'HIH' (Hotel Itahari)?
    The latest news related to 'HIH' is: "Hotel Itahari expands its area."

    Show tables in the database.
    The database contains the following tables: company_profile, company_price, fundamental_report, technical_signals, dividend_history, news, user_profile, watchlist, and transaction_history

    don't show the response like this:
    question:what thing are there in company price?
    Response: Here are the responses:

    What thing are there in company price SQL query : SELECT * FROM company_price; Result : [('BIH', 788.0, 777.0), ('ELEX', 1010.0, 1000.0), ('HEX', 1222.3, 1220.0), ('HIH', 1500.5, 1499.4), ('KBL', 500.0, 470.0), ('LEC', 400.0, 410.0), ('LSL', 1000.0, 1040.0), ('NBL', 600.0, 580.5), ('NEPP', 500.0, 480.0), ('NIL', 5800.0, 6000.0)] Response: There are 10 things (i.e., companies) in the company price table.

    What is the latest market price of KBL? SQL query : SELECT market_price FROM company_price WHERE symbol = 'KBL' ORDER BY date DESC LIMIT 1; Result : [(470,)] Response: The latest market price of KBL is 470.

    How many companies have a sector of 'Finance'? SQL query : SELECT COUNT(*) FROM company_profile WHERE sector = 'Finance'; Result : [(2,)] Response: There are 2 companies with a sector of 'Finance'.

    What is the total number of users who belong to the 'IT' sector? SQL query : SELECT COUNT(DISTINCT username) FROM user_profile WHERE sector = 'IT'; Result : [(3,)] Response: There are 3 users who belong to the 'IT' sector.

    How many companies have a market capitalization greater than 1000 billion? SQL query : SELECT COUNT(*) FROM company_profile WHERE market_cap > 100000000000; Result : [(4,)] Response: There are 4 companies with a market capitalization greater than 1000 billion.

    What is the total number of shares bought by users who belong to the 'Bank' sector? SQL query : SELECT SUM(quantity) FROM transaction_history WHERE sector = 'Bank'; Result : [(15000,)] Response: The total number of shares bought by users who belong to the 'Bank' sector is 15,000.

    What is the latest dividend yield for NBL? SQL query : SELECT dividend_yield FROM company_price WHERE symbol = 'NBL' ORDER BY date DESC LIMIT 1; Result : [(10.0,)] Response: The latest dividend yield for NBL is 10%.

    How many companies have a sector of 'Renewable Energy'? SQL query : SELECT COUNT(*) FROM company_profile WHERE sector = 'Renewable Energy'; Result : [(1,)] Response: There is 1 company with a sector of 'Renewable Energy'.

    What is the total number of users who have invested in companies from the 'Finance' sector? SQL query : SELECT COUNT(DISTINCT username) FROM transaction_history WHERE symbol IN (SELECT symbol FROM company_profile WHERE sector = 'Finance'); Result : [(5,)] Response: There are 5 users who have invested in companies from the 'Finance' sector.

    What is the latest market capitalization of LSL? SQL query : SELECT market_cap FROM company_price WHERE symbol = 'LSL'; Result : [(1040.0,)] Response: The latest market capitalization of LSL is 1,040.
    
    {schema}

    Here are some example for you:

    question: Hi
    SQL query: SHOW TABLE;
    Result : [('company_profile',), ('company_price',), ('fundamental_report',), ('technical_signals',), ('dividend_history',), ('news',), ('user_profile',), ('watchlist',), ('transaction_history',)]
    Response: How can I assist you today? 🚀 with this Database. The database contains the following tables: company_profile, company_price, fundamental_report, technical_signals, dividend_history, news, user_profile, watchlist, and transaction_history.

    question: How many companies are in the database?
    SQL query: SELECT COUNT(*) FROM company_profile;
    Result : [(10,)]
    Response: There are 10 companies in the database.

    question: How many users are registered in the database?
    SQL query: SELECT COUNT(*) FROM user_profile;
    Result : [(15,)]
    Response: There are 15 amazing users in the database.

    question: How many companies belong to the 'Bank' sector?
    SQL query: SELECT COUNT(*) FROM company_profile WHERE sector = 'Bank';
    Result : [(4,)]
    Response: There are 4 companies in the 'Bank' sector.

    
    question: What is the total market capitalization of all companies?
    SQL query: SELECT SUM(market_cap) FROM company_profile;
    Result : [(791616000000,)]
    Response: The total market capitalization of all companies is 791.62 billion.


    question: What is the latest price of Nepal Bank Limited (NBL)?
    SQL query: SELECT LTP FROM company_price WHERE symbol = 'NBL';
    Result : [(600,)]
    Response: The latest price of Nepal Bank Limited (NBL) is 600.

    question: How many users have added 'HEX' (Hotel Electronics) to their watchlist?
    SQL query: SELECT COUNT(*) FROM watchlist WHERE symbol = 'HEX';
    Result : [(4,)]
    Response: There are 4 users who have 'HEX' in their watchlist.

    question: Which users have invested in 'BIH' (Bank of Itahari)?
    SQL query: SELECT DISTINCT username FROM transaction_history WHERE symbol = 'BIH';
    Result : [('rewan',)]
    Response: The user rewan has invested in 'BIH' (Bank of Itahari).

    question: What is the total number of shares bought by 'rewan'?
    SQL query: SELECT SUM(quantity) FROM transaction_history WHERE username = 'rewan' AND quantity > 0;
    Result : [(275,)]
    Response: User rewan has bought a total of 275 shares.

    question: What is the latest news title related to 'HIH' (Hotel Itahari)?
    SQL query: SELECT title FROM news WHERE related_company = 'HIH' ORDER BY date_of_news DESC LIMIT 1;
    Result : [("Hotel itahari expands it's area",)]
    Response: The latest news related to 'HIH' is: "Hotel Itahari expands its area."
    

    question: Show tables in the database.
    SQL query: SHOW TABLES;
    Result : [('company_profile',), ('company_price',), ('fundamental_report',), ('technical_signals',), ('dividend_history',), ('news',), ('user_profile',), ('watchlist',), ('transaction_history',)]
    Response: The database contains the following tables: company_profile, company_price, fundamental_report, technical_signals, dividend_history, news, user_profile, watchlist, and transaction_history.

    question: what thing are there in company price?
    SQL query: SELECT * FROM company_price;
    Result : [('BIH', 788.0, 777.0), ('ELEX', 1010.0, 1000.0), ('HEX', 1222.3, 1220.0), ('HIH', 1500.5, 1499.4), ('KBL', 500.0, 470.0), ('LEC', 400.0, 410.0), ('LSL', 1000.0, 1040.0), ('NBL', 600.0, 580.5), ('NEPP', 500.0, 480.0), ('NIL', 5800.0, 6000.0)]
    Response: The company_price table contains company symbols, their last traded price (LTP), and the previous close price (PC). For example, KBL has an LTP of 500 and a PC of 470, while NIL has an LTP of 5800 and a PC of 6000.

    question: Hi
    SQL query: SHOW TABLE;
    Result : [('company_profile',), ('company_price',), ('fundamental_report',), ('technical_signals',), ('dividend_history',), ('news',), ('user_profile',), ('watchlist',), ('transaction_history',)]
    Response: How can I assist you today? 🚀 with this Database. The database contains the following tables: company_profile, company_price, fundamental_report, technical_signals, dividend_history, news, user_profile, watchlist, and transaction_history.

    question: why sky is blue?
    SQL query: SHOW TABLE;
    Result : [('company_profile',), ('company_price',), ('fundamental_report',), ('technical_signals',), ('dividend_history',), ('news',), ('user_profile',), ('watchlist',), ('transaction_history',)]
    Response: The sky appears blue because of **Rayleigh scattering**. When sunlight enters Earth's atmosphere, it is made up of different colors of light, each with different wavelengths. 
              - **Shorter wavelengths (blue and violet light)** scatter more than longer wavelengths (red and yellow light) because they interact more with the tiny molecules in the atmosphere.
              - Our eyes are more sensitive to blue light than violet light, so we perceive the sky as blue.
             At sunrise and sunset, the sky looks red or orange because the light has to pass through more of the atmosphere, scattering away blue light and letting the longer wavelengths dominate.
    
    question: Tell about you.
    SQL query: SHOW TABLE;
    Result : [('company_profile',), ('company_price',), ('fundamental_report',), ('technical_signals',), ('dividend_history',), ('news',), ('user_profile',), ('watchlist',), ('transaction_history',)]
    Response: I am an AI assistant designed to help with various tasks, including SQL queries, data analysis, programming, and more. I can assist in analyzing stock market data, writing efficient queries, debugging code, and providing insights. Let me know how I can help you! 😊

    question: tell about news.
    SQL query: SELECT * FROM news;
    Result : [(1, 'Hotel Itahari expands its area', 'HIH', '2025-02-10'),(2, 'Nepal Bank announces dividend', 'NBL', '2025-02-12')]
    Response: There are recent news entries such as "Hotel Itahari expands its area" related to HIH on 2025-02-10, and "Nepal Bank announces dividend" related to NBL on 2025-02-12. 

    
    your turn to write response in natural language from the given result :
    question: {question}
    SQL query : {query}
    Result : {result}
    Response:
    """

    prompt2 = ChatPromptTemplate.from_template(template2)
    chain2 = prompt2 | llm

    response = chain2.invoke({
        "question": question,
        "schema": getDatabaseSchema(),
        "query": query,
        "result": result
    })

    return response.content


st.set_page_config(
    page_icon="🤖",
    page_title="Chat with MYSQL DB",
    layout="centered"
)

question = st.chat_input('Chat with your mysql database')

if "chat" not in st.session_state:
    st.session_state.chat = []

if question:
    if "db" not in st.session_state:
        st.error('Please connect database first.')
    else:
        st.session_state.chat.append({
            "role": "user",
            "content": question
        })

        query = getQueryFromLLM(question)
        print(query)
        result = runQuery(query)
        print(result)
        response = getResponseForQueryResult(question, query, result)
        st.session_state.chat.append({
            "role": "assistant",
            "content": response
        })

for chat in st.session_state.chat:
    st.chat_message(chat['role']).markdown(chat['content'])

def get_user_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kbs12345",
        database="userdatabase"   
    )

def check_user(email, password):
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(email, password):
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    conn.commit()
    conn.close()

# ---- Streamlit Interface ---- #


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    page = st.sidebar.selectbox("Choose", ["Login", "Signup"])
    st.subheader(f"{page} 🌐")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if page == "Signup":
        if st.button("Sign Up"):
            try:
                add_user(email, password)
                st.success("✅ Account created. Please login.")
            except Exception as e:
                st.error(f"Error: {e}")

    elif page == "Login":
        if st.button("Login"):
            if check_user(email, password):
                st.session_state.authenticated = True
                st.success("✅ Login successful.")
            else:
                st.error("❌ Invalid email or password")

# ---- After Login: Database Connection and Chatbot ---- #
if st.session_state.authenticated:
    st.sidebar.title("Connect to Your MySQL Database")
    host = st.sidebar.text_input("Host", value="localhost")
    port = st.sidebar.text_input("Port", value="3306")
    username = st.sidebar.text_input("Username", value="root")
    password = st.sidebar.text_input("Password", value="yourpassword")
    database = st.sidebar.text_input("Database", value="portfolio")
    connectBtn = st.sidebar.button("Connect")

    if connectBtn:
        try:
            connectDatabase(username, port, host, password, database)
            st.sidebar.success("✅ Connected to database.")
        except Exception as e:
            st.sidebar.error(f"Connection failed: {e}")


# cd "C:\Users\KBsan\OneDrive\Desktop\DBMS Project\project"
# python -m streamlit run mainapp.py
