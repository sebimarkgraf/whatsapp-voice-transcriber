#!/usr/bin/env python3
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from textwrap import dedent
from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)


class Summarizer:
    PROMPT_TEMPLATE = dedent("""Schreibe eine kurze deutsche Version der folgenden Sprachnachricht:
                                 "{text}"
                                 Wenn möglich, gliedere die Nachricht in Abschnitte und ergänze Überschriften.
                                 Gebe nur den gekürzten Text zurück:
                                 """)

    def __init__(self, model="superdrew100/llama3-abliterated"):
        llm = Ollama(model=model)
        prompt_template = PromptTemplate.from_template(self.PROMPT_TEMPLATE)

        self.llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    def summarize(self, text: str) -> str:
        logger.debug(f"Summarizing: {text}")
        return self.llm_chain.invoke(text)
