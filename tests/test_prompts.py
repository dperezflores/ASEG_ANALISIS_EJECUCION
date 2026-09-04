from __future__ import annotations

import unittest

from application.analyzer import DocumentAnalyzer
from domain.schemas import ResultadoExtraccion
from infrastructure.prompts.file_repository import FilePromptRepository


class FakeProvider:
    provider_name = "Fake"
    model_name = "fake-model"
    prompt_version = "test"

    def __init__(self):
        self.last_prompt = None
        self.last_schema = None

    def analizar_pdf(self, archivo_pdf, prompt, esquema):
        self.last_prompt = prompt
        self.last_schema = esquema
        return ResultadoExtraccion(estado="OK", datos=[])


class PromptsTest(unittest.TestCase):
    def setUp(self):
        self.repository = FilePromptRepository()

    def test_existen_los_cuatro_prompts(self):
        for nombre in (
            "estimaciones",
            "facturas",
            "comprobantes_pago",
            "polizas",
        ):
            with self.subTest(nombre=nombre):
                prompt = self.repository.get(nombre)
                self.assertTrue(prompt.strip())

    def test_analyzer_carga_prompt_desde_repositorio(self):
        provider = FakeProvider()
        analyzer = DocumentAnalyzer(provider, self.repository)

        analyzer.analyze("Estimaciones", object())

        self.assertIn("carátulas de estimación", provider.last_prompt)
        self.assertIsNotNone(provider.last_schema)


if __name__ == "__main__":
    unittest.main()
