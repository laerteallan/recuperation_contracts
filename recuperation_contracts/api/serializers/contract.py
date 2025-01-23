from rest_framework import serializers

from api.exceptions import ObjectNotFound, ParamInvalid
from api.internal_services.validate_cpf import ValidateCPF
from api.models import Contracts

from .invoice import InvoiceSerializer


class ContractsSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    issue_date = serializers.DateField(required=True)
    born_date = serializers.DateField(required=True)
    value = serializers.FloatField(required=True)
    cpf = serializers.CharField(max_length=15)
    country = serializers.CharField(max_length=50)
    province = serializers.CharField(max_length=2)
    city = serializers.CharField(max_length=50)
    telephone = serializers.CharField(max_length=20)
    tax = serializers.FloatField(required=True)
    invoices = InvoiceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Contracts
        fields = ("id", "issue_date", "born_date", "value", "cpf", "country",
                  "province", "city", "telephone", "tax", "invoices")
    
    def __get_contract_by_id(self, pk):
        try:
            contract = Contracts.objects.get(pk=pk)
            return contract
        except Contracts.DoesNotExist as error:
            raise ObjectNotFound("Contract Not found. {} id".format(pk))
    
    def create(self, validate_data):
        cpf = validate_data.get("cpf", "")
        if not ValidateCPF.validate_cpf(cpf):
            raise ParamInvalid("CPF Invalid {cpf}".format(cpf=cpf))
        cpf = cpf.replace(".", "").replace("-", "")
        validate_data.update({"cpf": cpf})
        invoices = validate_data.pop("invoices")
        contract = Contracts.objects.create(**validate_data)
        for item in invoices:
            item.update({"contract": contract})
            InvoiceSerializer().create(item)
        return contract.id

    def get_by_id(self, pk):
        contract = self.__get_contract_by_id(pk)
        return contract

class ConsolidateContractsSerializer(serializers.ModelSerializer):

    value_tot_pay_out = serializers.FloatField()
    value_tot_receive = serializers.FloatField()
    average_tax = serializers.FloatField()
    quantity_contracts = serializers.IntegerField()
    class Meta:
        model = Contracts
        fields = ("value_tot_pay_out", "value_tot_receive", "average_tax", "quantity_contracts")
