import langchain_memory.langchain_llms as langchain_llms
import requests
import json
import time

human_input = '喝茶还是咖啡'
history = [('', '你要和什么咖啡?')]
llm = langchain_llms.CharacterGLm()

begin_time = time.time() * 1000
# 请求模型
try:
    response = llm.invoke(human_input, stop=["you"],history=history)
    history_benlun = (human_input,response)
    history.append(history_benlun)
    print(response)
except Exception as e:
    print(f"Error: {e}")

end_time = time.time() * 1000
used_time = round(end_time - begin_time, 3)

