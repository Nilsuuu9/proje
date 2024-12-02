import random

# Belirlenen Türk filmleri ve ilgili ipuçları
movies = {
    "Hababam Sınıfı": {
        "main_star": "Kemal Sunal",
        "hints": [
            "This movie is about a group of high school students' adventures.",
            "The main character is known as İnek Şaban.",
            "Based on a work by Rıfat Ilgaz."
        ]
    },
    "Eşkıya": {
        "main_star": "Şener Şen",
        "hints": [
            "The story of a man seeking revenge after being imprisoned.",
            "Considered a classic of Turkish cinema.",
            "Directed by Yavuz Turgul."
        ]
    },
    "Babam ve Oğlum": {
        "main_star": "Çetin Tekindor",
        "hints": [
            "This movie portrays the relationship between a father and his son.",
            "Released in 2005.",
            "Directed by Çağan Irmak."
        ]
    }
}

def colorful_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    return colors.get(color, "") + text + colors["reset"]

def main():
    score = 0
    attempts = 3
    movie_name = random.choice(list(movies.keys()))
    hints = movies[movie_name]["hints"]
    encouragements = [
        "Keep going! You got this!",
        "Don't give up!",
        "You are doing great!",
    ]

    print(colorful_text("Guess the movie! Here are your hints:", "blue"))
    for hint in hints:
        print(colorful_text("- " + hint, "cyan"))

    while attempts > 0:
        guess = input(colorful_text("Enter your guess (or type 'exit' to quit): ", "yellow")).strip()
        
        if guess.lower() == "exit":
            break
        
        if guess.lower() == movie_name.lower():
            print(colorful_text("Correct! You guessed the full movie name.", "green"))
            score += 5
        elif guess.lower() == movies[movie_name]["main_star"].lower():
            print(colorful_text("Correct! You guessed the main star.", "green"))
            score += 4
        elif guess.lower() in [info.lower() for info in movies[movie_name]["hints"]]:
            print(colorful_text("Correct! You guessed some other information.", "green"))
            score += 2
        else:
            print(colorful_text("Wrong guess. Try again.", "red"))
            score -= 2
        
        attempts -= 1
        if attempts > 0:
            print(colorful_text(f"Score: {score} | Attempts left: {attempts}", "magenta"))
            print(colorful_text(random.choice(encouragements), "magenta"))

    print(colorful_text(f"Game Over! Your final score is: {score}", "magenta"))

if __name__ == "__main__":
    main()
