from users.views import UserLoginView, UserRegistrationView, UserProfileView, UserLogoutView, EmailVerificationView
from django.contrib.auth.decorators import login_required
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    # Так как мы наследуемся от UpdateView - class UserProfileView(UpdateView)
    # То нам нужно указать с каким обьектом мы работаем - <int:pk>
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]









