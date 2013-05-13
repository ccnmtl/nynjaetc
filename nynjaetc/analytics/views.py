from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.models import User
from nynjaetc.main.models import Section, UserProfile
from quizblock.models import Question
from django.http import HttpResponse
import csv

@login_required
@staff_member_required
def analytics_csv(request):
    return table_to_csv (request, generate_the_table())

@login_required
@staff_member_required
@render_to('analytics/analytics_table.html')
def analytics_table(request):
    """keep the code in here to a minimum"""
    return {
        'the_table': generate_the_table()
    }
    
def table_to_csv(request, table):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=nynjaetc.csv'
    writer = csv.writer(response)
    for row in  table:
        writer.writerow(row)
    return response

def generate_the_table():
    testing = False
    all_sections = Section.objects.get(pk=1).get_tree()
    all_questions = find_the_questions(all_sections)
    all_users = []    
    if testing:
        all_users = [User.objects.get (id=5)]
    else:
        all_users = User.objects.all()
    
    the_table = []
    the_table.append (generate_heading(all_sections, all_questions))
    for the_user in all_users:
        the_table.append (generate_row(the_user, all_sections, all_questions))
    return the_table


def find_the_questions(sections_in_order):
    """ returns all the questions,
    in all the quizzes,
    in the order they are presented
    in the sections."""
    result = []
    for the_section in sections_in_order:
        for the_pageblock in the_section.pageblock_set.all():
            if the_pageblock.block().__class__.display_name == 'Quiz':
                result.extend (the_pageblock.block().question_set.all())
    return result

def self_and_descendants(section):
    """Self and descendants, in depth-first order."""
    result = []
    traverse_tree(section, result)
    return result


def traverse_tree(node, the_list):
    the_list.append(node)
    for k in node.get_children():
        traverse_tree(k, the_list)

def generate_heading(all_sections, all_questions):
    result = [
        'User ID'
        , 'username'
        , 'plaintext email'
        , 'joined'
        , 'last login'
        , 'is staff'
        , 'encrypted email'
        , 'hrsa id'
    ]
    result.extend (["%d: %s" % (section.id, section) for section in all_sections])
    result.extend (["%d: %s" % (question.id, question) for question in all_questions])
    return result

def generate_row(the_user, all_sections, all_questions):
    line =  generate_row_info(the_user, all_sections, all_questions)
    result = [
        line ['the_user'].id
        ,line['the_user'].username
        ,line['the_user'].email
        ,line['the_user'].date_joined
        ,line['the_user'].last_login
        ,line['the_user'].is_staff
    ]
    the_profile = line['the_profile']
    if the_profile:
        result.extend ([
            the_profile.encrypted_email,
            the_profile.hrsa_id
        ])
    else:
        result.extend ([
            None,
            None
        ])
    result.extend (line['user_sections' ])
    result.extend (line['user_questions'])
    return result

    
def generate_row_info(the_user, all_sections, all_questions):

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
        
    the_profile = None    
    try:
        the_profile = the_user.get_profile()
    except UserProfile.DoesNotExist:
        pass
            
    return {
        'the_user': the_user,
        'the_profile': the_profile,
        'user_questions': user_questions,
        'user_sections': user_sections,
    }


def timestamps_for(the_user):
    the_timestamps = the_user.sectiontimestamp_set.all()
    result =  dict([(t.section.id, t.timestamp ) for t in the_timestamps])
    return result


def responses_for(the_user):
    """The user's responses to quiz questions.
    If there is more than one response
    to a question, returns the most recent."""
    result = {}
    
    for sub in the_user.submission_set.order_by('submitted'):
        for resp in sub.response_set.all():
            result[resp.question.id] = resp.value
    return result

