import json
import sys
from pymilvus import MilvusClient

if len(sys.argv) == 3:
    file_name = sys.argv[1]
    collection_name = sys.argv[2]
else:
    raise Exception("Usage: uploadVector.py <FileName> <CollectionName>")

# 创建Milvus客户端连接
client = MilvusClient(
    uri="http://localhost:19530"
)
with open(file_name, "r") as f:
    data = json.loads(f.read())
    res = client.insert(
        collection_name=collection_name,
        data=data
    )
print("Upload Vector Success.")