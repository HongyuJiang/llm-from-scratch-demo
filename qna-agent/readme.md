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

1. 初始化 Faiss 向量库, 仅当首次运行和 resource/qa 中文件有修改时需要重新运行，首次运行将下载预训练模型权重，时间较长。该步骤将对resouce/qa/下的所有文件根据不同类型进行向量化。目前已支持 txt、csv、md 三种类型。
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