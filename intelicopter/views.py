import json
import csv
from django.shortcuts import render
from django.db.models import Max
from models import Question, Option, Trigger, Group, Activity, Criterion


def home(request):
    create_example_data()
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
        #answers = answers_in_string.split(",")
        answers = request.POST.getlist('answers')

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
        data[unicode(str(highest_question_number+next_question_tracker), "utf-8")] = "skip".split()
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
    latest_options = json.dumps(latest_options) # to be able to use in template Javascript

    latest_question_type = latest_question.question_type

    # converting to string format to send to template
    if len(data) > 0:
        data_in_string = json.dumps(data)

    # get number of questions answered at the moment for question number feature.
    questions_left = Question.objects.count() - (highest_question_number + next_question_tracker) + 1

    return render(request, 'question.html', {'data':data,
                                             'type':latest_question_type,
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

    # debugging
    numpass = []

    for activity in activities:
        numpass.append(check_activity_relevance(data, activity))
        if check_activity_relevance(data, activity):
            relevant_activities.append(activity.name)
        activities_checked += 1

    return render(request, 'results.html', {"activities_number": activities_number,
                                            "activities_checked": numpass,
                                            "relevant_activities": relevant_activities})


def check_activity_relevance(data, activity):
    criteria = Criterion.objects.filter(activity=activity)
    number_of_criteria_without_radio_group = Criterion.objects.filter(activity=activity).filter(radio_group_id=None).count()
    number_of_radio_groups = Criterion.objects.filter(activity=activity).aggregate(Max('radio_group_id'))['radio_group_id__max']
    if number_of_radio_groups is not None:
        number_of_criteria = number_of_criteria_without_radio_group + number_of_radio_groups
    else:
        number_of_criteria = number_of_criteria_without_radio_group
    radio_groups_passed = []
    pass_counter = 0
    for criterion in criteria:
        if (criterion.radio_group_id is None) or (criterion.radio_group_id is not None and criterion.radio_group_id not in radio_groups_passed):
            question_number = criterion.question.id
            question_text = criterion.question_text
            question_range = criterion.range
            radio_group_id = criterion.radio_group_id
            for answer in data[unicode(str(question_number), "utf-8")]:
                if answer == unicode(str("skip"), "utf-8"):
                    return False
                elif question_range is None:
                    if question_text == answer:
                        pass_counter += 1
                        if criterion.radio_group_id is not None:
                            radio_groups_passed.append(radio_group_id)
                elif question_range == -2:
                    if float(question_text) > float(answer):
                        pass_counter += 1
                        if criterion.radio_group_id is not None:
                            radio_groups_passed.append(radio_group_id)
                elif question_range == -1:
                    if float(question_text) >= float(answer):
                        pass_counter += 1
                        if criterion.radio_group_id is not None:
                            radio_groups_passed.append(radio_group_id)
                elif question_range == 1:
                    if float(question_text) <= float(answer):
                        pass_counter += 1
                        if criterion.radio_group_id is not None:
                            radio_groups_passed.append(radio_group_id)
                elif question_range == 2:
                    if float(question_text) < float(answer):
                        pass_counter += 1
                        if criterion.radio_group_id is not None:
                            radio_groups_passed.append(radio_group_id)

    if pass_counter == number_of_criteria or number_of_criteria == 0:
        return True
    else:
        return False


def get_csv_data(filename):
    data = []
    with open('filename' + '.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    data.pop(0)  # to remove the first row, which is the heading
    return data


def refresh_database():
    # clear database
    Question.objects.all().delete()
    Option.objects.all().delete()
    Trigger.objects.all().delete()
    Group.objects.all().delete()
    Activity.objects.all().delete()
    Criterion.objects.all().delete()

    # question
    data = get_csv_data("question")
    for row in data:
        Question.objects.create(id=int(row[0]),
                                text=row[1],
                                question_type=int(row[2]))

    # option
    data = get_csv_data("option")
    for row in data:
        Option.objects.create(id=int(row[0]),
                              question=Question.objects.get(id=int(row[1])),
                              option_text=row[2])

    # trigger
    data = get_csv_data("trigger")
    for row in data:
        Trigger.objects.create(id=int(row[0]),
                               question=Question.objects.get(id=int(row[1])),
                               trigger_question=Question.objects.get(id=int(row[2])),
                               trigger_text=row[3])

    # group
    data = get_csv_data("group")
    for row in data:
        Group.objects.create(id=int(row[0]),
                             name=row[1],
                             description=row[2],
                             address=row[3],
                             postal_code=row[4],
                             contact_name=row[5],
                             contact_number=row[6],
                             contact_email=row[7])

    # activity
    data = get_csv_data("activity")
    for row in data:
        Group.objects.create(id=int(row[0]),
                             group=Group.objects.get(id=int(row[1])),
                             name=row[2],
                             description=row[3],
                             address=row[4],
                             postal_code=row[5],
                             contact_name=row[6],
                             contact_number=row[7],
                             contact_email=row[8])

    # criterion
    data = get_csv_data("criterion")
    for row in data:
        range_value = row[4]
        radio_group_id_value = row[5]
        if range_value is "":
            range_value = None
        if radio_group_id_value is "":
            radio_group_id_value = None

        Criterion.objects.create(id=int(row[0]),
                                 activity=Activity.objects.get(id=int(row[1])),
                                 question=Question.objects.get(id=int(row[2])),
                                 question_text=row[3],
                                 range=range_value,
                                 radio_group_id=radio_group_id_value)


def create_example_data():
    Question.objects.all().delete()
    Option.objects.all().delete()
    Trigger.objects.all().delete()
    Group.objects.all().delete()
    Activity.objects.all().delete()
    Criterion.objects.all().delete()

    qn1 = Question.objects.create(id=1, text="What is your gender?", question_type=1)
    qn2 = Question.objects.create(id=2, text="Are you pregnant?", question_type=1)
    qn3 = Question.objects.create(id=3, text="Are you employed?", question_type=1)
    qn4 = Question.objects.create(id=4, text="What is your income?", question_type=4)
    qn5 = Question.objects.create(id=5, text="How many kids do you have?", question_type=4)

    option1 = Option.objects.create(id=1, question=qn1, option_text="Male")
    option2 = Option.objects.create(id=2, question=qn1, option_text="Female")
    option3 = Option.objects.create(id=3, question=qn2, option_text="Yes")
    option4 = Option.objects.create(id=4, question=qn2, option_text="No")
    option5 = Option.objects.create(id=5, question=qn2, option_text="I am not sure")
    option6 = Option.objects.create(id=6, question=qn3, option_text="Yes")
    option7 = Option.objects.create(id=7, question=qn3, option_text="No")

    trigger = Trigger.objects.create(id=1, question=qn2, trigger_question=qn1, trigger_text="Female")

    group1 = Group.objects.create(id=1,
                                  name="Example Group 1",
                                  description="This is an example Group",
                                  postal_code="640547")

    activity1 = Activity.objects.create(id=1,
                                        group=group1,
                                        name="Males Only Activity")
    activity2 = Activity.objects.create(id=2,
                                        group=group1,
                                        name="Pregnant Only Activity")
    activity3 = Activity.objects.create(id=3,
                                        group=group1,
                                        name="Everyone's Activity")
    activity4 = Activity.objects.create(id=4,
                                        group=group1,
                                        name="EmployedYesNo Activity")
    activity5 = Activity.objects.create(id=5,
                                        group=group1,
                                        name="PoorerThan10 Activity")
    activity6 = Activity.objects.create(id=6,
                                        group=group1,
                                        name="PoorerThan10ORMoreThan5kids Activity")

    criterion1 = Criterion.objects.create(id=1,
                                          activity=Activity.objects.get(id=1),
                                          question=Question.objects.get(id=1),
                                          question_text="Male")
    criterion2 = Criterion.objects.create(id=2,
                                          activity=Activity.objects.get(id=2),
                                          question=Question.objects.get(id=2),
                                          question_text="Yes")
    criterion3 = Criterion.objects.create(id=3,
                                          activity=Activity.objects.get(id=4),
                                          question=Question.objects.get(id=3),
                                          question_text="Yes")
    criterion4 = Criterion.objects.create(id=4,
                                          activity=Activity.objects.get(id=4),
                                          question=Question.objects.get(id=3),
                                          question_text="No")
    criterion5 = Criterion.objects.create(id=5,
                                          activity=Activity.objects.get(id=5),
                                          question=Question.objects.get(id=4),
                                          question_text="10",
                                          range=-1)
    criterion6 = Criterion.objects.create(id=6,
                                          activity=Activity.objects.get(id=6),
                                          question=Question.objects.get(id=4),
                                          question_text="10",
                                          range=-2,
                                          radio_group_id=1)
    criterion7 = Criterion.objects.create(id=7,
                                          activity=Activity.objects.get(id=6),
                                          question=Question.objects.get(id=5),
                                          question_text="5",
                                          range=2,
                                          radio_group_id=1)