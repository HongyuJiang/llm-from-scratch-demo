from langchain.text_splitter import MarkdownTextSplitter


def naive_text_split(file_path, MAX_SEQ_LEN):
    all_texts = []
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    paragraphs = text.split('\n')  # 按换行符分割文本

    for paragraph in paragraphs:
        while len(paragraph) > MAX_SEQ_LEN:
            # 使用句号进一步分割
            split_paragraphs = paragraph.split('。', 1)
            paragraph = split_paragraphs[0]
            all_texts.append(split_paragraphs[1])

    all_texts.append(paragraph)

    return [{'question': '', 'answer': text.strip()} for text in all_texts]


def markdown_text_split(file_path, MAX_SEQ_LEN):
    markdown_splitter = MarkdownTextSplitter(chunk_size=256, chunk_overlap=32)
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    docs = markdown_splitter.create_documents([markdown_text])

    return [{'question': '', 'answer': doc.page_content} for doc in docs]