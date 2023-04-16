from dj_rest_auth.registration.views import ResendEmailVerificationView

from django.contrib import admin
from django.urls import path, include, re_path
from django_base.views import HelloWorldView

from courses.views import CoursesView
from django_base.views import EmailVerification

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello-world/', HelloWorldView.as_view(), name='hellow_world'),
    path('course/', CoursesView.as_view(), name='course'),
    
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/resend-email/', ResendEmailVerificationView.as_view(), name='rest_resend_email'),
    re_path("signup/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", EmailVerification.as_view(), name='account_confirm_email'),
]
