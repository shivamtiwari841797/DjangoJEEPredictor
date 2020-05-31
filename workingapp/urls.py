from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('result',views.result,name='result'),
	path('plot',views.plot,name='plot'),
	path('plotalt',views.plotalt,name='plotalt')

]