from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from .factories import (
    TreatmentNodeFactory, TreatmentPathFactory)


class BasicTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def tearDown(self):
        self.u.delete()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_edit(self):
        response = self.c.get("/edit/")
        self.assertEquals(response.status_code, 200)

    def test_reset(self):
        response = self.c.post(
            "/",
            dict(action="reset"),
        )
        self.assertEquals(response.status_code, 302)

    def test_submit(self):
        response = self.c.post(
            "/",
            dict(action=""),
        )
        self.assertEquals(response.status_code, 302)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class GetNextStepsTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def tearDown(self):
        self.u.delete()

    def test_not_ajax(self):
        r = self.c.post("/_rgt/123/123/")
        self.assertEqual(r.status_code, 403)

    def test_ajax_allowed(self):
        tn = TreatmentNodeFactory()
        tp = TreatmentPathFactory(tree=tn)

        r = self.c.post("/_rgt/%d/%d/" % (tp.id, tn.id), dict(),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertNotEqual(r.status_code, 403)
