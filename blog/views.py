from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from mysite import settings
from .models import Post, Consultation, UserModel
from django.shortcuts import get_object_or_404
from .forms import PostForm, ConsultationForm, SignUp, FilterDate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q


def post_list(request):
    posts = Post.objects.order_by('-likes')
    return render(request, 'suggestions/list_suggs.html', {'posts': posts, 'request': request})


def cons_list(request):
    consultations = Consultation.objects.order_by('-creation')
    form = FilterDate(request.GET)
    if form.is_valid():
        if form.cleaned_data["dateFrom"]:
            consultations = consultations.filter(date__gte=form.cleaned_data["dateFrom"])
        if form.cleaned_data["dateTo"]:
            consultations = consultations.filter(date__lte=form.cleaned_data["dateTo"])
        if form.cleaned_data["search"]:
            if ' ' in form.cleaned_data["search"]:
                consultations = consultations.annotate(similarity=Greatest(
                    TrigramSimilarity('theme', form.cleaned_data["search"]),
                    TrigramSimilarity('discription', form.cleaned_data["search"]))).filter(
                    similarity__gte=0.1).order_by('-similarity')

                # consultations = consultations.annotate(
                #     similarity=TrigramSimilarity('theme', form.cleaned_data["search"]), ).filter(
                #     similarity__gte=0.1).order_by('-similarity')
            else:
                vector = SearchVector('theme', weight='A') + SearchVector('discription', weight='B') # или там, или там, или вместе
                query = SearchQuery(form.cleaned_data["search"])
                consultations = consultations.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1).order_by('-rank')
        if form.cleaned_data["contact"]:
            consultations = consultations.filter(contact=int(form.cleaned_data["contact"][0]))
        if form.cleaned_data["hashtegs"]:
            q_lst = form.cleaned_data["hashtegs"][1:len(form.cleaned_data["hashtegs"])].split("#")
            print(q_lst)
            consultations = consultations.filter(hashteg__in=q_lst)

    return render(request, 'consultations/main.html',
                  {'request': request, 'consultations': consultations, 'form': form})


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
    password = get_random_string(5)
    if request.method == "POST":
        # userm = UserModel(password1=password, password2=password)
        # print(password)
        form = SignUp(request.POST, initial={'password1': password, 'password2': password})
        if form.is_valid():
            user = form.save(commit=False)
            # password = get_random_string(5)
            # user.password1 = password
            # user.password2 = password
            send_mail('Подтверждение регистрации на Cherdak', 'Имя пользователя:' + '\n' +
                      'Пароль: ' + password, settings.EMAIL_HOST_USER, [user.email])
            user.save()
            return redirect('login')
    else:
        form = SignUp(initial={'password1': password, 'password2': password})
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
                consultation.hashteg = consultation.hashteg[1:len(consultation.hashteg)].split("#")
                print(consultation.hashteg)
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