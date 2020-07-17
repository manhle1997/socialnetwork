from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


from app.forms import RegistrationForm, EditProfileForm, AddImageAvatar
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from app.models import UserProfile
from home.models import Post
from home.models import Friend



def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username,
                                password=request.POST['password1'])

            login(request, user)
            return redirect('home')

    return render(request, 'accounts/reg_form.html', {'reg_form': form})
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #
    #     if form.is_valid():
    #         user = form.save()
    #         user = authenticate(username=user.username,
    #                             password=request.POST['password1'])
    #
    #         login(request, user)
    #         return redirect('home')
    # else:
    #     form = RegistrationForm()
    #
    #     context = {'reg_form': form}
    #     return render(request, 'accounts/reg_form.html', context)



def view_profile(request, pk=None):
    users = User.objects.exclude(id=request.user.id) #Lấy ra các đối tượng user mà không phải mình
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except:
        friends = None

    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    # print(user.username)
    # print(friends)
    if str(request.user) == str(user.username):
        temp = 'Me'
    else:
        if user in friends:
            temp = 'False'
        else:
            temp = 'True'

    posts = Post.objects.filter(user=user)
    args = {'user': user, 'temp':temp, 'friends': friends, 'posts': posts}
    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        user_add_avatar = UserProfile.objects.get(user=request.user)
        form_add_avatar = AddImageAvatar(request.POST, request.FILES, instance=request.user)

        form_edit_profile = EditProfileForm(request.POST, instance=request.user)
        if form_edit_profile.is_valid() and form_add_avatar.is_valid() :
            user_add_avatar.image = form_add_avatar.cleaned_data['image']
            user_add_avatar.save()
            form_edit_profile.save()

            return redirect('view_profile')
    else:
        form_edit_profile = EditProfileForm(instance=request.user)
        form_add_avatar = AddImageAvatar(request.POST)
        context = {'form_edit_profile': form_edit_profile, 'form_add_avatar': form_add_avatar}
        return render(request, 'accounts/edit_form.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('view_profile')
        else:
            return redirect('chane_password')
    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'accounts/passwordchange_form.html', context)


def add_image_avatar(request):
    # p = get_object_or_404(UserProfile, pk=id)
    # form = AddImageAvatar()

    if request.method == 'POST':
        user = request.user
        userProfile = UserProfile.objects.get(user=user)
        form = AddImageAvatar(request.POST, request.FILES, instance=user)
        if form.is_valid():
            userProfile.image = form.cleaned_data['image']
            userProfile.save()
            return redirect('view_profile')
    else:
        form = AddImageAvatar(request.POST)
    return render(request, 'accounts/add_images_avatar.html', {'form': form})


