from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from django.db.models import Count
from .form import Biddingform
from django.contrib import messages
from account.mail import CustomMail
# Create your views here.
def home(request):

    context = {

    }
    return render(request, 'home/home.html', context)

# Create your views here.
def product_detail(request,slug):
    product = Post.objects.get(slug=slug)
    post = Post.objects.all()[::-1]
    isAlreadyBid = False
    try:
        Bidding.objects.get(post_id=product.id, user_id=request.user.id)
        isAlreadyBid = True
    except:
        isAlreadyBid = False
        pass
    category_list = Category.objects.annotate(total_category=Count('post'))
    context = {
        'product': product,
        'category_list': category_list,
        'post': post,
        'isAlreadyBid': isAlreadyBid,
    }
    return render(request, 'product_detail.html', context)


def product_bid(request, slug):
    product = Post.objects.get(slug=slug)
    form = Biddingform(request.POST)
    if request.method == "POST":
        if form.is_valid():
            try:
                data = form.save(commit=False)
                data.post = product
                data.user = request.user
                data.save()
                email = Account.objects.get(id=product.user_id).email #email account of the post_id
                mail = CustomMail('bidding_template.html', 'Bidding Notification', [email,], biding_price=request.POST['bidingprice'], message=request.POST['message'], bidbyemail=request.user.email)
                mail.push()
                messages.add_message(request, messages.SUCCESS,"Succesfully Bid, Thank You")
                return redirect('product:product_detail', slug)
            except:
                messages.add_message(request, messages.ERROR, "You cannot Bid the product twice.")
                return redirect('product:product_detail', slug)
        else:
            messages.add_message(request, messages.ERROR,"Sorry couldn't bid this product, sorry for inconvienient service.")
            return redirect('product:product_detail', slug)

    context = {
    'product': product,
    'form': form,
    }
    return render(request, 'bid.html', context)

def product_delete(request,slug):
    product_delete= Post.objects.get(slug=slug)

    if request.method == "POST":
        try:
            product_delete.delete()
            messages.add_message(request, messages.SUCCESS, ('Succesfully Deleted'))
            return redirect('account:posts', request.user.id)
        except:
            messages.add_message(request, messages.ERROR, ('Error Occured'))


    context = {
        'product_delete': product_delete
    }
    return render(request, 'delete_product.html', context)

def products_status(request, bid, num):
    if (num<0 or num>2):
        return redirect('error.html')

    else:
        subject = ""
        message = ""
        bidding = Bidding.objects.get(id=bid)
        bidding.status = product_status[num][1]
        product = Post.objects.get(id=bidding.post.id)
        title = product.title
        bidding.first_time = False
        bidding.save()
        if num == 1:
            subject = "Biding Accepted"
            message = "Congratulation, Your Biding is Accepted for product named "+ title
        else:
            subject = "Biding Rejected"
            message = "Sorry, Your Biding is Rejected for product named "+ title

        email = Account.objects.get(id=bidding.user.id).email
        mail = CustomMail(template_name='bidingresponse.html', subject=subject, email_list=[email, ],
                          message= message)
        mail.push()
        messages.add_message(request, messages.SUCCESS, "Succesfully " + product_status[num][1])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def search(request):
    search_query = request.GET.get('q')
    result = Post.objects.filter(title__icontains=search_query)
    context = {
    }
    if len(result) == 0:
        context.update({'noresult':'Sorry you searched nothing matched to the Product'})
    else:
        context.update({'result': result})
    print(len(result))
    return render(request, 'search_result.html', context)






