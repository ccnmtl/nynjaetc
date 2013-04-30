from nynjaetc.main.models import SectionTimestamp
from datetime import datetime
from django.utils.timezone import utc
from nynjaetc.main.models import Preference, SectionPreference
from pagetree.helpers import get_section_from_path




def whether_already_visited (section, user):    
    return SectionTimestamp.objects.filter(user=user, section = section).exists()



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
        
def is_in_one_of (section, set_of_parents):
    """Whether a section is identical to, or the descendant of, one of a set of possible parent sections."""
    result = False
    if section in set_of_parents:
        result = True
    for q in set_of_parents:
        if is_descendant_of (section, q):
            result = True
    return result
    
    
def is_descendant_of(child, parent):
    if parent == child:
        return False
    if child in self_and_descendants(parent):
        return True
    return False

def self_and_descendants(section):
    """Self and descendants, in depth-first order."""
    result = []
    traverse_tree(section, result)
    return result
        
def traverse_tree (node, the_list):
    the_list.append(node)
    for k in node.get_children():
        traverse_tree(k, the_list)
        
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


