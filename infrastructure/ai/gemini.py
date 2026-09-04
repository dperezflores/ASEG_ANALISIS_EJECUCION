from __future__ import annotations

import re
import time
from typing import Type

from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from domain.schemas import ResultadoExtraccion


TAMANO_MAXIMO_PDF = 50 * 1024 * 1024
PROMPT_VERSION = "2026-09-02-ejecucion-v1"


class GeminiProvider:
    provider_name = "Gemini"
    prompt_version = PROMPT_VERSION

    def __init__(self, api_key: str, model_name: str):
        if not api_key.strip():
            raise ValueError("La clave API de Gemini está vacía.")
        self.api_key = api_key.strip()
        self.model_name = model_name.strip() or "gemini-2.5-flash"

    @staticmethod
    def _segundos_reintento(error: Exception, intento: int) -> int:
        texto = str(error)
        coincidencia = re.search(
            r"retry(?:\s+in|\s+after)?\s+(\d+)",
            texto,
            re.IGNORECASE,
        )
        if coincidencia:
            return min(120, int(coincidencia.group(1)) + 1)
        return min(120, 15 * (2**intento))

    def _llamar(
        self,
        contenidos: list,
        esquema: Type[BaseModel],
        max_reintentos: int = 3,
    ):
        cliente = genai.Client(api_key=self.api_key)

        for intento in range(max_reintentos):
            try:
                return cliente.models.generate_content(
                    model=self.model_name,
                    contents=contenidos,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_json_schema=esquema.model_json_schema(by_alias=True),
                        temperature=0.0,
                    ),
                )
            except Exception as exc:
                texto = str(exc).lower()
                recuperable = any(
                    marca in texto
                    for marca in (
                        "429",
                        "quota",
                        "resource_exhausted",
                        "503",
                        "unavailable",
                    )
                )
                if not recuperable or intento == max_reintentos - 1:
                    raise
                time.sleep(self._segundos_reintento(exc, intento))

        raise RuntimeError("No fue posible completar la llamada a Gemini")

    def analizar_pdf(
        self,
        archivo_pdf,
        prompt: str,
        esquema: Type[BaseModel],
    ) -> ResultadoExtraccion:
        try:
            contenido = archivo_pdf.getvalue()

            if not contenido:
                raise ValueError("El archivo PDF está vacío")
            if len(contenido) > TAMANO_MAXIMO_PDF:
                raise ValueError("El PDF supera el límite de 50 MB admitido por Gemini")

            documento = types.Part.from_bytes(
                data=contenido,
                mime_type="application/pdf",
            )
            response = self._llamar([documento, prompt], esquema)

            parsed = response.parsed
            if parsed is None:
                parsed = esquema.model_validate_json(response.text)
            elif not isinstance(parsed, BaseModel):
                parsed = esquema.model_validate(parsed)

            contenido_json = parsed.model_dump(by_alias=True, mode="json")
            datos = (
                contenido_json
                if isinstance(contenido_json, list)
                else [contenido_json]
            )

            usage = getattr(response, "usage_metadata", None)
            consumo = (
                usage.model_dump(mode="json")
                if hasattr(usage, "model_dump")
                else {}
            )

            return ResultadoExtraccion(
                estado="OK",
                datos=datos,
                metadatos={
                    "proveedor": self.provider_name,
                    "modelo": self.model_name,
                    "version_prompt": self.prompt_version,
                    "consumo": consumo,
                },
            )
        except ValidationError as exc:
            return ResultadoExtraccion(
                estado="ERROR",
                errores=[f"La respuesta de IA no cumple el esquema: {exc}"],
                metadatos={
                    "proveedor": self.provider_name,
                    "modelo": self.model_name,
                },
            )
        except Exception as exc:
            return ResultadoExtraccion(
                estado="ERROR",
                errores=[f"Fallo en IA: {exc}"],
                metadatos={
                    "proveedor": self.provider_name,
                    "modelo": self.model_name,
                },
            )
