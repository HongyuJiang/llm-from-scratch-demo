# Startup for QA Agent

### Model usages
* LLM：deepseek-v2-chat
* Embedding：acge_text_embedding
* Vector Comp Lib：Faiss

### 运行步骤

1. 申请模型 API
https://www.deepseek.com


2. 配置 LLM_API_KEY 和 PYTHONPATH
```shell
export LLM_API_KEY=<YOUR DEEPSEEK API KEY>
export PYTHONPATH=$(pwd):$PYTHONPATH
```

3. 初始化 Faiss 向量库, 仅当首次运行和 resource/qa 中文件有修改时需要重新运行
```shell
python retrieval/qa_embedding.py
```

4.1 本地运行 QnA Agent 入口 
```shell
python core/qna_entry.py 
```

4.2 作为 API 运行
```shell
python api.py
```