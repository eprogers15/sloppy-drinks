from django.db.models import Q, Prefetch, Min
from django.core.paginator import Paginator
from django.shortcuts import render
from drinks.models import Drink, Image, Episode

def drink_index(request):
    drinks = Drink.objects.all().prefetch_related(Prefetch('episode_set', queryset=Episode.objects.all(), to_attr="episode_number"), Prefetch('image_set', Image.objects.filter(recipe=True), to_attr="image_filename")).annotate(episode_number=Min('episode__number'), image_filename=Min('image__filename')).order_by('name')
    page_num = request.GET.get('page', 1)
    page = Paginator(object_list=drinks, per_page=15).get_page(page_num)

    return render(
        request=request,
        template_name='drink_index.html',
        context={
            'page': page
        }
    )

def drink_index_partial(request):
    search = request.GET.get('q')
    sort = request.GET.get('sort')
    page_num = request.GET.get('page', 1)

    if search:
        drinks = Drink.objects.filter(Q(name__icontains=search) | Q(ingredients__name__icontains=search)).prefetch_related(Prefetch('episode_set', queryset=Episode.objects.all(), to_attr="episode_number"), Prefetch('image_set', Image.objects.filter(recipe=True), to_attr="image_filename")).annotate(episode_number=Min('episode__number'), image_filename=Min('image__filename')).order_by(sort)
    else:
        drinks = Drink.objects.all().prefetch_related(Prefetch('episode_set', queryset=Episode.objects.all(), to_attr="episode_number"), Prefetch('image_set', Image.objects.filter(recipe=True), to_attr="image_filename")).annotate(episode_number=Min('episode__number'), image_filename=Min('image__filename')).order_by(sort)
        
    page = Paginator(object_list=drinks, per_page=15).get_page(page_num)

    return render(
        request=request,
        template_name='drink_index_partial.html',
        context={
            'page': page
        }
    )

def drink_detail(request, slug):
    drink = Drink.objects.prefetch_related('episode_set', 'image_set').get(slug=slug)
    recipe_image = drink.image_set.filter(recipe=True)[0]
    non_recipe_images = drink.image_set.filter(recipe=False).order_by('filename')
    episodes = drink.episode_set.all().order_by('number')
    similar_drinks = Image.objects.filter(drink__in=drink.get_similar_drinks())
    context = {
        "drink": drink,
        "recipe_image": recipe_image,
        "non_recipe_images": non_recipe_images,
        "episodes": episodes,
        "similar_drinks": similar_drinks,
    }
    return render(request, "drink_detail.html", context)