from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # tasks

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('IN PROGRESS','In Progress'),
        ('COMPLETED','Completed')
    ]
    assigned_to = models.ManyToManyField(Employee,related_name='tasks')
    project = models.ForeignKey("Project", on_delete = models.CASCADE, default=1, related_name='allTask')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIGN')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # details

    def __str__(self):
        return self.title


# One to One ---> This Example is out of this project ---> Ekta Student er Ektai Student_profile ase
                            # One to One : models.OneToOneField()
# One to Many ---> Ekta project e onekgula task thakte pare:
                            # One to Many : models.ForenignKey()
# Many to Many ---> Ekta Task onek Employee korte pare, Abar Ekta Employee Onekgula Task Korte pare


class Task_detail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_CHOICE = (
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    # assigned_to = models.CharField(max_length=200)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICE, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for Task {self.task.title}"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    # allTask

    def __str__(self):
        return self.name
    


from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.core.mail import send_mail

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