from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.runtime import get_runtime
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase


load_dotenv()


SYSTEM_PROMPT = """You are a careful SQLite analyst.

Rules:
- Think step-by-step.
- When you need data, call the tool `execute_sql` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Limit to 5 rows of output unless the user explicitly asks otherwise.
- If the tool returns 'Error:', revise the SQL and try again.
- Prefer explicit column lists; avoid SELECT *.
"""


@dataclass
class RuntimeContext():
    database: SQLDatabase
    
    
@tool
def execute_sql(query: str) -> str:
    """Execute SQL query and return results."""
    runtime_context = get_runtime(RuntimeContext)
    
    try:
        return runtime_context.context.database.run(query)
    
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    database = SQLDatabase.from_uri("sqlite:///Chinook.db")

    agent = create_agent(
        model=ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=1.0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        ),
        tools=[execute_sql],
        system_prompt=SYSTEM_PROMPT,
        context_schema=RuntimeContext
    )
    
    for step in agent.stream(
        input={
            "messages": "What are tables in the database?"
        },
        context=RuntimeContext(database=database),
        stream_mode="values"
    ):
        
        step["messages"][-1].pretty_print()
