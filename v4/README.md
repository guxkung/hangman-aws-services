# AWS Hangman for Certification Prep

A fun and educational game to help you prepare for AWS certification exams by learning AWS services and their key features.

## Features

- **Learn While Playing**: Guess AWS service names based on their descriptions
- **Certification Focus**: Each service includes certification exam study notes
- **Auto-Updating Database**: Fetch the latest AWS service information and exam updates
- **Customizable Content**: Add or modify services and study notes
- **Progress Tracking**: Monitor your learning with game statistics

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the game:
```
python aws_hangman.py
```

### Main Menu Options

1. **Play Game**: Start a standard game with random service selection
2. **Filter by Category**: Play with services from a specific category (Compute, Storage, etc.)
3. **Filter by Difficulty**: Choose Easy, Medium, or Hard services
4. **Add New AWS Service**: Expand the database with custom entries
5. **Update Existing Service**: Modify descriptions or study notes
6. **View Statistics**: See your game performance
7. **Update AWS Services Database**: Fetch the latest AWS service information
8. **Exit**: Quit the game

### Automatic Updates

The game can automatically update its AWS services database from:
- AWS Documentation
- AWS Certification Exam Guides
- AWS Blogs and What's New announcements

This ensures you're always studying with the most current information for your certification exams.

## Files

- `aws_hangman.py`: Main game code
- `aws_services.json`: Database of AWS services with certification notes
- `aws_service_updater.py`: Script to fetch the latest AWS service information
- `requirements.txt`: Required Python packages

## Contributing

Feel free to enhance this game by:
- Adding more AWS services and certification notes
- Improving the automatic update functionality
- Enhancing the game mechanics

## License

This project is open source and available for educational purposes.

