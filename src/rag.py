import json
import os
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv
from pypdf import PdfReader


load_dotenv()


KNOWLEDGE_BASE_PATH = Path("data/knowledge_base")
VECTOR_STORE_PATH = Path("data/vector_store.json")

EMBEDDING_MODEL = "nvidia/nemotron-3-embed-1b:free"


def get_embeddings(texts):
    """Generate embeddings using OpenRouter."""

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured."
        )

    response = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": texts,
            "encoding_format": "float",
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return [
        item["embedding"]
        for item in data["data"]
    ]


def load_documents():

    documents = []

    for file_path in KNOWLEDGE_BASE_PATH.iterdir():

        if file_path.suffix.lower() == ".txt":

            text = file_path.read_text(
                encoding="utf-8"
            )

            documents.append({
                "text": text,
                "source": file_path.name
            })

        elif file_path.suffix.lower() == ".pdf":

            reader = PdfReader(str(file_path))

            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            documents.append({
                "text": text,
                "source": file_path.name
            })

    return documents


def split_text(text, max_chars=700):
    """Split policy documents at paragraph boundaries."""

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        if not current_chunk:
            current_chunk = paragraph

        elif len(current_chunk) + len(paragraph) + 2 <= max_chars:
            current_chunk += "\n\n" + paragraph

        else:
            chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def create_vector_store():

    print("1. Loading documents...")

    documents = load_documents()

    print(
        f"2. Loaded {len(documents)} document(s)"
    )

    all_chunks = []
    all_sources = []

    for document in documents:

        chunks = split_text(
            document["text"]
        )

        all_chunks.extend(chunks)

        all_sources.extend(
            [document["source"]] * len(chunks)
        )

    print(
        f"3. Created {len(all_chunks)} chunks"
    )

    print("4. Generating embeddings...")

    embeddings = get_embeddings(
        all_chunks
    )

    print(
        f"5. Received {len(embeddings)} embeddings"
    )

    vector_store = {
        "documents": all_chunks,
        "sources": all_sources,
        "embeddings": embeddings,
    }

    VECTOR_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        VECTOR_STORE_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            vector_store,
            file
        )

    print(
        "6. Vector store saved successfully!"
    )

    print(
        f"7. Stored {len(all_chunks)} chunks"
    )


def search_knowledge_base(
    query,
    top_k=3
):

    if not VECTOR_STORE_PATH.exists():

        raise FileNotFoundError(
            "Vector store does not exist. "
            "Run ingestion first."
        )

    with open(
        VECTOR_STORE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        vector_store = json.load(file)

    query_embedding = get_embeddings(
        [query]
    )[0]

    query_vector = np.array(
        query_embedding
    )

    document_vectors = np.array(
        vector_store["embeddings"]
    )

    # Cosine similarity
    similarities = (
        document_vectors @ query_vector
        /
        (
            np.linalg.norm(
                document_vectors,
                axis=1
            )
            *
            np.linalg.norm(query_vector)
        )
    )

    top_indices = np.argsort(
        similarities
    )[::-1][:top_k]

    results = []

    for index in top_indices:

        results.append({
            "text": vector_store["documents"][index],
            "source": vector_store["sources"][index],
            "score": float(
                similarities[index]
            )
        })

    return results


if __name__ == "__main__":

    print(
        "Starting RAG ingestion..."
    )

    create_vector_store()

    print(
        "Knowledge base created successfully!"
    )
def generate_rag_response(query):
    from src.llm import generate_response

    results = search_knowledge_base(
        query,
        top_k=3
    )

    context = "\n\n".join(
        [
            f"SOURCE: {result['source']}\n"
            f"CONTENT:\n{result['text']}"
            for result in results
        ]
    )

    messages = [
        {
            "role": "system",
            "content": """
You are an enterprise policy assistant.

STRICT RULES:
1. Answer ONLY from the provided enterprise context.
2. Do NOT use general knowledge.
3. Do NOT make assumptions about how other organizations work.
4. Do NOT add stakeholders, approvals, requirements, procedures,
   or policies that are not explicitly present in the context.
5. If the context does not explicitly contain the answer, say:
   "I don't have enough information in the enterprise knowledge base."
6. Prefer the exact policy wording from the context.
7. Mention the source document when possible.
"""
        },
        {
            "role": "user",
            "content": f"""
ENTERPRISE CONTEXT:

{context}

QUESTION:

{query}

Answer the question using ONLY the enterprise context above.
"""
        }
    ]

    answer = generate_response(messages)

    return answer, results