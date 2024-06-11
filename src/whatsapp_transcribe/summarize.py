#!/usr/bin/env python3
from langchain_core.prompts import PromptTemplate

from textwrap import dedent
import logging
from langchain_community.chat_models import ChatOllama
from os import environ
from typing import Optional

logger = logging.getLogger(__name__)


class Summarizer:
    PROMPT_TEMPLATE = dedent("""Schreibe eine kurze deutsche Version der folgenden Sprachnachricht:
                                 "{text}"
                                 Wenn möglich, gliedere die Nachricht in Abschnitte und ergänze Überschriften.
                                 Gebe nur den gekürzten Text zurück:
                                 """)

    def __init__(self, model: Optional[str] = None):
        model = (
            model
            if model is not None
            else environ.get(
                "SUMMARIZE_MODEL", "DiscoResearch/Llama3-DiscoLeo-Instruct-8B-v0.1"
            )
        )
        llm = ChatOllama(
            base_url=environ.get("OLLAMA_HOST", "http://localhost:11434"),
            model=model,
        )
        prompt_template = PromptTemplate.from_template(self.PROMPT_TEMPLATE)

        self.llm_chain = prompt_template | llm

    def summarize(self, text: str) -> str:
        logger.debug(f"Summarizing: {text}")
        return dict(self.llm_chain.invoke(text))["content"]
