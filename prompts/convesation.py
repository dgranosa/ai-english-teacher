from prompts.base import BasePrompter
from text_to_speech import text_to_speech


class ConversationPrompter(BasePrompter):
    def __init__(self, model, config):
        super().__init__(model)

        self.topic = config['topic']
        self.subtopic = config['subtopic']

    @staticmethod
    def config():
        return {
            'topic': 'General Conversation',
            'subtopic': ['Today', 'Travel']
        }
    
    def __call__(self, messages, num_messages=7):
        messages = self.generate_messages(messages, num_messages)
        result = self.model.invoke(messages)
        audio = text_to_speech(result.content)
        return {'is_user': False, 'message': result.content, 'audio': audio }

    def first_message(self):
        topic_message = {
            'Today': "Hi, how was your day today?",
            'Travel': "What is the last place you traveled to?"
        }
        
        return topic_message[self.subtopic]
    
    def generate_base_prompt(self):
        topic_description = {
            'Today': "Let's have a conversation about today's day (where have I been, what have I done, who did I meet, ...).",
            'Travel': "Let's have a conversation about my last travel experience."
        }

        return f"""
You are my English teacher. We are having a conversation about various topics in English, but we are using only simple words and sentences.
When I make a grammatical error, please correct me and explain what I did wrong and how to correct it, but explain it in Croatian language (keep my sentences in English).
Then, in the next paragraph, continue the conversation in English. Keep your answers to 60 words or less.
If the conversation ever stalls, please ask me questions in the same context of the conversation.

---
Following is the structure if I don't make any grammatical errors:
[Continue the conversation in English]
---
Following is the structure if I make a grammatical error:
Ispravak: [Corrected English sentence with explanation of grammatical error in Croatian language]

[Continue the conversation in English]
---

{topic_description[self.subtopic]}
Start the conversation with a simple question.
"""