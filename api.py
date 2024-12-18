from chain.QA_chain_self import QA_chain_self
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
from database.create_db import create_db_info
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
from loglog import logger
app = FastAPI()  # 创建 api 对象

template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
{context}
问题: {question}
有用的回答:"""

# 指定文件存储目录
UPLOAD_DIR = Path("./database/knowledge_db")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # 如果目录不存在，则创建

# 定义一个数据模型，用于接收POST请求中的数据


class Item(BaseModel):
    prompt: str  # 用户 prompt
    model: str = "glm-4"  # 使用的模型
    temperature: float = 0.6  # 温度系数
    if_history: bool = False  # 是否使用历史对话功能
    # API_Key
    api_key: str = None
    # Secret_Key
    secret_key: str = None
    # access_token
    access_token: str = None
    # APPID
    appid: str = None
    # APISecret
    Spark_api_secret: str = None
    # Secret_key
    Wenxin_secret_key: str = None
    # 数据库路径
    db_path: str = ""
    # 源文件路径
    file_path: str = ""
    # prompt template
    prompt_template: str = template
    # Template 变量
    input_variables: list = ["context", "question"]
    # Embdding
    embedding: str = "m3e"
    # Top K
    top_k: int = 5
    # embedding_key
    embedding_key: str = None


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    saved_files = []  # 用于记录成功保存的文件路径

    try:
        for file in files:
            # 保存文件的完整路径
            file_location = UPLOAD_DIR / file.filename

            # 分块写入文件
            with open(file_location, "wb") as buffer:
                while content := await file.read(1024):  # 分块读取文件
                    buffer.write(content)

            saved_files.append(str(file_location))  # 记录保存的路径

        info = create_db_info()

        return JSONResponse(content={
            "message": "Files uploaded successfully",
            "files": saved_files,
            "db": info
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/get_response")
async def get_response(item: Item):
    logger.info(f"接收到的数据为：{item}")
    # 首先确定需要调用的链
    if not item.if_history:
        if item.model == None:
            item.model = "glm-4"

        if item.embedding_key == None:
            item.embedding_key = item.api_key

        if item.embedding == None:
            item.embedding = "m3e"

        if item.temperature == None:
            item.temperature = 0.6

        if item.top_k == None:
            item.top_k = 5

        if len(item.file_path) == 0:
            item.file_path = None

        if len(item.db_path) == 0:
            item.db_path = None
        

        chain = QA_chain_self(model=item.model, temperature=item.temperature, top_k=item.top_k, file_path=item.file_path, persist_path=item.db_path,
                              appid=item.appid, api_key=item.api_key, embedding=item.embedding, template=template, Spark_api_secret=item.Spark_api_secret, Wenxin_secret_key=item.Wenxin_secret_key, embedding_key=item.embedding_key)

        response = chain.answer(question=item.prompt)

        return response

    # 由于 API 存在即时性问题，不能支持历史链
    else:
        return "API 不支持历史链"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8022)
