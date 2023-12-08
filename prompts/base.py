from langchain.schema import HumanMessage, SystemMessage, AIMessage

class BasePrompter:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def config():
        return {}

    def __call__(self, messages, num_messages=7):
        messages = self.generate_messages(messages, num_messages)
        result = self.model.invoke(messages)
        return {'is_user': False, 'message': result.content }
    
    def first_message(self):
        return ""
    
    def generate_base_prompt(self):
        return ""
        
    def generate_messages(self, messages, num_messages=7):
        base_prompt = self.generate_base_prompt()

        result = []
        result.append(SystemMessage(content=base_prompt))
        for chat in messages[-num_messages:]:
            if chat['is_user']:
                result.append(HumanMessage(content=chat['message']))
            else:
                result.append(AIMessage(content=chat['message']))

        return result