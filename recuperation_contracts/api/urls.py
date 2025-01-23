from django.urls import path

from .views import ContractsListView, ContractUpdateDestroy, ConsolidateContractListView

urlpatterns = [
    path('contracts/', ContractsListView.as_view(), name="contracts"),
    path('contracts/<int:pk>', ContractUpdateDestroy.as_view(), name="details_contract"),
    path('contracts/consolidate/', ConsolidateContractListView.as_view(), name="contracts"),

]
