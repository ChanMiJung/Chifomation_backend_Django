from django.shortcuts import render
from api.models import Brand

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
            chicken.img_url = '/media/chickens/bhc/havanero_poteking_fride.png'
            value['chickens'].append(chicken)
            count += 1
            if count == 3:
                count = 0
                break
        brands.append(value)
        idx += 1
    return render(request, 'posts/list.html', {'brands': brands})