from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),

    path('event/',views.event, name='event'),

    path('event/<str:id>',views.join_event_Y,name='join-event'),
    path('event/details/<str:id>',views.view_event,name='view-event'),
    path('event/complete/<str:id>',views.complete_event,name='complete-event'),

    path('feedback/<int:id>',views.feedback,name='feedback'),
    path('my_view/<int:by>/<int:to>', views.my_view, name='my_view'),

    path('clear_notifications/<int:of_whom>', views.clear_notifications, name='clear_notifications'),
    path('feedback2/<int:notification_id>', views.feedback2, name='feedback2'),
    path('preferences', views.set_preferences, name='set_preferences')

]