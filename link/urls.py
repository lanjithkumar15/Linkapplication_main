from django.urls import path
from . import views
from django.conf.urls import handler404, handler500

urlpatterns = [
    
    path('homepage/', views.homepage, name='homepage'),
    path('add/', views.add_application, name='add_application'),
    path('edit/<int:pk>/', views.edit_application, name='edit_application'),

    path('delete/<int:pk>/confirm/', views.delete_application_confirm, name='delete_application_confirm'),
    path('delete/<int:pk>/', views.delete_application, name='delete_application'),

    path('createsection/', views.create_section, name='createsection'),
    path('assignsections/', views.assign_sections, name='assign_sections'),
    path('delete_section/', views.delete_section, name='delete_section'),

    path('login/',views.login,name="login"),
    path('login_view/',views.login_view,name="login_view"),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    
]

handler404 = 'link.views.custom_404'
# handler500 = 'link.views.custom_500'