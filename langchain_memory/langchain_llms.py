import time
import logging
import requests
from typing import Optional, List, Dict, Mapping, Any

import langchain
from langchain.llms.base import LLM
from langchain.cache import InMemoryCache

logging.basicConfig(level=logging.INFO)

# 启动llm的缓存
langchain.llm_cache = InMemoryCache()


class CharacterGLm(LLM):
    # characte模型服务url
    url = "http://127.0.0.1:8595/chat"

    @property
    def _llm_type(self) -> str:
        return "chatglm"

    def _construct_query(self, prompt: str,history:list) -> Dict:
        """构造请求体"""
        query = {
            "human_input": prompt,
            "history_input":history
        }
        return query

    @classmethod
    def _post(cls, url: str, query: Dict) -> Any:
        """POST请求"""
        _headers = {"Content-Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url, json=query, headers=_headers, timeout=60)
        return resp

    def _call(self, prompt: str,history:list, stop: Optional[List[str]] = None,) -> str:
        """调用模型并返回预测结果"""
        # construct query
        query = self._construct_query(prompt=prompt, history=history)

        # post
        resp = self._post(url=self.url, query=query)

        if resp.status_code == 200:
            resp_json = resp.json()
            try:
                predictions = resp_json["response"]
                # 确保返回的是字符串类型
                if isinstance(predictions, str):
                    return predictions
                else:
                    return predictions[0]
            except KeyError:
                raise ValueError("模型返回的JSON格式不正确，未找到'response'键。")
        else:
            raise RuntimeError(f"请求模型失败，HTTP状态码：{resp.status_code}")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        _param_dict = {
            "url": self.url
        }
        return _param_dict

class llama3_(LLM):
    # llama3模型服务url
    url = "http://127.0.0.1:8001/chat_lama"

    @property
    def _llm_type(self) -> str:
        return "llama3"

    def _construct_query(self, prompt: str,) -> Dict:
        """构造请求体"""
        query = prompt
        return query

    @classmethod
    def _post(cls, url: str, query: Dict) -> Any:
        """POST请求"""
        _headers = {"Content-Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url, json=query, headers=_headers, timeout=60)
        return resp

    def _call(self, prompt: str, stop: Optional[List[str]] = None,) -> str:
        """调用模型并返回预测结果"""
        # construct query
        query = self._construct_query(prompt=prompt)

        # post
        resp = self._post(url=self.url, query=query)

        if resp.status_code == 200:
            resp_json = resp
            print(resp_json)

            # 假设服务器返回的JSON中有一个'text'键包含了预测的文本
            predictions_text = resp_json  # 如果没有'text'键，就返回空字符串
            print("predictions_text:", predictions_text)

            return predictions_text  # 确保返回的是一个字符串
        else:
            raise RuntimeError(f"请求模型失败，HTTP状态码：{resp.status_code}")

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        _param_dict = {
            "url": self.url
        }
        return _param_dict


if __name__ == "__main__":
    llm = CharacterGLm()
    # history = [('', '打扰一下，麻烦您让个座')]
    history = []
    while True:
        human_input = input("Human: ")

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
        used_time = round(end_time - begin_time, 3)
        logging.info(f"CharacterGLM process time: {used_time}ms")

    # llm = llama3_()
    # # history = [('', '打扰一下，麻烦您让个座')]
    # query_huifang_historical_replay = [
    #     {"role": "system", "content": f"""你要找到用户的对话中提到的对话历史根据已知信息来搜集和总结对话历史:例如,
    #         input: 我昨天和你说什么了?
    #         Today's time: 2023-04-20 17:13:29.843463
    #         history : [('', '哥哥，我会死吗？','2023-4-19'), ('不会的', '真的吗？那我可以放心的活下去对吗？','2023-4-19'), ('是的', '那我要努力的活下去','2023-4-20'),
    #      ('嗯,加油', '哥哥,如果有一天我不在了,你怎么办?','2023-4-20'), ('我会很伤心', '我怕我不在了,你就再也找不到你最好的朋友了','2023-4-20')]
    #         output: 你和我说我不会死
    #         """},
    #     {"role": "user", "content": f"我昨天和你说什么了?"},
    # ]
    # human_input = query_huifang_historical_replay
    #
    # begin_time = time.time() * 1000
    # # 请求模型
    # response = llm._call(prompt=human_input)
    # print(response)
    #
    #
    # end_time = time.time() * 1000
    # used_time = round(end_time - begin_time, 3)
    # logging.info(f"CharacterGLM process time: {used_time}ms")