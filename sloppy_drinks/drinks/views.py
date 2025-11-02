import logging
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q, Prefetch, Min, Count, Subquery
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from drinks.forms import CustomLoginForm
from drinks.models import Drink, Ingredient, Image, Episode, FavoriteDrink
from .forms import CustomUserCreationForm

# Initialize logger for this module
logger = logging.getLogger(__name__)

def drink_index(request):
    try:
        drinks = Drink.objects.all().prefetch_related(
            Prefetch('episode_set', queryset=Episode.objects.all(), to_attr="episode_number"), 
            Prefetch('image_set', Image.objects.filter(recipe=True), to_attr="recipe_image")
        ).annotate(episode_number=Min('episode__number')).order_by('name')
        
        filter_ingredients = Ingredient.objects.filter(filter=True).order_by('name')
        
        # Handle pagination with error checking
        try:
            page_num = int(request.GET.get('page', 1))
            if page_num < 1:
                page_num = 1
        except (ValueError, TypeError):
            page_num = 1
            logger.warning(f'Invalid page number in request: {request.GET.get("page")}')
        
        paginator = Paginator(object_list=drinks, per_page=15)
        page = paginator.get_page(page_num)
        
        # Add favorite status for authenticated users after pagination
        if request.user.is_authenticated:
            favorite_drink_names = set(
                FavoriteDrink.objects.filter(user=request.user)
                .values_list('drink__name', flat=True)
            )
            # Annotate each drink in the page with favorite status
            for drink in page.object_list:
                drink.is_favorited = drink.name in favorite_drink_names
        else:
            # Set is_favorited to False for non-authenticated users
            for drink in page.object_list:
                drink.is_favorited = False
        
        return render(
            request=request,
            template_name='drink_index.html',
            context={
                'page': page,
                'filter_ingredients': filter_ingredients,
            }
        )
    except Exception as e:
        logger.error(f'Error in drink_index view: {e}', exc_info=True)
        messages.error(request, 'An error occurred loading the drink index.')
        # Return minimal context if error occurs
        return render(
            request=request,
            template_name='drink_index.html',
            context={'page': [], 'filter_ingredients': []}
        )

def drink_index_partial(request):
    try:
        # Get and sanitize search input
        search = request.GET.get('q', '').strip()
        if search and len(search) > 200:
            logger.warning(f'Search query too long: {len(search)} characters')
            search = ''
            messages.warning(request, 'Search query too long')
        
        # Validate and sanitize sort parameter
        sort = request.GET.get('sort', 'name')
        allowed_sorts = ['name', '-name', 'episode_number', '-episode_number']
        if sort not in allowed_sorts:
            logger.warning(f'Invalid sort parameter: {sort}')
            sort = 'name'
        
        # Get and validate filter parameter
        filter_param = request.GET.get('filter')
        if filter_param:
            filter_values = [f.strip() for f in filter_param.split(",") if f.strip()]
            # Verify filter values exist in database
            if filter_values:
                valid_ingredients = set(Ingredient.objects.filter(
                    name__in=filter_values, 
                    filter=True
                ).values_list('name', flat=True))
                if len(valid_ingredients) != len(filter_values):
                    invalid = set(filter_values) - valid_ingredients
                    logger.warning(f'Invalid filter ingredients: {invalid}')
                filter_values = list(valid_ingredients)
        else:
            filter_values = []
        
        # Get and validate favorites parameter
        favorites_param = request.GET.get('favorites', '').strip()
        favorites_filter = favorites_param.lower() in ('true', '1', 'on', 'yes')
        
        # If favorites is checked but user is not authenticated, redirect to login
        if favorites_filter and not request.user.is_authenticated:
            # Check if this is an HTMX request
            if request.headers.get('HX-Request'):
                # For HTMX requests, return a redirect response
                from django.http import HttpResponse
                response = HttpResponse()
                response['HX-Redirect'] = reverse('login')
                return response
            else:
                return redirect('login')
        
        # Handle pagination with error checking
        try:
            page_num = int(request.GET.get('page', 1))
            if page_num < 1:
                page_num = 1
        except (ValueError, TypeError):
            page_num = 1
            logger.warning(f'Invalid page number in request: {request.GET.get("page")}')
        
        # Build queries with proper error handling
        drinks = Drink.objects.all()
        
        # Apply favorites filter if checked and user is authenticated
        if favorites_filter and request.user.is_authenticated:
            favorite_drink_names = FavoriteDrink.objects.filter(
                user=request.user
            ).values_list('drink__name', flat=True)
            drinks = drinks.filter(name__in=favorite_drink_names)
        
        if filter_values:
            ingredients_filter_subquery = Drink.objects.filter(
                ingredients__name__in=filter_values
            ).annotate(num_filter_ingredients=Count('name')).filter(
                num_filter_ingredients=len(filter_values)
            ).values('name')
        
        if search:
            search_filter_subquery = Drink.objects.filter(
                Q(name__icontains=search) | Q(ingredients__name__icontains=search)
            ).values('name')
        
        # Apply ingredient filter if specified
        if filter_values:
            drinks = drinks.filter(name__in=Subquery(ingredients_filter_subquery))
        
        # Apply search filter if specified
        if search:
            drinks = drinks.filter(name__in=Subquery(search_filter_subquery))
        
        drinks = drinks.prefetch_related(
            Prefetch('episode_set', queryset=Episode.objects.all(), to_attr="episode_number"), 
            Prefetch('image_set', Image.objects.filter(recipe=True), to_attr="recipe_image")
        ).annotate(episode_number=Min('episode__number')).order_by(sort)
            
        paginator = Paginator(object_list=drinks, per_page=15)
        page = paginator.get_page(page_num)
        
        # Add favorite status for authenticated users after pagination
        if request.user.is_authenticated:
            favorite_drink_names = set(
                FavoriteDrink.objects.filter(user=request.user)
                .values_list('drink__name', flat=True)
            )
            # Annotate each drink in the page with favorite status
            for drink in page.object_list:
                drink.is_favorited = drink.name in favorite_drink_names
        else:
            # Set is_favorited to False for non-authenticated users
            for drink in page.object_list:
                drink.is_favorited = False
        
        filter_ingredients = Ingredient.objects.filter(filter=True).order_by('name')

        return render(
            request=request,
            template_name='drink_index_partial.html',
            context={
                'page': page,
                'filter_ingredients': filter_ingredients,
            }
        )
    except Exception as e:
        logger.error(f'Error in drink_index_partial view: {e}', exc_info=True)
        # Check if this is an HTMX request
        if request.headers.get('HX-Request'):
            # Return error message for HTMX
            return render(
                request=request,
                template_name='errors/htmx_error.html',
                context={'error_message': 'An error occurred loading drinks. Please try again.'},
                status=500
            )
        else:
            messages.error(request, 'An error occurred loading drinks.')
            return redirect('drink_index')

