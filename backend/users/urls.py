from django.urls import include, path

urlpatterns = [
    path(r'', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken'))

]
