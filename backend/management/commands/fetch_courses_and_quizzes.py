import requests
import random
import openai
from django.core.management.base import BaseCommand
from myapp.models import Course, Quiz

# Add your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Udemy API key
UDemy_API_KEY = "YOUR_UDEMY_API_KEY"

# QuizAPI API Key
QuizAPI_KEY = "YOUR_QUIZAPI_KEY"

# Open Trivia API URL for quizzes
OTDB_API_URL = 'https://opentdb.com/api.php?amount=10&type=multiple'

class Command(BaseCommand):
    help = "Fetch and add courses and quizzes from external APIs to the database"

    def handle(self, *args, **kwargs):
        self.fetch_and_store_courses()
        self.fetch_and_store_quizzes()

    def fetch_and_store_courses(self):
        """ Fetch courses from Udemy API and store them in the Course model """
        url = 'https://www.udemy.com/api-2.0/courses/'
        headers = {'Authorization': f'Bearer {UDemy_API_KEY}'}

        response = requests.get(url, headers=headers)
        courses = response.json()['results']

        for course_data in courses:
            course_name = course_data['title']
            description = course_data['headline']

            # Check if the course already exists
            if not Course.objects.filter(name=course_name).exists():
                Course.objects.create(name=course_name, description=description)
                self.stdout.write(f"Course '{course_name}' added successfully.")
            else:
                self.stdout.write(f"Course '{course_name}' already exists.")

    def fetch_and_store_quizzes(self):
        """ Fetch quizzes from OTDB and QuizAPI and store them in the Quiz model """
        # Fetch quizzes from Open Trivia Database
        response = requests.get(OTDB_API_URL)
        quizzes = response.json()['results']

        for quiz_data in quizzes:
            question = quiz_data['question']
            options = quiz_data['incorrect_answers'] + [quiz_data['correct_answer']]
            random.shuffle(options)
            correct_answer = quiz_data['correct_answer']

            # Check if the quiz already exists
            if not Quiz.objects.filter(question=question).exists():
                Quiz.objects.create(
                    question=question,
                    options=','.join(options),
                    correct_answer=correct_answer
                )
                self.stdout.write(f"Quiz '{question}' added successfully.")
            else:
                self.stdout.write(f"Quiz '{question}' already exists.")

        # Fetch quizzes from QuizAPI
        url = 'https://quizapi.io/api/v1/questions'
        headers = {'X-Api-Key': QuizAPI_KEY}
        response = requests.get(url, headers=headers)
        quizzes = response.json()

        for quiz_data in quizzes:
            question = quiz_data['question']
            options = quiz_data['answers']
            correct_answer = quiz_data['correct_answer']

            # Store the quiz in the database if not exists
            if not Quiz.objects.filter(question=question).exists():
                Quiz.objects.create(
                    question=question,
                    options=','.join(options.values()),  # Convert dictionary to list
                    correct_answer=correct_answer
                )
                self.stdout.write(f"Quiz '{question}' added successfully.")
            else:
                self.stdout.write(f"Quiz '{question}' already exists.")
