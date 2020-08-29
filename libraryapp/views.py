import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .models import Post, Category, Image, Film, User, Subcategory, Reading, Review, Key
from .examples.config import pagination


def index(request):

    if request.user.is_authenticated:

        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()
        context = {
            'categories': categories,
            'subcategories': subcategories
        }
        return render(request, "libraryapp/index.html", context)

    return HttpResponseRedirect(reverse("login"))


def category(request, category):

    if request.user.is_authenticated:
        if request.method != "POST":
            try:
                category_obj = Category.objects.get(pk=category)
            except Category.DoesNotExist:
                return JsonResponse({
                    "error": f"Category does not exist."
                }, status=400)
            categories = Category.objects.all()
            subcategories = Subcategory.objects.all().filter(category=category_obj.id)

            results = Reading.objects.all().order_by('-date')
            count = len(results)
            pages = pagination(request, results, 10)

            context = {
                'category_obj': category_obj,
                'categories': categories,
                'subcategories': subcategories,
                'category1': category,
                'count': count,
                'items': pages[0],
                'page_range': pages[1]
            }
            return render(request, "libraryapp/category.html", context)

        nameSubcategory = request.POST["newNameSubcategory"]
        try:
            category_obj = Category.objects.get(pk=category)
        except Category.DoesNotExist:
            return JsonResponse({
                "error": f"User does not exist."
            }, status=400)

        Subcategory.objects.get_or_create(
            name=nameSubcategory, category=category_obj)

        return HttpResponseRedirect(reverse("category", args=(category,)))

    return HttpResponseRedirect(reverse("login"))


# Global search engine for the Reading Materials
def search(request, category):
    try:
        category_obj = Category.objects.get(pk=category)
    except Category.DoesNotExist:
        return JsonResponse({
            "error": f"Category does not exist."
        }, status=400)

    try:
        valueName = request.GET.get("specific_search")
    except KeyError:
        valueName = None

    query = request.GET.get("q")

    if query is not None:
        if valueName is not None:
            if valueName == 'value-title':
                results = Reading.objects.filter(
                    Q(title__icontains=query)).order_by('-date')
            elif valueName == 'value-author':
                results = Reading.objects.filter(
                    Q(author__icontains=query)).order_by('-date')
            elif valueName == 'value-year':
                results = Reading.objects.filter(
                    Q(year__icontains=query)).order_by('-date')
        results = Reading.objects.filter(Q(title__icontains=query) | Q(
            author__icontains=query) | Q(year__icontains=query)).order_by('-date')
    elif query is None:
        results = Reading.objects.all().order_by('-date')
    count = len(results)
    pages = pagination(request, results, 3)

    categories = Category.objects.all()
    subcategories = Subcategory.objects.all().filter(category=category_obj.id)
    context = {
        'category_obj': category_obj,
        'categories': categories,
        'subcategories': subcategories,
        'category1': category,
        'query': query,
        'count': count,
        'items': pages[0],
        'page_range': pages[1]
    }
    return render(request, "libraryapp/category.html", context)

# Specific search engine for each Reading Material's subcategory


def search_subcategoy(request, category, subcategory):
    try:
        category_obj = Category.objects.get(pk=category)
    except Category.DoesNotExist:
        return JsonResponse({
            "error": f"Category does not exist."
        }, status=400)
    try:
        subcategory_obj = Subcategory.objects.get(pk=subcategory)
    except Subcategory.DoesNotExist:
        return JsonResponse({
            "error": f"Subcategory does not exist."
        }, status=400)

    try:
        valueName = request.GET.get("specific_search")
    except KeyError:
        valueName = None

    query = request.GET.get("q")
    specific_readings = Reading.objects.filter(
        subcategory=subcategory_obj).order_by('-date')

    if query is not None:
        if valueName is not None:
            if valueName == 'value-title':
                results = specific_readings.filter(
                    Q(title__icontains=query)).order_by('-date')
            elif valueName == 'value-author':
                results = specific_readings.filter(
                    Q(author__icontains=query)).order_by('-date')
            elif valueName == 'value-year':
                results = specific_readings.filter(
                    Q(year__icontains=query)).order_by('-date')
        results = specific_readings.filter(Q(title__icontains=query) | Q(
            author__icontains=query) | Q(year__icontains=query)).order_by('-date')
    elif query is None:
        results = specific_readings

    count = len(results)

    pages = pagination(request, results, 3)

    context = {
        'category_obj': category_obj,
        'subcategory_obj': subcategory_obj,
        'query': query,
        'count': count,
        'items': pages[0],
        'page_range': pages[1]
    }
    return render(request, "libraryapp/reading.html", context)


