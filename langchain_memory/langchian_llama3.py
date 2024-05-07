import os
import json

from flask import Flask
from flask import request
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
import torch
import domin.prompts as prompts
import domin.config as con

# system params


MODEL_PATH = r'F:\models\meta-llama\Meta-Llama-3-8B-Instruct'  # 更新为你的模型路径
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, trust_remote_code=True, torch_dtype=torch.bfloat16)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def root():
    """root
    """
    return "Welcome to langchain_character model."

@app.route("/chat_lama", methods=["POST"])
def chat():
    """chat
    """
    data_seq = request.get_data()
    data_dict = json.loads(data_seq)
    messages = data_dict
    print('用户输入>>>',messages)

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.001,
        top_p=0.1,
    )
    response = outputs[0][input_ids.shape[-1]:]
    result_seq = tokenizer.decode(response, skip_special_tokens=True)
    # response = str(result_seq)
    response = result_seq
    print('模型输出结果>>>',response)

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)