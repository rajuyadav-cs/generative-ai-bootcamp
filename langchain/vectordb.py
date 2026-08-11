from embeddings import embeddedpdfs, embedding, splitted_pdfs
# print("Number of chunks:", len(embeddedpdfs))
# print("Vector dimension:", len(embeddedpdfs[0]))
# print("Vector type:", type(embeddedpdfs[0]))
# print("First 5 values:", embeddedpdfs[0][:5])

# ------------Cosine Similarity Practice------------------
# vectors = embeddedpdfs[:3][:3]
# print(vectors)
# from sklearn.metrics.pairwise import cosine_similarity
# similarity = cosine_similarity(vectors)
# print(f"\n-----------------------------------------\n{similarity}")

import faiss
import numpy as np

vectors = np.array(embeddedpdfs).astype("float32")

dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(vectors)

print("Total vectors:", index.ntotal)

query = "How much money did Drylab raise?"
query_vector = embedding.embed_query(query)
query_vector = np.array([query_vector]).astype("float32")
distances, indices = index.search(query_vector, 3)

for i in indices[0]:
    print(splitted_pdfs[i].page_content)
    print("--------------------------------")