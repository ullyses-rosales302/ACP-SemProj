import random
import time
import json


class MazeTriviaGame:
    def __init__(self):
        # Define multiple levels with more complex layouts
        self.levels = [
            [
                ["S", ".", "?", ".", "#", ".", "F"],
                [".", "#", "#", ".", "#", ".", "#"],
                [".", ".", ".", "?", ".", ".", "."],
                ["#", "#", "T", "#", "#", ".", "."],
                [".", ".", "?", ".", ".", "C", "."],
            ],
            [
                ["S", ".", ".", "#", ".", "?", "F"],
                [".", "#", "#", "#", "#", "#", "."],
                [".", ".", ".", ".", "T", ".", "."],
                [".", "?", "#", ".", "#", "#", "."],
                [".", ".", ".", ".", ".", ".", "."],
            ],
            [
                ["S", ".", "?", ".", "#", "?", "F"],
                [".", "#", "#", ".", "#", ".", "#"],
                ["?", ".", ".", ".", ".", "C", "."],
                ["#", "#", "?", "#", "#", ".", "."],
                ["?", ".", "T", ".", ".", ".", "."],
            ],
        ]
        self.current_level = 0
        self.player_position = (0, 0)  # Starting point
        self.trivia_questions = {
            "general": [
                {"question": "What is the capital of France?", "answer": "Paris"},
                {"question": "What is 5 + 7?", "answer": "12"},
                {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
            ],
            "science": [
                {"question": "What is the chemical symbol for water?", "answer": "H2O"},
                {"question": "What gas do plants absorb from the atmosphere?", "answer": "Carbon dioxide"},
                {"question": "What is the speed of light in m/s?", "answer": "299792458"},
            ],
            "history": [
                {"question": "Who discovered America?", "answer": "Christopher Columbus"},
                {"question": "Who was the first president of the USA?", "answer": "George Washington"},
                {"question": "In which year did World War II end?", "answer": "1945"},
            ],
        }
        self.answered_questions = set()  # Store answered questions by their text
        self.checkpoints = {}  # Checkpoints for each level
        self.start_time = None
        self.time_limit = 300  # 5 minutes per level

    def display_maze(self):
        """Display the maze with the player's current position."""
        maze = self.levels[self.current_level]
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if (row, col) == self.player_position:
                    print("P", end=" ")  # Player position
                else:
                    print(maze[row][col], end=" ")
            print()

    def ask_question(self):
        """Ask a random trivia question."""
        category = random.choice(list(self.trivia_questions.keys()))
        questions = self.trivia_questions[category]
        
        # Filter out answered questions (check by question text)
        unanswered_questions = [q for q in questions if q["question"] not in self.answered_questions]
        
        if not unanswered_questions:  # Check if there are any unanswered questions
            print("No more unanswered questions in this category!")
            return False  # Or handle this case however you'd like
        
        question_data = random.choice(unanswered_questions)
        question, answer = question_data["question"], question_data["answer"]

        user_answer = input(f"Trivia ({category}): {question}\nYour answer: ").strip()
        if user_answer.lower() == answer.lower():
            print("Correct! You can proceed.")
            self.answered_questions.add(question)  # Store question text
            return True
        else:
            print("Wrong answer! You are sent back to the last checkpoint.")
            self.player_position = self.checkpoints.get(self.current_level, (0, 0))
            return False

    def move_player(self, direction):
        """Move the player in the specified direction."""
        maze = self.levels[self.current_level]
        row, col = self.player_position
        if direction == "up":
            new_position = (row - 1, col)
        elif direction == "down":
            new_position = (row + 1, col)
        elif direction == "left":
            new_position = (row, col - 1)
        elif direction == "right":
            new_position = (row, col + 1)
        else:
            print("Invalid move!")
            return False

        # Check if the new position is valid
        if (
            0 <= new_position[0] < len(maze)
            and 0 <= new_position[1] < len(maze[0])
            and maze[new_position[0]][new_position[1]] != "#"
        ):
            self.player_position = new_position
            cell = maze[new_position[0]][new_position[1]]
            if cell == "?":
                return self.ask_question()
            elif cell == "T":
                print("Oh no! You hit a trap and are sent back a step.")
                self.player_position = (row, col)
            elif cell == "C":
                print("Checkpoint reached! Progress saved.")
                self.checkpoints[self.current_level] = new_position
            return True
        else:
            print("You hit a wall! Try a different direction.")
            return False

    def play(self):
        """Start the game."""
        print("Welcome to the Enhanced Maze Trivia Game!")
        print("Navigate through the maze and answer trivia questions to reach the finish line.")
        print("Controls: 'up', 'down', 'left', 'right'")
        print("S = Start, F = Finish, ? = Trivia Question, T = Trap, C = Checkpoint, # = Wall\n")

        self.start_time = time.time()
        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.time_limit:
                print("Time's up! Game over!")
                break

            print(f"Time remaining: {self.time_limit - int(elapsed_time)} seconds")
            self.display_maze()
            move = input("Your move: ").strip().lower()
            if not self.move_player(move):
                continue

            # Check if player reached the finish
            maze = self.levels[self.current_level]
            if self.player_position == (0, len(maze[0]) - 1):  # Finish line position
                print("Congratulations! You completed this level!")
                self.current_level += 1
                if self.current_level >= len(self.levels):
                    print("You completed all levels! You are a maze master!")
                    break
                else:
                    print("Get ready for the next level!")
                    self.player_position = (0, 0)  # Reset position for the new level
                    self.start_time = time.time()  # Reset timer


# --- Example Usage ---
if __name__ == "__main__":
    game = MazeTriviaGame()  # Create an instance of the game
    game.play()  # Call the play method on the instance
