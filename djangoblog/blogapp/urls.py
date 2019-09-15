
from django.urls import path
from .import views

app_name = "blogapp"

urlpatterns = [
    path('', views.index.as_view(), name="index"),
    path('author/<name>', views.getauthor.as_view(), name="author"),
    path('article/<int:id>', views.getsingle.as_view(), name="single_post"),
    path('topic/<name>', views.getTopic.as_view(), name="topic"),
    path('login', views.getLogin, name="login"),
    path('logout', views.getLogout, name="logout"),
    path('create', views.getCreate.as_view(), name="create"),
    path('profile', views.getProfile.as_view(), name="profile"),
    path('update/<int:pid>', views.getUpdate.as_view(), name="update"),
    path('delete/<int:pid>', views.getDelete.as_view(), name="delete"),
    path('register', views.getRegister, name="register"),
    path('category', views.getCategory.as_view(), name="category"),
    path('creat/topic', views.creatTopic.as_view(), name="creatTopic")
    # path('updateCategory/<int:pid>', views.getCategoryUpdate, name="updateCategory"),
    # path('deleteCategory/<int:pid>', views.getCategoryDelete, name="deleteCategory")
]

