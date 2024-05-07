import os
from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import torch
import domin.prompts as prompts
import domin.config as con
from typing import List



app = FastAPI()

MODEL_PATH = 'F:/models/CharacterGLM-6b'  # 更新为你的模型路径
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

pr = prompts.Prompt()
session_meta = pr.prompts_chatbot(favorability=con.favorability)

class ChatInput(BaseModel):
    text: str


@app.post("/chat/")
async def chat(input: ChatInput):
    query = input.text
    if query.strip() == "stop":
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Chat stopped")

        # 这里可以添加处理"clear"命令的逻辑，如果需要的话

    # 与模型交互并获取响应
    # 注意：这里的stream_chat方法可能需+要根据你的模型库进行相应的调整
    responses = []
    for response in model.chat(tokenizer=tokenizer, session_meta=session_meta, query=query):
        responses.append(response)
        print(response)
        # list_.append(_[-1])
    return {'response':responses}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)