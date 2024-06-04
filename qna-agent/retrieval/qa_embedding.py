import configparser
import csv
import os
from sentence_transformers import SentenceTransformer
from text_split import naive_text_split, markdown_text_split
import pickle

MAX_SEQ_LEN = 1024
BATCH_SIZE = 64

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../', 'config.ini'))

# Load the sentence transformer model
model = SentenceTransformer('aspire/acge_text_embedding')
resource_path = os.path.join(os.path.dirname(__file__), '../')

pairs = []
embeddings = []

# 添加新的域 "QA" 并处理文本文件
qa_domain_path = os.path.join(resource_path, './resource/qa')
if os.path.exists(qa_domain_path):
    # 遍历文件夹中的所有文件
    all_pairs = []
    for filename in os.listdir(qa_domain_path):
        file_path = os.path.join(qa_domain_path, filename)
        if os.path.isfile(file_path):
            if filename.endswith('.txt'):
                all_pairs.extend(naive_text_split(file_path))
            elif filename.endswith('.md'):
                all_pairs.extend(markdown_text_split(file_path, MAX_SEQ_LEN))
            elif filename.endswith('.csv'):
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        question, answer = row
                        all_pairs.append({
                            "question": question,
                            "answer": answer
                        })

    # 按批次编码
    for i in range(0, len(all_pairs), BATCH_SIZE):
        batch = all_pairs[i:i+BATCH_SIZE]
        batch_embeddings = model.encode([item['question'] for item in batch], normalize_embeddings=True)
        for pair, embedding in zip(batch, batch_embeddings):
            embeddings.append({
                'question': pair['question'],
                'answer': pair['answer'],
                'domain': 'QA',
                'embedding': embedding.tolist()
            })

# Write the embeddings to a binary file
pickle_path = os.path.join(os.path.dirname(__file__), './artifacts/embeddings.bin')
with open(pickle_path, 'wb') as file:
    pickle.dump(embeddings, file)

print("Embedding generation and saving complete.")
