from django.shortcuts import render
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import get_object_or_404

def hello(request):
    context = {'name':'Aria',
               'now':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               'news':[
                   {
                       'id':1,
                       'title':'news1'
                   },
                   {
                        'id':2,
                        'title':'news2'
                   },
                   {
                        'id':3,
                        'title':'news3'
                   }
               ]
               }
    return render(request,'index.html',context)


def resume(request,id):
    user = get_object_or_404(User,id=id)
    context = {'user': user}
    return render(request,'resume.html',context)