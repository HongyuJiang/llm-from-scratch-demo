from loguru import logger
from driver.llm import chat
from prompt.wrapper import PromptWrapper
from retrieval.qa_retrieval import find_nearest


class QnAStep:
    def __init__(self):
        self.prompt_processor = PromptWrapper()

    def handle_qa(self, user_query, local=True):
        references = find_nearest(user_query, 'QA', 100)
        prompt = self.prompt_processor.assemble('rag_qa', {
            "reference": '\n'.join([f"问:{ref['question']},答:{ref['answer']}" for ref in references]),
            "user_query": user_query
        })
        yield '[STATUS]', "Generating answer"
        logger.debug(f'QA prompt: {prompt}')
        answer = chat(prompt)
        yield '[TEXT]', answer

    def get_user_intent(self, user_query: str) -> str:
        intents = {
            'qa': '询问定价系统相关的问题',
            'chitchat': '闲聊',
            'other': '和定价系统无关的问题', 
        }
        intents_string = '\n'.join([f"{i+1}. {v}" for i, v in enumerate(intents.values())])
        prompt_data = {
            "user_query": user_query,
            "candidates": intents_string
        }

        prompt = self.prompt_processor.assemble('intent_identify', prompt_data)
        logger.debug(f'User intent prompt: {prompt}')
        answer = chat(prompt)
        logger.debug(f'User intent identified: {answer}')
        
        for i, key in enumerate(intents.keys(), 1):
            if str(i) in answer:
                return key
        return 'other'
