from email import message
import os
from dotenv import find_dotenv, load_dotenv
from langchain_core.utils import get_from_dict_or_env
# import openai
import zhipuai


def parse_llm_api_key(model: str, env_file: dict = None):
    """
    通过 model 和 env_file 的来解析平台参数
    """
    if env_file == None:
        _ = load_dotenv(find_dotenv())
        env_file = os.environ
    if model == "openai":
        return env_file["OPENAI_API_KEY"]
    elif model == "wenxin":
        return env_file["wenxin_api_key"], env_file["wenxin_secret_key"]
    elif model == "spark":
        return env_file["spark_api_key"], env_file["spark_appid"], env_file["spark_api_secret"]
    elif model == "zhipuai":
        return get_from_dict_or_env(env_file, "zhipuai_api_key", "ZHIPUAI_API_KEY")
        # return env_file["ZHIPUAI_API_KEY"]
    else:
        raise ValueError(f"model{model} not support!!!")


def get_completion(prompt: str, model: str, temperature=0.1, api_key=None, secret_key=None, access_token=None, appid=None, api_secret=None, max_tokens=2048):
    # 调用大模型获取回复，支持上述三种模型+gpt
    # arguments:
    # prompt: 输入提示
    # model：模型名
    # temperature: 温度系数
    # api_key：如名
    # secret_key, access_token：调用文心系列模型需要
    # appid, api_secret: 调用星火系列模型需要
    # max_tokens : 返回最长序列
    # return: 模型返回，字符串
    # 调用 GPT
    if model in ["gpt-3.5-turbo", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0613", "gpt-4", "gpt-4-32k"]:
        # return get_completion_gpt(prompt, model, temperature, api_key, max_tokens)
        return "不支持的模型"
    # elif model in ["ERNIE-Bot", "ERNIE-Bot-4", "ERNIE-Bot-turbo"]:
        # return get_completion_wenxin(prompt, model, temperature, api_key, secret_key)
    # elif model in ["Spark-1.5", "Spark-2.0"]:
        # return get_completion_spark(prompt, model, temperature, api_key, appid, api_secret, max_tokens)
    elif model in ["glm-4", "glm-4-flash"]:
        return get_completion_glm(prompt, model, temperature, api_key, max_tokens)
    else:
        return "不正确的模型"


# def get_completion_gpt(prompt: str, model: str, temperature: float, api_key: str, max_tokens: int):
#     # 封装 OpenAI 原生接口
#     if api_key == None:
#         api_key = parse_llm_api_key("openai")
#     openai.api_key = api_key
#     # 具体调用
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,  # 模型输出的温度系数，控制输出的随机程度
#         max_tokens=max_tokens,  # 回复最大长度
#     )
#     # 调用 OpenAI 的 ChatCompletion 接口
#     return response.choices[0].message["content"]


def get_completion_glm(prompt: str, model: str, temperature: float, api_key: str, max_tokens: int):
    # 获取GLM回答
    if api_key == None:
        api_key = parse_llm_api_key("zhipuai")

    # response = zhipuai.model_api.invoke(
    #     model=model,
    #     prompt=[{"role": "user", "content": prompt}],
    #     temperature=temperature,
    #     max_tokens=max_tokens
    # )

    client = zhipuai.ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content
