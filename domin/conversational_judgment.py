from datetime import datetime
import langchain_memory.langchain_llms as langchain_llms
def user_history(user_input,history):  # 查找用户的对话历史

    query_huifang_historical_replay = [
        # 例子：
        {"role": "system", "content": f"""你要找到用户的对话中提到的对话历史根据已知信息来搜集和总结对话历史:例如,
        input: 我昨天和你说什么了?  
        Today's time: 2023-04-20 17:13:29.843463
        history : [('', '哥哥，我会死吗？','2023-4-19'), ('不会的', '真的吗？那我可以放心的活下去对吗？','2023-4-19'), ('是的', '那我要努力的活下去','2023-4-20'),
     ('嗯,加油', '哥哥,如果有一天我不在了,你怎么办?','2023-4-20'), ('我会很伤心', '我怕我不在了,你就再也找不到你最好的朋友了','2023-4-20')]
        output: 你和我说我不会死
        """},
        # 用户具体的输入和具体的历史对话
        {"role": "user", "content": f"input:{user_input}  history: {history}output:"},
    ]
    return query_huifang_historical_replay

def Determine_use(user_input):# 判断用户想干什么
    query_history = [
        # 例子，给大模型对照的例子
        {"role": "system", "content": """You need to judge whether the user wants to query history. If yes, output [1], otherwise output [0]. For example,
            input: What did I just say?  
            output: [1]
            """},
        # 用户的当前输入
        {"role": "user", "content": f"input:{user_input} output:"},
    ]
    return query_history

if __name__ == '__main__':
    history = [('', '哥哥，我会死吗？','2024-4-19'), ('不会的', '真的吗？那我可以放心的活下去对吗？','2024-4-20'), ('是的', '那我要努力的活下去','2023-4-20'),
     ('嗯,加油', '哥哥,如果有一天我不在了,你怎么办?','2024-4-20'), ('我会很伤心', '我怕我不在了,你就再也找不到你最好的朋友了','2024-4-20')]

    model = langchain_llms.llama3_()
    print("对话历史:",history)
    user_input = '我昨天说了什么?'
    print('用户输入:',user_input)
    con= user_history(user_input,history)
    print(con)
    res = model._call(prompt=con)
    print('模型输出',res)