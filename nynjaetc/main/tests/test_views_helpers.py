from datetime import datetime
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.utils.timezone import utc
from nynjaetc.main.models import Preference
from nynjaetc.main.models import SectionPreference
from nynjaetc.main.models import SectionTimestamp
from nynjaetc.main.views_helpers import whether_already_visited
from nynjaetc.main.views_helpers import already_visited_pages
from nynjaetc.main.views_helpers import self_and_descendants
from nynjaetc.main.views_helpers import is_descendant_of
from nynjaetc.main.views_helpers import is_in_one_of
from nynjaetc.main.views_helpers import module_info
from pagetree.models import Hierarchy


class WAVTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="test1")
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.u.delete()
        self.root.delete()
        self.h.delete()

    def test_whether_already_visited_none(self):
        SectionTimestamp.objects.all().delete()
        self.assertFalse(whether_already_visited(self.section1, self.u))

    def test_whether_already_visited_some(self):
        SectionTimestamp.objects.create(
            section=self.section1,
            user=self.u,
            timestamp=datetime.utcnow().replace(tzinfo=utc), )
        self.assertTrue(whether_already_visited(self.section1, self.u))


class AVPTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="test1")
        self.anon_u = AnonymousUser()
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.u.delete()
        self.root.delete()
        self.h.delete()

    def test_already_visited_pages_none(self):
        self.assertEquals(
            already_visited_pages(self.section1, self.u),
            [])

    def test_already_visited_pages_anon(self):
        """ calling with anon user returns the section """
        self.assertEquals(
            already_visited_pages(self.section1, self.anon_u),
            self.section1)


class IIOOTest(TestCase):
    def setUp(self):
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.root.delete()
        self.h.delete()

    def test_is_in_one_of_empty(self):
        self.assertFalse(is_in_one_of(self.root, []))

    def test_is_in_one_of_self(self):
        self.assertTrue(is_in_one_of(self.root, [self.root]))

    def test_is_in_one_of(self):
        self.assertTrue(is_in_one_of(self.section1, [self.root]))


class IDOTest(TestCase):
    def setUp(self):
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.root.delete()
        self.h.delete()

    def test_is_descendant_of_same(self):
        self.assertFalse(is_descendant_of(self.root, self.root))

    def test_is_descendant_of_parent_child(self):
        self.assertFalse(is_descendant_of(self.root, self.section1))

    def test_is_descendant_of_child_parent(self):
        self.assertTrue(is_descendant_of(self.section1, self.root))


class SADTest(TestCase):
    def setUp(self):
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.root.delete()
        self.h.delete()

    def test_self_and_descendants(self):
        result = self_and_descendants(self.root)
        self.assertEquals(result, [self.root, self.section1])


class ModuleInfoTest(TestCase):
    def setUp(self):
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.root.delete()
        self.h.delete()

    def test_module_info(self):
        result = module_info(self.section1)
        self.assertTrue('id' in result[0])
        self.assertTrue('label' in result[0])
        self.assertTrue('url' in result[0])

    def test_module_info_special(self):
        p = Preference.objects.create(slug='top_nav_link_to_latest')
        SectionPreference.objects.create(
            section=self.section1,
            preference=p)
        result = module_info(self.section1)
        self.assertTrue('id' in result[0])
        self.assertTrue('label' in result[0])
        self.assertTrue('url' in result[0])
        self.assertTrue(result[0]['url'].startswith('/latest'))
