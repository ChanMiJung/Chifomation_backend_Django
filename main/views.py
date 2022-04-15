from types import new_class
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from api.models import Brand, Category, Chicken, Comment
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, Page
from django.template.loader import render_to_string

# Create your views here.
def list(request):
    brand_chickens = Brand.objects.all()
    categories = Category.objects.all()
    brands = []
    idx = 1
    new_chickens = []
    new_count = 0
    # popularity_chickens = []
    popularity_count = 0
    for brand in brand_chickens:
        value = {
            'idx' : idx,
            'name' : brand.name,
            'chickens' : []
        }
        for chicken in brand.chicken_set.all():
            if chicken.hash_tag:
                tags = chicken.hash_tag.split(',')
                
                for i in range(len(tags)):
                    tags[i] = '#' + tags[i]
                chicken.tags = tags
            
            
            if len(new_chickens) < 3 and chicken.new:
                new_chickens.append(chicken)
                new_count += 1
            if len(value['chickens']) < 3 and chicken.popularity:
                value['chickens'].append(chicken)
                # popularity_chickens.append(chicken)
                popularity_count += 1
            if new_count == 3 and popularity_count == 3:
                new_count = 0
                popularity_count = 0
                break
            
        brands.append(value)
        idx += 1

    # 회원님들의 리뷰
    comments = Comment.objects.all()
    if len(comments) > 10:
        comments = comments[-10:]

    return render(request, 'posts/list.html', {'brands': brands, 'categories': categories, 'new_chickens': new_chickens, 'comments': comments, 'star_range': range(1, 6)})

def search(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    chickens = []
    sub_menu = request.GET.get('sub_menu', 'brand')

    search_parameter = request.GET.get('search').strip()
    category = request.GET.get('category')
    if search_parameter == '':
        return redirect('main:list')
    page = int(request.GET.get('page', 1))
    # brand = Brand.objects.filter(name=q).first()
    
    brand = Brand.objects.filter(name__icontains=search_parameter).first()
    if brand or sub_menu == 'category':
        for chicken in brand.chicken_set.all():
            if (category and category == chicken.category.name) or not category:
                tags = chicken.hash_tag.split(',')
                for i in range(len(tags)):
                    tags[i] = '#' + tags[i]
                chicken.tags = tags
                chicken.brand_name = brand.name
                chickens.append(chicken)

        sub_menu = 'category'
        paginator = Paginator(chickens, 5)
    else:
        raw_chickens = Chicken.objects.filter(name__icontains=search_parameter)
        for chicken in raw_chickens:
            if (category and category == chicken.category.name) or not category:
                tags = chicken.hash_tag.split(',')
                for i in range(len(tags)):
                    tags[i] = '#' + tags[i]
                chicken.tags = tags
                chicken.brand_name = chicken.brand.name
                chicken.category_name = chicken.category.name
                chickens.append(chicken)
        paginator = Paginator(chickens, 5)
    
    try:
        page_chickens = paginator.page(page)
    except EmptyPage:
        page_chickens = Page([], page, paginator)
    
    if request.is_ajax():
        content = ''
        for chicken in page_chickens:
            content += render_to_string('posts/chicken-item.html', {'chicken': chicken}, request=request)
        return JsonResponse({"content": content, "end_pagination": True if page >= paginator.num_pages else False, 'search_parameter': search_parameter})
    
    return render(request, 'posts/search.html',  {'search_parameter': search_parameter, 'sub_menu': sub_menu, 'brands': brands, 'chickens': page_chickens, 'categories': categories, "end_pagination": True if page >= paginator.num_pages else False,})

def detail(request, chicken_id):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    # 치킨 상세정보
    chicken = get_object_or_404(Chicken, id=chicken_id)
    if chicken.hash_tag:
        tags = chicken.hash_tag.split(',')
        for i in range(len(tags)):
            tags[i] = '#' + tags[i]
        chicken.tags = tags
    chicken.average_score = float(chicken.score)
    chicken.img_url = '/static/media/chickens/bhc/havanero_poteking_fride.png'
    chicken.brand_name = chicken.brand.name
    chicken.category_name = chicken.category.name
    
    # 리뷰
    page = int(request.GET.get('page', 1))
    comments = Comment.objects.filter(chicken_id=chicken_id).order_by('-id')
    paginator = Paginator(comments, 5)
    page_comments = paginator.get_page(page)

    if request.is_ajax():
        content = ''
        for comment in page_comments:
            content += render_to_string('posts/comment-item.html', {'comment': comment, 'star_range': range(1, 6)}, request=request)
        return JsonResponse({"content": content, 'end_pagination': True if page >= paginator.num_pages else False,})
    
    

    # 같은 브랜드 다른 치킨
    brand_chickens = Chicken.objects.filter(brand_id=chicken.brand_id)

    return render(request, 'posts/detail.html', {'user': request.user, 'chicken': chicken, 'comments': page_comments, 'brand_chickens': brand_chickens, 'categories': categories, 'brands': brands, 'star_range': range(1, 6), 'end_pagination': True if page >= paginator.num_pages else False,})

@require_POST
def enroll_comment(request):
    
    comment = Comment()
    comment.content = request.POST.get('comment').strip()
    comment.star = float(request.POST.get('score'))
    comment.user_id = request.user.id
    comment.chicken_id = request.POST.get('chicken_id')
    comment.save()

    chicken = get_object_or_404(Chicken, id=comment.chicken_id)
    comments = Comment.objects.filter(chicken_id=request.POST.get('chicken_id'))
    comment_sum = Comment.objects.filter(chicken_id=request.POST.get('chicken_id')).aggregate(Sum('star'))
    if comments:
        chicken.score = round((comment_sum['star__sum']/comments.count()),1)
        chicken.save()
    return JsonResponse({'valid': True})

@require_POST
def get_comments(request):
    
    comments = Comment.objects.filter(chicken_id=request.POST.get('chicken_id')).order_by('-id')
    print(comments)
    if comments:
        return JsonResponse({'valid': True, 'comments': comments})
    else:
        return JsonResponse({'valid': True, 'comments': []})