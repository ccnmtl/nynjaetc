from django.test import TestCase
from .factories import TreatmentNodeFactory, TreatmentPathFactory


class TreatmentNodeTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNodeFactory()
        self.assertEqual(str(tn), "  treatmentnode")

    def test_json(self):
        tn = TreatmentNodeFactory()
        self.assertTrue('id' in tn.to_json().keys())
        self.assertTrue('name' in tn.to_json().keys())
        self.assertTrue('type' in tn.to_json().keys())
        self.assertTrue('duration' in tn.to_json().keys())
        self.assertTrue('help' in tn.to_json().keys())


class TreatmentPathTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNodeFactory()
        tp = TreatmentPathFactory(tree=tn)
        self.assertEqual(str(tp), "treatmentpath")
