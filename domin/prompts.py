import os
import json
import domin.config as cn

class Prompt(object):
    def __init__(self):
        self.session_meta = {
            'stranger': {
                'description': '初次相识',
            },
            'acquaintance': {
                'description': '十分熟悉',
            },
            'friend': {
                'description': '男女朋友',
            },
            'close_friend': {
                'description': '夫妻关系',
            }
        }

    def get_relationship_level(self, favorability):
        """根据好感度返回关系级别"""
        if 0 <= favorability < 25:
            return 'stranger' #
        elif 25 <= favorability < 50:
            return 'acquaintance'
        elif 50 <= favorability < 75:
            return 'friend'
        elif 75 <= favorability <= 100:
            return 'close_friend'
        else:
            return 'unknown'

    def get_session_meta(self, favorability):
        """根据好感度获取会话元数据"""
        # 元数据指的是 初次相识 ，十分熟悉 ， 男女朋友 ， 夫妻关系
        level = self.get_relationship_level(favorability)
        return self.session_meta.get(level, {})

    def find_bot_name_in_jsonl(self, bot_id):
        """查找bot_id对应的一整条数据"""

        # 检查文件是否存在
        file_path = r'../character_setting/user_men.jsonl'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

            # 尝试打开并读取文件
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        data = json.loads(line)  # 解析每一行的JSON数据
                        # 使用递归函数在数据中查找指定的bot_name
                        if bot_id == data['bot_id']:
                            return data
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON: {line}")
                        continue  # 如果某行不是有效的JSON，则 跳过该行并继续处理下一行
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return '无法读取文件'  # 如果无法读取文件，则返回None
        return '遍历完整个文件都没有找到指定的bot_name' # 如果遍历完整个文件都没有找到指定的bot_name，则返回None

    def prompts_chatbot(self, favorability):
        """根据bot_id查询对应的聊天状态，然后在查询不同聊天状态对应的角色介绍 user_info，bot_name，user_name"""

        # 根据bot_id获取数据
        bot_name = self.find_bot_name_in_jsonl(cn.bot_id)
        # 根据不同key拿到不同的val，代表不同的聊天状态
        session_meta_first_meeting = bot_name['session_meta_first_meeting'] # 初次相识
        session_meta_acquaintance = bot_name['session_meta_acquaintance'] # 十分熟悉
        session_meta_boy_gril = bot_name['session_meta_boy_gril'] # 男女朋友
        session_meta_man_wife = bot_name['session_meta_man_wife'] # 夫妻关系
        # 获取 好感度对应的val
        level = self.get_relationship_level(favorability)
        # 根据不同的val返回不同的 聊天状态
        if level == 'stranger':
            return session_meta_first_meeting
        elif level == 'acquaintance':
            return session_meta_acquaintance
        elif level == 'friend':
            return session_meta_boy_gril
        elif level == 'close_friend':
            return session_meta_man_wife
        else:
            # 都没有就返回未知
            return 'unknown'

    # 使用示例
if __name__ == '__main__':
    prompt_instance = Prompt()
    favorability = 60  # 假设当前的好感度
    session_meta = prompt_instance.get_session_meta(favorability)
    bot_name = prompt_instance.find_bot_name_in_jsonl('小白')
    print(f"当前好感度级别是：{prompt_instance.get_relationship_level(favorability)}")
    print(f"相关的会话元数据是：{session_meta}")
    print(prompt_instance.prompts_chatbot(favorability))