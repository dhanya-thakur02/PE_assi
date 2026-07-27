import json
import os
import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearchEngine:

    def __init__(self,
                 dataset_path="embedding_index_3m.json",
                 cache_path="cached_embeddings.pkl"):

        self.dataset_path = dataset_path
        self.cache_path = cache_path

        print("Loading MiniLM model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.dataset = self.load_dataset()
        self.summary_embeddings = self.load_or_create_embeddings()

    def load_dataset(self):

        with open(self.dataset_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        print(f"Loaded {len(data)} records.")

        return data

    def load_or_create_embeddings(self):

        if os.path.exists(self.cache_path):

            print("Loading cached embeddings...")

            with open(self.cache_path, "rb") as file:
                embeddings = pickle.load(file)

            return embeddings

        print("Generating embeddings for all summaries...")
        embeddings = []

        total = len(self.dataset)

        for index, record in enumerate(self.dataset):

            summary = record["summary"]

            embedding = self.model.encode(summary)

            embeddings.append(embedding)

            if (index + 1) % 100 == 0:
                print(f"Processed {index+1}/{total}")

        with open(self.cache_path, "wb") as file:
            pickle.dump(embeddings, file)

        print("Embeddings saved successfully!")

        return embeddings

    def search(self, query, top_k=5):

        query_embedding = self.model.encode(query)

        scores = []

        for index, embedding in enumerate(self.summary_embeddings):

            similarity = cosine_similarity(
                [query_embedding],
                [embedding]
            )[0][0]

            scores.append((similarity, index))

        scores.sort(reverse=True)

        results = []

        for similarity, index in scores[:top_k]:

            record = self.dataset[index]

            results.append({
                "title": record["title"],
                "speaker": record["speaker"],
                "summary": record["summary"],
                "videoId": record["videoId"],
                "start": record["start"],
                "score": similarity
            })

        return results