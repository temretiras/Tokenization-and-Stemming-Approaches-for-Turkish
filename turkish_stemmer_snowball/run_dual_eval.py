import os
from evaluator_dual import evaluate_dual
from data_loader import load_conllu_pairs


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Detect .conllu file containing "dev" in the name
    target_file = None
    for file in os.listdir(current_dir):
        if file.endswith(".conllu") and "dev" in file:
            target_file = os.path.join(current_dir, file)
            break

    if not target_file:
        print("Error: No .conllu file containing 'dev' found in the current directory.")
        return

    print(f"File found: {os.path.basename(target_file)}")

    # Load data
    words, lemmas = load_conllu_pairs(target_file)

    # Output path
    results_dir = os.path.join(current_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    dataset_name = os.path.basename(target_file).replace(".conllu", "")
    export_path = os.path.join(results_dir, f"{dataset_name}_eval.csv")

    print("\nEvaluating the stemmer")
    evaluate_dual(words, lemmas, tolerance=0.7, export_path=export_path)


if __name__ == "__main__":
    main()
