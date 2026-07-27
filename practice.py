from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


sentence1 = "Artificial Intelligence is transforming healthcare."
sentence2 = "AI is changing the medical field."
sentence3 = "I love eating pizza."


embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)


similarity12 = cosine_similarity([embedding1], [embedding2])[0][0]
similarity13 = cosine_similarity([embedding1], [embedding3])[0][0]

print("Sentence 1:", sentence1)
print("Sentence 2:", sentence2)
print("Sentence 3:", sentence3)

print("\nSimilarity (Sentence 1 ↔ Sentence 2):", similarity12)
print("Similarity (Sentence 1 ↔ Sentence 3):", similarity13)