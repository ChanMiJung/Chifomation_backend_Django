from django.shortcuts import render

# Create your views here.
def signIn(request):
    return render(request, 'accounts/signIn.html')

def signUp(request):
    return render(request, 'accounts/userInfo.html')

def profile(request):
    return render(request, 'accounts/profile.html')