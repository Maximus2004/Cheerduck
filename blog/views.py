from django.shortcuts import render
from django.utils import timezone
from .models import Post, Consultation
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, ConsultationForm, SignUp
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import Http404

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/suggs_list.html', {'posts': posts})

def cons_list(request):
    consultations = Consultation.objects.filter(creation__lte=timezone.now()).order_by('creation')
    print(consultations)
    return render(request, 'blog/post_list.html', {'consultations': consultations})

def post_detail(request, pk):  # новое представление данных 
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=True)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def user_new(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('cons_list')
    else:
        form = SignUp()
    return render(request, 'blog/signup.html', {'form': form})


def cons_new(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        print(form)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.owner = request.user
            consultation.creation = timezone.now()
            consultation.email = request.user.email
            consultation.save()
            return redirect('consultation_detail', pk=consultation.pk)            
    else:
        form = ConsultationForm()
    return render(request, 'blog/consultation_edit.html', {'form': form})

def cons_detail(request, pk):  # новое представление данных 
    consultation = get_object_or_404(Consultation, pk = pk)
    return render(request, 'blog/consultation_detail.html', {'consultation': consultation})

def cons_detail(request, pk):  # новое представление данных 
    consultation = get_object_or_404(Consultation, pk = pk)
    if request.user != consultation.owner:
    # if not request.user.is_staff or not request.user.is_superuser:
        return render(request, 'blog/consultation_detail_not_owner.html', {'consultation': consultation})
    else:
        return render(request, 'blog/consultation_detail.html', {'consultation': consultation})

def cons_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            consultation = form.save(commit=True)
            consultation.author = request.user
            consultation.save()
            return redirect('consultation_detail', pk = consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'blog/consultation_edit.html', {'form': form})