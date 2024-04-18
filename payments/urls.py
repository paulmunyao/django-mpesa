from django.urls import path
from . import views

urlpatterns = [
    path('stk-push-callback/', views.stk_push_callback, name='stk_push_callback'),
    path('callback/', views.callback, name="callback"),
]