def subcategory(request, category, subcategory):

    if request.user.is_authenticated:
        try:
            category_obj = Category.objects.get(pk=category)
        except Category.DoesNotExist:
            return JsonResponse({
                "error": f"Category does not exist."
            }, status=400)
        try:
            subcategory_obj = Subcategory.objects.get(pk=subcategory)
        except Subcategory.DoesNotExist:
            return JsonResponse({
                "error": f"Subcategory does not exist."
            }, status=400)

        # Film and Videos
        if category_obj.name == 'Film and Videos':
            context = {
                'category_obj': category_obj,
                'subcategory_obj': subcategory_obj
            }

            if request.method == 'POST':
                title = request.POST["title"]
                link = request.POST["video_link"]
                description = request.POST["description"]
                newFilm = Film(
                    subcategory=subcategory_obj, user=request.user, title=title, link=link, description=description)
                newFilm.save()
                return HttpResponseRedirect(reverse("subcategory", args=(category, subcategory)))

            films = Film.objects.all().filter(subcategory=subcategory_obj).order_by('-date')

            pages = pagination(request, films, 3)
            context['items'] = pages[0]
            context['page_range'] = pages[1]

            return render(request, "libraryapp/film.html", context)

        # Reading Material
        elif category_obj.name == 'Reading Material':
            context = {}
            if request.method == 'POST':
                uploaded_file = request.FILES['pdf']
                try:
                    uploaded_cover = request.FILES['cover']
                    fs = FileSystemStorage()
                    coverName = fs.save(uploaded_cover.name, uploaded_cover)
                    cover = fs.url(coverName)
                    context['coverUrl'] = fs.url(coverName)
                except KeyError:
                    cover = None

                title = request.POST["title"]
                author = request.POST["author"]
                year = request.POST["year"]
                fs = FileSystemStorage()
                fileName = fs.save(uploaded_file.name, uploaded_file)
                pdf = fs.url(fileName)
                newReading = Reading(
                    subcategory=subcategory_obj, user=request.user, title=title, author=author, year=year, pdf=pdf, cover=cover)
                newReading.save()
                context['fileUrl'] = fs.url(fileName)
                return HttpResponseRedirect(reverse("subcategory", args=(category, subcategory)))

            readings = Reading.objects.all().filter(
                subcategory=subcategory_obj).order_by('-date')
            count = len(readings)
            context['items'] = readings
            context['count'] = count
            context['category_obj'] = category_obj
            context['subcategory_obj'] = subcategory_obj

            return render(request, "libraryapp/reading.html", context)

        #  Images gallery
        elif category_obj.name == 'Images gallery':
            context = {
                'category_obj': category_obj,
                'subcategory_obj': subcategory_obj,
            }
            if request.method == 'POST':
                uploaded_file = request.FILES['image']

                title = request.POST["title"]
                description = request.POST["description"]
                fs = FileSystemStorage()
                fileName = fs.save(uploaded_file.name, uploaded_file)
                image = fs.url(fileName)
                newImage = Image(
                    subcategory=subcategory_obj, user=request.user, title=title, image=image, description=description)
                newImage.save()
                context['fileUrl'] = image
                return HttpResponseRedirect(reverse("subcategory", args=(category, subcategory)))

            images = Image.objects.all().filter(subcategory=subcategory_obj).order_by('-date')

            pages = pagination(request, images, 9)
            context['items'] = pages[0]
            context['page_range'] = pages[1]

            return render(request, "libraryapp/gallery.html", context)

        #  Chat
        elif category_obj.name == 'Chat room':
            if request.method != "POST":

                post_list = Post.objects.all().filter(subcategory=subcategory).order_by('-date')
                pages = pagination(request, post_list, 10)

                context = {
                    'category_obj': category_obj,
                    'subcategory_obj': subcategory_obj,
                    'items': pages[0],
                    'page_range': pages[1],
                }
                return render(request, "libraryapp/chat.html", context)

            postText = request.POST["post"]
            try:
                uploaded_image = request.FILES['image_post']
            except KeyError:
                uploaded_image = None

            if postText is not None:
                if uploaded_image is not None:
                    fs = FileSystemStorage()
                    fileName = fs.save(uploaded_image.name, uploaded_image)
                    image_post = fs.url(fileName)
                else:
                    image_post = None

            newPost = Post(subcategory=subcategory_obj,
                           content=postText, user=request.user, image=image_post)
            newPost.save()
            return HttpResponseRedirect(reverse("subcategory", args=(category, subcategory)))

        return HttpResponseRedirect(reverse("category", args=(category,)))
    return HttpResponseRedirect(reverse("login"))


