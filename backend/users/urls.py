from django.urls import include, path

urlpatterns = [
    path(r'', include('djoser.urls')),
    path('/signin'),
    path('/signup')

]
