from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer
import torch

negative = -1
positive = 1

def get_text_favorability(input):
    """根据用户输入文本情感分析判断 积极还是消极，后续可以发展，评分机制，一般消极和非常消极扣分不一样"""

    tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment')
    model=AutoModelForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment')

    output=model(torch.tensor([tokenizer.encode(input)]))
    # print(torch.nn.functional.softmax(output.logits,dim=-1))
    softmax = torch.nn.functional.softmax(output.logits, dim=-1)

    negative_probability = softmax[0][0].item() # 消极
    positive_probability = softmax[0][1].item() # 积极

    # 判断情绪
    if positive_probability > negative_probability:
        return negative
    else:
        return positive