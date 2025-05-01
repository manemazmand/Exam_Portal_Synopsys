import random
import sys
import csv
import threading
import time
import random
from colorama import Fore, Style, init
init(autoreset=True)

class Question:
    def __init__(self, prompt, options, correct_option):
        self.prompt = prompt
        self.options = options
        self.correct_option = correct_option

class Exam:
    def __init__(self, subject, questions):
        self.subject = subject
        self.questions = questions
        self.score = 0

# Described the whole process of taking exam
    def take_exam(self):
        print(f"\nStarting exam: {self.subject}\n")
        correct_answers = 0
        detailed_results = []
        for idx, question in enumerate(self.questions, 1):
            print(f"Q{idx}: {question.prompt}")
            for opt in question.options:
                print(opt)

            answer = self.get_answer_with_timeout(20)  # 10 Second for the question

            if answer == question.correct_option:
                print(Fore.GREEN + "Correct!\n")
                correct_answers += 1
                detailed_results.append((question, True))
            else:
                print(Fore.RED + f"Wrong! Correct answer was: {question.correct_option}\n")
                detailed_results.append((question, False))

            if answer is None:
                print("\nTime's up! Moving to next question.")
            elif answer == question.correct_option:
                self.score += 1
        self.show_result()
        
    def get_answer_with_timeout(self, timeout):
        answer = [None]
        timer_running = [True]

        def read_input():
            user_input = ""
            while timer_running[0]:
                ch = sys.stdin.read(1)
                if ch in ['\n', '\r']:
                    break
                user_input += ch
            answer[0] = user_input.strip().upper()
            timer_running[0] = False

        def countdown():
            for remaining in range(timeout, 0, -1):
                if not timer_running[0]:
                    break
                sys.stdout.write(f"\rTime left: {remaining:2d} sec  Your answer (A/B/C/D): {''}")
                sys.stdout.flush()
                time.sleep(1)
            if timer_running[0]:
                print("\nTime's up! Moving to next question.")

        input_thread = threading.Thread(target=read_input)
        timer_thread = threading.Thread(target=countdown)

        input_thread.daemon = True
        timer_thread.daemon = True

        input_thread.start()
        timer_thread.start()

        input_thread.join(timeout)
        timer_running[0] = False
        timer_thread.join()

        if answer[0] is None or answer[0] == "":
            return None
        return answer[0]

    def show_result(self):
        total = len(self.questions)
        percentage = (self.score / total) * 100
        print(f"\nExam Completed. Your score: {self.score}/{total}")
        print(f"Percentage: {percentage:.2f}%")
        if percentage >= 90:
            print("Grade: A")
        elif percentage >= 75:
            print("Grade: B")
        elif percentage >= 60:
            print("Grade: C")
        else:
            print("Grade: Fail")
    
        username = input("\nEnter your username to save the result: ").strip()
        save_result_to_csv(username, self.subject, self.score, total, percentage)    
        
   
#All the questions
def load_questions(subject):
    sample_questions = {
        "Math": [
            Question("What is 2 + 2?", ["A) 3", "B) 4", "C) 5", "D) 6"], "B"),
            Question("What is 5 * 6?", ["A) 30", "B) 35", "C) 25", "D) 20"], "A"),
            Question("What is 10 / 2?", ["A) 2", "B) 3", "C) 5", "D) 6"], "C"),
            Question("What is the square root of 16?", ["A) 2", "B) 4", "C) 8", "D) 6"], "B"),
            Question("What is 12 - 7?", ["A) 5", "B) 6", "C) 7", "D) 8"], "A")
        ],
        "Programming": [
            Question("What does 'print' do in Python?", ["A) Inputs data", "B) Outputs data", "C) Loops data", "D) Deletes data"], "B"),
            Question("Correct file extension for Python?", ["A) .pt", "B) .pyt", "C) .py", "D) .python"], "C"),
            Question("Which keyword is used to create a function?", ["A) func", "B) def", "C) function", "D) define"], "B"),
            Question("Which symbol is used for comments?", ["A) //", "B) /* */", "C) #", "D) <!-- -->"], "C"),
            Question("Which data type is [1, 2, 3]?", ["A) tuple", "B) list", "C) dict", "D) set"], "B")
        ],
        "History": [
            Question("Who discovered America?", ["A) Christopher Columbus", "B) Isaac Newton", "C) Galileo", "D) Einstein"], "A"),
            Question("Year WWII ended?", ["A) 1940", "B) 1945", "C) 1950", "D) 1939"], "B"),
            Question("First president of USA?", ["A) Abraham Lincoln", "B) Thomas Jefferson", "C) George Washington", "D) John Adams"], "C"),
            Question("Where were the pyramids built?", ["A) Rome", "B) Egypt", "C) Greece", "D) China"], "B"),
            Question("Fall of the Berlin Wall year?", ["A) 1985", "B) 1987", "C) 1989", "D) 1991"], "C")
        ],
        "English": [
            Question("Synonym for 'quick'?", ["A) Slow", "B) Fast", "C) Lazy", "D) Dull"], "B"),
            Question("Correct spelling:", ["A) Recieve", "B) Receive", "C) Recive", "D) Receeve"], "B"),
            Question("Opposite of 'happy'?", ["A) Sad", "B) Angry", "C) Mad", "D) Glad"], "A"),
            Question("Meaning of 'benevolent'?", ["A) Evil", "B) Kind", "C) Angry", "D) Greedy"], "B"),
            Question("Plural of 'child'?", ["A) Childs", "B) Childes", "C) Children", "D) Childrens"], "C")
        ],
        "Physics": [
            Question("Unit of force?", ["A) Joule", "B) Newton", "C) Watt", "D) Pascal"], "B"),
            Question("Speed of light?", ["A) 300,000 km/s", "B) 150,000 km/s", "C) 100,000 km/s", "D) 500,000 km/s"], "A"),
            Question("What is gravity?", ["A) Magnetic force", "B) Force pulling objects", "C) Electric field", "D) Light energy"], "B"),
            Question("Unit of power?", ["A) Watt", "B) Newton", "C) Pascal", "D) Ohm"], "A"),
            Question("Basic unit of electric current?", ["A) Volt", "B) Ampere", "C) Ohm", "D) Watt"], "B")
        ]
    }

    questions = sample_questions.get(subject, [])
    return random.sample(questions, min(3, len(questions)))

