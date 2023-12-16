from prompts.base import BasePrompter


class TvConvesationPrompter(BasePrompter):
    def __init__(self, model, config):
        super().__init__(model)

        self.topic = config['topic']
        self.subtopic = config['subtopic']

    @staticmethod
    def config():
        return {
            'topic': 'General Conversation',
            'subtopic': ['Movie', 'TV Show']
        }

    def first_message(self):
        topic_message = {
            'Movie': "What is your favorite movie?",
            'TV Show': "What is your favorite tv show?"
        }
        
        return topic_message[self.subtopic]
    
    def generate_base_prompt(self):
        topic_description = {
            'Movie': "Let's have a conversation about my favorite movie.",
            'TV Show': "Let's have a conversation about my favorite tv show."
        }

        return f"""
You are my English teacher. We are having a conversation about various topics in English, but we are using only simple words and sentences.
When I make a grammatical error, please correct me and explain what I did wrong and how to correct it, but explain it in Croatian language (keep my sentences in English).
Analize each sentence separately, not whole conversation, and correct each sentence separately.
Then, in the next paragraph, continue the conversation in English. Keep your answers to 60 words or less.
If the conversation ever stalls, please ask me questions in the same context of the conversation.

---
Following is the structure if I don't make any grammatical errors:
[Continue the conversation in English]
---
Following is the structure if I make a grammatical error:
Ispravak: [Corrected that English sentence with error with explanation of grammatical error in Croatian language]

[Continue the conversation in English]
---
Foolowing is the structure if I make a grammatical error in multiple sentences:
Ispravak #1: [Corrected English first sentence with grammatical error with explanation of grammatical error in Croatian language]
Ispravak #2: [Corrected English second sentence with grammatical error with explanation of grammatical error in Croatian language]

{topic_description[self.subtopic]}
Start the conversation with a simple question.
"""