from django.urls import path
from . import views

urlpatterns = [
	path('', views.dashboard),
	path('home', views.Home.as_view()),
	path('channel-monitoring', views.channel_monitoring),
	path('delete', views.delete_keyword),
	path('update', views.update_keyword),
	path('blah', views.blah)
]
