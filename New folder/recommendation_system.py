from data_set import data

def show_genres(category):
    while True:
        print(f"\nAvailable {category} genres:")
        for i, genre in enumerate(data[category], start=1):
            print(f"{i}. {genre['Genre']}")
        print("0. Go Back to Main Menu")
        choice = input("\nChoose a genre number: ")

        if choice == "0":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(data[category]):
            return data[category][int(choice) - 1]
        print("Invalid choice. Try again.")

def show_subtopics(genre_data):
    while True:
        print(f"\nSubtopics in {genre_data['Genre']}:")
        subtopics = [k for k in genre_data.keys() if k != "Genre"]
        for i, subtopic in enumerate(subtopics, start=1):
            print(f"{i}. {subtopic}")
        print("0. Go Back to Genres")

        sub_choice = input("\nChoose a subtopic number: ")

        if sub_choice == "0":
            return None
        if sub_choice.isdigit() and 1 <= int(sub_choice) <= len(subtopics):
            return genre_data[subtopics[int(sub_choice) - 1]]
        print("Invalid choice. Try again.")

def main():
    while True:
        print("\n=== Welcome to the Recommendation System! ===")
        print("1. Movies")
        print("2. Books")
        print("0. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            category = "Movies"
        elif choice == "2":
            category = "Books"
        else:
            print("Invalid choice. Try again.")
            continue

        while True:
            genre_data = show_genres(category)
            if genre_data is None:
                break

            recs = show_subtopics(genre_data)
            if recs is None:
                continue

            print("\nHere are some recommendations:")
            for item in recs:
                print(f"- {item}")

            input("\nPress Enter to go back to subtopics...")

if __name__ == "__main__":
    main()
