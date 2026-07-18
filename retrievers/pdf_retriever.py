import json
import traceback
from pathlib import Path

print("[PDF RETRIEVER] Importing faiss...")
import faiss
print("[✓] faiss imported.")

print("[PDF RETRIEVER] Importing numpy...")
import numpy as np
print("[✓] numpy imported.")

print("[PDF RETRIEVER] Importing SentenceTransformer...")
from sentence_transformers import SentenceTransformer
print("[✓] SentenceTransformer imported.")


class PDFRetriever:

    def __init__(
        self,
        embedding_dir=None,
        model_name="all-mpnet-base-v2",
        top_k=5,
    ):

        print("=" * 60)
        print("PDFRetriever.__init__() START")
        print("=" * 60)

        try:

            if embedding_dir is None:

                embedding_dir = (
                    Path(__file__).resolve().parent.parent
                    / "embeddings"
                )

            self.embedding_dir = Path(embedding_dir)
            self.top_k = top_k

            print(f"[1] Embedding directory: {self.embedding_dir}")

            faiss_path = self.embedding_dir / "corpus.faiss"

            print(f"[2] FAISS exists: {faiss_path.exists()}")
            print(f"[2] Loading FAISS from: {faiss_path}")

            self.index = faiss.read_index(str(faiss_path))

            print("[✓] FAISS loaded.")

            metadata_path = self.embedding_dir / "chunk_metadata.json"

            print(f"[3] Metadata exists: {metadata_path.exists()}")
            print(f"[3] Loading metadata...")

            with open(
                metadata_path,
                "r",
                encoding="utf-8"
            ) as f:

                self.metadata = json.load(f)

            print(f"[✓] Metadata loaded.")
            print(f"[✓] Metadata entries: {len(self.metadata)}")

            print("[4] Loading SentenceTransformer...")
            print(f"[4] Model name: {model_name}")

            self.embedder = SentenceTransformer(model_name)

            print("[✓] SentenceTransformer loaded.")

            print("=" * 60)
            print("PDFRetriever.__init__() FINISHED")
            print("=" * 60)

        except Exception as e:

            print("=" * 60)
            print("PDFRetriever FAILED")
            print("=" * 60)

            print(type(e).__name__)
            print(e)

            traceback.print_exc()

            raise

    # -----------------------------------------------------

    def _embed_query(self, query):

        print("[PDFRetriever] Encoding query...")

        embedding = self.embedder.encode(
            query,
            normalize_embeddings=True
        )

        print("[✓] Query encoded.")

        return np.array(
            [embedding],
            dtype=np.float32
        )

    # -----------------------------------------------------

    def retrieve(self, query):

        print(f"[PDFRetriever] Retrieving for: {query}")

        query_embedding = self._embed_query(query)

        print("[PDFRetriever] Searching FAISS...")

        scores, indices = self.index.search(
            query_embedding,
            self.top_k
        )

        print("[✓] FAISS search complete.")

        retrieved_chunks = []
        confidence_scores = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            meta = self.metadata[idx]

            retrieved_chunks.append({
                "company": meta.get("company"),
                "pdf": meta.get("pdf_name"),
                "page": meta.get("page"),
                "chunk": meta.get("chunk_id"),
                "text": meta.get("text")
            })

            confidence_scores.append(float(score))

        confidence = (
            float(np.mean(confidence_scores))
            if confidence_scores
            else 0.0
        )

        print(f"[✓] Retrieved {len(retrieved_chunks)} chunks.")

        return {
            "context": retrieved_chunks,
            "confidence": confidence,
            "needs_llm": True,
            "metadata": {
                "num_chunks": len(retrieved_chunks)
            }
        }
