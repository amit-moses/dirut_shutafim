from django.urls import path


from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/", views.search, name="search"),
    path("myads/", views.myads, name="myads"),
    path("apr/<int:apr_id>", views.single_page_view, name="single_page_view"),
    path("ad/<int:apr_id>", views.newadd, name="newadd"),
    path("ad/", views.newadd, name="newadd"),
    path("api/", views.api, name="api"),
]
