from nynjaetc.main.models import SectionTimestamp
from datetime import datetime
from django.utils.timezone import utc
from nynjaetc.main.models import SectionPreference


def whether_already_visited(section, user):
    return SectionTimestamp.objects.filter(user=user, section=section).exists()


def already_visited_pages(section, user):
    """The already_visited_pages in a section
    or its descendants, in DFS order."""
    if user.is_anonymous():
        return section

    user_timestamp_sections = [
        st.section for st in SectionTimestamp.objects.filter(user=user)]
    return [t for t in self_and_descendants(section)
            if t in user_timestamp_sections]


def is_in_one_of(section, set_of_parents):
    """Whether a section is either one of,
    or the descendant of one of,
    a set of possible parent sections."""
    result = False
    if section in set_of_parents:
        result = True
    for q in set_of_parents:
        if is_descendant_of(section, q):
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
    return [section] + list(section.get_descendants())


def set_timestamp_for_section(section, user):
    assert user is not None
    assert section is not None
    section_timestamp, created = SectionTimestamp.objects.get_or_create(
        section=section,
        user=user,
        defaults={'timestamp': datetime.utcnow().replace(tzinfo=utc)})
    assert section_timestamp is not None
    section_timestamp.set_to_now()


def module_info(section):
    """ In the top nav (and nowhere else),
    some modules need to have a special URL
    depending on preferences in the database."""
    result = []
    modules = section.hierarchy.get_root().get_children()
    prefs = SectionPreference.objects.filter(
        section__in=modules, preference__slug='top_nav_link_to_latest')
    special_modules = [p.section for p in prefs]
    for x in modules:
        info = {'id': x.id, 'label': x.label}
        if x in special_modules:
            prefix = '/latest'
        else:
            prefix = ''
        info['url'] = '%s%s' % (prefix,  x.get_absolute_url())
        result.append(info)
    return result
