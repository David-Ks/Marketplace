from django.urls import path, include, re_path
from allauth.account import views as allauthViews

from . import views
from .views import AddReviewView, DelivaryAdminView

urlpatterns = [
    # path('', include('allauth.account.urls')),
    path("signup/", allauthViews.signup, name="account_signup"),
    path("login/", allauthViews.login, name="account_login"),
    path("logout/", allauthViews.logout, name="account_logout"),
    path("password/reset/", allauthViews.password_reset, name="account_reset_password"),
    path("password/reset/done/", allauthViews.password_reset_done, name="account_reset_password_done"),
    path("password/reset/key/done/", allauthViews.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", allauthViews.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("confirm-email/", allauthViews.email_verification_sent, name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", allauthViews.confirm_email, name="account_confirm_email"),

    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/new/review/", AddReviewView.as_view(), name="profile_new_review"),

    path("del/admin/", DelivaryAdminView.as_view(), name="delivery"),
]
