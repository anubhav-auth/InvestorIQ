import os
from dotenv import load_dotenv
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from datasets import Dataset
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import run_analyst

load_dotenv()

def create_evaluation_dataset():
    """
    Creates a small dataset for evaluating the RAG system.
    """
    questions = [
        "How has the recent AI chip demand impacted Nvidia's stock and strategy?",
        "What is the current market sentiment regarding electric vehicles, and what are the key challenges for companies in this sector?",
    ]

    contexts = [
        [
            "Nvidia's strategic focus has heavily shifted towards dominating the AI and data center markets.",
            "Recent earnings calls highlighted record-breaking revenue from their data center division, largely fueled by the demand for their H100 and A100 GPUs.",
            "CEO Jensen Huang emphasized that 'the AI revolution is in full swing,' and Nvidia is positioned as the primary engine for this transformation.",
            "This strategic pivot has resulted in a significant increase in their stock price over the last year...",
        ],
        [
            "The electric vehicle (EV) market is facing a paradigm shift.",
            "While early adoption was driven by environmental concerns, recent consumer behavior indicates a stronger emphasis on total cost of ownership and technological features.",
            "Companies are now competing on battery range, charging speed, and in-car software.",
            "The next 3-5 years will be critical in determining which companies can scale production to meet demand while managing battery supply chain complexities.",
        ],
    ]
    
    ground_truths = [
        "Nvidia's strategy has shifted to AI and data centers due to high demand for their GPUs, leading to record revenue and a stock price increase. CEO Jensen Huang stated that 'the AI revolution is in full swing'.",
        "The EV market is shifting, with consumers now prioritizing cost and tech features over just environmental concerns. Competition is focused on battery, charging, and software. The next few years are critical for scaling production and managing supply chains."
    ]


    answers = []
    for q in questions:
        print(f"--- Processing question: '{q}' ---")
        report = run_analyst(q)
        answers.append(report)
        time.sleep(60)

    return Dataset.from_dict({
        "question": questions,
        "contexts": contexts,
        "answer": answers,
        "ground_truth": ground_truths,
    })

def evaluate_rag_pipeline():
    """
    Runs the RAGAS evaluation on the created dataset.
    """
    print("Creating evaluation dataset...")
    eval_dataset = create_evaluation_dataset()

    print("Running RAGAS evaluation...")
    result = evaluate(
        eval_dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        ],
    )

    print("--- Evaluation Complete ---")
    print(result)

if __name__ == "__main__":
    evaluate_rag_pipeline()