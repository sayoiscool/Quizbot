import requests
import html
import random # Shuffle the options to randomize their order


quiz_rules = "The rules are simple. \nYou get a list of 10 questions - a mix of multiple choice and true/false questions to answer. \nSelect your answer where necessary and you get your scores at the end of the quiz. \nTry not to google your answers! Remember, it's just fun! \nSo, what do you say? Shall we crack on?"

username = input("Enter your name: ")
def welcome_msg():
   #Displays a welcome message and asks if the user wants to see the quiz rules.
   print(f"Hi {username}! I'm Jane, your quiz facilitator. \nWelcome to Triviawrld. It is a fun quiz designed to test on your knowledge on random science facts. \nWould you like me to go over the quiz rules?")
   while True:
    a = input("Yes / No: ").lower()  
    if a == "yes":  
        print(quiz_rules)
        return True # Indicate the user is ready to proceed
    elif a == "no": 
        print("No worries, maybe some other time.")
        return False  # Indicate the user opted out
    else: 
        print("Please enter either 'Yes' or 'No'")
#welcome_msg()
def quiz_start_msg():
    #Asks if the user is ready to start the quiz
    proceed = welcome_msg() # Get the user's response from welcome_msg
    if not proceed:  # If the user opted out in welcome_msg, stop here
        print("Exiting the quiz. Goodbye!")
        return False #return without a value in your code means that the function exits early and returns None
    while True:
        b = input("Yes / No").lower()
        if b == "yes":
            print("Great! Let's begin")
            return True
        elif b == "no":
            print("No worries, maybe some other time")
            return False
        else:
            print("Please enter Yes or No")
#quiz_start_msg()

def get_posts():
    #Fetches quiz questions from the API.
    url = 'https://opentdb.com/api.php?amount=10&category=17&difficulty=easy'
    
    try:
        response = requests.get(url) #send a GET request to the API to retrieve the data. Response object contains all the information returned by the API, such as the status code and the actual data.
        if response.status_code == 200:
            posts = response.json() #If the request was successful (status_code == 200), the function extracts the JSON data using .json().
            return posts #The data is stored in the variable posts and returned to the caller.(The JSON will typically contain trivia questions, their categories, answers, etc.)
        else:
            print('Error:', response.status_code) #If response code is not 200, the error status code is printed, i.e 404/500
            return None #and re-raises the error for debugging
    except requests.exceptions.RequestException as e:
        print('Error:', e)  #If a network error or other request-related exception occurs (e.g., no internet, timeout, invalid URL), it’s caught by the except block.
        return None #The error message is printed, and the function returns none
#get_posts()


def begin_quiz():  
    quiz = get_posts()
    #Runs the quiz and calculates the score.
    score = 0  
    for index, i in enumerate(quiz['results'], start=1):
        question = html.unescape(i['question']) #handle weird/incorrectly formatted texts from the api call
        correct_answer = html.unescape(i['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in i['incorrect_answers']]
        print(f"{index}. {question}")
        options = [correct_answer] + incorrect_answers #combine string 'correct_answer' with list 'incorrect_answer'
        
        random.shuffle(options)
        
        #for idx, i in enumerate(options, start=0):
            #letter = chr(65 + idx) #chr(65 + idx) converts the index to a letter (65 is ASCII for "A").
        option_letters = {chr(97 + idx): option for idx, option in enumerate(options)}  # {'a': option1, 'b': option2, ...}
        for letter, option in option_letters.items():
            print(f"{letter}) {option}") #extract everything after the bracket
            #numbered_option =  f"{letter}){i}"
        
        while True:
            user_input = input("Enter your answer (a, b, c, d): ").lower()
            # Validate the input
            if user_input in option_letters:
                # Get the selected answer
                user_answer = option_letters[user_input]
                
                # Check if it's correct
                if user_answer == correct_answer:
                    print("Correct!")
                    score += 1
                else:
                    print(f"Wrong answer! The correct answer is: {correct_answer}")
                
                break  # Exit the loop after a valid answer
            else:
                print("Invalid input. Please enter a valid option (a, b, c, d).")
    print(f"Your total score is: {score}")
    return True
#begin_quiz()

def quiz_complete():
    #Asks the user if they want to play again after completing the quiz.
    print("Congratulations on completing the quiz! \nWould you like to play again?")
    while True:
        z = input("Yes / No: ").lower()  
        if z == "yes":  
            begin_quiz()
            break # Break out of the loop if the user enters "yes"
        elif z == "no": 
            print("Thanks for taking part. Until next time...")
            break  # Break out of the loop if the user enters "no"
        else: 
            print("Please enter either 'Yes' or 'No'")
#quiz_complete()

def run_quiz():
    #Main function to run the whole quiz
    while True:
        proceed_quiz = quiz_start_msg()  # Ask if the user is ready to start
        if not proceed_quiz:  # If the user opts out, stop the quiz
            break  # Exit the loop and stop the quiz
        
        begin_quiz()  # Start the quiz
        
        play_again = quiz_complete()  # Ask if they want to play again
        if not play_again:  # If the user says "no" to playing again, exit
            break  # Exit the loop and end the quiz
run_quiz()