from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv
from .models import Quiz, StudentProgress

import openai
import logging
import os
import random
import cv2
import pytesseract

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(['POST'])
def ask_gpt(request):
    """
    Endpoint to ask GPT a question using OpenAI API.
    Accepts POST requests with a 'question' parameter.
    """
    user_question = request.data.get('question')
    if not user_question:
        return Response({'error': 'Please provide a question.'}, status=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful AI tutor named LearnAI."},
                      {"role": "user", "content": user_question}]
        )
        answer = response.choices[0].message['content'].strip()
        return Response({'answer': answer})
    except Exception as e:
        logger.error(f"Error in ask_gpt: {str(e)}")
        return Response({'error': 'An error occurred while processing the question.'}, status=500)


@api_view(['GET'])
def generate_quiz(request):
    """
    Endpoint to generate a random quiz from the database.
    """
    try:
        quizzes = Quiz.objects.all()
        if not quizzes.exists():
            return Response({'error': 'No quizzes available'}, status=404)

        quiz = random.choice(quizzes)
        options = quiz.options.split(',')
        random.shuffle(options)

        return Response({
            'question': quiz.question,
            'options': options,
            'correct_answer': quiz.correct_answer
        })
    except Exception as e:
        logger.error(f"Error in generate_quiz: {str(e)}")
        return Response({'error': 'An error occurred while generating the quiz.'}, status=500)


@api_view(['POST'])
def scan_notes(request):
    """
    Endpoint to scan an image containing handwritten notes and extract text.
    """
    if 'file' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=400)

    uploaded_file = request.FILES['file']
    if not uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        return Response({'error': 'Invalid file type. Please upload an image.'}, status=400)

    try:
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = os.path.join(fs.location, filename)

        img = cv2.imread(file_path)
        text = pytesseract.image_to_string(img)

        fs.delete(filename)  # Clean up the file
        return Response({'scanned_text': text})
    except Exception as e:
        logger.error(f"Error in scan_notes: {str(e)}")
        return Response({'error': 'An error occurred while processing the image.'}, status=500)


def award_points(user, points):
    """
    Function to award points to a user.
    """
    try:
        progress, _ = StudentProgress.objects.get_or_create(user=user)
        progress.points += points
        progress.save()
    except Exception as e:
        logger.error(f"Error in award_points: {str(e)}")


def award_badge(user, badge):
    """
    Function to award a badge to a user.
    """
    try:
        progress, _ = StudentProgress.objects.get_or_create(user=user)
        if badge not in progress.badges:
            progress.badges += f", {badge}"
            progress.save()
    except Exception as e:
        logger.error(f"Error in award_badge: {str(e)}")
