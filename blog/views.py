from django.utils import timezone
from .models import Post, Consultation, UserModel
from django.shortcuts import get_object_or_404
from .forms import PostForm, ConsultationForm, SignUp
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect


def post_list(request):
    posts = Post.objects.order_by('-likes')
    return render(request, 'suggestions/list_suggs.html', {'posts': posts, 'request': request})


def cons_list(request):
    consultations = Consultation.objects.order_by('-creation')
    return render(request, 'consultations/main.html', {'request': request, 'consultations': consultations})


def post_new(request):
    if request.user.username:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'suggestions/new_sugg.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")


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
    return render(request, 'suggestions/post_edit.html', {'form': form})


def post_detail(request, pk):  # новое представление данных
    post = get_object_or_404(Post, pk=pk)
    conses = Consultation.objects.filter(posts=post)
    if request.user == post.author:
        return render(request, 'suggestions/sugg_detail.html', {'post': post, 'conses': conses})
    else:
        return render(request, 'suggestions/sugg_detail.html', {'post': post, 'conses': conses})


def user_new(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('login')
    else:
        form = SignUp()
    return render(request, 'user/signup.html', {'form': form})


def cons_new(request):
    if request.user.username:
        if request.method == "POST":
            form = ConsultationForm(request.POST)
            if form.is_valid():
                consultation = form.save(commit=False)
                consultation.owner = request.user
                consultation.creation = timezone.now()
                consultation.email = request.user.email
                consultation.save()
                return redirect('consultation_detail', pk=consultation.pk)
        else:
            form = ConsultationForm()
        return render(request, 'consultations/create_consultation.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")


def cons_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.user != consultation.owner:
        return render(request, 'consultations/consultation_notOwner.html', {'consultation': consultation})
    else:
        return render(request, 'consultations/consultation_owner.html',
                      {'consultation': consultation, 'members': consultation.members.all()})


def cons_edit(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            consultation = form.save(commit=True)
            consultation.owner = request.user
            consultation.save()
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)
    return render(request, 'consultations/create_consultation.html', {'form': form})


def profile(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'user/profile.html', {'consultation': consultation})


def main_profile(request):
    cons = Consultation.objects.filter(owner=request.user)
    return render(request, 'user/main_profile.html', {'cons': cons})


def my_conses(request):
    cons = Consultation.objects.filter(owner=request.user)
    return render(request, 'consultations/my_conses.html', {'cons': cons})


def likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.username:
        post.likes += 1
        post.save()
        return HttpResponseRedirect("suggs/")
    else:
        return HttpResponseRedirect("login/")


# def grades(request, pk):
#     user = get_object_or_404(UserModel, pk = pk)
#     user.grades += 1
#     user.save()
#     return HttpResponseRedirect("profile/")

def delete_cons(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    consultation.delete()
    return HttpResponseRedirect("/myconses/")


def profile_edit(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == "POST":
        form = SignUp(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            return redirect('login')
    else:
        form = SignUp(instance=user)
    return render(request, 'user/profile_edit.html', {'form': form})


def new_member(request, pk):
    cons = get_object_or_404(Consultation, pk=pk)
    if request.user.username:
        cons.members.add(request.user)
        cons.save()
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/")


def similar(request, pk):
    post = get_object_or_404(Post, pk=pk)
    conses = Consultation.objects.filter(posts=post)
    return render(request, 'suggestions/similar.html', {'conses': conses})


def create(request, pk):
    if request.user.username:
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = ConsultationForm(request.POST)
            if form.is_valid():
                consultation = form.save(commit=False)
                consultation.owner = request.user
                consultation.creation = timezone.now()
                consultation.email = request.user.email
                consultation.posts = post
                consultation.save()
                return redirect('consultation_detail', pk=consultation.pk)
        else:
            form = ConsultationForm()
        return render(request, 'consultations/create_consultation.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")
# TODO 1) выяснить, почему пользователь начинает существовать только после входа, а не после регистрации
# TODO 2) выяснить, почему не работает редактирование модели пользователя (редактирует, но потом не может вернуться на main_profile)
# TODO 3) Добавить грейды
