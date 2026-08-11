import chromadb

from sentence_transformers import SentenceTransformer
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings


# =========================================================
# CUSTOM E5 EMBEDDING FUNCTION
# =========================================================

class E5EmbeddingFunction(EmbeddingFunction):

    def __init__(self, mode="passage"):
        self.model = SentenceTransformer(
            "intfloat/multilingual-e5-base",
            device="cuda"
        )

        self.mode = mode

    def __call__(self, input: Documents) -> Embeddings:

        # E5 model ke according prefix add karna
        texts = [
            f"{self.mode}: {text}"
            for text in input
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()


# =========================================================
# CHROMADB
# =========================================================

client = chromadb.Client()


# Documents ke liye embedding function
embedding_function = E5EmbeddingFunction(
    mode="passage"
)


collection = client.create_collection(
    name="courses",
    embedding_function=embedding_function
)


# =========================================================
# ADD DOCUMENTS
# =========================================================

collection.add(

    ids=[
        "course_1",
        "course_2",
        "course_3"
    ],

    documents=[
        "Python is used for backend development.",
        "ChromaDB is used for vector search.",
        "FastAPI is a Python framework for APIs."
    ],

    metadatas=[
        {
            "topic": "python",
            "level": "beginner"
        },
        {
            "topic": "database",
            "level": "intermediate"
        },
        {
            "topic": "backend",
            "level": "intermediate"
        }
    ]
)


# =========================================================
# DATA RETRIEVING
# =========================================================

# result = collection.get()

# print(result)


print("-------------------------------------")


# =========================================================
# DATA RETRIEVING USING SPECIFIC ID
# =========================================================

# result = collection.get(
#     ids=["course_2"]
# )

# print(result)


print("------------------------------------------")


# =========================================================
# SEMANTIC SEARCH
# =========================================================

query = "I want to learn vector databases"


# Query ke liye alag embedding function
query_embedding_function = E5EmbeddingFunction(
    mode="query"
)


# Query ka embedding generate
query_embedding = query_embedding_function(
    [query]
)


result = collection.query(

    query_embeddings=query_embedding,

    n_results=2
)


# print("Query:")
# print(query)

# print("\nDocuments:")
# print(result["documents"])

# print("\nDistances:")
# print(result["distances"])


print("------------------------------")


# =========================================================
# METADATA FILTERING
# =========================================================

# query = "Python programming"

# query_embedding = query_embedding_function(
#     [query]
# )

# result = collection.query(
#     query_embeddings=query_embedding,
#     n_results=2,
#     where={"level": "beginner"}
# )

# print(result["documents"])


# =========================================================
# TASK-1
# ADDING 3 MORE DOCUMENTS
# =========================================================

collection.add(

    ids=[
        "course_4",
        "course_5",
        "course_6"
    ],

    documents=[
        "Machine Learning is used to train machines to learn patterns from data.",
        "JavaScript is a programming language used for making responsive websites.",
        "RAG is a pipeline used to provide context to LLMs."
    ],

    metadatas=[
        {
            "topic": "machine learning",
            "level": "intermediate"
        },
        {
            "topic": "javascript",
            "level": "intermediate"
        },
        {
            "topic": "RAG",
            "level": "advanced"
        }
    ]
)


# =========================================================
# TASK-2 CRUD
# =========================================================


# ---------------- DELETE ----------------

# collection.delete(
#     ids=["course_6"]
# )


# ---------------- GET SPECIFIC DOCUMENT ----------------

# result = collection.get(
#     ids=["course_4"]
# )

# print(result)


# ---------------- GET USING METADATA FILTER ----------------

# result = collection.get(
#     where={"level": "advanced"}
# )

# print(result)


# =========================================================
# HINDI / MULTILINGUAL QUERY
# =========================================================

query = "Python kya hai?"

query_embedding = query_embedding_function(
    [query]
)

result = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print(result["documents"])
# print(result["distances"])


# =========================================================
# CHROMADB VERSION
# =========================================================

print("ChromaDB Version:", chromadb.__version__)

