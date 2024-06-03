from loguru import logger
from driver.llm import chat
from prompt.wrapper import PromptWrapper


class GeneralStep:
    @staticmethod
    def rewrite_query(history, user_query):
        # format history to string with content and role
        prompt_processor = PromptWrapper()
        history_str = ''
        for item in history[:8]:
            history_str += f"{item['role']}: {item['content']} \n"
    
        prompt = prompt_processor.assemble('rewrite', {
            "history": history_str,
            "user_query": user_query
        })

        logger.info(f"Rewrite query prompt: {prompt}")

        result = chat(prompt)
        logger.info(f"Rewrite query result: {result}")
        return result