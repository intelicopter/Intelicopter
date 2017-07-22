import json

from django.shortcuts import render, redirect

from models import Question, Option, Trigger, Group, Activity, Criterion


# Create your views here.

def home(request):
    #create_example_data()
    return render(request, 'home.html', {})


def question(request):
    return process_answer(request)


def process_answer(request):

    # "data" will be stored in JSON format in this way:
    # {
    #     "1": {
    #         "1": "yes"
    #     },
    #     "2": {
    #         "1": "Leg",
    #         "2": "Hand"
    #     }
    # }

    try:
        # get data from templates
        data_in_string = request.POST['data']  # will be in JSON format shown above
        answers_in_string = request.POST['answers']  # will be in array format
    except:
        # if first time, initialise data
        data_in_string = '{"0":null}'
        answers_in_string = ''

    # convert JSON to dictionary
    data = json.loads(data_in_string)

    highest_question_number = 0
    answers = []
    if len(answers_in_string) > 0:
        answers = answers_in_string.split(",")

    if len(data) > 0:
        # get the highest key number. Length works because unanswered questions are also in the data dictionary as blank
        highest_question_number = len(data) - 1

    if len(answers) > 0:
        # latest qn will be the highest question number previously answered
        data[unicode(str(highest_question_number+1), "utf-8")] = answers
        highest_question_number = len(data) - 1  # get the highest key number

    # get latest question object
    next_question_tracker = 1


    # check if last question
    try:
        latest_question = Question.objects.get(id=highest_question_number+next_question_tracker)
    except:
        # return render(request, 'results.html', {})
        # return redirect(get_relevant_activities, request=request, data=data)
        return get_relevant_activities(request, data)  # future development

    # if not triggered, go to the next question
    while not check_if_triggered(latest_question, data):
        data[unicode(str(highest_question_number+next_question_tracker), "utf-8")] = "skip"
        next_question_tracker += 1
        try:
            latest_question = Question.objects.get(id=highest_question_number + next_question_tracker)
        except:
            #return render(request, 'results.html', {})
            #return redirect(get_relevant_activities, request=request, data=data)
            return get_relevant_activities(request, data)  # future development

    latest_question_text = latest_question.text

    # get the options for the latest question
    latest_options = []
    for options in Option.objects.filter(question=latest_question):
        latest_options.append(options.option_text)


    # converting to string format to send to template
    if len(data) > 0:
        data_in_string = json.dumps(data)

    # get number of questions answered at the moment for question number feature
    questions_left = Question.objects.count() - (highest_question_number + next_question_tracker) + 1

    return render(request, 'question.html', {'data':data,
                                             'question':latest_question_text,
                                             'options':latest_options,
                                             "answers_in_string":answers_in_string,
                                             "data_in_string":data_in_string,
                                             "highest_question_number":highest_question_number,
                                             "questions_left":questions_left})


def check_if_triggered(question, data):
    triggers = Trigger.objects.filter(question=question)

    # for every trigger, insert key value pair into list k:[,,,]
    trigger_list = {}
    for trigger in triggers:
        trigger_question_id = str(trigger.trigger_question.id).encode('UTF-8')
        if trigger_question_id in data:
            if trigger.trigger_text.encode('UTF-8') not in data[trigger_question_id]:
                return False
    
    # for every trigger, find if key exist in data, if not found, break loop and return false
    # if found, compare if lists are the same, if not same, return false
    # return true at the end of loop
    return True
    
    
def get_relevant_activities(request, data):
    #to store relevant activities
    relevant_activities = []
    activities_checked = 0

    # get all activity objects
    activities = Activity.objects.all()
    activities_number = Activity.objects.all().count()

    for activity in activities:
        if check_activity_relevance(data, activity):
            relevant_activities.append(activity)
            activities_checked += 1

    return render(request, 'results.html', {"activities_number": activities_number,
                                            "activities_checked": activities_checked,
                                            "relevant_activities": relevant_activities})


def check_activity_relevance(data, activity):
    criteria = Criterion.objects.filter(activity=activity, radio_group_id__isnull=True)
    number_of_criteria = Criterion.objects.filter(activity=activity, radio_group_id__isnull=True).count()
    pass_counter = 0
    for criterion in criteria:
        question_number = criterion.question.id
        question_text = criterion.question_text
        question_range = criterion.range
        radio_group_id = criterion.radio_group_id
        for answers in data[unicode(str(question_number), "utf-8")]:
            for answer in answers:
                if answer == "skip":
                    return False
                elif question_range is None:
                    if question_text == answer:
                        pass_counter += 1
                elif question_range == -2:
                    if float(question_text) < float(answer):
                        pass_counter += 1
                elif question_range == -1:
                    if float(question_text) <= float(answer):
                        pass_counter += 1
                elif question_range == 1:
                    if float(question_text) > float(answer):
                        pass_counter += 1
                elif question_range == 2:
                    if float(question_text) <= float(answer):
                        pass_counter += 1

    if pass_counter == number_of_criteria or criteria is None:
        return True
    else:
        return False


def create_example_data():

    # qn1 = Question.objects.create(id=1, text="What is your gender?", question_type=1)
    # qn2 = Question.objects.create(id=2, text="Are you pregnant?", question_type=1)
    # qn3 = Question.objects.create(id=3, text="Are you employed?", question_type=1)
    #
    # option1 = Option.objects.create(id=1, question=qn1, option_text="Male")
    # option2 = Option.objects.create(id=2, question=qn1, option_text="Female")
    # option3 = Option.objects.create(id=3, question=qn2, option_text="Yes")
    # option4 = Option.objects.create(id=4, question=qn2, option_text="No")
    # option5 = Option.objects.create(id=5, question=qn2, option_text="I am not sure")
    # option6 = Option.objects.create(id=6, question=qn3, option_text="Yes")
    # option7 = Option.objects.create(id=7, question=qn3, option_text="No")
    #
    # trigger = Trigger.objects.create(id=1, question=qn2, trigger_question=qn1, trigger_text="Female")
    #
    # group1 = Group.objects.create(id=1,
    #                               name="Example Group 1",
    #                               description="This is an example Group",
    #                               postal_code="640547")
    #
    # activity1 = Activity.objects.create(id=1,
    #                                     group=group1,
    #                                     name="Males Only Activity")
    # activity2 = Activity.objects.create(id=2,
    #                                     group=group1,
    #                                     name="Pregnant Only Activity")
    # activity3 = Activity.objects.create(id=3,
    #                                     group=group1,
    #                                     name="Everyone's Activity")
    # activity4 = Activity.objects.create(id=4,
    #                                     group=group1,
    #                                     name="EmployedYesNo Activity")

    # criterion1 = Criterion.objects.create(id=1,
    #                                       activity=Activity.objects.get(id=1),
    #                                       question=Question.objects.get(id=1),
    #                                       question_text="Male")
    # criterion2 = Criterion.objects.create(id=2,
    #                                       activity=Activity.objects.get(id=2),
    #                                       question=Question.objects.get(id=2),
    #                                       question_text="Yes")
    # criterion3 = Criterion.objects.create(id=3,
    #                                       activity=Activity.objects.get(id=4),
    #                                       question=Question.objects.get(id=3),
    #                                       question_text="Yes")
    # criterion4 = Criterion.objects.create(id=4,
    #                                       activity=Activity.objects.get(id=4),
    #                                       question=Question.objects.get(id=3),
    #                                       question_text="No")

    return True