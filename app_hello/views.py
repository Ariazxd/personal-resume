from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Profile, Skill
from .forms import (
    UserForm,
    ProfileForm,
    ExperienceFormSet,
    EducationFormSet,
    ProjectFormSet,
    SkillFormSet,
)


def resume(request, id):
    user = get_object_or_404(User, id=id)
    context = {'user': user}
    return render(request, 'resume.html', context)


def index(request):
    ITEM_PER_PAGE = 5

    # ---------- values coming from the filter form ----------
    q = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    selected_skills = request.GET.getlist('skills')

    users = User.objects.all().order_by('id')

    # ---------- search: name or job title ----------
    if q:
        users = users.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(profile__job_title__icontains=q)
        )

    # ---------- location ----------
    if location:
        users = users.filter(profile__location__icontains=location)

    # ---------- skills: the user must have ALL the selected skills ----------
    # Skill belongs to Profile, so the lookup goes through profile
    for skill in selected_skills:
        users = users.filter(profile__skill__title__iexact=skill)

    users = users.distinct()

    # ---------- list of skills shown in the sidebar ----------
    skills = (
        Skill.objects
        .order_by('title')
        .values_list('title', flat=True)
        .distinct()
    )

    # ---------- pagination ----------
    paginator = Paginator(users, ITEM_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))

    # keep the filters in the pagination links (everything except "page")
    params = request.GET.copy()
    params.pop('page', None)

    context = {
        'page_obj': page_obj,
        'skills': skills,
        'selected_skills': selected_skills,
        'q': q,
        'querystring': params.urlencode(),
        'locations': (
            Profile.objects.exclude(location__isnull=True)
            .exclude(location='')
            .values_list('location', flat=True)
            .distinct()
        ),
    }
    return render(request, 'index.html', context)


def my_form(request):
    q = request.GET.get('q', '')
    users = User.objects.all()
    if q:
        users = User.objects.filter(first_name__icontains=q)
    context = {
        'users': users,
        'q': q
    }
    return render(request, 'my_form.html', context)


@login_required
def resume_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        experience_formset = ExperienceFormSet(request.POST, instance=profile)
        education_formset = EducationFormSet(request.POST, instance=profile)
        project_formset = ProjectFormSet(request.POST, instance=profile)
        skill_formset = SkillFormSet(request.POST, instance=profile)

        all_forms = [
            user_form, profile_form, experience_formset,
            education_formset, project_formset, skill_formset,
        ]
        # a list (not a generator) so every form is validated and shows its errors
        if all([f.is_valid() for f in all_forms]):
            for f in all_forms:
                f.save()
            return redirect("resume-edit")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        experience_formset = ExperienceFormSet(instance=profile)
        education_formset = EducationFormSet(instance=profile)
        project_formset = ProjectFormSet(instance=profile)
        skill_formset = SkillFormSet(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'experience_formset': experience_formset,
        'education_formset': education_formset,
        'project_formset': project_formset,
        'skill_formset': skill_formset,
    }
    return render(request, 'resume-edit.html', context)
