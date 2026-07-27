from search_engine import SemanticSearchEngine
import time

print("=" * 50)
print("SEMANTIC SEARCH ENGINE")
print("=" * 50)

engine = SemanticSearchEngine()

while True:

    query = input("\nEnter query (or type 'exit'): ")

    if query.lower() == "exit":
        print("Exiting...")
        break

    print("\n" + "=" * 42)
    print("User Query:")
    print(f'"{query}"')
    print("=" * 42)

    print("\nStep 1: Processing query...")
    time.sleep(0.5)
    print("Query received successfully.")

    print("\nStep 2: Generating query embedding...")
    time.sleep(0.5)
    print("Query converted into a 384-dimensional semantic vector.for compairing with dataset embeddings.")

    print("\nStep 3: Comparing with dataset...")
    time.sleep(0.5)
    print(f"Compared with {len(engine.dataset)} summary embeddings.")

    print("\nStep 4: Calculating cosine similarity...")
    time.sleep(0.5)

    print("Calling search()...")       
    results = engine.search(query)
    print("search() completed.")       

    print("Similarity scores computed.")

    print("\nStep 5: Ranking results...")
    time.sleep(0.5)
    print("Top 5 most relevant summaries selected.")

    print("\n" + "=" * 42)
    print("SEARCH RESULTS")
    print("=" * 42)

    for i, result in enumerate(results, start=1):
        print(f"\nRank #{i}")
        print("-" * 42)
        print(f"Similarity Score : {result['score']:.4f}")
        print(f"Title            : {result['title']}")
        print(f"Speaker          : {result['speaker']}")
        print(f"Summary          : {result['summary']}")
        print(f"Timestamp        : {result['start']} sec")
        print(f"Video Link       : https://www.youtube.com/watch?v={result['videoId']}&t={result['start']}s")