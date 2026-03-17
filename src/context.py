from pydantic import BaseModel, ConfigDict, Field
from tavily import AsyncTavilyClient
from httpx import AsyncClient


class RuntimeContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tavily_client: AsyncTavilyClient = Field(exclude=True)
    async_http_client: AsyncClient = Field(exclude=True)
