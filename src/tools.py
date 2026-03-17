from langchain.tools import tool, ToolRuntime
from src.condenser import CondenserCompose, KlopotenkoHTMLCondenser, MarkdownCondenser
from src.context import RuntimeContext


@tool
async def search_web(query: str, runtime: ToolRuntime[RuntimeContext]) -> str:
    """Use this to search the web for recepies, or ingredients definitions. You may search for a substitute
    of a certain ingredient if user does not have one.
    
    Parameters
    ----------
    query : str
        A question that Google Search Engine accept and search for the links.
    runtime : Runtime[RuntimeContext]
        Injecting context into the tool invokation.
    
    Returns
    -------
    str
        Links for a website.
    """
    response = await runtime.context.tavily_client.search(
        query=query, include_domains=["klopotenko.com"]
    )
    
    string = f"""This is all results:

    Results:
    """

    for index, result in enumerate(response["results"], start=1):
        
        string += f"""
        {index}. {result["title"]}. URL: {result["url"]} Revelance Score: {result["score"]} Content: {result["content"]}
        """
    
    return string

    
@tool
async def lookup_link(link: str, runtime: ToolRuntime[RuntimeContext]) -> str:
    """Use this to get any useful information from the link.
    
    Parameters
    ----------
    link : str
        Link to follow for the lookup.
    runtime : Runtime[RuntimeContext]
        Injecting context into the tool invokation.
    
    Returns
    -------
    str
        Information extracted from the website page.
        
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
    html = (await runtime.context.async_http_client.get(link)).content.decode()
    return condenser.condence(html)
