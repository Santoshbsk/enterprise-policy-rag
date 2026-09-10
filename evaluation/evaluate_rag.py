import json
import os
import sys
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from ragas.llms import LangchainLLMWrapper

# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from config import GEMINI_API_KEY, LLM_MODEL, PROJECT_ROOT
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)

from rag import ask_question


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATASET_PATH = PROJECT_ROOT / "evaluation" / "eval_dataset.json"
RESULTS_DIR = PROJECT_ROOT / "evaluation" / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load evaluation dataset
# --------------------------------------------------

def load_evaluation_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Run RAG against evaluation questions
# --------------------------------------------------

def build_ragas_dataset(test_cases):

    questions = []
    answers = []
    contexts = []
    references = []

    for index, test_case in enumerate(test_cases, start=1):

        question = test_case["question"]
        reference_answer = test_case["reference_answer"]

        print()
        print("=" * 70)
        print(f"Evaluating {index}/{len(test_cases)}")
        print(f"Question: {question}")

        try:

            answer, results = ask_question(
                query=question,
                top_k=3
            )

            retrieved_documents = results.get("documents", [[]])[0]

            retrieved_contexts = [
                document
                for document in retrieved_documents
                if document
            ]

            print(f"Retrieved chunks: {len(retrieved_contexts)}")
            print(f"Answer: {answer}")

            questions.append(question)
            answers.append(answer)
            contexts.append(retrieved_contexts)
            references.append(reference_answer)

        except Exception as error:

            print(f"ERROR: {error}")

            questions.append(question)
            answers.append(
                "ERROR: RAG pipeline failed to generate an answer."
            )
            contexts.append([])
            references.append(reference_answer)

    return Dataset.from_dict(
        {
            "user_input": questions,
            "response": answers,
            "retrieved_contexts": contexts,
            "reference": references
        }
    )

evaluator_llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

evaluator_llm = LangchainLLMWrapper(evaluator_llm)

evaluator_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)
# --------------------------------------------------
# Evaluate with Ragas
# --------------------------------------------------

def evaluate_rag(dataset):

    print()
    print("=" * 70)
    print("Starting Ragas evaluation...")
    print("=" * 70)

    result = evaluate(
        dataset=dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
    )

    return result


# --------------------------------------------------
# Save results
# --------------------------------------------------

def save_results(result):

    result_df = result.to_pandas()

    output_csv = RESULTS_DIR / "ragas_results.csv"

    result_df.to_csv(
        output_csv,
        index=False
    )

    print()
    print("=" * 70)
    print("RAGAS RESULTS")
    print("=" * 70)

    print(result_df)

    print()
    print(f"Results saved to:")
    print(output_csv)

    # Calculate overall averages
    metric_columns = [
        "context_precision",
        "context_recall",
        "faithfulness",
        "answer_relevancy"
    ]

    print()
    print("AVERAGE METRICS")
    print("-" * 70)

    for metric in metric_columns:

        if metric in result_df.columns:

            value = result_df[metric].mean()

            print(
                f"{metric:25s}: {value:.4f}"
            )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    print(GEMINI_API_KEY)
    print()
    print("=" * 70)
    print("ENTERPRISE POLICY RAG - RAGAS EVALUATION")
    print("=" * 70)

    test_cases = load_evaluation_dataset()

    print(f"Loaded {len(test_cases)} evaluation questions.")

    dataset = build_ragas_dataset(test_cases)

    result = evaluate_rag(dataset)

    save_results(result)


if __name__ == "__main__":
    main()