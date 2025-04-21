from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # task

    def __str__(self):
        return self.name

class Task(models.Model):
    assigned_to_employee = models.ManyToManyField(Employee,related_name='tasks')
    project = models.ForeignKey("Project", on_delete = models.CASCADE, default=1, related_name='allTask')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # details


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
    assigned_to = models.CharField(max_length=200)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICE, default=LOW)


class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    # allTask