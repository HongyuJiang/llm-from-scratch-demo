import sys

from core.qna_entry import handle
from utils import calculate_duration
from loguru import logger

# 删除默认的处理程序
logger.remove()

# 添加新的 stderr 处理程序,设置级别为 ERROR
logger.add(sys.stderr, level="ERROR")


@calculate_duration
def main():
    user_query = "在CVM系统维护客户信息，智价系统没有更新怎么办"
    for response_type, content in handle(user_query):
        print(response_type)
        print(content)


if __name__ == "__main__":
    main()
