#### 1.1 简介

使用 langchain 搭配 glm 实现的 RAG 系统

可使用文件

- [x] pdf

- [x] markdown

- [x] txt

- [ ] docx

- [ ] pptx

- [ ] html

- [ ] xlsx

#### 1.2 核心逻辑

整个 RAG 过程包括如下操作：

1. 用户提出问题 Query

2. 加载和读取知识库文档

3. 对知识库文档进行分割

4. 对分割后的知识库文本向量化并存入向量库建立索引

5. 对问句 Query 向量化

6. 在知识库文档向量中匹配出与问句 Query 向量最相似的 top k 个

7. 匹配出的知识库文本文本作为上下文 Context 和问题⼀起添加到 prompt 中

8. 提交给 LLM 生成回答 Answer

具体项目结构如下图所示：
[![pAypn9x.jpg](https://s21.ax1x.com/2024/11/06/pAypn9x.jpg)](https://imgse.com/i/pAypn9x)

#### 1.3 项目运行

- 在.env 文件中配置环境变量

- 启动服务为本地 API

```shell
cd project
python api.py
```

- 运行项目

```shell
cd project
python run_gradio.py 
```

#### Acknowledgement
特别感谢 https://github.com/logan-zou/Chat_with_Datawhale_langchain 项目提供的灵感和支持。该项目为本项目的开发提供了宝贵的参考和帮助。