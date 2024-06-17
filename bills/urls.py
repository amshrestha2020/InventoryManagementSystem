from django.urls import path
from bills.views import BillListView, BillCreateView, BillUpdateView, BillDeleteView

urlpatterns = [
    path('bills/', BillListView.as_view(), name="bill_list"),
    path('new-bill/', BillCreateView.as_view(), name='bill_create'),
    path('bill/<slug:slug>/update/', BillUpdateView.as_view(), name='bill_update'),
    path('bill/<int:pk>/delete/', BillDeleteView.as_view(), name='bill_delete'),
]