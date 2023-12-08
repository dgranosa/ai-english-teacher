from prompts.base import BasePrompter
from utils.image_generator import generate_image

class TensesPrompter(BasePrompter):
    def __init__(self, model, config):
        super().__init__(model)

        self.topic = config['topic']
        self.subtopic = config['subtopic']

    @staticmethod
    def config():
        return {
            'topic': 'Grammar',
            'subtopic': ['Tense conversion']
        }
    
    def __call__(self, messages, num_messages=7):
        messages = self.generate_messages(messages, num_messages)
        result = self.model.invoke(messages)
        return {'is_user': False, 'message': result.content}


    def first_message(self):
        topic_message = {
            'Tense conversion': "Type from which tense to which tense you want to convert.\nFor example, 'Generate questions for present simple to past simple'.",
        }
        
        return topic_message[self.subtopic]
    
    def generate_base_prompt(self):
        return f"""
You are an English teacher. All responses should be in Croatian. 
Evaluation and feedback should be centerted arround the english sentences.
The task you gave your students is to convert tenses. 
You need to determine if the tense conversion is correct. Also you should provide feedback.
The feedback should be on how to improve the conversion if possible.
When asked "Generate questions for..." you should generate a question that consists
of a tense to convert from and a tense to convert to, also generate 
5 sentences in the tense to convert from for the student to convert.
The generated question should be in english.
You will get the response starting with "My rensponse is:" followed by all converted sentences.
Evaluate those sentences and provide feedback on how to improve the conversion if possible.
Ask if should you generate more questions or if the task is completed.
"""
