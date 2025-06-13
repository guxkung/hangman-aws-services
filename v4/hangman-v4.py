import random
import os
import json
import time
import subprocess
import sys
from datetime import datetime

class AwsHangman:
    def __init__(self):
        self.aws_services = self.load_services()
        self.categories = self.get_categories()
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.current_service = None
        self.description = None
        self.certification_notes = None
        self.word_completion = None
        self.guessed_letters = []
        self.guessed_words = []
        self.tries = 6
        self.score = 0
        self.game_history = []
        
    def load_services(self):
        """Load AWS services from file or use default if file doesn't exist"""
        try:
            with open('aws_services.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            # Default services with certification notes
            return {
                "EC2": {
                    "description": "Elastic compute service that provides resizable compute capacity in the cloud",
                    "category": "Compute",
                    "difficulty": "Easy",
                    "certification_notes": "Know instance types, pricing models, and auto scaling capabilities"
                },
                "S3": {
                    "description": "Object storage service that offers industry-leading scalability, data availability, security, and performance",
                    "category": "Storage",
                    "difficulty": "Easy",
                    "certification_notes": "Understand storage classes, lifecycle policies, and bucket policies"
                },
                "LAMBDA": {
                    "description": "Serverless compute service that lets you run code without provisioning or managing servers",
                    "category": "Compute",
                    "difficulty": "Medium",
                    "certification_notes": "Focus on triggers, execution context, and integration with other services"
                },
                "DYNAMODB": {
                    "description": "Fully managed NoSQL database service that provides fast and predictable performance with seamless scalability",
                    "category": "Database",
                    "difficulty": "Medium",
                    "certification_notes": "Know about partition keys, sort keys, and read/write capacity units"
                },
                "RDS": {
                    "description": "Managed relational database service that makes it easy to set up, operate, and scale a relational database",
                    "category": "Database",
                    "difficulty": "Medium",
                    "certification_notes": "Understand multi-AZ deployments, read replicas, and backup options"
                }
            }
    
    def save_services(self):
        """Save the current AWS services to a file"""
        with open('aws_services.json', 'w') as file:
            json.dump(self.aws_services, file, indent=4)
    
    def get_categories(self):
        """Extract unique categories from services"""
        return sorted(list(set(service["category"] for service in self.aws_services.values())))
    
    def add_service(self, name, description, category, difficulty, certification_notes):
        """Add a new AWS service to the database"""
        self.aws_services[name.upper()] = {
            "description": description,
            "category": category,
            "difficulty": difficulty,
            "certification_notes": certification_notes
        }
        self.categories = self.get_categories()
        self.save_services()
        
    def update_service(self, name, description=None, category=None, difficulty=None, certification_notes=None):
        """Update an existing AWS service"""
        if name.upper() in self.aws_services:
            service = self.aws_services[name.upper()]
            if description:
                service["description"] = description
            if category:
                service["category"] = category
            if difficulty:
                service["difficulty"] = difficulty
            if certification_notes:
                service["certification_notes"] = certification_notes
            self.save_services()
            self.categories = self.get_categories()
            return True
        return False
    
    def delete_service(self, name):
        """Delete an AWS service from the database"""
        if name.upper() in self.aws_services:
            del self.aws_services[name.upper()]
            self.save_services()
            self.categories = self.get_categories()
            return True
        return False

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_hangman(self):
        """Display the hangman based on the number of tries left"""
        stages = [
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / 
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |      
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |      |
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |      
               |      
               |     
               -
            """,
            """
               --------
               |      |
               |      
               |      
               |      
               |     
               -
            """
        ]
        return stages[self.tries]

    def select_service(self, category=None, difficulty=None):
        """Select a random AWS service based on category and difficulty"""
        filtered_services = {}
        
        for name, info in self.aws_services.items():
            if (category is None or info["category"] == category) and \
               (difficulty is None or info["difficulty"] == difficulty):
                filtered_services[name] = info
        
        if not filtered_services:
            return None
            
        service_name = random.choice(list(filtered_services.keys()))
        service_info = filtered_services[service_name]
        
        self.current_service = service_name
        self.description = service_info["description"]
        self.certification_notes = service_info["certification_notes"]
        self.word_completion = '_' * len(service_name)
        self.guessed_letters = []
        self.guessed_words = []
        self.tries = 6
        
        return service_name
    
    def make_guess(self, guess):
        """Process a guess and update game state"""
        guess = guess.upper()
        result = {
            "valid": True,
            "message": "",
            "game_over": False,
            "won": False
        }
        
        # Check if the guess is a single letter
        if len(guess) == 1 and guess.isalnum():
            if guess in self.guessed_letters:
                result["valid"] = False
                result["message"] = f"You already guessed the letter {guess}"
            elif guess not in self.current_service:
                result["message"] = f"{guess} is not in the word."
                self.tries -= 1
                self.guessed_letters.append(guess)
            else:
                result["message"] = f"Good job, {guess} is in the word!"
                self.guessed_letters.append(guess)
                
                # Update the word completion
                word_as_list = list(self.word_completion)
                indices = [i for i, letter in enumerate(self.current_service) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                self.word_completion = "".join(word_as_list)
                
                if "_" not in self.word_completion:
                    result["game_over"] = True
                    result["won"] = True
        
        # Check if the guess is a word
        elif len(guess) == len(self.current_service) and guess.isalnum():
            if guess in self.guessed_words:
                result["valid"] = False
                result["message"] = f"You already guessed the word {guess}"
            elif guess != self.current_service:
                result["message"] = f"{guess} is not the word."
                self.tries -= 1
                self.guessed_words.append(guess)
            else:
                result["game_over"] = True
                result["won"] = True
                self.word_completion = self.current_service
        
        else:
            result["valid"] = False
            result["message"] = "Not a valid guess."
        
        # Check if out of tries
        if self.tries <= 0:
            result["game_over"] = True
            result["won"] = False
        
        return result
    
    def update_score(self, won):
        """Update the player's score"""
        if won:
            difficulty_multiplier = {"Easy": 1, "Medium": 2, "Hard": 3}
            service_info = self.aws_services[self.current_service]
            self.score += 10 * difficulty_multiplier[service_info["difficulty"]]
        
        # Record game history
        self.game_history.append({
            "service": self.current_service,
            "result": "won" if won else "lost",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_study_tip(self):
        """Get a certification study tip for the current service"""
        return self.certification_notes
    
    def display_game_state(self):
        """Return a string representation of the current game state"""
        output = []
        output.append(f"Category: {self.aws_services[self.current_service]['category']}")
        output.append(f"Difficulty: {self.aws_services[self.current_service]['difficulty']}")
        output.append(f"Hint: {self.description}")
        output.append(self.display_hangman())
        output.append(f"Word: {' '.join(self.word_completion)}")
        output.append(f"Letters guessed: {', '.join(self.guessed_letters)}")
        output.append(f"Words guessed: {', '.join(self.guessed_words)}")
        output.append(f"Tries left: {self.tries}")
        output.append(f"Current score: {self.score}")
        
        return "\n".join(output)
    
    def show_statistics(self):
        """Show game statistics"""
        if not self.game_history:
            return "No games played yet."
        
        total_games = len(self.game_history)
        games_won = sum(1 for game in self.game_history if game["result"] == "won")
        win_rate = (games_won / total_games) * 100 if total_games > 0 else 0
        
        stats = [
            f"Total games played: {total_games}",
            f"Games won: {games_won}",
            f"Games lost: {total_games - games_won}",
            f"Win rate: {win_rate:.1f}%",
            f"Current score: {self.score}"
        ]
        
        return "\n".join(stats)

def main():
    print("AWS Hangman for Certification Prep - Coming soon!")
    game = AwsHangman()
    
    while True:
        game.clear_screen()
        print("\n===== AWS HANGMAN FOR CERTIFICATION PREP =====\n")
        print("1. Play Game")
        print("2. Filter by Category")
        print("3. Filter by Difficulty")
        print("4. Add New AWS Service")
        print("5. Update Existing Service")
        print("6. View Statistics")
        print("7. Update AWS Services Database")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            play_game(game)
        elif choice == "2":
            play_with_category_filter(game)
        elif choice == "3":
            play_with_difficulty_filter(game)
        elif choice == "4":
            add_new_service(game)
        elif choice == "5":
            update_service(game)
        elif choice == "6":
            view_statistics(game)
        elif choice == "7":
            update_aws_services_database(game)
        elif choice == "8":
            print("\nThank you for using AWS Hangman for Certification Prep!")
            break
        else:
            input("Invalid choice. Press Enter to continue...")

def play_game(game, category=None, difficulty=None):
    """Play the hangman game"""
    game.clear_screen()
    
    # Select a service based on filters
    service = game.select_service(category, difficulty)
    if not service:
        input("No services match your criteria. Press Enter to return to the menu...")
        return
    
    game_over = False
    won = False
    
    while not game_over:
        game.clear_screen()
        print("\n===== AWS HANGMAN =====\n")
        print(game.display_game_state())
        print("\n")
        
        guess = input("Please guess a letter or the full word: ")
        result = game.make_guess(guess)
        
        if not result["valid"]:
            game.clear_screen()
            print(result["message"])
            time.sleep(1)
            continue
        
        game_over = result["game_over"]
        won = result["won"]
        
        if result["message"]:
            game.clear_screen()
            print(result["message"])
            time.sleep(1)
    
    # Game result
    game.clear_screen()
    print(game.display_game_state())
    print("\n")
    
    if won:
        print(f"Congratulations! You guessed the AWS service: {service}")
    else:
        print(f"Sorry, you ran out of tries. The AWS service was: {service}")
    
    # Show certification study tip
    print("\nCertification Study Tip:")
    print(game.get_study_tip())
    
    # Update score
    game.update_score(won)
    
    input("\nPress Enter to continue...")

def play_with_category_filter(game):
    """Play the game with a category filter"""
    game.clear_screen()
    print("\n===== SELECT CATEGORY =====\n")
    
    for i, category in enumerate(game.categories, 1):
        print(f"{i}. {category}")
    print(f"{len(game.categories) + 1}. Back to Main Menu")
    
    try:
        choice = int(input("\nEnter your choice: "))
        if 1 <= choice <= len(game.categories):
            selected_category = game.categories[choice - 1]
            play_game(game, category=selected_category)
        elif choice == len(game.categories) + 1:
            return
        else:
            input("Invalid choice. Press Enter to continue...")
    except ValueError:
        input("Invalid input. Press Enter to continue...")

def play_with_difficulty_filter(game):
    """Play the game with a difficulty filter"""
    game.clear_screen()
    print("\n===== SELECT DIFFICULTY =====\n")
    
    for i, difficulty in enumerate(game.difficulty_levels, 1):
        print(f"{i}. {difficulty}")
    print(f"{len(game.difficulty_levels) + 1}. Back to Main Menu")
    
    try:
        choice = int(input("\nEnter your choice: "))
        if 1 <= choice <= len(game.difficulty_levels):
            selected_difficulty = game.difficulty_levels[choice - 1]
            play_game(game, difficulty=selected_difficulty)
        elif choice == len(game.difficulty_levels) + 1:
            return
        else:
            input("Invalid choice. Press Enter to continue...")
    except ValueError:
        input("Invalid input. Press Enter to continue...")

def add_new_service(game):
    """Add a new AWS service"""
    game.clear_screen()
    print("\n===== ADD NEW AWS SERVICE =====\n")
    
    name = input("Enter service name: ")
    if name.upper() in game.aws_services:
        input("Service already exists. Press Enter to continue...")
        return
    
    description = input("Enter service description: ")
    
    print("\nAvailable categories:")
    for i, category in enumerate(game.categories, 1):
        print(f"{i}. {category}")
    print(f"{len(game.categories) + 1}. Add new category")
    
    try:
        choice = int(input("\nSelect category or add new: "))
        if 1 <= choice <= len(game.categories):
            category = game.categories[choice - 1]
        elif choice == len(game.categories) + 1:
            category = input("Enter new category name: ")
        else:
            input("Invalid choice. Press Enter to continue...")
            return
    except ValueError:
        input("Invalid input. Press Enter to continue...")
        return
    
    print("\nSelect difficulty level:")
    for i, difficulty in enumerate(game.difficulty_levels, 1):
        print(f"{i}. {difficulty}")
    
    try:
        choice = int(input("\nEnter your choice: "))
        if 1 <= choice <= len(game.difficulty_levels):
            difficulty = game.difficulty_levels[choice - 1]
        else:
            input("Invalid choice. Press Enter to continue...")
            return
    except ValueError:
        input("Invalid input. Press Enter to continue...")
        return
    
    certification_notes = input("Enter certification study notes: ")
    
    game.add_service(name, description, category, difficulty, certification_notes)
    input("Service added successfully. Press Enter to continue...")

def update_service(game):
    """Update an existing AWS service"""
    game.clear_screen()
    print("\n===== UPDATE AWS SERVICE =====\n")
    
    # List all services
    services = sorted(game.aws_services.keys())
    for i, service in enumerate(services, 1):
        print(f"{i}. {service}")
    print(f"{len(services) + 1}. Back to Main Menu")
    
    try:
        choice = int(input("\nSelect service to update: "))
        if 1 <= choice <= len(services):
            service_name = services[choice - 1]
        elif choice == len(services) + 1:
            return
        else:
            input("Invalid choice. Press Enter to continue...")
            return
    except ValueError:
        input("Invalid input. Press Enter to continue...")
        return
    
    service_info = game.aws_services[service_name]
    
    print(f"\nUpdating {service_name}")
    print("Leave blank to keep current value")
    
    description = input(f"Description [{service_info['description']}]: ")
    description = description if description else service_info['description']
    
    print("\nAvailable categories:")
    for i, category in enumerate(game.categories, 1):
        print(f"{i}. {category}")
    print(f"{len(game.categories) + 1}. Add new category")
    print(f"{len(game.categories) + 2}. Keep current ({service_info['category']})")
    
    try:
        choice = int(input("\nSelect category: "))
        if 1 <= choice <= len(game.categories):
            category = game.categories[choice - 1]
        elif choice == len(game.categories) + 1:
            category = input("Enter new category name: ")
        elif choice == len(game.categories) + 2:
            category = service_info['category']
        else:
            input("Invalid choice. Press Enter to continue...")
            return
    except ValueError:
        category = service_info['category']
    
    print("\nSelect difficulty level:")
    for i, difficulty in enumerate(game.difficulty_levels, 1):
        print(f"{i}. {difficulty}")
    print(f"{len(game.difficulty_levels) + 1}. Keep current ({service_info['difficulty']})")
    
    try:
        choice = int(input("\nEnter your choice: "))
        if 1 <= choice <= len(game.difficulty_levels):
            difficulty = game.difficulty_levels[choice - 1]
        elif choice == len(game.difficulty_levels) + 1:
            difficulty = service_info['difficulty']
        else:
            input("Invalid choice. Press Enter to continue...")
            return
    except ValueError:
        difficulty = service_info['difficulty']
    
    certification_notes = input(f"Certification notes [{service_info['certification_notes']}]: ")
    certification_notes = certification_notes if certification_notes else service_info['certification_notes']
    
    game.update_service(service_name, description, category, difficulty, certification_notes)
    input("Service updated successfully. Press Enter to continue...")

def view_statistics(game):
    """View game statistics"""
    game.clear_screen()
    print("\n===== GAME STATISTICS =====\n")
    print(game.show_statistics())
    input("\nPress Enter to continue...")
 
if __name__ == "__main__":
    main()

def update_aws_services_database(game):
    """Update AWS services database with latest information"""
    game.clear_screen()
    print("\n===== UPDATE AWS SERVICES DATABASE =====\n")
    print("This will fetch the latest AWS service information and certification updates.")
    print("The process may take a few minutes to complete.")
    print("\nUpdate sources:")
    print("1. AWS Documentation")
    print("2. AWS Certification Exam Guides")
    print("3. AWS Blogs and What's New")
    print("4. All of the above")
    print("5. Back to Main Menu")
    
    choice = input("\nSelect update source: ")
    
    if choice == "5":
        return
    
    try:
        # Check if the updater script exists
        if not os.path.exists("aws_service_updater.py"):
            print("\nError: aws_service_updater.py not found.")
            print("Please make sure the updater script is in the same directory.")
            input("\nPress Enter to continue...")
            return
        
        # Run the updater script with appropriate arguments
        update_command = [sys.executable, "aws_service_updater.py"]
        
        if choice == "1":
            update_command.append("--docs-only")
        elif choice == "2":
            update_command.append("--cert-only")
        elif choice == "3":
            update_command.append("--blogs-only")
        # Choice 4 runs everything (default)
        
        print("\nStarting update process...")
        result = subprocess.run(update_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\nUpdate completed successfully!")
            print(result.stdout)
            
            # Reload services after update
            game.aws_services = game.load_services()
            game.categories = game.get_categories()
            
            input("\nPress Enter to continue...")
        else:
            print("\nError during update process:")
            print(result.stderr)
            input("\nPress Enter to continue...")
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        input("\nPress Enter to continue...")

