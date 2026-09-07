from __future__ import annotations

from uuid import UUID

from application.analysis_service import AnalysisService
from application.analyzer import DocumentAnalyzer
from application.services.analysis_history_service import AnalysisHistoryService
from application.services.auth_service import AuthService
from application.services.work_service import WorkService
from config.settings import get_secret
from infrastructure.ai.gemini import GeminiProvider
from infrastructure.database.analysis_repository import NeonAnalysisRepository
from infrastructure.database.connection import Database
from infrastructure.database.user_repository import NeonUserRepository
from infrastructure.database.work_repository import NeonWorkRepository
from infrastructure.prompts.file_repository import FilePromptRepository


_prompt_repository = FilePromptRepository()


def _build_database() -> Database:
    return Database(get_secret("DATABASE_URL", ""))


def build_analysis_service(
    api_key: str,
    model_name: str,
    work_id: UUID | None = None,
) -> AnalysisService:
    provider = GeminiProvider(api_key, model_name)
    analyzer = DocumentAnalyzer(provider, _prompt_repository)
    repository = NeonAnalysisRepository(_build_database()) if work_id else None
    return AnalysisService(analyzer, repository, work_id)


def build_analysis_history_service() -> AnalysisHistoryService:
    return AnalysisHistoryService(NeonAnalysisRepository(_build_database()))


def build_auth_service() -> AuthService:
    return AuthService(NeonUserRepository(_build_database()))


def build_work_service() -> WorkService:
    return WorkService(NeonWorkRepository(_build_database()))
