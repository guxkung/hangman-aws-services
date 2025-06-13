import random
import os
import time

# AWS services with their descriptions
aws_services = {
    "EC2": "Elastic compute service that provides resizable compute capacity in the cloud",
    "S3": "Object storage service that offers industry-leading scalability, data availability, security, and performance",
    "LAMBDA": "Serverless compute service that lets you run code without provisioning or managing servers",
    "DYNAMODB": "Fully managed NoSQL database service that provides fast and predictable performance with seamless scalability",
    "RDS": "Managed relational database service that makes it easy to set up, operate, and scale a relational database",
    "SNS": "Fully managed messaging service for both application-to-application and application-to-person communication",
    "SQS": "Fully managed message queuing service that enables you to decouple and scale microservices",
    "CLOUDFRONT": "Content delivery network service that securely delivers data, videos, applications, and APIs globally",
    "IAM": "Web service that helps you securely control access to AWS resources",
    "CLOUDWATCH": "Monitoring and observability service that provides data and insights to monitor applications",
    "ROUTE53": "Highly available and scalable cloud Domain Name System web service",
    "GLACIER": "Secure, durable, and extremely low-cost Amazon S3 storage class for data archiving and long-term backup",
    "FARGATE": "Serverless compute engine for containers that works with both Amazon ECS and Amazon EKS",
    "ATHENA": "Interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL",
    "GLUE": "Fully managed extract, transform, and load service that makes it easy to prepare and load data for analytics"
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_hangman(tries):
    """Display the hangman based on the number of tries left."""
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
    return stages[tries]

def play_hangman():
    """Main function to play the Hangman game."""
    clear_screen()
    print("\nWelcome to AWS Hangman!")
    print("Guess the AWS service name based on its description.\n")
    
    # Select a random AWS service
    service = random.choice(list(aws_services.keys()))
    description = aws_services[service]
    
    # Initialize game variables
    word_completion = '_' * len(service)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    
    print(f"Hint: {description}")
    print(display_hangman(tries))
    print(f"Word: {' '.join(word_completion)}")
    print("\n")
    
    while not guessed and tries > 0:
        guess = input("Please guess a letter or the full word: ").upper()
        
        # Check if the guess is a single letter
        if len(guess) == 1 and guess.isalnum():
            if guess in guessed_letters:
                clear_screen()
                print(f"You already guessed the letter {guess}")
            elif guess not in service:
                clear_screen()
                print(f"{guess} is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                clear_screen()
                print(f"Good job, {guess} is in the word!")
                guessed_letters.append(guess)
                
                # Update the word completion
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(service) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                
                if "_" not in word_completion:
                    guessed = True
        
        # Check if the guess is a word
        elif len(guess) == len(service) and guess.isalnum():
            if guess in guessed_words:
                clear_screen()
                print(f"You already guessed the word {guess}")
            elif guess != service:
                clear_screen()
                print(f"{guess} is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = service
        
        else:
            clear_screen()
            print("Not a valid guess.")
        
        # Display current game state
        print(f"Hint: {description}")
        print(display_hangman(tries))
        print(f"Word: {' '.join(word_completion)}")
        print(f"Letters guessed: {', '.join(guessed_letters)}")
        print(f"Words guessed: {', '.join(guessed_words)}")
        print(f"Tries left: {tries}")
        print("\n")
    
    # Game result
    if guessed:
        print(f"Congratulations! You guessed the AWS service: {service}")
    else:
        print(f"Sorry, you ran out of tries. The AWS service was: {service}")
    
    # Ask to play again
    play_again = input("Would you like to play again? (y/n): ").lower()
    if play_again == 'y':
        play_hangman()
    else:
        print("Thanks for playing AWS Hangman! Hope you learned something about AWS services.")

if __name__ == "__main__":
    play_hangman()
