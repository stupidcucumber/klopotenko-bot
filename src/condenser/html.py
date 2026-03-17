from src.condenser.base import Condenser
from bs4 import BeautifulSoup


class HTMLCondenser(Condenser):
    
    def _replace_a_with_its_content_method(self, html: BeautifulSoup) -> BeautifulSoup:
        for a_tag in html.find_all("a"):
            a_tag.unwrap()
        return html
    
    def _remove_tags_method(self, html: BeautifulSoup) -> BeautifulSoup:
        tags = [
            "img", "style", "head", "header", "foot", "footer", "script", "svg"
        ]
        for tag_instance in html(tags):
            tag_instance.extract()
        return html
    
    def condence(self, data: str) -> str:
        html = BeautifulSoup(data, 'html.parser')
        for method_name in self.__dir__():
            if not method_name.endswith("_method"):
                continue
            method: BeautifulSoup = self.__getattribute__(method_name)
            html = method(html)
        return html.prettify()
    
    
class KlopotenkoHTMLCondenser(HTMLCondenser):
    
    def _remove_section(self, html: BeautifulSoup, section_class: str) -> BeautifulSoup:
        for div_tag in html(["div"]):
            if "class" in div_tag.attrs and section_class in div_tag.attrs["class"]:
                div_tag.extract()
                
        for section_tag in html(["section"]):
            if "class" in section_tag.attrs and section_class in section_tag.attrs["class"]:
                section_tag.extract()
        return html
    
    def _remove_sections_method(self, html: BeautifulSoup) -> BeautifulSoup:
        sections = [
            "news-wrapper",
            "monthly-purchases",
            "new-recipes",
            "subscription-banner",
            "course-wrapper",
            "header-search",
            "interaction-buttons",
            "tag-share",
            "widget_text",
            "ai-viewports",
            "su-posts",
            "modal-body"
        ]

        for section in sections:
            html = self._remove_section(html, section_class=section)
        
        return html
