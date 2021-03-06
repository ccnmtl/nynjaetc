from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.conf import settings
from pagetree.models import Section
from pagetree.helpers import get_section_from_path, get_hierarchy
from pagetree.helpers import get_module, needs_submit, submitted
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from pagetree.generic.views import EditView as GenericEditView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from nynjaetc.main.models import SectionPreference, UserProfile
from nynjaetc.main.views_helpers import whether_already_visited
from nynjaetc.main.views_helpers import self_and_descendants
from nynjaetc.main.views_helpers import set_timestamp_for_section
from nynjaetc.main.views_helpers import is_in_one_of
from nynjaetc.main.views_helpers import module_info
from nynjaetc.main.models import SectionTimestamp, SectionQuizAnsweredCorrectly
from nynjaetc.main.models import SectionAlternateNavigation
from django.template import RequestContext, loader
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
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


def has_submitted_pretest(the_user, hierarchy="main"):
    h = get_hierarchy(hierarchy)
    the_pretest_section = Section.objects.get(
        sectionpreference__preference__slug=settings.PRETEST_PREF_SLUG,
        hierarchy=h)
    for s in Submission.objects.filter(user=the_user):
        if s.quiz.pageblock().section == the_pretest_section:
            return True
    return False


class Pretest(object):
    def __init__(self, section):
        self.section = section

    def user_has_submitted(self, path, user):
        return path == '' and has_submitted_pretest(
            user, hierarchy=self.section.hierarchy.name)


class NullPretest(object):
    def user_has_submitted(self, path, user):
        return False


def get_pretest(hierarchy="main"):
    h = get_hierarchy(hierarchy)
    try:
        return Pretest(
            Section.objects.get(
                hierarchy=h,
                sectionpreference__preference__slug='pre-test'))
    except Section.DoesNotExist:
        return NullPretest()


def whether_to_show_nav(section, user):
    suppress_nav_sections = Section.objects.filter(
        sectionpreference__preference__slug=(
            'suppress_nav_until_pre_test_submitted'))
    if is_in_one_of(section, suppress_nav_sections):
        return has_submitted_pretest(user, hierarchy=section.hierarchy.name)
    return True


def send_to_first_child(section, root):
    is_root = (section.id == root.id)
    is_child_of_root = (
        section.get_parent() and section.get_parent().id == root.id)
    if len(section.get_children()) > 0 and section.get_next():
        # don't send to first child if there is no first child.
        if is_root or is_child_of_root:
            return True
    return False


def get_section_preferences(section):
    return dict(
        (sp.preference.slug, True)
        for sp in SectionPreference.objects.filter(section=section))


def get_can_download_stats(user):
    return (
        'can_download_stats'
        in [g.name for g in user.groups.all()])


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class PageView(LoggedInMixin, View):
    template_name = "main/page.html"
    hierarchy = "main"

    def precheck(self, request, path):
        # bypass the inital material if the user has already submitted
        # the pretest:
        pretest = get_pretest(hierarchy=self.hierarchy)
        if pretest.user_has_submitted(path, request.user):
            return HttpResponseRedirect(
                pretest.section.get_next().get_absolute_url())

        section = get_section_from_path(path, hierarchy=self.hierarchy)
        set_timestamp_for_section(section, request.user)

        # We're leaving the top level pages as blank and navigating
        # around them.
        if send_to_first_child(section, section.hierarchy.get_root()):
            return HttpResponseRedirect(section.get_next().get_absolute_url())
        self.section = section
        return None

    def post(self, request, path):
        r = self.precheck(self.request, path)
        if r is not None:
            return r
        # user has submitted a form. deal with it
        if request.POST.get('action', '') == 'reset':
            return HttpResponseRedirect(self.section.get_absolute_url())
        proceed = self.section.submit(request.POST, request.user)
        if proceed and self.section.get_next():
            return HttpResponseRedirect(
                self.section.get_next().get_absolute_url())
        # giving them feedback before they proceed
        return HttpResponseRedirect(self.section.get_absolute_url())

    def get(self, request, path):
        r = self.precheck(self.request, path)
        if r is not None:
            return r
        return render(request, self.template_name, self.get_context(request))

    def get_context(self, request):
        path_list = list(self.section.get_ancestors())[1:]
        path_list.append(self.section)
        return dict(
            section=self.section,
            path=path_list,
            depth=len(path_list),
            can_download_stats=get_can_download_stats(request.user),
            module=get_module(self.section),
            needs_submit=needs_submit(self.section),
            is_submitted=submitted(self.section, request.user),
            modules=self.section.hierarchy.get_root().get_children(),
            root=self.section.hierarchy.get_root(),
            section_preferences=get_section_preferences(self.section),
            module_info=module_info(self.section),
            already_answered=SectionQuizAnsweredCorrectly.objects.filter(
                section=self.section, user=request.user).exists(),
            already_visited=whether_already_visited(
                self.section, request.user),
            whether_to_show_nav=whether_to_show_nav(
                self.section, request.user)
        )


