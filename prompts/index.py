from prompts.convesation import ConversationPrompter
from prompts.tv_convesation import TvConvesationPrompter

prompters = [ConversationPrompter, TvConvesationPrompter]

def get_all_configs():
    configs = {}
    for prompter in prompters:
        config = prompter.config()
        if config['topic'] not in configs:
            configs[config['topic']] = []

        configs[config['topic']] += config['subtopic']
    return configs

def get_prompter(topic, subtopic):
    for prompter in prompters:
        config = prompter.config()
        if config['topic'] == topic and subtopic in config['subtopic']:
            return prompter

    return None