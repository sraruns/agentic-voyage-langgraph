#import tools from langchain
from langchain.agents import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.agent_toolkits.playwright.toolkit import PlayWrightBrowserToolkit
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain_experimental.tools import PythonREPLTool
from dotenv import load_dotenv
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import  WikipediaQueryRun
import os
from playwright.async_api import async_playwright
import requests
load_dotenv(override=True)



telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

serper = GoogleSerperAPIWrapper()

# define telegram tool
def telegram_push (text: str):
    response = requests.post(url, data = {"chat_id": chat_id, "text": text})
    if response.status_code == 200:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

telegram_tool = Tool(
    name="telegram_push",
    func=telegram_push,
    description="Send a message to a Telegram chat"
)

# define playwirght tool

async def browser_search():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright

# define serper tool
serper = GoogleSerperAPIWrapper()
serper_tool= Tool(
    name="serper",
    func=serper.run,
    description="Search the web for information"
)

# file tool
def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()

# wikipedia tool
wikipedia = WikipediaAPIWrapper()
wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia)

# python repl tool
python_repl = PythonREPLTool()