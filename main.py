# from pymilvus import MilvusClient

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)

connections.connect(db_name="default", host="localhost", port="19530")

# utility.drop_collection("hello_milvus")

fields = [
    FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="random", dtype=DataType.DOUBLE),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=8)
]
schema = CollectionSchema(fields, "hello_milvus is the simplest demo to introduce the APIs")
hello_milvus = Collection("hello_milvus", schema)
# hello_milvus_1 = Collection("hello_milvus_1", schema)


import random

entities = [
    [i for i in range(3000)],  # field pk
    [float(random.randrange(-20, -10)) for _ in range(3000)],  # field random
    [[random.random() for _ in range(8)] for _ in range(3000)],  # field embeddings
]

# print(entities)

insert_result = hello_milvus.insert(entities)

index = {
    "index_type": "IVF_FLAT",
    "metric_type": "COSINE",
    "params": {"nlist": 128},
}
hello_milvus.create_index("embeddings", index)

hello_milvus.load()
vectors_to_search = entities[-1][-2:]
search_params = {
    "metric_type": "COSINE",
    "params": {"nprobe": 10},
}
result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, output_fields=["random"])

result2 = hello_milvus.query(expr="random > -14", output_fields=["random", "embeddings"])

result = hello_milvus.search(vectors_to_search, "embeddings", search_params, limit=3, expr="random > -12", output_fields=["random"])

print(utility.list_collections())

# utility.drop_collection("hello_milvus")
