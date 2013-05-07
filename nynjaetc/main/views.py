from annoying.decorators import render_to
from django.http import HttpResponseRedirect, HttpResponse
from pagetree.models import Section
from pagetree.helpers import get_section_from_path
from pagetree.helpers import get_module, needs_submit, submitted
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from nynjaetc.main.models import Preference, SectionPreference
from nynjaetc.main.views_helpers import whether_already_visited, already_visited_pages_except_most_forward_one, already_visited_pages, self_and_descendants, is_descendant_of,  set_timestamp_for_section, module_info, is_in_one_of
from nynjaetc.main.models import SectionTimestamp, SectionQuizAnsweredCorrectly


@login_required
@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    tmp = SectionPreference.objects.filter(section=section)
    section_preferences = dict((sp.preference.slug, True) for sp in tmp)
    
    #figure out which questions the user has already answered:
    try:
        quiz_sequences = Preference.objects.get(slug='quiz_sequence').sections()
    except Preference.DoesNotExist:
        quiz_sequences = []
    in_quiz_sequence = is_in_one_of (section, quiz_sequences)
    already_visited = whether_already_visited (section, request.user)
    
    next_already_visited = whether_already_visited(section.get_next(), request.user)

    #import pdb
    #pdb.set_trace()
    already_answered = SectionQuizAnsweredCorrectly.objects.filter(section=section, user = request.user).exists()

    #factoring this out:
    #already_answered = False
    #for q in quiz_sequences:
    #    if section in already_visited_pages_except_most_forward_one(q, request.user):
    #        already_answered = True
            
    # for future reference, log the fact that we have displayed this page.
    
    set_timestamp_for_section (section, request.user)
    
    
    if section.id == root.id:
        # trying to visit the root page
        if section.get_next():
            # just send them to the first child
            return HttpResponseRedirect(section.get_next().get_absolute_url())

    if request.method == "POST":
        # user has submitted a form. deal with it
        if request.POST.get('action', '') == 'reset':
            #section.reset(request.user)
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
            section_preferences = section_preferences,
            module_info = module_info(section),            
            already_answered = already_answered,
            in_quiz_sequence = in_quiz_sequence,
            already_visited = already_visited
            
        )


@login_required
def latest_page(request, path):
    """Returns the most recently viewed section BY TIMESTAMP in {the page itself or its descendants}."""
    """Used only for nav purposes."""
    section = get_section_from_path(path)
    pool = self_and_descendants(section)
    if  request.user.is_anonymous():
        return page (request, section.get_path())
    user_timestamps = SectionTimestamp.objects.filter(user=request.user)    
    already_visited = [t for t in user_timestamps if t.section in pool]
    if len(already_visited) == 0:
        return page (request, section.get_path())
    most_recently_visited = sorted(already_visited, key=lambda x: x.timestamp)[-1]
    latest_section_visited =  most_recently_visited.section
    
    return page (request, latest_section_visited.get_path())


@login_required
def record_section_as_answered_correctly(request):
    if request.method == "POST" and request.is_ajax and request.POST.has_key ('section_id'):
        section_id = int (request.POST['section_id'])
        section = Section.objects.get(pk=section_id)
        receipt = SectionQuizAnsweredCorrectly.objects.create(section = section, user = request.user)
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
                
