from django.shortcuts import render
from django.utils import timezone
from .models import Post, Consultation
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, UserForm, ConsultationForm
from django.shortcuts import render

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def cons_list(request):
    consultations = Consultation.objects.filter(creation__lte=timezone.now()).order_by('creation')
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
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=True)
            user.save()
            return redirect('cons_list')
    else:
        user_form = UserForm()
    return render(request, 'blog/new_user.html', {'user_form': user_form})


def cons_new(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=True)
            consultation.author = request.user
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