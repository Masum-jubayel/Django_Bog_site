from email.quoprimime import body_check

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from .models import author, category, article, postComment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .form import createForm, registerUser, creatAuthor, commentForm, categroyForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.views import View


# Create your views here.
class index(TemplateView):
    def get(self, request):
        post = article.objects.all()
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search) |
                Q(category__name__icontains=search)

            )
        paginator = Paginator(post, 8)  # Show 8 contacts per page

        page = request.GET.get('page')
        total_article = paginator.get_page(page)
        context = {
            "post": total_article
        }

        return render(request, "index.html", context)


class getauthor(TemplateView):
    def get(self, request, name):
        post_author = get_object_or_404(User, username=name)
        auth = get_object_or_404(author, name=post_author.id)
        post = article.objects.filter(article_author=auth.id)
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search) |
                Q(category__name__icontains=search)

            )
        paginator = Paginator(post, 8)  # Show 8 contacts per page

        page = request.GET.get('page')
        total_article = paginator.get_page(page)
        context = {
            "post": total_article,
            "auth": auth
        }
        return render(request, "profile.html", context)


class getsingle(View):
    def get(self, request, id):
        post = get_object_or_404(article, pk=id)
        first = article.objects.first()
        last = article.objects.last()
        getComment = postComment.objects.filter(post=id)
        related = article.objects.filter(category=post.category).exclude(id=id)[:8]
        form = commentForm
        context = {
            "post": post,
            "first": first,
            "last": last,
            "related": related,
            "form": form,
            "getComment": getComment
        }

        return render(request, "single.html", context)

    def post(self, request, id):
        post = get_object_or_404(article, pk=id)
        form = commentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            return redirect('blog:single_post', id=id)


class getTopic(TemplateView):
    def get(self, request, name):
        cat = get_object_or_404(category, name=name)
        post = article.objects.filter(category=cat.id)
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search) |
                Q(category__name__icontains=search)

            )
        paginator = Paginator(post, 8)  # Show 25 contacts per page

        page = request.GET.get('page')
        total_article = paginator.get_page(page)
        context = {
            "post": total_article,
            "cat": cat
        }

        return render(request, "category.html", context)


def getLogin(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    else:
        if request.method == 'POST':
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('blog:index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password mismatch')
    return render(request, "login.html")


def getLogout(request):
    logout(request)
    return redirect('blog:index')


class getCreate(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            you = get_object_or_404(author, name=request.user.id)
            form = createForm
            context = {
                "form": form,
                "you": you
            }
            return render(request, 'create.html', context)
        else:
            return redirect('blog:login')

    def post(self, request):
        you = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = you
            instance.save()
            messages.success(request, 'Posted new Article !!!')
            return redirect('blog:profile')


class getUpdate(TemplateView):
    def get(self, request, pid):
        if request.user.is_authenticated:
            you = get_object_or_404(author, name=request.user.id)
            post = get_object_or_404(article, id=pid)
            form = createForm(request.POST or None, request.FILES or None, instance=post)
            context = {
                "form": form,
                "you": you
            }
            return render(request, 'create.html', context)
        else:
            return redirect('blog:login')

    def post(self, request, pid):
        post = get_object_or_404(article, id=pid)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        you = get_object_or_404(author, name=request.user.id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = you
            instance.save()
            messages.success(request, 'Article Updated Successfully !!')
            return redirect('blog:profile')


class getDelete(TemplateView):
    def get(self, request, pid):
        if request.user.is_authenticated:
            post = get_object_or_404(article, id=pid)
            post.delete()
            messages.warning(request, 'Article Deleted Successfully !!')
            return redirect('blog:profile')
        else:
            return redirect('blog:login')


class getProfile(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, id=request.user.id)
            author_profile = author.objects.filter(name=user.id)
            if author_profile:
                authorUser = get_object_or_404(author, name=request.user.id)
                post = article.objects.filter(article_author=authorUser.id)
                context = {
                    "post": post,
                    "user": authorUser
                }
                return render(request, 'logged_in_profile.html', context)
            else:
                form = creatAuthor(request.POST or None, request.FILES or None)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.name = user
                    instance.save()
                    return redirect('blog:profile')
                return render(request, 'creatauthor.html', {"form": form})

        else:
            return redirect('blog:login')


def getRegister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Registration successfully completed ")
        return redirect('blog:login')
    return render(request, 'register.html', {"form": form})


class getCategory(TemplateView):
    def get(self, request):
        query = category.objects.all()
        return render(request, 'topics.html', {"topic": query})


class creatTopic(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                form = categroyForm
                return render(request, 'create_category.html', {"form": form})
            else:
                raise Http404("You are a not authorized to access this page")
        else:
            return redirect('blog:login')

    def post(self, request):
        form = categroyForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Category Create Successfully Completed")
            return redirect('blog:category')

# def getCategoryUpdate(request, pid):
#     if request.user.is_authenticated:
#         you = get_object_or_404(author, name=request.user.id)
#         post = get_object_or_404(article, id=pid)
#         form = createForm(request.POST or None, request.FILES or None, instance=post)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.article_author = you
#             instance.save()
#             messages.success(request, 'Article Updated Successfully !!')
#             return redirect('blog:category')
#         context = {
#             "form": form,
#             "you": you
#         }
#         return render(request, 'create_category.html', context)
#     else:
#         return redirect('blog:login')
#
#
# def getCategoryDelete(request, pid):
#     if request.user.is_authenticated:
#         post = get_object_or_404(article, id=pid)
#         post.delete()
#         messages.warning(request, 'Article Deleted Successfully !!')
#         return redirect('blog:category')
#     else:
#         return redirect('blog:login')
