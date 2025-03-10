from django.urls import path
from nav.views import IndexView, scan_qr, signup_view, login_view, logout_view, store_search, search_history, settings_view

urlpatterns = [
    path('home', IndexView.as_view(), name='home'),
    path('scan-qr/', scan_qr, name='scan_qr'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('store-search/', store_search, name='store_search'),
    path('search-history/', search_history, name='search_history'),
    path('settings/', settings_view, name='settings'),

]