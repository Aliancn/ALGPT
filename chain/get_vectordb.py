import os
from database.create_db import create_db, load_knowledge_db
from embedding.call_embedding import get_embedding


def get_vectordb(file_path: str = None, persist_path: str = None, embedding="m3e", embedding_key: str = None):
    """
    获取向量数据库
    :param file_path: 语料库路径
    :param persist_path: 持久化路径
    :param embedding: 词向量模型
    :param embedding_key: 词向量模型的key
    :return: 向量数据库
    """
    embedding = get_embedding(embedding=embedding, embedding_key=embedding_key)
    if persist_path is None:
        persist_path = os.path.join(os.path.dirname(__file__), '../vector_db')
    if os.path.exists(persist_path):  # 持久化目录存在
        contents = os.listdir(persist_path)
        if len(contents) == 0:  # 但是下面为空
            # print("目录为空")
            vectordb = create_db(file_path, persist_path, embedding)
            # presit_knowledge_db(vectordb)
            vectordb = load_knowledge_db(persist_path, embedding)
        else:
            # print("目录不为空")
            vectordb = load_knowledge_db(persist_path, embedding)
    else:  # 目录不存在，从头开始创建向量数据库
        vectordb = create_db(file_path, persist_path, embedding)
        # presit_knowledge_db(vectordb)
        vectordb = load_knowledge_db(persist_path, embedding)

    return vectordb
