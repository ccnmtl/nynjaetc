import factory
from nynjaetc.treatment_activity.models import (
    TreatmentNode, TreatmentPath)


def TreatmentNodeFactory():
    # treebeard nodes do not factory easily
    return TreatmentNode.add_root(
        name="treatmentnode",
        type='RT',
        duration=0,
        value=0,
    )


class TreatmentPathFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TreatmentPath
    name = "treatmentpath"
    # NOTE: you must pass in the TreatmentNode tree
    # factoryboy can't auto-instantiate one

    cirrhosis = False
    treatment_status = 0
    drug_choice = 'boceprevir'
