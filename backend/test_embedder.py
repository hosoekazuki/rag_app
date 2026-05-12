from services.embedder import load_markdown, split_text, embed_texts

text = load_markdown("data/algorithms/binary_search.md")
print(f"Word Count: {len(text)}")
chunks = split_text(text)
print(f"Chunk Count: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\n--- chunk {i+1} ---")
    print(chunk[:100])
embeddings = embed_texts(chunks)
print(f"\ndemention Counts of Embedding: {len(embeddings[0])}")
print(f"first 5th vectors: {embeddings[0][:5]}")
