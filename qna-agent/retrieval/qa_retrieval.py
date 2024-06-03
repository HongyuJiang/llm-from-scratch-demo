import configparser
import os
import faiss
import numpy as np
import torch
import pickle

from sentence_transformers import SentenceTransformer
import time

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../', 'config.ini'))
model_path = config['embedding']['model_path']
embedding_len = config['embedding']['dimension']

# Load data from pickle file
pickle_path = os.path.join(os.path.dirname(__file__), './artifacts/embeddings.bin')
with open(pickle_path, 'rb') as file:
    data = pickle.load(file)

# Group data by domain
data_by_domain = {}
for d in data:
    domain = d['domain']
    if domain not in data_by_domain:
        data_by_domain[domain] = []
    data_by_domain[domain].append(d)

# Initialize Faiss indexes for each domain
indexes = {}
for domain, domain_data in data_by_domain.items():
    vectors = [d['embedding'] for d in domain_data]
    texts = [d['answer'] for d in domain_data]

    dim = int(embedding_len)  # Vector dimension
    k = 3
    measure = faiss.METRIC_L2
    param = 'HNSW64'
    index = faiss.index_factory(dim, param, measure)
    index_transform = faiss.IndexPreTransform(index)
    print(f"Transforming vectors for domain {domain}...")
    index_transform.train(np.array(vectors, dtype=np.float32))
    index_transform.add(np.array(vectors, dtype=np.float32))
    index_path = os.path.join(os.path.dirname(__file__), f"./artifacts/faiss_{domain}.index")
    faiss.write_index(index_transform, index_path)
    indexes[domain] = index_transform

# Load HuggingFace model and tokenizer
model = SentenceTransformer('aspire/acge_text_embedding')


def find_nearest(text: str, domain: str, threshold: float = 100):
    start_time = time.time()

    with torch.no_grad():
        user_query_vector = model.encode([text], normalize_embeddings=True)

    # Convert the tensor to a list
    embedding_list = user_query_vector.tolist()[0]

    # Perform Faiss search
    index_transform = indexes.get(domain)
    if index_transform is None:
        return []  # No data for the given domain

    D, I = index_transform.search(np.array([embedding_list], dtype=np.float32), k)

    # Retrieve the text corresponding to the retrieved embeddings
    domain_data = data_by_domain[domain]
    hits = [domain_data[i] for i, d in zip(I[0], D[0]) if d < threshold]

    return hits

if __name__ == '__main__':
    print(find_nearest('什么是对公存款', 'QA', 100))