from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q


def resume(request,id):
    user = get_object_or_404(User,id=id)
    context = {'user': user}
    return render(request,'resume.html',context)

def index(request):
    q = request.GET.get('q')
    if q:
        users = User.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(profile__job_title__icontains=q)
        )
    else:
        users = User.objects.all()
    ITEM_PER_PAGE = 5
    paginator = Paginator(users, ITEM_PER_PAGE )  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "q": q
    }
    return render(request, "index.html", context)
    # users=User.objects.all()
    # context={
    #     'users':users
    # }
    # return render(request,'index.html',context)

def my_form(request):
    q = request.GET.get('q')
    users = User.objects.all()
    if q:
        users = User.objects.filter(first_name__icontains=q)
    context = {
         'users':users,
         'q': q
               
    }
    return render(request,'my_form.html',context)