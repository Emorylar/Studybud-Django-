#URL for route directories

from django.contrib import admin
from django.urls import path, include  #6. include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))     #6. to call base.urls at default empty string
]
