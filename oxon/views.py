from django.shortcuts import render
from product.models import Post
from account.models import Account, Follow
from datetime import datetime, timezone
from account.models import Account

# Create your views here.
def home(request):
    product = Post.objects.all()[:6]

    for p in product:
        if p.lastbiddate <= datetime.now(timezone.utc):
            p.delete()



    context = {
        'product':product,
    }
    return render(request, 'home.html', context)

def error(request):

    return render(request,'error.html', context={})

