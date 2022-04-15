from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from .models import User
import re

# Create your views here.
def signIn(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return JsonResponse({'valid': True})
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if not user:
            return JsonResponse({'valid': False})
        login(request, user)
        return JsonResponse({'valid': True})
    return render(request, 'accounts/signIn.html')

def signUp(request):
    if request.method == "POST":
        result = check_info(request.POST, 'signup')
        if result['valid']:
            user = User()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.nickname = request.POST.get('nickname')
            user.phoneNum = request.POST.get('phoneNum')
            user.save()
        return JsonResponse(result)
    return render(request, 'accounts/signUp.html')


def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def update(request):
    if request.method == 'POST':
        result = check_info(request.POST, 'update')
        user = User.objects.filter(username=request.user.username).first()
        if result['valid']:
            user.set_password(request.POST.get('password1'))
            user.nickname = request.POST.get('nickname')
            user.phoneNum = request.POST.get('phoneNum')
            user.save()
            login(request, user)
        return JsonResponse(result)
    return render(request, 'accounts/update.html', {'user': request.user})

def signOut(request):
    logout(request)
    return redirect('accounts:signIn')

def check_info(data, method):
    if method == 'signup' and 'username' in data.keys():
        username = data.get('username')
        if User.objects.filter(username=username).count() > 0 and len(username) > 0:
            return {'valid': False, 'message': '이미 존재하는 아이디입니다.'}
        else:
            if not re.search('^(?=.*?[a-z0-9_])[a-z0-9_]{5,20}$', username):
                return {'valid': False, 'message': '5~20자의 영문 소문자, 숫자, 특수기호(_)만 사용 가능합니다.'}
            return {'valid': True}
    if 'password1' in data.keys():
        password1 = data.get('password1')
        if not re.search("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&_]{8,16}$", password1):
            return {'valid': False, 'message': '8~16자의 영문 대/소문자, 숫자, 특수기호를 사용하세요.'}
    if 'password2' in data.keys():
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            return {'valid': False, 'message': '비밀번호가 일치하지 않습니다.'}
    if method == 'signup' and 'firstName' in data.keys():
        first_name = data.get('firstName')
        if not re.search('^[가-힣A-Za-z]+$', first_name):
            return {'valid': False, 'message': '한글과 영어 대/소문자를 사용하세요. (특수기호, 공백 사용 불가)'}
    if 'nickname' in data.keys():
        nickname = data.get('nickname')
        if not re.search("^(?=.*[A-Za-z가-힣0-9])[A-Za-z가-힣0-9]{4,10}$", nickname):
            return {'valid': False, 'message': '4~10자의 한글, 영문 대/소문자, 숫자를 사용하세요.'}
    if 'phoneNum' in data.keys():
        phoneNum = data.get('phoneNum')
        if not re.search("^[0-9]", phoneNum):
            return {'valid': False, 'message': '형식에 맞지 않는 번호입니다.'}
        
    return {'valid': True}


@require_POST
def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username=username).count() > 0 and len(username) > 0:
        return JsonResponse({'valid': False, 'message': '이미 존재하는 아이디입니다.'})
    return JsonResponse({'valid': True})

@require_POST
def check_nickname(request):
    nickname = request.POST.get('nickname')
    if User.objects.filter(nickname=nickname).count() > 0 and len(nickname) > 0:
        return JsonResponse({'valid': False, 'message': '4~10자의 한글, 영문 대/소문자, 숫자를 사용하세요.'})
    return JsonResponse({'valid': True})

@require_POST
def check_user_info(request):
    if 'username' in request.POST.keys():
        username = request.POST.get('username')
        if User.objects.filter(username=username).count() > 0 and len(username) > 0:
            return JsonResponse({'valid': False, 'message': '이미 존재하는 아이디입니다.'})
        else:
            if not re.search('^(?=.*?[a-z0-9_])[a-z0-9_]{5,20}$', username):
                return JsonResponse({'valid': False, 'message': '5~20자의 영문 소문자, 숫자, 특수기호(_)만 사용 가능합니다.'})
            return JsonResponse({'valid': True})
    if 'password1' in request.POST.keys():
        password1 = request.POST.get('password1')
        if not re.search("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&_]{8,16}$", password1):
            return JsonResponse({'valid': False, 'message': '8~16자의 영문 대/소문자, 숫자, 특수기호를 사용하세요.'})
    if 'password2' in request.POST.keys():
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return JsonResponse({'valid': False, 'message': '비밀번호가 일치하지 않습니다.'})
    if 'firstName' in request.POST.keys():
        first_name = request.POST.get('firstName')
        if not re.search('^[가-힣A-Za-z]+$', first_name):
            return JsonResponse({'valid': False, 'message': '한글과 영어 대/소문자를 사용하세요. (특수기호, 공백 사용 불가)'})
    if 'nickname' in request.POST.keys():
        nickname = request.POST.get('nickname')
        if not re.search("^(?=.*[A-Za-z가-힣0-9])[A-Za-z가-힣0-9]{4,10}$", nickname):
            return JsonResponse({'valid': False, 'message': '4~10자의 한글, 영문 대/소문자, 숫자를 사용하세요.'})
    if 'phoneNum' in request.POST.keys():
        phoneNum = request.POST.get('phoneNum')
        if not re.search("^[0-9]", phoneNum):
            return JsonResponse({'valid': False, 'message': '형식에 맞지 않는 번호입니다.'})
        
    return JsonResponse({'ret': True})

@require_POST
def confirm_authenticate(request):
    if request.user.is_authenticated:
        return JsonResponse({'valid': True})
    return JsonResponse({'valid': False})