from __future__ import annotations

from typing import Protocol, Type

from pydantic import BaseModel

from core.schemas import ResultadoExtraccion


class AIProvider(Protocol):
    provider_name: str
    model_name: str
    prompt_version: str

    def analizar_pdf(
        self,
        archivo_pdf,
        prompt: str,
        esquema: Type[BaseModel],
    ) -> ResultadoExtraccion:
        ...
