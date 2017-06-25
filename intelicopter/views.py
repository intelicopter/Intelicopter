from django.shortcuts import render
from intelicopter.models import Question, Option, Trigger
import json

# Create your views here.

def home(request):
    create_example_data()
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
    # get max questions here
    #if statement to check if last question
    latest_question = Question.objects.filter(question_id=highest_question_number + next_question_tracker)[0]
    while not check_if_triggered(latest_question, data):
        next_question_tracker += 1
        latest_question = Question.objects.filter(question_id=highest_question_number + next_question_tracker)[0]

    latest_options = Question.objects.filter(question=latest_question)

    # to handle going back to the previous page
    previous_data = dict(data)
    data[highest_question_number + next_question_tracker] = []

    return render(request, 'question.html', {'previous_data':previous_data, 'data':data, 'options':latest_options})


def check_if_triggered(question, data):
    triggers = Trigger.objects.filter(question=question)
    trigger_list = {}
    
    # for every trigger, insert key value pair into list
    return True
    
    
def get_relevant_items(request):
    return True


def create_example_data():
    qn1 = Question.objects.create(1, "What is your gender?", 1)
    qn2 = Question.objects.create(2, "Are you pregnant?", 1)
    qn3 = Question.objects.create(3, "Are you employed?", 1)

    qn1.save()
    qn2.save()
    qn3.save()

    option1 = Option.objects.create(1, qn1, "Male")
    option2 = Option.objects.create(2, qn1, "Female")
    option3 = Option.objects.create(3, qn2, "Yes")
    option4 = Option.objects.create(4, qn2, "No")
    option5 = Option.objects.create(5, qn2, "I am not sure")
    option6 = Option.objects.create(6, qn3, "Yes")
    option7 = Option.objects.create(7, qn3, "No")

    option1.save()
    option2.save()
    option3.save()
    option4.save()
    option5.save()
    option6.save()
    option7.save()

    trigger = Trigger.objects.create(1, qn2, qn1, "Female")
    trigger.save()