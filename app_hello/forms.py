from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Profile, Experience, Education, Project, Skill


class StyledFormMixin:
    """Gives every widget the same CSS class so the edit page looks consistent."""

    def _style_fields(self):
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                continue
            widget.attrs.setdefault('class', 'form-control')
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault('rows', 3)


# ---------------------------------------------------------------
# Single-object forms
# ---------------------------------------------------------------

class UserForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['job_title', 'phone', 'location', 'description', 'intrests']
        labels = {
            'job_title': 'Job title',
            'phone': 'Phone',
            'location': 'Location',
            'description': 'About me',
            'intrests': 'Interests',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the model fields are null=True but not blank=True, so Django would
        # force the user to fill every one of them: make them optional
        for field in self.fields.values():
            field.required = False
        self._style_fields()


# ---------------------------------------------------------------
# Rows that belong to a profile (many per profile)
# ---------------------------------------------------------------

class ExperienceForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'location', 'date_range', 'position', 'job_description']
        labels = {
            'title': 'Company',
            'location': 'Location',
            'date_range': 'Date range',
            'position': 'Position',
            'job_description': 'Description',
        }
        widgets = {
            'date_range': forms.TextInput(attrs={'placeholder': '2022 - 2024'}),
            'job_description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class EducationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Education
        fields = ['university', 'location', 'date_range', 'degree', 'study_description']
        labels = {
            'university': 'University',
            'location': 'Location',
            'date_range': 'Date range',
            'degree': 'Degree',
            'study_description': 'Description',
        }
        widgets = {
            'date_range': forms.TextInput(attrs={'placeholder': '2018 - 2022'}),
            'study_description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        labels = {'title': 'Title', 'description': 'Description'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class SkillForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'level']
        labels = {'title': 'Skill', 'level': 'Level (1-5)'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['level'].initial = 1
        self._style_fields()


# ---------------------------------------------------------------
# Formsets: "all the experiences / educations / ... of ONE profile"
# ---------------------------------------------------------------

ExperienceFormSet = inlineformset_factory(
    Profile, Experience, form=ExperienceForm, extra=1, can_delete=True,
)

EducationFormSet = inlineformset_factory(
    Profile, Education, form=EducationForm, extra=1, can_delete=True,
)

ProjectFormSet = inlineformset_factory(
    Profile, Project, form=ProjectForm, extra=1, can_delete=True,
)

SkillFormSet = inlineformset_factory(
    Profile, Skill, form=SkillForm, extra=1, can_delete=True,
)
