# 项目结构 
    

```
    character_setting
    |---user_men.json 用户为男性 即 ai为女性
    |---user_women.json 用户为女性 即 ai为男性
    |---定义角色的示例.json 自定义角色的示例 
    
    domin 对话管理
    |---caht-flow  对话流程[未开发]
    |---config  设置[参数] （设置好感度）
    |---prompt  选择提示词[目前只有小白 未来计划加入自定义模块] （根据不同的好感度选择不同的提示词，检索本地文件）
    |---conversational_judgment.py  中控llm选择提示词  （查找用户历史对话 or 判断用户想干什么）
    |---text_favorability.py  情感分析文本
    
    langchain_memory langchain对话模块 [计划开发历史]
    |---langchain_character.py    character模型的flaskapi
    |---langchian_llama3.py     llama3.py模型的flaskapi
    |---langchain_llms.py 自定义langchain模型的api连接
    |---langchain_embdedding_bge.py langchian短途历史【使用bge模型和charmadb矢量数据库来达到效果 正在开发】
    |---langchian_llama3_history.py 用llama3查询历史
    
    lin_xin_demo 官方demo
    |---character.json 提示词
    |---web_demo_streamlit.py 官方网页demo  # 
    
    model 模型下载文件夹

    model_work 模型
    |---CharacterGLM_6b.py 开放fast api
    |---CharacterGLM_6b_api.py 连接fast api
    |---yi_6b.py 暂定模型控制
```

```
　　 へ　　　　　／|
　　/＼7　　∠＿/
　 /　│　　 ／　／
　│　Z ＿,＜　／　　 /`ヽ
　│　　　　　ヽ　　 /　　〉
　 Y　　　　　`　 /　　/
　ｲ●　､　●　　⊂⊃〈　　/
　()　 へ　　　　|　＼〈
　　>ｰ ､_　 ィ　 │ ／／
　 / へ　　 /　ﾉ＜| ＼＼
　 ヽ_ﾉ　　(_／　 │／／
　　7　　　　　　　|／
　　＞―r￣￣`ｰ―＿
```