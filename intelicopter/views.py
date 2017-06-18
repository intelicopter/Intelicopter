from django.shortcuts import render
from intelicopter.models import Question, Option, Trigger
import json

# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def question(request):
    return process_answer(request)


def process_answer(request):
    # get data from templates
    data_in_string = request.POST['data']  # will be in JSON format
    answers_in_string = request.PORT['answers'] # will be in array format

    #process JSON
    data = json.loads(data_in_string)
    answers = json.loads(answers_in_string.split())

    highest_question_number = max(data.iterkeys(), key=(lambda key: data[key]))

    # if first time, initialise new rank and number as 1
    if data.len is None:
        data = {}
    else:
        data[highest_question_number] = answers # latest qn will be the highest question number previously answered

    # get latest question object
    next_question_tracker = 1
    latest_question = Question.objects.filter(question_id=highest_question_number + next_question_tracker)[0]
    while not check_if_triggered(latest_question):
        next_question_tracker += 1
        latest_question = Question.objects.filter(question_id=highest_question_number + next_question_tracker)[0]

    latest_options = Question.objects.filter(question=latest_question)

    # to handle going back to the previous page
    previous_data = dict(data)
    data[highest_question_number + next_question_tracker] = []

    return render(request, 'question.html', {'previous_data':previous_data, 'data':data, 'options':latest_options})


def check_if_triggered(question):
    #triggers = Trigger.objects.filter(question=latest_question)
    return True