from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.models import User
from nynjaetc.main.models import Section
from quizblock.models import Question

@login_required
@staff_member_required
@render_to('analytics/analytics_table.html')
def analytics_table(request):
    """keep the code in here to a minimum"""
    return generate_the_table()


def generate_the_table():

    all_sections = Section.objects.all()
    all_questions = Question.objects.all()
    the_table = []
    for the_user in User.objects.all():
        the_table.append (generate_row(the_user, all_sections, all_questions))
        
    return {
        'the_table': the_table,
        'all_sections': all_sections,
        'all_questions': all_questions
    }





def generate_row(the_user, all_sections, all_questions):

    responses = responses_for(the_user)
    timestamps = timestamps_for(the_user)

    user_sections = []
    user_questions = []
    section_ids  = timestamps.keys()
    question_ids = responses.keys()

    for the_section in all_sections:
        if the_section.id in section_ids:
            user_sections.append (timestamps[the_section.id])
        else:
            user_sections.append (None)
            
    for the_question in all_questions:
        if the_question.id in question_ids:
            user_questions.append (responses[the_question.id])
        else:
            user_questions.append (None)
    return {
        'the_user': the_user,
        'user_questions': user_questions,
        'user_sections': user_sections,
    }

    
    
def timestamps_for(the_user):
    the_timestamps = the_user.sectiontimestamp_set.all()
    result =  dict([(t.section.id, t.timestamp ) for t in the_timestamps])
    return result


def responses_for(the_user):
    result = {}
    #prinxt dir (the_user)
    #prinxt the_user.submission_set.all()
    for sub in the_user.submission_set.all():
        #prinxt sub.quiz
        #prinxt dir(sub)
        #prinxt sub.response_set.all()
        for resp in sub.response_set.all():
            #prinxt resp
            #prinxt dir (resp)
            result[resp.question.id] = resp.value
            #prinxt resp.question
            #prinxt resp.question.id
            #prinxt resp.value

    return result

