import tkinter as tk
from tkinter import messagebox
import csv
import random
import time

class TriviaMazeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Trivia Maze Game")
        self.master.geometry("600x600")

        self.player_name = ""
        self.level = 1
        self.total_score = 0  # Track score across all levels
        self.start_time = 0
        self.time_remaining = 200  # Changed time to 200 seconds
        self.timer_running = False

        self.maze_size = 7  # Maximum size of the mazes (7x7 for the largest level)
        self.current_position = [0, 0]  # Starting at top-left corner
        self.levels = [
            [
                ["S", ".", "?", ".", "#", ".", "F"],
                [".", "#", "#", ".", "#", ".", "#"],
                [".", ".", ".", "?", ".", ".", "."],
                ["#", "#", "T", "#", "#", ".", "."],
                [".", ".", "?", ".", ".", "C", "."],
            ],
            [
                ["S", "?", ".", "#", "T", "?", "F"],
                [".", "#", ".", ".", "#", ".", "#"],
                ["?", ".", "#", "?", ".", ".", "."],
                [".", "#", "T", "#", "T", "#", "."],
                ["C", "?", ".", ".", "?", ".", "F"],
            ],
            [
                ["S", "?", "#", "T", "#", "?", "F"],
                ["#", ".", ".", ".", "#", "?", "#"],
                ["T", "?", "#", "?", ".", "?", "."],
                ["T", ".", "T", "#", "T", "#", "?"],
                ["?", "?", "?", "T", "?", "?", "F"],
            ]
        ]
        self.maze = self.levels[0]  # Set the starting level
        self.current_position = self.find_start_position()

        self.questions = self.load_questions()
        self.leaderboard = self.load_leaderboard()

        # UI elements
        self.title_label = tk.Label(self.master, text="Trivia Maze Game", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.name_label = tk.Label(self.master, text="Enter your name: ", font=("Arial", 14))
        self.name_label.pack()

        self.name_entry = tk.Entry(self.master, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, font=("Arial", 14))
        self.start_button.pack(pady=10)

        self.timer_label = tk.Label(self.master, text="Time: 200", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.maze_frame = tk.Frame(self.master)
        self.maze_frame.pack(pady=20)

        self.questions_asked = 0  # Keep track of the number of questions asked

    def start_game(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        self.name_entry.config(state="disabled")
        self.start_button.config(state="disabled")
        self.start_time = time.time()
        self.timer_running = True
        self.start_timer()
        self.update_maze()

    def start_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.time_remaining = max(0, 200 - int(elapsed_time))  # Adjusted to 200 seconds
            self.timer_label.config(text=f"Time: {self.time_remaining}")
            if self.time_remaining > 0:
                self.master.after(1000, self.start_timer)
            else:
                self.end_game()

    def load_questions(self):
        return [
            {"question": "What is 2+2?", "options": ["3", "4", "5", "6"], "answer": "4"},
            {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
            {"question": "What is 5*5?", "options": ["20", "25", "30", "35"], "answer": "25"},
            {"question": "What is the capital of Japan?", "options": ["Tokyo", "Seoul", "Beijing", "Bangkok"], "answer": "Tokyo"},
            {"question": "What is the color of the sky?", "options": ["Blue", "Green", "Red", "Yellow"], "answer": "Blue"},
            {"question": "What is 10+10?", "options": ["15", "20", "25", "30"], "answer": "20"},
            {"question": "What is the largest ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"},
            {"question": "Who is the author of Harry Potter?", "options": ["J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "C.S. Lewis"], "answer": "J.K. Rowling"},
            {"question": "What is the square root of 16?", "options": ["2", "3", "4", "5"], "answer": "4"},
            {"question": "What is the capital of Italy?", "options": ["Rome", "Venice", "Milan", "Florence"], "answer": "Rome"},
        ]

    def load_leaderboard(self):
        leaderboard_data = []
        try:
            with open("leaderboard.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:
                        try:
                            player_name = row[0]
                            score = int(row[1])
                            time_remaining = float(row[2])
                            leaderboard_data.append([player_name, score, time_remaining])
                        except ValueError:
                            continue
            leaderboard_data.sort(key=lambda x: x[1], reverse=True)
        except FileNotFoundError:
            return leaderboard_data
        return leaderboard_data

    def save_to_leaderboard(self):
        with open("leaderboard.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.player_name, self.total_score, self.time_remaining])

    def find_start_position(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == "S":
                    return [i, j]

    def update_maze(self):
        for widget in self.maze_frame.winfo_children():
            widget.destroy()

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                room = self.maze[i][j]

                if room == "#":
                    color = "black"
                elif room == "." or room == "?":
                    color = "white"
                elif room == "S":
                    color = "green"
                elif room == "F":
                    color = "red"
                elif room == "T":
                    color = "orange"
                elif room == "C":
                    color = "blue"

                if [i, j] == self.current_position:
                    color = "yellow"

                room_button = tk.Button(self.maze_frame, text=room, width=5, height=2, bg=color, command=lambda x=i, y=j: self.enter_room(x, y))
                room_button.grid(row=i, column=j, padx=5, pady=5)

    def enter_room(self, x, y):
        room = self.maze[x][y]

        if room == "#":
            messagebox.showinfo("Blocked", "You hit a wall!")
            return
        elif room == "T":
            messagebox.showinfo("Trap", "You fell into a trap!")
            self.end_game()
            return
        elif room == "F":
            messagebox.showinfo("Finished", "Congratulations, you reached the finish!")
            self.level += 1
            if self.level > 3:
                self.end_game()
            else:
                self.maze = self.levels[self.level - 1]
                self.current_position = self.find_start_position()
                self.update_maze()
        elif room == "C":
            self.total_score += 10  # Update total score

        if room == "?":
            self.ask_question()

        self.current_position = [x, y]
        self.update_maze()

    def ask_question(self):
        if self.questions_asked < len(self.questions):
            question_data = self.questions[self.questions_asked]
            self.questions_asked += 1
            self.show_question(question_data["question"], question_data["options"], question_data["answer"])

    def show_question(self, question_text, options, correct_answer):
        question_window = tk.Toplevel(self.master)
        question_window.title(f"Question {self.questions_asked}")

        question_label = tk.Label(question_window, text=question_text, font=("Arial", 14))
        question_label.pack(pady=20)

        var = tk.StringVar()
        for option in options:
            option_button = tk.Radiobutton(question_window, text=option, value=option, variable=var, font=("Arial", 12))
            option_button.pack(anchor="w", padx=20)

        submit_button = tk.Button(question_window, text="Submit", command=lambda: self.check_answer(var.get(), correct_answer, question_window), font=("Arial", 14))
        submit_button.pack(pady=10)

    def check_answer(self, selected_answer, correct_answer, window):
        if selected_answer == correct_answer:
            self.total_score += 10
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            messagebox.showinfo("Incorrect", f"Wrong! The correct answer was {correct_answer}.")
        window.destroy()

    def end_game(self):
        self.timer_running = False
        self.save_to_leaderboard()
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.total_score}, Time: {self.time_remaining} seconds.")
        self.show_leaderboard()

    def show_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title("Leaderboard")

        leaderboard_label = tk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 16))
        leaderboard_label.pack(pady=20)

        leaderboard_list = "\n".join([f"{row[0]} - {row[1]} points - {row[2]} seconds" for row in self.leaderboard])
        leaderboard_text = tk.Label(leaderboard_window, text=leaderboard_list, font=("Arial", 12))
        leaderboard_text.pack(pady=10)

def main():
    root = tk.Tk()
    game = TriviaMazeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
