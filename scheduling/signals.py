from scheduling import models as m
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed


def emp_service_mm_changed(instance, model, action, pk_set, **kwargs):
    """
    :param instance: the instance that triggered the signal (either a service or an employee instance)
    :param model: this will return the class of the model is being added it is the oposite of the above
    :param action: this will tell what action triggered this and if it's pre or pos
    :param pk_set: the list primary keys for the model
    :param kwargs: to allow extra values without breaking the function
    :return: This function will check the owner of the instance and the owner of all the instances of the opposite class
    that has the pk on pk_set, if one of the entities on the list doesn't belong to the same owner, it will raise a
    validation error.
    """
    if action == 'pre_add':
        for entity in model.objects.filter(pk__in=pk_set):
            if instance.owner_id != entity.owner_id:
                raise ValidationError('services must be of the same owner as employee')


m2m_changed.connect(emp_service_mm_changed, sender=m.Employee.services.through)
