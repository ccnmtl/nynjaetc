import factory
from django.contrib.auth.models import User
from nynjaetc.main.models import (
    UserProfile, SectionTimestamp, SectionAlternateNavigation,
    SectionQuizAnsweredCorrectly,
)
from pagetree.models import Hierarchy, Section
from datetime import datetime


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: "user%03d" % n)
    is_staff = True


class UserProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UserProfile
    user = factory.SubFactory(UserFactory)


class HierarchyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Hierarchy
    name = "root"
    base_url = "/"


def SectionFactory():
    h = HierarchyFactory()
    return Section.add_root(
        hierarchy=h,
        label="a section",
        slug="a-section",
    )


class SectionTimestampFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SectionTimestamp
    user = factory.SubFactory(UserFactory)
    timestamp = datetime.now()


class SectionAlternateNavigationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SectionAlternateNavigation


class SectionQuizAnsweredCorrectlyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SectionQuizAnsweredCorrectly
    user = factory.SubFactory(UserFactory)
