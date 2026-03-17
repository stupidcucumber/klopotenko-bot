from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import requests
from src.condenser import CondenserCompose, KlopotenkoHTMLCondenser, MarkdownCondenser

load_dotenv()

tavily_client = TavilyClient()


SYSTEM_PROMPT = """You are the Yevgen Klopotenko - the best chief on a planet. Your main purpose is to
provide a customer with simple and tasty recipies that use ingredients customer has. If
a customer has any follow up questions you answer them.

If there is Error or Exception while you were trying to use the tool then investigate and retry. You only allowed to search
through klopotenko.com website.
""" 


@tool
def search_web(query: str) -> str:
    """Use this to search the web for recepies, or ingredients definitions. You may search for a substitute
    of a certain ingredient if user does not have one.
    
    Parameters
    ----------
    query : str
        A question that Google Search Engine accept and search for the links.
    
    Returns
    -------
    str
        Links for a website.
    """
    response = tavily_client.search(
        query=query, include_domains=["klopotenko.com"]
    )
    
    string = f"""This is all results:

    Results:
    """

    for index, result in enumerate(response["results"], start=1):
        
        string += f"""
        {index}. {result["title"]}. URL: {result["url"]}
        """
    
    return string

    
@tool
def lookup_link(link: str) -> str:
    """Use this to get any useful information from the link.
    
    Parameters
    ----------
    link : str
        Link to follow for the lookup.
    
    Returns
    -------
    str
        Information extracted from the website.
        
    Raises
    ------
    ValueError
        In case if link you pass do not belongs to klopotenko.com website.
    """
    if "klopotenko.com" not in link:
        raise ValueError("This website does not belong to klopotenko.com domain!")
    condenser = CondenserCompose(
        condensers=[
            KlopotenkoHTMLCondenser(),
            MarkdownCondenser()
        ]
    )
    html = requests.get(link).content.decode()
    return condenser.condence(html)



model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")  
agent = create_agent(
    model=model, 
    system_prompt=SYSTEM_PROMPT, 
    # checkpointer=InMemorySaver(),
    tools=[search_web, lookup_link]
)
    


if __name__ == "__main__":
    from googlesearch import search
    
    results = search("Necromancer Diablo IV")
    print(results)
    
    for index, search_result in enumerate(results):
        print(f"Search result {index}")
        print("\tSearch result title: ", search_result.title)
        print("\tSearch result link: ", search_result.url)