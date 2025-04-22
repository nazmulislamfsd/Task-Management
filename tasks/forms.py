from django import forms
from tasks.models import Task

# django Form

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label='Task Title')
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label='Due Date')
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label='Assigned To', choices=[])


    def __init__(self, *args, **kwargs):
        # print(args,kwargs)
        employees = kwargs.pop('employees',[])
        # print(employees)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]


class StyledFormMixin:
    '''Mixing to apply style to form field'''

    default_classes = "border-2 border-gray-300 rounded-md p-2 w-full h-96"

    def apply_style_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 rounded-md"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })




# django Model Form
class TaskModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','due_date','assigned_to']

        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }


        '''Menual widget'''
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': "border-2 border-gray-300 rounded-md p-2 w-full h-96", 'placeholder': "Task Title"
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': "border-2 border-gray-300 rounded-md w-full h-32", 'placeholder': "Task Description"
        #     }),
        #     'due_date':forms.SelectDateWidget(attrs={
        #         'class': "border-2 border-gray-300 rounded-md"
        #     }),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         'class': "space-y-2"
        #     })
        # }

    '''Using Mixing Widget'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style_widgets()
        