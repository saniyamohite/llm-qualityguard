import pandas as pd


def main():
    print("Starting LLM QualityGuard...")

    dataset_path = "data/evaluation_dataset.csv"

    df = pd.read_csv(dataset_path)

    print(f"Loaded {len(df)} evaluation records.")

    print(f"Policies: {df['policy_id'].nunique()}")
    print(f"Categories: {df['category'].nunique()}")
    print(f"Question types: {df['question_type'].nunique()}")
    print(f"Difficulty levels: {df['difficulty'].nunique()}")

    print()
    print("Dataset columns:")
    for column in df.columns:
        print(f" - {column}")

    print()
    print("Evaluation results are not generated yet.")
    print("Next stage: retrieval → LLM answer → evaluation.")

    print()
    print("QualityGuard pipeline completed.")


if __name__ == "__main__":
    main()
