from django.shortcuts import render
from intelicopter.models import Question, Option, Trigger

# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def question(request):
    return process_answer(request)


def process_answer(request):
    # get JSON
    data = request.POST['data']

    # if first time, initialise new rank and number as 1
    if data.len is None:
        data = {
            "rank":1,
            "question":1,
            "questions":{}
        }

    # parse JSON
    rank = data["rank"]
    question = data["question"]
    questions = data["questions"]

    # get latest question object
    latest_question = Question.objects.filter(question_id=question+1)[0]

    # check if triggered, if true, show options
    #triggers = Trigger.objects.filter(question=latest_question)

    # else, repeat with next question, if end of questions for rank, go to next rank
    # bring to answering page

    return render(request, 'question.html', {})