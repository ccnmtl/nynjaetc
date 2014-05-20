from django.test import TestCase
from .factories import (
    TreatmentNodeFactory, TreatmentPathFactory, TreatmentActivityBlockFactory)


class TreatmentNodeTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNodeFactory()
        self.assertEqual(str(tn), "  treatmentnode")
        tn = TreatmentNodeFactory(type='DP')
        self.assertEqual(str(tn), "  Decision Point: treatmentnode")
        tn = TreatmentNodeFactory(duration=5)
        self.assertEqual(str(tn), "  5 weeks: treatmentnode")

    def test_json(self):
        tn = TreatmentNodeFactory()
        self.assertTrue('id' in tn.to_json().keys())
        self.assertTrue('name' in tn.to_json().keys())
        self.assertTrue('type' in tn.to_json().keys())
        self.assertTrue('duration' in tn.to_json().keys())
        self.assertTrue('help' in tn.to_json().keys())

    def test_is_decisionpoint(self):
        tn = TreatmentNodeFactory(type='DP')
        self.assertTrue(tn.is_decisionpoint())
        tn.type = 'PR'
        tn.save()
        self.assertFalse(tn.is_decisionpoint())


class TreatmentPathTest(TestCase):
    def test_unicode(self):
        tn = TreatmentNodeFactory()
        tp = TreatmentPathFactory(tree=tn)
        self.assertEqual(str(tp), "treatmentpath")


class TreatmentActivityBlockTest(TestCase):
    def test_needs_submit(self):
        tab = TreatmentActivityBlockFactory()
        self.assertFalse(tab.needs_submit())

    def test_edit_form(self):
        tab = TreatmentActivityBlockFactory()
        f = tab.edit_form()
        self.assertTrue(f is not None)

    def test_unlocked(self):
        tab = TreatmentActivityBlockFactory()
        self.assertTrue(tab.unlocked(None))

    def test_treatment_paths(self):
        tab = TreatmentActivityBlockFactory()
        self.assertEqual(tab.treatment_paths().count(), 0)
        tn = TreatmentNodeFactory()
        tp = TreatmentPathFactory(tree=tn)
        self.assertEqual(list(tab.treatment_paths()), [tp])