def reading(request, category, subcategory, reading_id):
    if request.user.is_authenticated:
        if request.method != "POST":
            try:
                category_obj = Category.objects.get(pk=category)
            except Category.DoesNotExist:
                return JsonResponse({
                    "error": f"Category does not exist."
                }, status=400)
            try:
                subcategory_obj = Subcategory.objects.get(pk=subcategory)
            except Subcategory.DoesNotExist:
                return JsonResponse({
                    "error": f"Subcategory does not exist."
                }, status=400)
            try:
                reading_obj = Reading.objects.get(pk=reading_id)
            except Reading.DoesNotExist:
                return JsonResponse({
                    "error": f"Reading does not exist."
                }, status=400)

            reviews = Review.objects.all().filter(reading=reading_obj).order_by('-date')
            pages = pagination(request, reviews, 10)

            context = {
                'category_obj': category_obj,
                'subcategory_obj': subcategory_obj,
                'reading_obj': reading_obj,
                'items': pages[0],
                'page_range': pages[1],
            }
            return render(request, "libraryapp/reading_details.html", context)

        reading_obj = Reading.objects.get(pk=reading_id)
        reviewText = request.POST["review"]
        try:
            uploaded_image = request.FILES['image_review']
        except KeyError:
            uploaded_image = None
        if reviewText is not None:
            if uploaded_image is not None:
                fs = FileSystemStorage()
                fileName = fs.save(uploaded_image.name, uploaded_image)
                image_post = fs.url(fileName)
            else:
                image_post = None
        newReview = Review(reading=reading_obj,
                           content=reviewText, user=request.user, image=image_post)
        newReview.save()
        return HttpResponseRedirect(reverse("reading", args=(category, subcategory, reading_id,)))

    return HttpResponseRedirect(reverse("login"))

#  API - like reading
@csrf_exempt
def bananaLike(request, category, subcategory, reading_id):

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    print('aqui estoy')
    try:
        reading_obj = Reading.objects.get(pk=reading_id)
    except Reading.DoesNotExist:
        return JsonResponse({"error": "Post doesn't exist."}, status=404)
    user = request.user
    if user in reading_obj.liked_readings.all():
        reading_obj.liked_readings.remove(user)
    else:
        reading_obj.liked_readings.add(user)
        reading_obj.save()
    return JsonResponse({"message": "Post deleted"}, status=201)


# API - delete reading
def delete_reading(request, category, subcategory, reading_id):
    if request.method == 'POST':
        try:
            reading = Reading.objects.get(pk=reading_id)
        except Reading.DoesNotExist:
            return JsonResponse({
                "error": f"Reading does not exist."
            }, status=400)
        reading.delete()
    return HttpResponseRedirect(reverse("subcategory", args=(category, subcategory,)))


#  API - edit post
@csrf_exempt
@login_required
def edit(request, post_id):

    if request.method == "PUT":

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post doesn't exist."}, status=404)

        data = json.loads(request.body)

        newBody = data.get("body")
        userId = data.get("userId")

        try:
            User.objects.get(pk=userId)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=400)

        if newBody is not None:
            post.content = data["body"]
            post.save()
            return HttpResponse(status=204)

    elif request.method == "DELETE":
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post doesn't exist."}, status=404)

        data = json.loads(request.body)
        userId = data.get("userId")

        try:
            User.objects.get(pk=userId)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=400)

        post.delete()
        return JsonResponse({"message": "Post deleted"}, status=201)

    return JsonResponse({"error": "PUT or DELETE request required."}, status=400)


#  API - edit review
@csrf_exempt
@login_required
def editReview(request, review_id):
    print('im here though')

    if request.method == "PUT":
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return JsonResponse({"error": "Review doesn't exist."}, status=404)

        data = json.loads(request.body)
        newBody = data.get("body")

        if newBody is not None:
            review.content = data["body"]
            review.save()
            return HttpResponse(status=204)

    elif request.method == "DELETE":
        print('im here though')
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return JsonResponse({"error": "Review doesn't exist."}, status=404)

        review.delete()
        return JsonResponse({"message": "Review deleted"}, status=201)

    return JsonResponse({"error": "PUT or DELETE request required."}, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "libraryapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "libraryapp/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        user_key = request.POST["key"]

        try:
            key = Key.objects.get(pk=1)
        except Category.DoesNotExist:
            return JsonResponse({
                "error": f"Category does not exist."
            }, status=400)

        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "libraryapp/register.html", {
                "message": "Passwords must match."
            })

        if user_key != key.key:
            return render(request, "libraryapp/register.html", {
                "message": "Incorrect key"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "libraryapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "libraryapp/register.html")
