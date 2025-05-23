from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.core.mail import send_mail
from tasks.models import Task



# Signals 

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employee_task_creation(sender, instance, action, **kwargs):
    if action=='post_add':
        assigned_email = [emp.email for emp in instance.assigned_to.all()]
        
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}.",
            "nazmulislamfsd@gmail.com",
            assigned_email,
            fail_silently=False
        )


@receiver(post_delete, sender=Task)
def delete_associate_detail(sender, instance, **kwargs):
    if instance.details:
        print(instance)
        print(instance.details)


# pre save 
# @receiver(pre_save, sender=Task)
# def notify_task_creation(sender, instance, **kwargs):
#     print("sender: ", sender)
#     print("instance: ", instance)
#     print("kwargs: ", kwargs)
#     instance.is_completed = True


# post save 
# @receiver(post_save, sender=Task)
# def notify_task_created(sender, instance, created, **kwargs):
#     if created:
#         print("Hello!!!!!!!")