def drink_detail(request, slug):
    try:
        logger.info(f'Drink detail view accessed for slug: {slug}')
        
        drink = get_object_or_404(
            Drink.objects.prefetch_related('episode_set', 'image_set'), 
            slug=slug
        )
        
        # Handle recipe image with error checking
        try:
            recipe_image = drink.image_set.get(recipe=True)
        except Image.DoesNotExist:
            logger.warning(f'Drink {slug} has no recipe image')
            recipe_image = None
            messages.warning(request, 'Recipe image not available for this drink.')
        except MultipleObjectsReturned:
            logger.warning(f'Drink {slug} has multiple recipe images')
            recipe_image = drink.image_set.filter(recipe=True).first()
            messages.warning(request, 'Multiple recipe images found. Showing the first one.')
        
        non_recipe_images = drink.image_set.filter(recipe=False).order_by('filename')
        episodes = drink.episode_set.all().order_by('number')
        
        # Add favorite status for authenticated users
        if request.user.is_authenticated:
            drink.is_favorited = FavoriteDrink.objects.filter(user=request.user, drink=drink).exists()
        else:
            drink.is_favorited = False
        
        # Handle similar drinks calculation with error checking
        try:
            similar_drinks = drink.get_similar_drinks().prefetch_related(
                Prefetch('image_set', Image.objects.filter(recipe=True), to_attr="recipe_image")
            )
        except Exception as e:
            logger.error(f'Error calculating similar drinks for {slug}: {e}')
            similar_drinks = []

        context = {
            "drink": drink,
            "recipe_image": recipe_image,
            "non_recipe_images": non_recipe_images,
            "episodes": episodes,
            "similar_drinks": similar_drinks,
        }
        return render(request, "drink_detail.html", context)
    except Exception as e:
        logger.error(f'Error in drink_detail view for slug {slug}: {e}', exc_info=True)
        messages.error(request, 'An error occurred loading this drink.')
        return redirect('drink_index')

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('drink_index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect(reverse('drink_index'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('drink_index')
        return super().dispatch(request, *args, **kwargs)

# Custom error handlers
def custom_404(request, exception):
    """Custom 404 error handler"""
    logger.warning(f'404 error: {request.path} - {exception}')
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    """Custom 500 error handler"""
    logger.error('500 error occurred', exc_info=True)
    return render(request, 'errors/500.html', status=500)

def toggle_favorite_drink(request, slug):
    """Toggle favorite status for a drink"""
    if not request.user.is_authenticated:
        return render(request, 'errors/404.html', status=404)
    
    try:
        drink = get_object_or_404(Drink, slug=slug)
        is_favorited = FavoriteDrink.toggle_favorite_drink(request.user, drink)
        favorite_count = request.user.favoritedrink_set.count()
        
        return render(request, 'heart_icon_partial.html', {
            'is_favorited': is_favorited,
            'favorite_count': favorite_count
        })
    except Exception as e:
        logger.error(f'Error toggling favorite for slug {slug}: {e}', exc_info=True)
        return render(request, 'errors/500.html', status=500)