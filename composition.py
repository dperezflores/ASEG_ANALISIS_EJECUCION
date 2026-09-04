from __future__ import annotations

from application.analysis_service import AnalysisService
from application.analyzer import DocumentAnalyzer
from infrastructure.ai.gemini import GeminiProvider
from infrastructure.prompts.file_repository import FilePromptRepository


_prompt_repository = FilePromptRepository()


def build_analysis_service(api_key: str, model_name: str) -> AnalysisService:
    provider = GeminiProvider(api_key, model_name)
    analyzer = DocumentAnalyzer(provider, _prompt_repository)
    return AnalysisService(analyzer)
