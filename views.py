from django.utils import timezone
from .models import Post, Consultation, LikeDislike
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, SignUp, ConsultationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import auth
import json
from django.http import HttpResponse, Http404
from django.views import View
from django.contrib.contenttypes.models import ContentType 

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


class VotesView(View):
    model = None     # Модель данных - Статьи или Комментарии
    vote_type = None # Тип комментария Like/Dislike
 
    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True
 
        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )