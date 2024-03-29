from prompts.math import MathPrompter
from prompts.convesation import ConversationPrompter
from prompts.tesnses import TensesPrompter
from prompts.tv_convesation import TvConvesationPrompter
from prompts.vocabulary import VocabularyPrompter

prompters = [ConversationPrompter, TvConvesationPrompter, MathPrompter, VocabularyPrompter, TensesPrompter]

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