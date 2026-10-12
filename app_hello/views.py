from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from app_hello.models import Profile

from .models import Skill


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
    for skill in selected_skills:
        users = users.filter(skill__title__iexact=skill)

    users = users.distinct()

    # ---------- list of skills shown in the sidebar ----------
    skills = (
        Skill.objects
        .order_by('title')
        .values_list('title', flat=True)
        .distinct()
    )

    # ---------- pagination ----------
    paginator = Paginator(users.distinct(), ITEM_PER_PAGE)
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
        'locations':Profile.objects.values_list('location',flat=True)
    }
    return render(request, 'index.html', context)

def my_form(request):
    q = request.GET.get('q','')
    users = User.objects.all()
    if q:
        users = User.objects.filter(first_name__icontains=q)
    context = {
        'users':users,
        'q':q
    }
    return render(request,'my_form.html',context)