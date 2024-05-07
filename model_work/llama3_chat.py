from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained('F:\models\meta-llama\Meta-Llama-3-8B-Instruct')
model = AutoModelForCausalLM.from_pretrained('F:\models\meta-llama\Meta-Llama-3-8B-Instruct',torch_dtype=torch.bfloat16).cuda()
inputs = '我去年和你说过去开房吗?'
messages = [
    {"role": "system", "content": """You need to judge whether the user wants to query history. If yes, output [1], otherwise output [0]. For example,
    input: What did I just say?  
    output: [1]
    """},
    {"role": "user", "content": f"input:{inputs} output:"},
]

messages_history = [
    {"role": "system", "content": """你需要对用户的输入内容进行查询对用户输入的历史对话进行,
    input: What did I just say?  
    output: [1]
    """},
    {"role": "user", "content": f"input:{inputs} output:"},
]
print(messages_history)

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
    temperature=0.6,
    top_p=0.9,
)
response = outputs[0][input_ids.shape[-1]:]
print(tokenizer.decode(response, skip_special_tokens=True))
