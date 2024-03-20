from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from drinks.models import Drink, Image, Episode

# Create your views here.
def drink_index(request):
    page_num = request.GET.get('page', 1)
    images = Image.objects.filter(recipe=True).distinct().order_by('drink__name')
    page = Paginator(object_list=images, per_page=6).get_page(page_num)

    return render(
        request=request,
        template_name='drink_index.html',
        context={
            'page': page
        }
    )

def drink_index_partial(request):
    if request.htmx:
        search = request.GET.get('q')
        sort = request.GET.get('sort')
        page_num = request.GET.get('page', 1)

        if sort == 'alpha-asc':
            if search:
                images = Image.objects.filter((Q(drink__name__icontains=search) | Q(drink__ingredients__name__icontains=search)) & Q(recipe=True)).distinct().order_by('drink__name')
            else:
                images = Image.objects.filter(recipe=True).order_by('drink__name')
        elif sort == 'alpha-desc':
            if search:
                images = Image.objects.filter((Q(drink__name__icontains=search) | Q(drink__ingredients__name__icontains=search)) & Q(recipe=True)).distinct().order_by('-drink__name')
            else:
                images = Image.objects.filter(recipe=True).order_by('-drink__name')
        elif sort == 'chron-asc':
            if search:
                episodes = Episode.objects.filter((Q(drink__name__icontains=search) | Q(drink__ingredients__name__icontains=search))).order_by('number')
            else:
                episodes = Episode.objects.all().order_by('number')
            drinks = []
            for episode in episodes:
                if episode.drink not in drinks:
                    drinks.append(episode.drink)
            images = []
            for drink in drinks:
                images.append(drink.image_set.get(recipe=True))
        elif sort == 'chron-desc':
            if search:
                episodes = Episode.objects.filter((Q(drink__name__icontains=search) | Q(drink__ingredients__name__icontains=search))).order_by('-number')
            else:
                episodes = Episode.objects.all().order_by('-number')
            drinks = []
            for episode in episodes:
                if episode.drink not in drinks:
                    drinks.append(episode.drink)
            images = []
            for drink in drinks:
                images.append(drink.image_set.get(recipe=True))
        else:
            images = Image.objects.filter(recipe=True).order_by('drink__name')
        
        page = Paginator(object_list=images, per_page=6).get_page(page_num)

        return render(
            request=request,
            template_name='drink_index_partial.html',
            context={
                'page': page
            }
        )

def drink_detail(request, slug):
    drink = Drink.objects.get(slug=slug)
    recipe_image = Image.objects.filter(drink=drink, recipe=True)[0]
    non_recipe_images = Image.objects.filter(drink=drink, recipe=False)
    episodes = Episode.objects.filter(drink=drink)
    context = {
        "drink": drink,
        "recipe_image": recipe_image,
        "non_recipe_images": non_recipe_images,
        "episodes": episodes,
    }
    return render(request, "drink_detail.html", context)