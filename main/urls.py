from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('admin', admin.site.urls),
    path("register", views.register, name="register"),
    path("logout", views.logout_request, name="logout_request"),
    path("login", views.login_request, name="login_request"),
    path("story/<str:id>", views.story_view, name="story_view"),
    path("phone_story/<str:id>", views.phone_story, name="story_view"),
    path("pass_on/<str:href>", views.pass_on, name="pass_on"),
    path("edit_story/<str:id>", views.edit_story, name="edit_story"),
    path("profile/<str:id>", views.profile_view, name="profile_view"),
    path("category/<str:category>", views.category_view, name="category_view"),
    path("writer", views.writer_view, name="writer_view"),
    path("editor in chief", views.supervisor_view, name="supervisor_view"),
    path("editor", views.editor_view, name="editor_view"),
    path("new_draft", views.new_draft, name="new_draft"),
    path("search", views.search, name="search"),
    path("change_state/<str:id>/<str:new_state>/<str:redirect_page>", views.change_state, name="change_state"),
    path("change_group/<str:id>/<str:new_group>/<str:redirect_page>", views.change_group, name="change_group"),
    path("remove_group/<str:id>/<str:redirect_page>", views.remove_group, name="change_group")
]