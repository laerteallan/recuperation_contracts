import logging
from functools import wraps

from django.core.exceptions import ValidationError
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from api.serializers.contract import (ConsolidateContractsSerializer,
                                      ContractsSerializer)

from .exceptions import AppError, ObjectNotFound
from .filters import ContractsFilter
from .models import Contracts
from api.serializers.invoice import InvoiceSerializer

log = logging.getLogger()


class InternalRequestHandler():

    @classmethod
    def api_method_wrapper(cls, function):
        p_method = function

        @wraps(p_method)
        def _execute_method(
            self: InternalRequestHandler, *path_parameter, **kwargs
        ):
            """Execute method of instance."""
            try:
                return p_method(self,  *path_parameter, **kwargs)
            except AppError as error:
                msg_error = {"error": str(error)}
                return Response(msg_error, error.status_app)
            except ValidationError as error:
                log.exception(str(error))
                msg_error = {"error": str(error)}
                return Response(msg_error, 400)
            except Exception as error:
                log.exception(str(error))
                return Response({"error": "Internal Server Error"})
        return _execute_method
    

class ContractsListView(generics.ListCreateAPIView):
    queryset = Contracts.objects.all()
    serializer_class = ContractsSerializer
    filterset_class = ContractsFilter
    
    @InternalRequestHandler.api_method_wrapper
    def list(self, request):
        queryset = self.filter_queryset(self.queryset)
        serializer = self.serializer_class(queryset, many=True) 
        return Response(serializer.data)

    @InternalRequestHandler.api_method_wrapper
    def post(self, request):
        contract = self.serializer_class()
        contract_id =  contract.create(request.data)
        return Response({"id": contract_id}, status.HTTP_201_CREATED)


class ConsolidateContractListView(generics.ListAPIView):
    queryset = Contracts.objects.all()
    serializer_class = ConsolidateContractsSerializer
    filterset_class = ContractsFilter
    
    @InternalRequestHandler.api_method_wrapper
    def list(self, request):
        queryset = self.filter_queryset(self.queryset)
        value_tot_receive = 0
        value_tot_pay_out = 0
        average_tax = 0
        count = 0 
        if not queryset:
            raise ObjectNotFound("Contracts Not found")
        for contract in queryset:
            count += 1
            average_tax += contract.tax
            for invoice in contract.invoices.values():
                value_tot_receive += invoice["value"]
            value_tot_pay_out += contract.value
        result = {
            "value_tot_pay_out": round(value_tot_pay_out, 2),
            "value_tot_receive": round(value_tot_receive, 2),
            "average_tax": round(average_tax/count, 2),
            "quantity_contracts": count,
        }
        serializer = self.serializer_class(result)

        return Response(serializer.data)


class ContractUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contracts.objects.all()
    serializer_class = ContractsSerializer
    filterset_class = ContractsFilter

    @InternalRequestHandler.api_method_wrapper
    def put(self, request, pk):
        contracts = self.serializer_class()
        object_contract = contracts.get_by_id(pk)
        data = request.data
        serializer_contract = ContractsSerializer(object_contract, data=data)
        invoices = data.get("invoices")
        if serializer_contract.is_valid():
            serializer_contract.save()
            invoice_serializer = InvoiceSerializer()
            invoice_serializer.delete_all_invoices_by_contract_id(pk)
            for invoice in invoices:
                invoice.update({"contract": object_contract})
                invoice_serializer.create(invoice)
            return Response(serializer_contract.data, status.HTTP_200_OK)

    @InternalRequestHandler.api_method_wrapper
    def get(self, request, pk):
        contracts = self.serializer_class()
        object_contract = contracts.get_by_id(pk)
        serealizer_contract = ContractsSerializer(object_contract)
        return Response(serealizer_contract.data, status.HTTP_200_OK)
    
    @InternalRequestHandler.api_method_wrapper
    def delete(self, request, pk):
        contracts = self.serializer_class()
        object_contract = contracts.get_by_id(pk)
        object_contract.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
