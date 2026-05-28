from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_student_group(sender, instance, created, **kwargs):
    if created:                                        # only fires on NEW users
        student_group, _ = Group.objects.get_or_create(name='Student')
        instance.groups.add(student_group)