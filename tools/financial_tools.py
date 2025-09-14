import os
import yfinance as yf
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_PATH = "vector_stores/faiss_news_index"

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


@tool
def search_financial_news(query: str) -> str:
    """
    Searches for relevant financial news articles from the knowledge base.
    Use this to find information on company strategies, market sentiment, product announcements,
    and reactions to economic events. The input should be a descriptive query
    about the information you are looking for.
    """
    print(f"Tool 'search_financial_news' called with query: {query}")
    # The 'allow_dangerous_deserialization' is needed for FAISS with LangChain
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(query)
    
    if not docs:
        return "No relevant financial news found for that query."
        
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def get_stock_performance(ticker: str) -> str:
    """
    Retrieves the latest stock performance data for a given ticker symbol.
    Use this to get current stock prices, recent price changes, and trading volume.
    The input must be a single valid stock ticker symbol (e.g., 'NVDA', 'AAPL').
    """
    print(f"Tool 'get_stock_performance' called with ticker: {ticker}")
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    if hist.empty:
        return f"Could not find historical data for ticker {ticker}."

    latest = hist.iloc[-1]
    prev_close = hist.iloc[-2]['Close']
    change = latest['Close'] - prev_close
    percent_change = (change / prev_close) * 100

    return (
        f"Data for {ticker}:\n"
        f"Latest Close Price: ${latest['Close']:.2f}\n"
        f"Change: ${change:.2f} ({percent_change:.2f}%)\n"
        f"Daily High: ${latest['High']:.2f}\n"
        f"Daily Low: ${latest['Low']:.2f}\n"
        f"Volume: {latest['Volume']:,}"
    )