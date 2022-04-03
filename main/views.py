from django.shortcuts import render, redirect
from api.models import Brand, Category, Chicken

# Create your views here.
def list(request):
    brand_chickens = Brand.objects.all()
    brands = []
    idx = 1
    for brand in brand_chickens:
        value = {
            'idx' : idx,
            'brand' : brand.name,
            'chickens' : []
        }
        count = 0
        for chicken in brand.chicken_set.all():
            tags = chicken.hash_tag.split(',')
            for i in range(len(tags)):
                tags[i] = '#' + tags[i]
            chicken.tags = tags
            chicken.img_url = 'media/chickens/bhc/havanero_poteking_fride.png'
            value['chickens'].append(chicken)
            count += 1
            if count == 3:
                count = 0
                break
        brands.append(value)
        idx += 1
    return render(request, 'posts/list.html', {'brands': brands})

def search(request):
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
        data = Category.objects.all()
    else:
        raw_chickens = Chicken.objects.filter(name__icontains=search_parameter)
        for chicken in raw_chickens:
            tags = chicken.hash_tag.split(',')
            for i in range(len(tags)):
                tags[i] = '#' + tags[i]
            chicken.tags = tags
            chicken.brand_name = chicken.brand.name
            chickens.append(chicken)

        data = Brand.objects.all()

    return render(request, 'posts/search.html',  {'search_parameter': search_parameter, 'sub_menu': sub_menu, 'sub_menu_data': data, 'chickens': chickens})
