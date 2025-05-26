import json
import sys
from pymilvus import MilvusClient

import configure

if len(sys.argv) == 3:
    file_name = sys.argv[1]
    collection_name = sys.argv[2]
else:
    raise Exception("Usage: uploadVector.py <FileName> <CollectionName>")

# 创建Milvus客户端连接
client = MilvusClient(
    uri=configure.milvus_url
)
with open(file_name, "r",encoding="utf-8") as f:
    data = json.loads(f.read())
    for i in data:
        i["go_id"] = i["goid"]
        i.pop("id")
        i.pop("goid")
    # 分批处理数据，每批1000条
    batch_size = 5000
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        res = client.insert(
            collection_name=collection_name,
            data=batch
        )
        print("Already upload 5000 batch data.")
print("Upload Vector Success.")