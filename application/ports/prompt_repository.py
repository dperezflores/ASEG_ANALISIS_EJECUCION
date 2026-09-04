from __future__ import annotations

from typing import Protocol


class PromptRepository(Protocol):
    def get(self, prompt_name: str) -> str:
        ...
