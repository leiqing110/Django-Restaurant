"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from APP01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/',views.login),
    url(r'^user_list/',views.user_list),
    url(r'^add_user/',views.add_user),
url(r'^delete_user/',views.delete_user),
url(r'^test/',views.test),
url(r'^edit_user/',views.edit_user),
url(r'^publisher_user/',views.publisher_list),
url(r'^book_list/',views.book_list),
url(r'^add_book/',views.add_book),
#url(r'^add_book/',views.Addbook.as_view()),
url(r'^delete_book/',views.delete_book),
url(r'^edit_book/',views.edit_book),
url(r'^movie_list/',views.movie_list),
url(r'^delete_movie/',views.delete_movie),
url(r'^add_movie/',views.add_movie),
url(r'^edit_movie/',views.edit_movie),
url(r'^goods_list/',views.goods_list),
url(r'^add_goods/',views.add_goods),
url(r'^delete_goods/',views.delete_goods),
url(r'^edit_goods/',views.edit_goods),
url(r'^huiyuan_list/',views.huiyuan_list),
url(r'^delete_huiyuan/',views.delete_huiyuan),
url(r'^edit_huiyuan/',views.edit_huiyuan),
url(r'^add_huiyuan/',views.add_huiyuan),
url(r'^upload/',views.upload),
url(r'^search/',views.search),
url(r'^search_huiyuan/',views.search_huiyuan),
url(r'^add_cart/',views.add_cart),
url(r'^search_good/',views.search_good),
url(r'^logout/',views.logout),
url(r'^cart/',views.cart),
url(r'^add_cart2/',views.add_cart2),
url(r'^add_cart/',views.add_cart),
url(r'^delete_cart/',views.delete_cart),
url(r'^count',views.count),
url(r'^settle_accounts',views.settle_accounts),
url(r'^order',views.order),
url(r'^refund',views.refund),
]
