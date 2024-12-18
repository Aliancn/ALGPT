# from database.create_db import create_db


# def test_create_db():
#     vectordb = create_db()

#     question = "色彩"

#     sim_docs = vectordb.similarity_search(question, k=10)
#     print(f"检索到的内容数：{len(sim_docs)}")
#     assert True


# if __name__ == "__main__":
#     test_create_db()


# from chain.QA_chain_self import QA_chain_self

# if __name__ == '__main__':
#     qa_chain = QA_chain_self(model='glm-4', temperature=0.6,
#                              top_k=6, file_path='./database/knowledge_db', persist_path='./vector_db/', embedding='m3e')
#     # question = "梅二的规定有哪些？"
#     question = "数据库报告中数据库的架构是什么？"
#     print(qa_chain.answer(question=question))




