from llm.call_llm import parse_llm_api_key
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import ZhipuAIEmbeddings
from loglog import logger


def get_embedding(embedding: str, embedding_key: str = None, env_file: str = None):
    """
    该函数用于加载 Embedding 模型
    """
    if embedding == 'm3e':
        logger.info("Using m3e-base model")
        return HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
    if embedding_key == None:
        embedding_key = parse_llm_api_key(embedding)
    if embedding == "openai":
        return OpenAIEmbeddings(openai_api_key=embedding_key)
    elif embedding == "zhipuai":
        return ZhipuAIEmbeddings(api_key=embedding_key, model="embedding-3")
    else:
        raise ValueError(f"embedding {embedding} not support ")
