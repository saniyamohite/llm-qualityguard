import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


def main():
    print("Loading knowledge base...")

    knowledge_base = pd.read_csv("data/knowledge_base.csv")

    print(f"Policies: {len(knowledge_base)}")

    print("Loading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Creating embeddings...")

    embeddings = model.encode(
        knowledge_base["content"].tolist(),
        show_progress_bar=True
    )

    np.save(
        "data/policy_embeddings.npy",
        embeddings
    )

    print()
    print("Embeddings saved to:")
    print("data/policy_embeddings.npy")

    print(f"Embedding shape: {embeddings.shape}")


if __name__ == "__main__":
    main()