def main():
    from src.agent import app

    if __name__ == "__main__":
        questions = [
        "Quelles sont les opportunités pour un professeur de physique ?",
        "Y a-t-il des offres en ingénierie informatique ?",
        "Quels sont les montants des bourses proposées ?",
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"QUESTION : {question}")
        print('='*60)
        result = app.invoke({"question": question})
        print("\n--- RÉPONSE ---")
        print(result["generation"])


if __name__ == "__main__":
    main()
