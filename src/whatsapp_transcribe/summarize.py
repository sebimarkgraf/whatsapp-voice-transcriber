#!/usr/bin/env python3
import logging
from os import environ
from textwrap import dedent
from typing import Optional

from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class Summarizer:
    PROMPT_TEMPLATE = dedent("""
    ###Instruction###
    Write a short German summary of the following voice message: "{text}".
    If possible, organize the summary into sections.
    Return only the condensed text.
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
