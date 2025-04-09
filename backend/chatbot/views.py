from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai
import os
from dotenv import load_dotenv
from django.http import HttpResponse
import cv2
import pytesseract
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import random

def generate_quiz(request):
    quizzes = Quiz.objects.all()
    quiz = random.choice(quizzes)
    
    options = quiz.options.split(',')
    random.shuffle(options)
    
    return JsonResponse({
        'question': quiz.question,
        'options': options,
        'correct_answer': quiz.correct_answer
def scan_notes(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        
        img = cv2.imread(file_url)
        text = pytesseract.image_to_string(img)
        
        return JsonResponse({'scanned_text': text})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

openai.api_key = 'your_openai_api_key'

def chatbot_query(request):
    question = request.GET.get('question', '')
    if not question:
        return JsonResponse({'error': 'No question provided'}, status=400)
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=100
    )
    
    return JsonResponse({'response': response.choices[0].text.strip()})

def test_chatbot(request):
    question = request.GET.get('question')  # Get the question from the query parameters
    
    if not question:
        return JsonResponse({"error": "No question provided"}, status=400)  # Return error if no question is provided
    
    # Process the question (you can call your chatbot logic here)
    response = "This is a mock response to your question: " + question
    
    return JsonResponse({"response": response})

load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(['GET', 'POST'])  # Accept both GET and POST requests
def ask_gpt(request):
    if request.method == 'POST':
        # Handle POST request
        user_question = request.data.get('question')

        if not user_question:
            return Response({'error': 'Please provide a question.'}, status=400)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor named LearnAI."},
                    {"role": "user", "content": user_question},
                ]
            )
            answer = response.choices[0].message['content'].strip()
            return Response({'answer': answer})

        except Exception as e:
            return Response({'error': str(e)}, status=500)

    elif request.method == 'GET':
        # Handle GET request
        user_question = request.GET.get('question', '')

        if user_question:
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",  # You can change the model if needed
                    prompt=user_question,
                    max_tokens=150
                )
                answer = response.choices[0].text.strip()
                return JsonResponse({'answer': answer})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'No question provided'}, status=400)


def award_points(user, points):
    progress, created = StudentProgress.objects.get_or_create(user=user)
    progress.points += points
    progress.save()

def award_badge(user, badge):
    progress, created = StudentProgress.objects.get_or_create(user=user)
    if badge not in progress.badges:
        progress.badges += f", {badge}"
        progress.save()
