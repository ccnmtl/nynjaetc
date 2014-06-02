from smoketest import SmokeTest
from django.contrib.auth.models import User
from quizblock.models import Question
from django.conf import settings


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = User.objects.all().count()
        # all we care about is not getting an exception
        self.assertTrue(cnt > -1)


class HRSA_ID_QuestionCheck(SmokeTest):
    def test_question(self):
        """ we expect the HRSA_ID_FIELD to correspond to
        a question that asks the user to enter their HRSA ID.
        There's no perfect way of making sure this is configured
        correctly, but for now we can at least check that the
        configured Question at least has some of the text
        that we expect.

        If this one errors, it probably means that the question doesn't
        exist. If it fails, it may mean that it's pointing to the wrong
        Question. There is also the possibility of a false positive
        if someone just changes the question text in a way that
        violates our expectations."""
        id = settings.HRSA_ID_FIELD[-2:]
        q = Question.objects.get(id=id)
        self.assertTrue("HRSA unique ID" in q.text)
