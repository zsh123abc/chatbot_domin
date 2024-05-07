import os
import json
from flask import Flask
from flask import request
from transformers import AutoTokenizer, AutoModel
import torch
import domin.prompts as prompts
import domin.config as con
from domin import text_favorability
# system params
# 根据好感度选择不同的提示词
pr = prompts.Prompt()
session_meta = pr.prompts_chatbot(favorability=con.favorability)
print(session_meta)
import os
# 设置环境变量，指定下载内容的缓存位置
os.environ['HF_DATASETS_CACHE'] = r'../model'
os.environ['TRANSFORMERS_CACHE'] = r'../model'


MODEL_PATH = r'../model/CharacterGLM-6b'  # 更新为你的模型路径
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def root():
    """root
    """
    return "Welcome to langchain_character model."

@app.route("/chat", methods=["POST"])
def chat():
    """chat
    """
    data_seq = request.get_data()
    data_dict = json.loads(data_seq)
    human_input = data_dict["human_input"]
    history = data_dict["history_input"]
    print('用户输入>>>',human_input)

    cur_input_favorability = text_favorability.get_text_favorability(human_input)
    con.favorability
    # 目前采用的是存本地json形式，后续改成langchain向量数据库的形式
    print('用户输入历史>>>',history)
    response,history= model.chat(tokenizer=tokenizer,max_length=512,history=history,query =  human_input,session_meta=session_meta)

    result_dict = {
        "response": response
    }
    result_seq = json.dumps(result_dict, ensure_ascii=False)
    print('模型输出>>>',result_seq)
    return result_seq

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8595, debug=False)