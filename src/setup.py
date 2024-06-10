# -*- coding: utf-8 -*-
import openai
import os
from dotenv import load_dotenv, find_dotenv
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache


def initialize_environment():
    """
    Initializes the environment by setting up the LLM cache and loading environment variables.
    """
    # Set up the LLM cache
    set_llm_cache(InMemoryCache())

    # Load environment variables from a .env file
    load_dotenv(find_dotenv())

    # Set the OpenAI API key from environment variables
    openai.api_key = os.environ.get("OPENAI_API_KEY")
