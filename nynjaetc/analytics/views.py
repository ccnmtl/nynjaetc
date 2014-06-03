from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.models import User
from nynjaetc.main.models import Section, UserProfile
from nynjaetc.main.models import SectionQuizAnsweredCorrectly
from django.http import HttpResponse
from django.conf import settings

import csv
import datetime


@login_required
@staff_member_required
def analytics_csv(request):
    """keep the code in here to a minimum"""
    return table_to_csv(request, generate_the_table())


@login_required
@staff_member_required
@render_to('analytics/analytics_table.html')
def analytics_table(request):
    """keep the code in here to a minimum"""
    return {
        'the_table': generate_the_table()
    }


@login_required
@staff_member_required
@render_to('analytics/analytics_table.html')
def analytics_table_testing(request):
    """keep the code in here to a minimum"""
    return {
        'the_table': generate_the_table(True)
    }


def table_to_csv(request, table):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=nynjaetc.csv'
    writer = csv.writer(response)
    for row in table:
        writer.writerow(row)
    return response


def generate_the_table(testing=False):

    the_tree = [s for s in Section.objects.all()][0].get_tree()
    all_sections = [s for s in the_tree if s.is_leaf_or_has_content()]
    all_questions = find_the_questions(all_sections)
    all_users = []
    if testing:
        all_users = User.objects.all().order_by('-last_login')
    else:
        all_users = User.objects.filter(is_staff=False).order_by('-last_login')

    the_table = []
    heading = generate_heading(all_sections, all_questions, testing)

    the_table.append(heading)

    for the_user in all_users:
        the_table.append(generate_row(the_user, all_sections,
                                      all_questions, testing))

    return the_table


def find_the_questions(sections_in_order):
    """ returns all the questions,
    in all the quizzes,
    in the order they are presented
    in the sections."""
    all_questions = []
    quizzes_we_want = settings.QUIZZES_TO_REPORT

    #first get all the questions in pagetree order:
    for the_section in sections_in_order:
        for the_pageblock in the_section.pageblock_set.all():
            if the_pageblock.block().__class__.display_name == 'Quiz':
                all_questions.extend(the_pageblock.block().question_set.all())

    #filter out most of the questions
    result = questions_we_want(all_questions, quizzes_we_want)
    return result


def questions_we_want(all_questions, quizzes_we_want):
    return [q for q in all_questions if q.quiz.id in quizzes_we_want]


def generate_heading(all_sections, all_questions, testing):
    result = [
        'hrsa id', 'encrypted email', 'joined', 'last login',
        'est. minutes spent', 'enduring materials checkbox',
    ]

    if testing:
        result.extend(['User ID', 'username', 'plaintext email', 'is staff'])

    for section in all_sections:
        result.append("%d: %s" % (section.id, section))

    result.extend(["%d: %s%s" % (question.id, question.text[0:64],
                                 (len(question.text) > 64 and '... ' or ''))
                   for question in all_questions])
    return result


def generate_row(the_user, all_sections, all_questions, testing):
    line = generate_row_info(the_user, all_sections, all_questions)

    the_profile = line['the_profile']

    result = []

    if the_profile:
        result.extend([
            the_profile.hrsa_id,
            the_profile.encrypted_email
        ])
    else:
        result.extend([
            None,
            None
        ])

    result.extend(
        [
            format_timestamp(line['the_user'].date_joined),
            format_timestamp(line['the_user'].last_login),
            line['est_time_spent'],
            line['read_intro'],
        ])

    if testing:
        result.extend([
            line['the_user'].id,
            line['the_user'].username,
            line['the_user'].email,
            line['the_user'].is_staff
        ])

    result.extend(line['user_sections'])
    result.extend(line['user_questions'])

    return result


def make_user_sections(all_sections, formatted_timestamps):
    return item_or_none_in_dict(all_sections, formatted_timestamps)


def make_user_questions(all_questions, responses):
    return item_or_none_in_dict(all_questions, responses)


def item_or_none_in_dict(all_items, the_dict):
    output = []
    for item in all_items:
        output.append(the_dict.get(item.id, None))
    return output


def generate_row_info(the_user, all_sections, all_questions):

    responses = responses_for(the_user)
    raw_timestamps, formatted_timestamps = timestamps_for(the_user)

    user_sections = make_user_sections(
        all_sections, formatted_timestamps)
    user_questions = make_user_questions(
        all_questions, responses)

    the_profile = None
    try:
        the_profile = the_user.get_profile()
    except UserProfile.DoesNotExist:
        pass

    return {
        'the_user': the_user,
        'est_time_spent': time_spent_estimate(raw_timestamps.values()),
        'the_profile': the_profile,
        'user_questions': user_questions,
        'user_sections': user_sections,
        'read_intro': checked_enduring_materials_box(the_user)
    }


def sum_of_gaps_longer_than_x_minutes(x, list_of_timestamps):
    """ as described in bug http://pmt.ccnmtl.columbia.edu/item/87836/
    basically if there are gaps that are longer than x,
    we assume the user was not doing the activity.
    so in that case we don't count that toward the total
    duration of the activity for them.
    Returns a value in seconds.
    """
    threshold = datetime.timedelta(minutes=x)
    if len(list_of_timestamps) < 2:
        return 0
    list_of_timestamps.sort()
    start_times = list_of_timestamps[:-1]
    end_times = list_of_timestamps[1:]
    gaps_longer_than_x_in_seconds = [
        (b - a).total_seconds()
        for a, b in zip(start_times, end_times)
        if (b - a > threshold)]
    return sum(gaps_longer_than_x_in_seconds)


def time_spent_estimate(list_of_timestamps):
    """Based on a list of timestamps, make an estimate,
    in minutes, of actual time spent paying attention
    to the activity."""
    if len(list_of_timestamps) == 0:
        return 0
    raw_estimate = (
        max(list_of_timestamps) - min(list_of_timestamps)).total_seconds()
    better_estimate = raw_estimate - sum_of_gaps_longer_than_x_minutes(
        70,
        list_of_timestamps)
    return "%0.1f" % (better_estimate / 60,)


# hard-coding the section pk is still a terrible idea
# but at least now it's injectable for testing
def checked_enduring_materials_box(the_user):
    section_pk = settings.ENDURING_MATERIALS_SECTION_ID
    enduring_materials_section = Section.objects.get(pk=section_pk)
    return SectionQuizAnsweredCorrectly.objects.filter(
        user=the_user, section=enduring_materials_section).exists()


def format_timestamp(ts):
    """Easy for humans and Microsoft Excel to understand."""
    return ts.strftime("%m/%d/%Y %I:%M:%S %p")


def timestamps_for(the_user):
    the_timestamps = the_user.sectiontimestamp_set.all()
    formatted_timestamps = dict(
        [(t.section.id, format_timestamp(t.timestamp))
         for t in the_timestamps])
    raw_timestamps = dict(
        [(t.section.id, t.timestamp) for t in the_timestamps])
    return (raw_timestamps, formatted_timestamps)


def responses_for(the_user):
    """The user's responses to quiz questions.
    If there is more than one response
    to a question, returns the most recent."""
    result = {}

    for sub in the_user.submission_set.order_by('submitted'):
        for resp in sub.response_set.all():
            result[resp.question.id] = resp.value
    return result
