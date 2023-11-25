"""models."""
from django.db import models


class CoupledInputResponse(models.Model):
    """ Django model used to store CoupledInput data. """
    """ This data needs to be shared and queried across users
        and XBlock instances (workaround).
    """

    class Meta:
        app_label = 'coupledinput'
        unique_together = (('course_id', 'student_id', 'block_id'),)

    course_id = models.CharField(max_length=50, db_index=True)
    student_id = models.CharField(max_length=32, db_index=True)
    block_id = models.CharField(max_length=50, db_index=True)
    prompt = models.TextField(blank=True, default='')
    response_one = models.TextField(blank=True, default='')
    response_two = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # Force validation of max_length
        self.full_clean()
        super().save(*args, **kwargs)

class CoupledInputUser(models.Model):
    """ Django model used to store CoupledInput data. """
    """ This data needs to be shared and queried across users
        and XBlock instances (workaround).
    """

    class Meta:
        app_label = 'coupledinput'
        unique_together = (('course_id', 'student_id'),)

    course_id = models.CharField(max_length=50, db_index=True)
    student_id = models.CharField(max_length=32, db_index=True)
    student_name = models.TextField(blank=True, default='')
    name_one = models.TextField(blank=True, default='')
    name_two = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # Force validation of max_length
        self.full_clean()
        super().save(*args, **kwargs)