class LatestPageView(LoggedInMixin, View):
    """Returns the most recently viewed section
    BY TIMESTAMP in {the page itself or its descendants}.
    Used only for nav purposes."""
    hierarchy_name = "main"
    hierarchy_base = "/"

    def get(self, request, path):
        section = get_section_from_path(
            path,
            hierarchy_name=self.hierarchy_name,
            hierarchy_base=self.hierarchy_base)
        pool = self_and_descendants(section)
        user_timestamps = SectionTimestamp.objects.filter(user=request.user)
        already_visited = [t for t in user_timestamps if t.section in pool]
        if len(already_visited) == 0:
            return HttpResponseRedirect("/" + section.get_path())
        most_recently_visited = sorted(
            already_visited, key=lambda x: x.timestamp)[-1]
        latest_section_visited = most_recently_visited.section

        return HttpResponseRedirect("/" + latest_section_visited.get_path())


class RecordSectionAsAnsweredCorrectlyView(LoggedInMixin, View):
    def post(self, request):
        if (request.is_ajax and 'section_id' in request.POST):
            section_id = int(request.POST['section_id'])
            section = Section.objects.get(pk=section_id)
            SectionQuizAnsweredCorrectly.objects.create(
                section=section, user=request.user)
            return HttpResponse('ok')
        return HttpResponse('')

    def get(self, request):
        return HttpResponse('')


class StaffViewMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffViewMixin, self).dispatch(*args, **kwargs)


class AltNavListView(StaffViewMixin, ListView):
    model = SectionAlternateNavigation


class CreateAltNavView(StaffViewMixin, CreateView):
    model = SectionAlternateNavigation
    success_url = "/manage/altnav/"

    def get_context_data(self, *args, **kwargs):
        data = super(CreateView, self).get_context_data(*args, **kwargs)
        data['all_sections'] = Section.objects.all()
        return data


class DeleteAltNavView(StaffViewMixin, DeleteView):
    model = SectionAlternateNavigation
    success_url = "/manage/altnav/"


class SecPrefListView(StaffViewMixin, ListView):
    model = SectionPreference


class DeleteSecPrefView(StaffViewMixin, DeleteView):
    model = SectionPreference
    success_url = "/manage/secpref/"


class CreateSecPrefView(StaffViewMixin, CreateView):
    model = SectionPreference
    success_url = "/manage/secpref/"

    def get_context_data(self, *args, **kwargs):
        data = super(CreateView, self).get_context_data(*args, **kwargs)
        data['all_sections'] = Section.objects.all()
        return data


class EditView(StaffViewMixin, GenericEditView):
    template_name = "main/edit_page.html"


def get_site(request):
    if Site._meta.installed:
        return Site.objects.get_current()
    else:
        return RequestSite(request)


class ResendActivationEmailView(View):
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(
            ResendActivationEmailView, self).dispatch(*args, **kwargs)

    def get(self, request):
        t = loader.get_template(
            'registration/resend_activation_email_form.html')
        c = RequestContext(request, {})
        return HttpResponse(t.render(c))

    def get_profile(self, email, request):
        if email == '':
            return (None, RequestContext(
                request, {'error': 'no_email_entered', 'email': email}))
        try:
            user_profile = UserProfile.find_user_profiles_by_plaintext_email(
                email)
            return (user_profile[0].user.registrationprofile_set.get(), None)
        except:
            return (None, RequestContext(
                request,
                {'error': 'no_email_found', 'email': email}))

    def post(self, request):
        email = request.POST.get('email', '')
        form_template = loader.get_template(
            'registration/resend_activation_email_form.html')
        confirm_template = loader.get_template(
            'registration/resend_activation_email_confirm.html')

        reg_profile, c = self.get_profile(email, request)
        if c is not None:
            return HttpResponse(form_template.render(c))

        if reg_profile.activation_key == 'ALREADY_ACTIVATED':
            c = RequestContext(request,
                               {'message': 'already_active', 'email': email})
            return HttpResponse(confirm_template.render(c))

        if reg_profile.activation_key_expired():
            c = RequestContext(request, {'error': 'expired', 'email': email})
            return HttpResponse(form_template.render(c))

        # ok success.
        site = get_site(request)

        reg_profile.send_activation_email(site)
        c = RequestContext(request,
                           {'message': 'success_message', 'email': email})
        return HttpResponse(confirm_template.render(c))
