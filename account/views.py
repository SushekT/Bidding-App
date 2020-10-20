from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import Account, Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from product.form import PostForm
from product.models import Post
from .form import editprofileform
from product.models import Bidding
from .token import generatetoken
from .mail import CustomMail

# Create your views here.
def register(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        contact = request.POST['contact']
        gender = request.POST['gender']
        if (len (password)>6):
            account = Account(email=email, address=address, contact_no=contact, gender=gender)
            account.set_password(password)
            try:
                account.token = generatetoken()
                account.save()
                messages.success(request, message="Account created successfully")
            except:
                messages.error(request, message="Email is already taken or Invalid Email")
        else:
            messages.error(request, message="Password must be greater than 6")
        return redirect('home')
    else:
        return redirect('home')

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_verified == False:
                return render(request, 'token_verification_message.html')
            return redirect('account:dashboard', request.user.id)
        else:
            messages.error(request, 'Email and password does not match')
            return redirect('home')

@login_required(login_url='/')
def verifyaccount(request,token):
    verifyaccount = Account.objects.get(id=request.user.id)
    context = {}
    if verifyaccount.token == token:
        verifyaccount.is_verified = True
        verifyaccount.save()
        context['success'] = 'Successfully verified'
    else:
        context['error'] = 'Sorry, could not be verified'

    return render(request, 'verifyaccount.html', context)



def dashboard(request, id):
    yourpost = Post.objects.filter(user_id=id)
    ft = Follow.objects.filter(followed_to = id)
    fb = Follow.objects.filter(followed_by = id)
    follower = ft.count()
    followed = fb.count()
    isAlreadyFollowed = False

    try:
        Follow.objects.get(followed_to=id, followed_by=request.user.id)
        isAlreadyFollowed = True
    except:
        isAlreadyFollowed = False

    acc = Account.objects.get(id=id)
    context = {
        'acc': acc,
        'id': id,
        'follower': follower,
        'followed': followed,
        'isAlreadyFollowed': isAlreadyFollowed
    }

    if request.user.is_verified == False:
        return render(request, 'token_verification_message.html')
    return render(request,'Dashboard.html', context)

def logouts(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/')
def addPost(request):
    if request.method == 'GET':
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'AddPost.html', context)
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            try:
                data.save()
                messages.success(request, 'successfully saved')
                return redirect('account:posts', request.user.id)
            except:
                print('12222222222222333333333333333333')
                return render(request, 'AddPost.html', context={'form': form})

        else:
            print('111111111111222222222222333333333333333')
            return render(request, 'AddPost.html', context={'form': form})

def changeImage(request):
    image = request.FILES.get('image')
    user_id = request.user.id
    acc = Account.objects.get(id=user_id)
    acc.image = image
    acc.save()
    return redirect('account:dashboard', request.user.id)


def yourpost(request, id):
    yourpost = Post.objects.filter(user_id = id)[::-1]
    acc = Account.objects.get(id=id)
    context = {
    'acc': acc,
    'yourpost': yourpost,
    'id': id,
    }
    return render(request,'yourpost.html', context)
@login_required(login_url='/')
def editpost(request, slug):
    editpost = Post.objects.get(slug=slug)
    if editpost.user_id == request.user.id:
        form = PostForm(request.POST or None, request.FILES or None, instance=editpost)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Successfully post updated")
            return redirect('account:posts', request.user.id)


        context = {
        'form': form,
        }
        return render(request, 'editpost.html', context)
    else:
        return redirect('error')

@login_required(login_url='/')
def bidding_details(request, id):
    bid = Bidding.objects.filter(post_id = id)
    acc = Account.objects.get(id=request.user.id)

    context = {
        'bidding': bid,
        'acc':acc,
    }

    return render(request,'biddingdetail.html', context)

@login_required(login_url='/')
def profile_edit(request):
    acc = Account.objects.get(id=request.user.id)
    form = editprofileform(request.POST or None, request.FILES or None, instance=acc)

    context = {
        'form': form,
        'acc': acc
    }
    if request.method == "POST":
        try:
            acc.date_of_birth = request.POST.get('date_of_birth')
            acc.country = request.POST.get('country')
            acc.address = request.POST.get('address')
            acc.gender = request.POST.get('gender')
            acc.contact_no = request.POST.get('contact_no')
            acc.image = request.FILES.get('image')
            acc.save(update_fields=['date_of_birth','country','address','gender','contact_no', 'image'])
            messages.add_message(request, messages.SUCCESS, "Successfully Profile updated")
            return redirect('account:dashboard', request.user.id)

        except:
            return render(request,'profile_edit.html', context)

        else:
            return render(request,'profile_edit.html', context)


    return render(request,'profile_edit.html', context)



def follow(request, id):
    follows = Follow(followed_to=id, followed_by=request.user.id)
    try:
        follows.save()
        messages.add_message(request, messages.SUCCESS, "Successfully Followed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        raise ValueError ("Already Followed")


def resend_the_mail(request):
    acc = Account.objects.get(id=request.user.id)
    acc.save()
    messages.add_message(request, messages.SUCCESS, 'Verification Mail has resent to your mail successfully')
    return redirect('home')



