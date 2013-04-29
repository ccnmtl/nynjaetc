from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from pagetree.helpers import get_section_from_path
from pagetree.helpers import get_module, needs_submit, submitted
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from nynjaetc.main.models import SectionTimestamp, Preference, SectionPreference
from datetime import datetime
from django.utils.timezone import utc

def set_timestamp_for_section (section, user):
    assert user != None
    assert section != None
    section_timestamp, created = SectionTimestamp.objects.get_or_create(section=section, user=user, defaults={'timestamp': datetime.utcnow().replace(tzinfo=utc)})
    assert section_timestamp != None
    section_timestamp.set_to_now()

def module_info (section):
    """ In the top nav (and nowhere else),
    some modules need to have a special URL
    depending on preferences in the database."""
    result = []
    modules = section.hierarchy.get_root().get_children()
    prefs = SectionPreference.objects.filter(section__in=modules, preference__slug='top_nav_link_to_latest')
    special_modules = [p.section for p in prefs]
    for x in modules:
        info = { 'id': x.id ,'label': x.label }
        if x in special_modules:
            prefix = '/latest'
        else:
            prefix = ''
        info ['url'] = '%s%s' % (prefix,  x.get_absolute_url())
        result.append (info)
    return result 


@login_required
@render_to('main/page.html')
def page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()
    module = get_module(section)
    tmp = SectionPreference.objects.filter(section=section)
    section_preferences = dict((sp.preference.slug, True) for sp in tmp)
    
    
    #figure out which questions the user has already answered:    
    quiz_sequences = Preference.objects.get(slug='quiz_sequence').sections()
    
    in_quiz_sequence = False
    for q in quiz_sequences:
        if section in self_and_descendants(q):
            in_quiz_sequence = True
    
    
    already_visited = whether_already_visited (section, request.user)
    
    
    already_answered = False
    for q in quiz_sequences:
        if section in already_visited_pages_except_most_forward_one(q, request.user):
            already_answered = True
            
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

def whether_already_visited (section, user):


    #print 'goat'
    #import pdb
    #pdb.set_trace()
    
    
    return SectionTimestamp.objects.filter(user=user, section = section).exists()


@staff_member_required
@render_to('main/edit_page.html')
def edit_page(request, path):
    section = get_section_from_path(path)
    root = section.hierarchy.get_root()

    return dict(section=section,
                module=get_module(section),
                modules=root.get_children(),
                root=section.hierarchy.get_root())

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



def already_visited_pages_except_most_forward_one (section, user):
    """Removes the most-forward page from already_visited_pages.
    If we didn't remove this last page, it would be possible to find out the answer of the last page just by reloading it."""
    result = already_visited_pages (section, user)
    if len(result) == 0:
        return result
        
    #print ("Visited descendents, EXCEPT FOR ONE, of  ", section)
    #print (result [0:-1])
    return result [0:-1]
    

def already_visited_pages (section, user):
    """The already_visited_pages in a section or its descendants, in DFS order."""
    if  user.is_anonymous():
        return section
        
    user_timestamp_sections = [st.section for st in SectionTimestamp.objects.filter(user=user)]
    return [t for t in self_and_descendants(section) if t in user_timestamp_sections]
        

def self_and_descendants(section):
    """Self and descendants, in depth-first order."""
    result = []
    traverse_tree(section, result)
    return result
        
def traverse_tree (node, the_list):
    the_list.append(node)
    for k in node.get_children():
        traverse_tree(k, the_list)

                


@render_to('main/instructor_page.html')
def instructor_page(request, path):
    return dict()
