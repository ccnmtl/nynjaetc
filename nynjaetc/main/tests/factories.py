import factory
from django.contrib.auth.models import User
from nynjaetc.main.models import (
    UserProfile, SectionTimestamp, SectionAlternateNavigation,
    SectionQuizAnsweredCorrectly, Preference, SectionPreference,
)
from pagetree.models import Hierarchy, Section
from quizblock.models import Quiz, Submission
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


class PreferenceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Preference
    slug = factory.Sequence(lambda x: "pref%d" % x)


class SectionPreferenceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SectionPreference
    preference = factory.SubFactory(PreferenceFactory)


class QuizFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Quiz


class SubmissionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Submission
    quiz = factory.SubFactory(QuizFactory)
    user = factory.SubFactory(UserFactory)
