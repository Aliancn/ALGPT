import tempfile
from embedding.call_embedding import get_embedding
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_chroma import Chroma
import os
import re
from loglog import logger

# 首先实现基本配置
# DEFAULT_DB_PATH = os.path.join(os.path.abspath(
#     __file__), "../database/knowledge_db")
DEFAULT_DB_PATH = os.path.join(os.path.dirname(
    __file__), "knowledge_db")
# DEFAULT_PERSIST_PATH = os.path.join(os.path.abspath(
#     __file__), "../vector_db")
DEFAULT_PERSIST_PATH = os.path.join(os.path.dirname(__file__), "../vector_db")


def get_files(dir_path):
    """
    获取目录下的所有文件

    Args:
        dir_path (_type_): _description_
    """
    files = []
    for root, dirs, fs in os.walk(dir_path):
        for f in fs:
            files.append(os.path.join(root, f))
    return files


def file_loader(file, loaders):
    if isinstance(file, tempfile._TemporaryFileWrapper):
        file = file.name
    if not os.path.isfile(file):
        [file_loader(os.path.join(file, f), loaders) for f in os.listdir(file)]
        return
    file_type = file.split('.')[-1]
    if file_type == 'pdf':
        loaders.append(PyMuPDFLoader(file))
    elif file_type == 'md':
        pattern = r"不存在|风控"
        match = re.search(pattern, file)
        if not match:
            loaders.append(UnstructuredMarkdownLoader(file))
    elif file_type == 'txt':
        loaders.append(UnstructuredFileLoader(file))
    return


def create_db_info(files=DEFAULT_DB_PATH, embeddings="m3e", persist_directory=DEFAULT_PERSIST_PATH):
    """
    该函数用于加载 PDF 文件，切分文档，生成文档的嵌入向量，创建向量数据库。
    """
    if files == None:
        vectordb = create_db(embeddings=embeddings)
    if embeddings == 'openai' or embeddings == 'm3e' or embeddings == 'zhipuai':
        vectordb = create_db(files, persist_directory, embeddings)

    logger.info(f"create db success")
    return f"db create success"


def create_db(dir=DEFAULT_DB_PATH, persist_directory=DEFAULT_PERSIST_PATH, embeddings="m3e"):
    """
    该函数用于加载 PDF 文件，切分文档，生成文档的嵌入向量，创建向量数据库。

    参数:
    file: 存放文件的路径。
    embeddings: 用于生产 Embedding 的模型

    返回:
    vectordb: 创建的数据库。
    """
    logger.info(f"开始创建向量数据库, dir: {dir}, embeddings: {embeddings}")
    if dir == None:
        return "can't load empty dir"
    files = get_files(dir)
    loaders = []
    [file_loader(file, loaders) for file in files]
    docs = []
    for loader in loaders:
        if loader is not None:
            docs.extend(loader.load())
    # 切分文档
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    if type(embeddings) == str:
        embeddings = get_embedding(embedding=embeddings)
    # 加载数据库
    logger.info(f"文档数量：{len(split_docs)}")
    logger.info(f"embedding 模型：{embeddings}")
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )

    logger.info(f"向量库中存储的数量：{vectordb._collection.count()}")

    return vectordb


def presit_knowledge_db(vectordb):
    """
    该函数用于持久化向量数据库。

    参数:
    vectordb: 要持久化的向量数据库。
    """
    vectordb.persist()


def load_knowledge_db(path=DEFAULT_PERSIST_PATH, embeddings="m3e"):
    """
    该函数用于加载向量数据库。

    参数:
    path: 要加载的向量数据库路径。
    embeddings: 向量数据库使用的 embedding 模型。

    返回:
    vectordb: 加载的数据库。
    """
    vectordb = Chroma(
        persist_directory=path,
        embedding_function=embeddings
    )
    return vectordb


if __name__ == "__main__":
    create_db(embeddings="m3e")
