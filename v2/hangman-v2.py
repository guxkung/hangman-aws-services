import random
import os
import json
import time
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

# Main function to be implemented in the next step
def main():
    print("AWS Hangman for Certification Prep - Coming soon!")

if __name__ == "__main__":
    main()
