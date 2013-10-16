from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
from pagetree.models import Section
from pagetree.helpers import get_section_from_path
from pagetree.helpers import get_module, needs_submit, submitted
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from nynjaetc.main.models import SectionPreference, UserProfile
from nynjaetc.main.views_helpers import whether_already_visited
from nynjaetc.main.views_helpers import self_and_descendants
from nynjaetc.main.views_helpers import set_timestamp_for_section
from  nynjaetc.main.views_helpers import is_in_one_of
from nynjaetc.main.views_helpers import module_info
from nynjaetc.main.models import SectionTimestamp, SectionQuizAnsweredCorrectly
from django.template import RequestContext, loader
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from nynjaetc.main.models import Preference
from quizblock.models import Submission



def background(request,  content_to_show):
    """ the pagetree page view breaks flatpages,
    so this is a simple workaround."""
    file_names = {
        'about': 'about.html',
        'credits': 'credits.html',
        'contact': 'contact.html',
        'help': 'help.html',
    }

    if content_to_show not in file_names.keys():
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)
    file_name = file_names[content_to_show]
    t = loader.get_template('main/standard_elements/%s' % file_name)
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def has_submitted_pretest(the_user):
    the_pretest_section = Section.objects.get (sectionpreference__preference__slug = 'pre-test')
    for s in Submission.objects.filter(user = the_user):
        if s.quiz.pageblock().section == the_pretest_section:
            return True
    return false

@login_required
@render_to('main/page.html')
def page(request, path):
    #bypass the inital material if the user has already submitted the pretest:
    the_pretest_section = Section.objects.get (sectionpreference__preference__slug = 'pre-test')
    if the_pretest_section:
        if path == '' and has_submitted_pretest(request.user):
            return HttpResponseRedirect(the_pretest_section.get_next().get_absolute_url())

    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    tmp = SectionPreference.objects.filter(section=section)
    section_preferences = dict((sp.preference.slug, True) for sp in tmp)
    already_visited = whether_already_visited(section, request.user)
    already_answered = SectionQuizAnsweredCorrectly.objects.filter(
        section=section, user=request.user).exists()
    set_timestamp_for_section(section, request.user)

    
    supress_nav_sections = Section.objects.filter (
        sectionpreference__preference__slug =
        'suppress_nav_until_pre_test_submitted'
    )

    whether_to_show_nav = True
    if is_in_one_of (section, supress_nav_sections):
        whether_to_show_nav = False
        if has_submitted_pretest(request.user):
            whether_to_show_nav = True


    # We're leaving the top level pages as blank and navigating around them.
    send_to_first_child = False
    is_root = (section.id == root.id)
    is_child_of_root = (
        section.get_parent() and section.get_parent().id == root.id)
    if len(section.get_children()) > 0 and section.get_next():
        # don't send to first child if there is no first child.
        if is_root or is_child_of_root:
            send_to_first_child = True
    if send_to_first_child:
        return HttpResponseRedirect(section.get_next().get_absolute_url())

    if request.method == "POST":
        # user has submitted a form. deal with it
        if request.POST.get('action', '') == 'reset':
            # section.reset(request.user)
            return HttpResponseRedirect(section.get_absolute_url())
        proceed = section.submit(request.POST, request.user)
        if proceed and section.get_next():
            return HttpResponseRedirect(section.get_next().get_absolute_url())
        else:
            # giving them feedback before they proceed
            return HttpResponseRedirect(section.get_absolute_url())

    else:
        path = list(section.get_ancestors())[1:]
        path.append(section)
        return dict(
            section=section,
            path=path,
            depth=len(path),
            can_download_stats=(
                'can_dowload_stats'
                in [g.name for g in request.user.groups.all()]
            ),
            module=module,
            needs_submit=needs_submit(section),
            is_submitted=submitted(section, request.user),
            modules=root.get_children(),
            root=section.hierarchy.get_root(),
            section_preferences=section_preferences,
            module_info=module_info(section),
            already_answered=already_answered,
            # in_quiz_sequence = in_quiz_sequence,
            already_visited=already_visited,
            whether_to_show_nav=whether_to_show_nav
        )


@login_required
def latest_page(request, path):
    """Returns the most recently viewed section
    BY TIMESTAMP in {the page itself or its descendants}.
    Used only for nav purposes."""

    section = get_section_from_path(path)
    pool = self_and_descendants(section)
    if request.user.is_anonymous():
        return page(request, section.get_path())
    user_timestamps = SectionTimestamp.objects.filter(user=request.user)
    already_visited = [t for t in user_timestamps if t.section in pool]
    if len(already_visited) == 0:
        return page(request, section.get_path())
    most_recently_visited = sorted(
        already_visited, key=lambda x: x.timestamp)[-1]
    latest_section_visited = most_recently_visited.section

    return page(request, latest_section_visited.get_path())


@login_required
def record_section_as_answered_correctly(request):
    if (request.method == "POST" and
            request.is_ajax and
            'section_id' in request.POST):
        section_id = int(request.POST['section_id'])
        section = Section.objects.get(pk=section_id)
        SectionQuizAnsweredCorrectly.objects.create(
            section=section, user=request.user)
        return HttpResponse('ok')
    return HttpResponse('')


@staff_member_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()

    return dict(section=section,
                module=get_module(section),
                modules=root.get_children(),
                root=section.hierarchy.get_root())


@csrf_protect
def resend_activation_email(request):
    """allows you to  resent the activation email to an arbitrary address."""
    if (request.method == "GET"):
        t = loader.get_template(
            'registration/resend_activation_email_form.html')
        c = RequestContext(request, {})
        return HttpResponse(t.render(c))

    if (request.method == "POST"):
        email = request.POST.get('email', '')
        form_template = loader.get_template(
            'registration/resend_activation_email_form.html')
        confirm_template = loader.get_template(
            'registration/resend_activation_email_confirm.html')

        if email == '':
            c = RequestContext(request,
                               {'error': 'no_email_entered', 'email': email})
            return HttpResponse(form_template.render(c))
        try:
            user_profile = UserProfile.find_user_profiles_by_plaintext_email(
                email)
            reg_profile = user_profile[0].user.registrationprofile_set.get()
        except:
            c = RequestContext(request,
                               {'error': 'no_email_found', 'email': email})
            return HttpResponse(form_template.render(c))

        if reg_profile.activation_key == 'ALREADY_ACTIVATED':
            c = RequestContext(request,
                               {'message': 'already_active', 'email': email})
            return HttpResponse(confirm_template.render(c))

        if reg_profile.activation_key_expired():
            c = RequestContext(request, {'error': 'expired', 'email': email})
            return HttpResponse(form_template.render(c))

        #ok success.
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        reg_profile.send_activation_email(site)
        c = RequestContext(request,
                           {'message': 'success_message', 'email': email})
        return HttpResponse(confirm_template.render(c))
