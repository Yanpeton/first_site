from django.shortcuts import render, redirect
from blog.models import Article, Comment, UserProfile
from blog.form import CommentForm, UserProfileForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
                                      PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta

PAGE_ARTICLE_NUM = 3
DISPLAY_COLLECTOR_NUM = 2


def split_page(articles, page_num):
    side_show_page_num = 1

    page_robot = Paginator(articles, PAGE_ARTICLE_NUM)
    try:
        articles_list = page_robot.page(page_num)
    except EmptyPage:
        articles_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        articles_list = page_robot.page(1)

    page_list = [-1]*len(page_robot.page_range)

    for i in page_robot.page_range:
        if i == 1 or i == page_robot.num_pages or (i <= articles_list.number + side_show_page_num and i >= articles_list.number - side_show_page_num):
            page_list[i-1] = i
        elif i == articles_list.number + side_show_page_num + 1 or i == articles_list.number - side_show_page_num - 1:
            page_list[i-1] = 0
    return articles_list, page_list


def check_is_completed(func):
    def inner(request, *args, **kwargs):
        if request.user.profile.is_completed is False and now() > \
           request.user.date_joined + timedelta(minutes=5):
            return redirect(to='complete')
        return func(request, *args, **kwargs)
    return inner


@check_is_completed
@login_required
def listing(request, **kwargs):
    context = {}
    tag = kwargs.get('tag')
    sort = kwargs.get('sort')
    page_num = request.GET.get('page')
    if tag in ['life', 'tech']:
        articles = Article.objects.filter(tag=tag)
        context['tag'] = tag
    else:
        articles = Article.objects.all()
        context['tag'] = 'all'
    if sort == 'up':
        articles = articles.order_by('watched_counts')
    elif sort == 'down':
        articles = articles.order_by('-watched_counts')

    context['articles_list'], context['page_list'] = split_page(articles,
                                                                page_num)
    return render(request, 'articles.html', context)


@check_is_completed
@login_required
def article_detail(request, error_form=None, **kwargs):
    context = {}
    article_id = kwargs['article_id']
    article = Article.objects.get(id=article_id)
    best_comments = Comment.objects.filter(best_comment=True,
                                           belong_to=article)
    collect = request.POST.get('collect')
    if best_comments:
        context['best_comments'] = best_comments
    if request.method == 'POST' and 'comment' in request.POST.keys():
        context['form'] = deal_with_comment(request, article)
    else:
        context['form'] = CommentForm
    context['article'] = article
    try:
        Article.objects.get(id=int(article.id)+1)
        next_article_id = int(article_id) + 1
    except ObjectDoesNotExist:
        next_article_id = ''
    if collect == 'yes':
        article.collectors.add(request.user)
    elif collect == 'no':
        article.collectors.remove(request.user)
    context['next_article_id'] = str(next_article_id)
    context['display_collector_num'] = DISPLAY_COLLECTOR_NUM
    return render(request, 'article_detail.html', context)


def deal_with_comment(request, article):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        c = Comment(user=request.user, comment=comment, belong_to=article)
        c.save()
        return CommentForm
    else:
        return form


def index_login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            userprofile, _ = UserProfile.objects.get_or_create(
                             belong_to=form.get_user())
            userprofile.real_last_login = form.get_user().last_login
            userprofile.save()
            login(request, form.get_user())
            return redirect(to='article_list')
    context['form'] = form
    context['register_or_login'] = 'Register'
    return render(request, 'register_login.html', context)


def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context['form'] = form
    context['register_or_login'] = 'Login'
    return render(request, 'register_login.html', context)


@login_required
def complete(request):
    return render(request, 'complete.html', {})


@login_required
def profile(request, error_form=None, message=None):
    context = {}
    if error_form:
        context['form'] = error_form
    else:
        context['form'] = UserProfileForm
    context['message'] = message
    return render(request, 'profile.html', context)


def profile_post(request):
    user_profile = request.user.profile
    form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
    if form.is_valid():
        form.save()                # 一步到位，不需要user_profile.save()了
    else:
        return profile(request, error_form=form)
    return redirect(to='profile')


@login_required
def pwd_change(request):
    context = {}
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return profile(request, message="Password changed successfully.")
    context['form'] = form
    return render(request, 'pwd_change.html', context)


@login_required
def collection_list(request):
    user = request.user
    print(user)
    articles = user.article_set.all()
    print(articles)
    return render(request, 'collection.html', {'articles': articles})
