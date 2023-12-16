from prompts.base import BasePrompter
from utils.image_generator import generate_image

class VocabularyPrompter(BasePrompter):
    def __init__(self, model, config):
        super().__init__(model)

        self.topic = config['topic']
        self.subtopic = config['subtopic']

    @staticmethod
    def config():
        return {
            'topic': 'Vocabulary',
            'subtopic': ['Quiz']
        }
    
    def __call__(self, messages, num_messages=7):
        messages = self.generate_messages(messages, num_messages)
        result = self.model.invoke(messages)
        return {'is_user': False, 'message': result.content}


    def first_message(self):
        topic_message = {
            'Quiz': "Type start to start the quiz.",
        }
        
        return topic_message[self.subtopic]
    
    def generate_base_prompt(self):
        return f"""
Generate a english vocabulary quiz.
If student answers correctly multiple times, you can give them a harder questions. If student answers incorrectly multiple times, you can give them an easier question.
"""
