from django.urls import path
from blogapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.home),
    path('register',views.registration),
    path('login/',views.ulogin),
    path('logout/',views.ulogout),
    path('createblog/',views.createblog),
    path('detailedblog/',views.detailedblog),
    path('myblogs/',views.myblogs),
    path('delete/<bid>',views.deletepost),
    path('detailblog/<bid>',views.detailedblog),
    path('edit/<bid>',views.editblog),
    path('bdetailfromhome/<bid>',views.bdetailshome),
    path('like/<bid>',views.like),
    path('category/<cat>',views.fetchCategory),
    path('comment/<bid>',views.handleComment),
    path('about',views.about),
    path('account',views.account),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
