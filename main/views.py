from django.shortcuts import render, redirect, get_object_or_404
from api.models import Brand, Category, Chicken, Comment

# Create your views here.
def list(request):
    brand_chickens = Brand.objects.all()
    categories = Category.objects.all()
    brands = []
    idx = 1
    for brand in brand_chickens:
        value = {
            'idx' : idx,
            'name' : brand.name,
            'chickens' : []
        }
        count = 0
        for chicken in brand.chicken_set.all():
            tags = chicken.hash_tag.split(',')
            for i in range(len(tags)):
                tags[i] = '#' + tags[i]
            chicken.tags = tags
            chicken.img_url = '/static/media/chickens/bhc/havanero_poteking_fride.png'
            value['chickens'].append(chicken)
            count += 1
            if count == 3:
                count = 0
                break
        brands.append(value)
        idx += 1
    return render(request, 'posts/list.html', {'brands': brands, 'categories': categories})

def search(request):
    brands = Brand.objects.all()
    categories = Category.objects.all()
    chickens = []
    sub_menu = 'brand'

    search_parameter = request.GET.get('search').strip()


    if search_parameter == '':
        return redirect('main:list')
    
    # brand = Brand.objects.filter(name=q).first()
    brand = Brand.objects.filter(name__icontains=search_parameter).first()
    if brand:
        for chicken in brand.chicken_set.all():
            tags = chicken.hash_tag.split(',')
            for i in range(len(tags)):
                tags[i] = '#' + tags[i]
            chicken.tags = tags
            chicken.brand_name = brand.name
            chickens.append(chicken)

        sub_menu = 'category'
    else:
        raw_chickens = Chicken.objects.filter(name__icontains=search_parameter)
        for chicken in raw_chickens:
            tags = chicken.hash_tag.split(',')
            for i in range(len(tags)):
                tags[i] = '#' + tags[i]
            chicken.tags = tags
            chicken.brand_name = chicken.brand.name
            chicken.category_name = chicken.category.name
            chickens.append(chicken)

    return render(request, 'posts/search.html',  {'search_parameter': search_parameter, 'sub_menu': sub_menu, 'brands': brands, 'chickens': chickens, 'categories': categories})

def detail(request, chicken_id):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    # 치킨 상세정보
    chicken = get_object_or_404(Chicken, id=chicken_id)
    tags = chicken.hash_tag.split(',')
    for i in range(len(tags)):
        tags[i] = '#' + tags[i]
    chicken.tags = tags
    chicken.img_url = '/static/media/chickens/bhc/havanero_poteking_fride.png'
    chicken.brand_name = chicken.brand.name
    chicken.category_name = chicken.category.name
    
    # 리뷰
    comments = Comment.objects.filter(chicken_id=chicken_id)

    # 같은 브랜드 다른 치킨
    brand_chickens = Chicken.objects.filter(brand_id=chicken.brand_id)

    return render(request, 'posts/detail.html', {'chicken': chicken, 'comments': comments, 'brand_chickens': brand_chickens, 'categories': categories, 'brands': brands})