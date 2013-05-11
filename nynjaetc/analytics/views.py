from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.contrib.auth.models import User


@login_required
@staff_member_required
@render_to('analytics/analytics_table.html')
def analytics_table(request):
    the_table = generate_the_table()
    return {'the_table': the_table}


def generate_the_table():
    return [generate_row(u) for u in User.objects.all()]

questions_we_care_about = {

}


def pages_visited_by(the_user):
    #prinxt dir (the_user)
    #prinxt the_user.sectiontimestamp_set.all()
    result = the_user.sectiontimestamp_set.all()
    if len(result) == 0:
        return None
    return result
    #return None


def quizzes_for(the_user):
    result = {}
    #passs
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

    if len(result.keys()) == 0:
        return None
    return result


def generate_row(the_user):

    quizzes = quizzes_for(the_user)
    pages = pages_visited_by(the_user)

    return {
        'the_user': the_user,
        'quizzes': quizzes,
        'pages': pages,
    }


def user_selected_i_agree(user):
    #import pdxb
    #pdbb.set_trace()

    """"user selected I agree on this page:
    https://nynjaetc.stage.ccnmtl.columbia.edu/enduring-materials/
    answers to questions on this page:
    https://nynjaetc.stage.ccnmtl.columbia.edu/intro/pre-test/
    answers to question on this page:
    https://nynjaetc.stage.ccnmtl.columbia.edu/post-test/
    list of pages the user skipped"""""
