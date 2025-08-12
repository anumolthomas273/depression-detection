"""stress_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.first),
    path('index',views.index),
    path('reg/addreg',views.addreg),
    path('reg/',views.reg),
    path('logint',views.logint,name='logint'),
    path('login/logint',views.logint,name='logint'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout),
    path('logout',views.logout),
    path('dash',views.dash),
    path('addremedys',views.addremedys),
    path('rem',views.rem),
    path('addmusic',views.addmusic),
    path('addvideo',views.addvideo),
    path('userview',views.userview),
    path('userprescribe',views.userprescribe),
    path('startwebcam',views.startwebcam),
    path('faq',views.faq),
    path('livevoice',views.livevoice),
    path('predict',views.predict),
    
    #path('addconsult',views.addconsult),
    #path('text_emotion',views.text_emotion),
    path('adddoctor',views.adddoctor),
    path('viewresults',views.viewresults),
    path('viewuserdoctor',views.viewuserdoctor),
    path('viewuser',views.viewuser),
    path('viewstress',views.viewstress),
    path('update/<int:id>',views.update,name="update"),
    path('update/update',views.addup,name="addup"),
    path('viewuserconsult',views.viewuserconsult),
    path('forget',views.forget),
    path('forgetpassword',views.forgetpassword),
    path('consult1/<int:id>',views.consult1,name='consult1'),
    path('aproveuser/<int:id>',views.aproveuser,name='aproveuser'),
    path('rejectuserrr/<int:id>',views.rejectuserrr,name='rejectuserrr'),
    path('admin/', admin.site.urls),
    path('addd',views.addd),
    path('data_submit',views.data_submit),
    
    path('dtt/<int:id>',views.dtt,name='dtt'),
    path('dtt/dconsult',views.dconsult,name='dconsult'),
    path('consult1/<int:id>',views.consult1,name='consult1'),
    path('consult1/addconsult',views.addconsult,name='addconsult'),
    path('viewremedies',views.viewremedies),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
