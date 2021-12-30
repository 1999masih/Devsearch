from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


# projects_list = [
#     {
#         'id': '1',
#         'title': 'Ecommerce Website',
#         'description': 'Fully functional ecommerce website'
#     },
#     {
#         'id': '2',
#         'title': 'Portfolio Website',
#         'description': 'A personal website to write articles and display work'
#     },
#     {
#         'id': '3',
#         'title': 'Social Network',
#         'description': 'An open source project built by the community'
#     }
# ]
# Create your views here.
def projects(request):
    # page = 'projects'
    # number = 10
    # context = {'page': page, 'number': number, 'projects': projects_list}
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)

# def project(request, pk):
#     # project_obj = None
#     # for i in projects_list:
#     #     if i['id'] == pk:
#     #         project_obj = i
#     project_obj = Project.objects.get(id=pk)
#     tags = project_obj.tags.all()
#     return render(request, 'projects/single-project.html', {'project':project_obj, 'tags' : tags})
def project(request, pk):
    # project_obj = None
    # for i in projects_list:
    #     if i['id'] == pk:
    #         project_obj = i
    project_obj = Project.objects.get(id=pk)
    
    return render(request, 'projects/single-project.html', {'project':project_obj})

@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    # project = Project.objects.get(id=pk)
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES ,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'projects/delete_template.html', context)
