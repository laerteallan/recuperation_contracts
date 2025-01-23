from django_filters import FilterSet
from .models import Contracts

class ContractsFilter(FilterSet):
    
    class Meta:
        model = Contracts
        fields = {
            'id': ["exact"], 
            'cpf': ["iexact", "icontains"], 
            'issue_date': ["year", "month"], 
            'province': ["exact"]
            }

