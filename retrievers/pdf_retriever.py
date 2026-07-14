import json
from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


class PDFRetriever:

    def __init__(
        self,
        embedding_dir="../embeddings",
        model_name="all-mpnet-base-v2",
        top_k=5,
    ):

        self.top_k = top_k

        embedding_dir = Path(embedding_dir)

        self.index = faiss.read_index(
            str(
                embedding_dir / "corpus.faiss"
            )
        )

        with open(
            embedding_dir / "chunk_metadata.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.metadata = json.load(f)

        self.embedder = SentenceTransformer(
            model_name
        )

    # -----------------------------------------------------

    def _embed_query(self, query):

        embedding = self.embedder.encode(
            query,
            normalize_embeddings=True
        )

        return np.array(
            [embedding],
            dtype=np.float32
        )

    # -----------------------------------------------------

    def retrieve(
        self,
        query
    ):

        query_embedding = self._embed_query(
            query
        )

        scores, indices = self.index.search(
            query_embedding,
            self.top_k
        )

        retrieved_chunks = []

        confidence_scores = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            meta = self.metadata[idx]

            retrieved_chunks.append({

                "company":
                    meta.get("company"),

                "pdf":
                    meta.get("pdf_name"),

                "page":
                    meta.get("page"),

                "chunk":
                    meta.get("chunk_id"),

                "text":
                    meta.get("text")

            })

            confidence_scores.append(
                float(score)
            )

        if len(confidence_scores):

            confidence = float(
                np.mean(confidence_scores)
            )

        else:

            confidence = 0.0

        return {

            "context":
                retrieved_chunks,

            "confidence":
                confidence,

            "needs_llm":
                True,

            "metadata": {

                "num_chunks":
                    len(retrieved_chunks)

            }

        }