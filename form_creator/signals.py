from django.apps import apps
from django.db.models.base import ModelBase
from . import models as fc_models


def on_seq_no_instance_saved(
    sender: ModelBase,
    instance: fc_models.SeqNoBaseModel,
    **kwargs,
):
    """When a subclass of `SeqNoBaseModel` is saved, update the sequence
    number.
    """
    fc_models.FormElementOrder.objects.create_or_update_from_element(instance)


def on_seq_no_instance_deleted(
    sender: ModelBase,
    instance: fc_models.SeqNoBaseModel,
    **kwargs,
):
    """When a subclass of `SeqNoBaseModel` is deleted, remove the sequence
    number record.
    """
    fc_models.FormElementOrder.objects.delete_element(instance)


def connect_seq_no_signals() -> None:
    """Connect the on save and delete signals to models which are subclasses
    of `SeqNoBaseModel`.
    """
    for model in apps.get_models():
        if issubclass(model, fc_models.SeqNoBaseModel):
            fc_models.SEQ_NO_INSTANCE_SAVED.connect(
                on_seq_no_instance_saved,
                sender=model,
            )
            fc_models.SEQ_NO_INSTANCE_DELETED.connect(
                on_seq_no_instance_deleted,
                sender=model,
            )
