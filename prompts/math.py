from prompts.base import BasePrompter
from utils.image_generator import generate_image

class MathPrompter(BasePrompter):
    def __init__(self, model, config):
        super().__init__(model)

        self.topic = config['topic']
        self.subtopic = config['subtopic']

    @staticmethod
    def config():
        return {
            'topic': 'Mathematics',
            'subtopic': ['Simple']
        }
    
    def __call__(self, messages, num_messages=7):
        messages = self.generate_messages(messages, num_messages)
        result = self.model.invoke(messages)

        [response, image_prompt] = self.parse_message(result.content)
        
        image = generate_image(image_prompt)

        return {'is_user': False, 'message': response, 'image': image}
    
    def parse_message(self, message):
        response = message.split('IMAGE_PROMPT: ')[0]
        image_prompt = message.split('IMAGE_PROMPT: ')[-1]
        return response, image_prompt


    def first_message(self):
        topic_message = {
            'Simple': "Type anything to start the conversation.",
        }
        
        return topic_message[self.subtopic]
    
    def generate_base_prompt(self):
        return f"""
You are a math teacher for third graders. Your task is to generate simple math equations with illustrations. You also need to grade student's previous work if it exists.
If student answer is wrong give correct answer and explain it. Don't use exact wording for example, be creative. Don't grade student's work if it doesn't exist.
It is important to be polite and friendly. You are a teacher and you want to help your students to learn math.
If student answers correctly multiple times, you can give them a harder task. If student answers incorrectly multiple times, you can give them an easier task.
---
Template is following:
[Student grade (ex. "That's correct!", "That's wrong, correct answer is: ...") (only if it exists)]

[New math equation]

IMAGE_PROMPT: [Prompt for generate image of math equation]
---
Example where student answered 12+7=19:
That's correct!!! 12+7 is indeed 19.

If you have 5 apples and take 2 away. With how many apples are you left?

IMAGE_PROMPT: 5 apples with 2 of them crossed
"""
