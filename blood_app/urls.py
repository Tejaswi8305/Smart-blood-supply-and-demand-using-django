from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_page, name='predict'),
    path('shortage/', views.shortage_check, name='shortage'),
    path('demand_graph/', views.demand_graph, name='demand_graph'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/',views.login_view,name='login'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('hospital_dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('complete/<int:id>/', views.complete_request, name='complete_request'),
    path('get-data/', views.get_data, name='get_data'),
]