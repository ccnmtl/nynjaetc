from django.test import TestCase
from .factories import TreatmentNodeFactory, TreatmentPathFactory


class TreatmentNodeTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNodeFactory()
        self.assertEqual(str(tn), "  treatmentnode")


class TreatmentPathTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNodeFactory()
        tp = TreatmentPathFactory(tree=tn)
        self.assertEqual(str(tp), "treatmentpath")
