from django.db.models.signals import post_save
from django.dispatch import receiver
from mentor_api.models import Mentor, Request, Session

@receiver(post_save, sender=Request)
def create_session_on_request_accept(sender, instance, created, **kwargs):
    if instance.accepted and created:
        session = Session.objects.create(
            mentor=instance.mentor,
            student=instance.student,
            request=instance
        )
        # Additional logic if needed

@receiver(post_save, sender=Session)
def update_related_objects_on_session_save(sender, instance, created, **kwargs):
    if created:
        # Delete the request from the mentor's requested mentorships
        instance.request.delete()

        # Add the session to the mentor's created sessions
        mentor = instance.mentor
        mentor.created_sessions.add(instance)


