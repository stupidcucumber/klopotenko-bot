from src.condenser.base import Condenser
from html_to_markdown import convert


class MarkdownCondenser(Condenser):
    
    def condence(self, data: str) -> str:
        return convert(data)