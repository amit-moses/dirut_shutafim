from django.urls import path


from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("search/", views.search, name="search"),
    path("myads/", views.myads, name="myads"),
    path("apr/", views.single_page_view, name="single_page_view"),
    path("apr/<int:apr_id>", views.single_page_view, name="single_page_view"),
    path("ad/<int:apr_id>", views.newadd, name="newadd"),
    path("ad/", views.newadd, name="newadd"),
    path("api/delete/", views.delete_apr, name="delete_apr"),
    path("api/delete/<int:apr_id>", views.delete_apr, name="delete_apr"),
    path("api/", views.api, name="api"),
    path("api/<int:apr_id>", views.api, name="api"),

    path("rest_password/", auth_views.PasswordResetView.as_view(), name='reset_password'),
    path("rest_password_sent/", auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    path("rest/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("rest_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
]
