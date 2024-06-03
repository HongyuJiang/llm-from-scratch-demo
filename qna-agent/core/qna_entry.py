from loguru import logger
from step.qna import QnAStep

llm_step = QnAStep()


def handle(user_query, history=[], local=True):
    if history:
        all_user_input = history + [user_query]
        user_query = ','.join(all_user_input)

    yield '[START]', None
    user_intent = llm_step.get_user_intent(user_query)
    logger.info(f'User intent: {user_intent}')
    yield '[STATUS]', "Analyzing"
    if user_intent == 'qa':
        for step in llm_step.handle_qa(user_query, local):
            yield step
    else:
        yield '[TEXT]', "Sorry, I don't understand your question."
    yield '[END]', None


if __name__ == '__main__':
    user_query = '刚在CVM系统维护客户信息，智价系统没有更新怎么办'
    for step in handle(user_query):
        print(step)