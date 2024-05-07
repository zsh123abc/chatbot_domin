from datetime import datetime
import langchain_memory.langchain_llms as langchain_llms
from domin import conversational_judgment





history = [('', '哥哥，我会死吗？','2024-4-19'), ('不会的', '真的吗？那我可以放心的活下去对吗？','2024-4-20'), ('是的', '那我要努力的活下去','2023-4-20'),
     ('嗯,加油', '哥哥,如果有一天我不在了,你怎么办?','2024-4-20'), ('我会很伤心', '我怕我不在了,你就再也找不到你最好的朋友了','2024-4-20')]
# 实例 llama3 模型
model = langchain_llms.llama3_()
print("对话历史:",history)
user_input = '我昨天说了什么?'
# 用户输入：我昨天说了什么，
# 回答：对应的历史记录
con= conversational_judgment.user_history(user_input,history)
print(con)
print('用户输入:',user_input)
res = model._call(prompt=con)
print('模型输出',res)