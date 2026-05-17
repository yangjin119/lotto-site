# config/urls.py
from django.contrib import admin
from django.urls import path, include  # include가 반드시 있어야 합니다!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lotto.urls')),   # 이 줄이 있어야 buy/ 주소를 인식합니다!
]