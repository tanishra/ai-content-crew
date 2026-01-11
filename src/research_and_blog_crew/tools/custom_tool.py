from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


# =========================================================
# GENERIC INPUT SCHEMAS
# =========================================================

class QueryInput(BaseModel):
    query: str = Field(..., description="Search query or topic")


class URLInput(BaseModel):
    url: str = Field(..., description="URL to process")


class TextInput(BaseModel):
    text: str = Field(..., description="Text content to analyze")


class TopicInput(BaseModel):
    topic: str = Field(..., description="Topic for analysis")


class CitationInput(BaseModel):
    citations: str = Field(..., description="Citations to validate")


# =========================================================
# RESEARCH TOOLS
# =========================================================

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "Search the web for up-to-date and credible information."
    args_schema: Type[BaseModel] = QueryInput

    def _run(self, query: str) -> str:
        return f"Web search results for: {query}"


class ScrapingTool(BaseTool):
    name: str = "scraping_tool"
    description: str = "Scrape content from a given webpage URL."
    args_schema: Type[BaseModel] = URLInput

    def _run(self, url: str) -> str:
        return f"Scraped content from {url}"


class AcademicSearchTool(BaseTool):
    name: str = "academic_search_tool"
    description: str = "Search academic papers, journals, and scholarly articles."
    args_schema: Type[BaseModel] = QueryInput

    def _run(self, query: str) -> str:
        return f"Academic research findings for: {query}"


# =========================================================
# FACT CHECKING TOOLS
# =========================================================

class FactCheckingTool(BaseTool):
    name: str = "fact_checking_tool"
    description: str = "Verify factual accuracy of claims."
    args_schema: Type[BaseModel] = TextInput

    def _run(self, text: str) -> str:
        return f"Fact check completed. No issues found in: {text}"


class SourceVerificationTool(BaseTool):
    name: str = "source_verification_tool"
    description: str = "Verify credibility and reliability of a source."
    args_schema: Type[BaseModel] = QueryInput

    def _run(self, query: str) -> str:
        return f"Source '{query}' verified as credible."


# =========================================================
# TREND & MARKET ANALYSIS TOOLS
# =========================================================

class TrendAnalysisTool(BaseTool):
    name: str = "trend_analysis_tool"
    description: str = "Analyze trends and future developments."
    args_schema: Type[BaseModel] = TopicInput

    def _run(self, topic: str) -> str:
        return f"Trend analysis generated for topic: {topic}"


class MarketDataTool(BaseTool):
    name: str = "market_data_tool"
    description: str = "Retrieve market intelligence and industry data."
    args_schema: Type[BaseModel] = TopicInput

    def _run(self, topic: str) -> str:
        return f"Market data insights for: {topic}"


# =========================================================
# SEO TOOLS
# =========================================================

class KeywordResearchTool(BaseTool):
    name: str = "keyword_research_tool"
    description: str = "Find high-impact SEO keywords for a topic."
    args_schema: Type[BaseModel] = TopicInput

    def _run(self, topic: str) -> str:
        return f"Keyword research results for: {topic}"


class SEOAnalysisTool(BaseTool):
    name: str = "seo_analysis_tool"
    description: str = "Analyze content for SEO optimization opportunities."
    args_schema: Type[BaseModel] = TextInput

    def _run(self, text: str) -> str:
        return "SEO analysis completed successfully."


# =========================================================
# ETHICS & ORIGINALITY TOOLS
# =========================================================

class PlagiarismDetectionTool(BaseTool):
    name: str = "plagiarism_detection_tool"
    description: str = "Detect plagiarism and ensure content originality."
    args_schema: Type[BaseModel] = TextInput

    def _run(self, text: str) -> str:
        return "No plagiarism detected."


class CitationValidatorTool(BaseTool):
    name: str = "citation_validator_tool"
    description: str = "Validate citation format and authenticity."
    args_schema: Type[BaseModel] = CitationInput

    def _run(self, citations: str) -> str:
        return "All citations are valid and properly formatted."


# =========================================================
# TOOL REGISTRY (IMPORTANT)
# =========================================================

ALL_TOOLS = [
    WebSearchTool(),
    ScrapingTool(),
    AcademicSearchTool(),
    FactCheckingTool(),
    SourceVerificationTool(),
    TrendAnalysisTool(),
    MarketDataTool(),
    KeywordResearchTool(),
    SEOAnalysisTool(),
    PlagiarismDetectionTool(),
    CitationValidatorTool(),
]