def load_all_questions():
    all_subjects = ["Math", "Programming", "History", "English", "Physics"]
    all_questions = []
    for subject in all_subjects:
        all_questions.extend(load_questions(subject))
    return all_questions

# Saving results to CSV file "exam_results"
def save_result_to_csv(username, subject, score, total_questions, percentage):
    filename = "exam_results.csv"
    header = ["Username", "Subject", "Score", "Total Questions", "Percentage"]

    try:
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            file.seek(0, 2)
            if file.tell() == 0:
                writer.writerow(header)
            writer.writerow([username, subject, score, total_questions, f"{percentage:.2f}%"])
    except Exception as e:
        print(f"Error saving results: {e}")

def view_results():
    try:
        with open('exam_results.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            results = list(reader)

            if len(results) <= 1:
                print("No past results found.")
            else:
                print("\n--- Past Exam Results ---")
                header = results[0]
                print(f"{header[0]:<20} {header[1]:<15} {header[2]:<10} {header[3]:<10}")
                print("-" * 60)

                for row in results[1:]:
                    print(f"{row[0]:<20} {row[1]:<15} {row[2]:<10} {row[3]:<10}")
    except FileNotFoundError:
        print("No results file found yet.")

    input("\nPress Enter to return to the main menu...")

def clear_results():
    filename = 'exam_results.csv'
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Subject', 'Score', 'Max Score'])  
        print(f"Results file '{filename}' has been cleared successfully!")
    except Exception as e:
        print(f"Failed to clear results: {e}")

#Statistics
def show_statistics():
    try:
        with open("exam_results.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No results found.")
        return

    if len(lines) <= 1:
        print("No exam results recorded yet.")
        return

    total_exams = 0
    total_percentage = 0
    best_percentage = 0

    for line in lines[1:]:
        parts = line.strip().split(",")
        if len(parts) < 5:
            continue
        username, subject, score, total_questions, percentage = parts

        percentage_value = float(percentage.replace('%', ''))

        total_exams += 1
        total_percentage += percentage_value
        if percentage_value > best_percentage:
            best_percentage = percentage_value

    avg_percentage = total_percentage / total_exams if total_exams > 0 else 0

    print("\nUser Exam Statistics:")
    print(f"Total exams taken: {total_exams}")
    print(f"Average percentage: {avg_percentage:.2f}%")
    print(f"Best percentage: {best_percentage:.2f}%\n")


def main():
    available_subjects = ["Math", "Programming", "History", "English", "Physics"]

    while True:
        print("\nWelcome to the Online Exam Portal")
        print("1. Take Exam")
        print("2. View Past Results")
        print("3. Clear Results")
        print("4. Random Quiz")
        print("5. Show Statistics")
        print("6. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            print("\nAvailable subjects:")
            for idx, subj in enumerate(available_subjects, 1):
                print(f"{idx}. {subj}")

            subj_choice = input("Choose subject by number: ").strip()
            try:
                subj_idx = int(subj_choice) - 1
                if subj_idx < 0 or subj_idx >= len(available_subjects):
                    raise IndexError
                subject = available_subjects[subj_idx]
            except (ValueError, IndexError):
                print("Invalid subject choice. Please try again.")
                continue  # Вернуться к меню выбора действия

            questions = load_questions(subject)
            exam = Exam(subject=subject, questions=questions)
            exam.take_exam()

        elif choice == '2':
            view_results()

        elif choice == '3':
            confirm = input("Are you sure you want to clear all results? (Y/N): ").strip().upper()
            if confirm == 'Y':
                clear_results()
            else:
                print("Clear results cancelled.")

        elif choice == '4':
            questions = load_all_questions()
            if len(questions) < 5:
                print("Not enough questions for a random quiz.")
                continue
            random_questions = random.sample(questions, 5)
            exam = Exam(subject="Random Quiz", questions=random_questions)
            exam.take_exam()

        elif choice == '5':
            show_statistics()

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
