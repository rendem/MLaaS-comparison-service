from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('frontend/', include('urls')),
    path('posts/', views.MlcmpView.as_view(), name='posts_list'),
    path('zip-posts/', views.BulkView.as_view()),
    re_path(r'f/', views.catchall),
    path('', views.mlcmp_list),
    path('<int:pk>/', views.mlcmp_detail),
    # path('', index, name="index"),
    # path('', views.ListMlcmp.as_view()),
    # path('<int:pk>/', views.DetailMlcmp.as_view()),
    # url(r'^api/mlcmp/$', views.mlcmp_list),
    # url(r'^api/mlcmp/(P[0-9]+)$', views.mlcmp_detail),
]
