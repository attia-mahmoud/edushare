from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("postmodal/<int:post_id>", views.postmodal, name="postmodal"),
    path("like/<int:postid>", views.like, name="like"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("editpost/<str:newcontent>/<str:newtitle>/<int:postid>", views.editpost, name="editpost"),
    path("user_page/<str:username>", views.user_page, name="user_page"),
    path("addfollow/<str:profile_user>", views.addfollow, name="addfollow"),
    path("removefollow/<str:profile_user>", views.removefollow, name="removefollow"),
    path("following", views.following, name="following"),
    path("explore", views.explore, name="explore"),
    path("sort/<str:sortBy>/<str:uniSort>/<str:subjectSort>", views.sort, name="sort"),
    path("search/<str:number>/<str:query>", views.search, name="search"),
    path("add_comment/<int:post_id>/<str:comment>", views.add_comment, name="add_comment"),
    path("getcomments/<int:post_id>", views.getcomments, name="getcomments"),
    path("userdata/<str:order>/<int:the_id>", views.userdata, name="userdata"),
    path("delete/<int:identity>/<str:kind>", views.delete, name="delete"),
    path("subject/<str:subject>", views.subject_page, name="subject"),
    path("post/<int:identity>", views.post, name="post"),
    path("all_subjects/", views.all_subjects, name="all_subjects"),
    path("all_questions/<str:subject>", views.all_questions, name="all_questions")



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)