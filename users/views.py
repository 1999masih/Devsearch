from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
# Create your views here.


def login_user(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, "users/login_register.html")

def logout_user(request):
    logout(request)
    messages.info(request, 'Username was logged out!')
    return redirect('login')

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error occured during registiration!')

    context = {'page':page, 'form': form}   
    return render(request, 'users/login_register.html', context)

def profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                    Q(short_intro__icontains=search_query) |
                                    Q(skill__in=skills))
    context = {'profiles': profiles, 'search_query': search_query}
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")

    context = {'profile':profile, 'top_skills':top_skills, 'other_skills':other_skills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def user_account(request):

    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    # other_skills = profile.skill_set.filter(description="")

    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfuly!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            
            form.save()
            messages.success(request, 'Skill was updated successfuly!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)

def delete_skill(request, pk):
    
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfuly!')
        return redirect('account')
    context = {'object':skill}
    return render(request, 'delete_template.html', context)




