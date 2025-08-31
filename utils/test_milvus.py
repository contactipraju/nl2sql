# save as test_milvus.py and run: python test_milvus.py
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import random
import time

HOST = "127.0.0.1"
PORT = "19530"
TEST_COLLECTION = "health_check_demo"

def wait_for_ready(retries=30, delay=2):
    for i in range(retries):
        try:
            connections.connect(host=HOST, port=PORT, timeout=2)
            # A simple call that requires server readiness
            ver = utility.get_server_version()
            print(f"Connected. Milvus version: {ver}")
            return True
        except Exception as e:
            print(f"Attempt {i+1}/{retries} not ready yet: {e}")
            time.sleep(delay)
    return False

def ensure_collection():
    if utility.has_collection(TEST_COLLECTION):
        utility.drop_collection(TEST_COLLECTION)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=4),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=128)
    ]
    schema = CollectionSchema(fields, description="health check collection")
    coll = Collection(name=TEST_COLLECTION, schema=schema)
    return coll

def main():
    if not wait_for_ready():
        print("Milvus did not become ready in time.")
        return

    # Create a small collection
    coll = ensure_collection()
    print("Created collection.")

    # Insert a couple of rows
    rng = random.Random(42)
    ids = [1, 2, 3]
    vectors = [[rng.random() for _ in range(4)] for _ in ids]
    texts = [f"row-{i}" for i in ids]
    mr = coll.insert([ids, vectors, texts])
    print(f"Inserted {mr.insert_count} rows.")

    # Build index and load
    coll.create_index("vector", {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 16}})
    coll.load()
    print("Index created and collection loaded.")

    # Simple vector search
    query_vec = [0.5, 0.5, 0.5, 0.5]
    res = coll.search(
        data=[query_vec],
        anns_field="vector",
        param={"metric_type": "L2", "params": {"nprobe": 8}},
        limit=2,
        output_fields=["text"]
    )
    for hits in res:
        for hit in hits:
            print(f"Hit id={hit.id}, distance={hit.distance:.4f}, text={hit.entity.get('text')}")

    # Cleanup (optional)
    coll.release()
    utility.drop_collection(TEST_COLLECTION)
    print("Cleanup done. Milvus is working.")

if __name__ == "__main__":
    main()
