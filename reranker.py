from sentence_transformers import CrossEncoder


RERANKER_MODEL = "BAAI/bge-reranker-base"

reranker = CrossEncoder(RERANKER_MODEL)


def rerank_documents(query, documents, top_k=3):

    pairs = [
        (query, document)
        for document in documents
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(
            documents,
            scores,
            range(len(documents))
        ),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_k]