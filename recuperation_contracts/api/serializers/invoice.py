from rest_framework import serializers

from api.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    invoice_number = serializers.IntegerField()
    value = serializers.FloatField()
    due_date = serializers.DateField()


    class Meta:
        model = Invoice
        fields = ("id", "invoice_number", "value", "due_date")
    
    def create(self, validate_data):
        Invoice.objects.create(**validate_data)
       
    def delete_all_invoices_by_contract_id(self, contract_pk):
        Invoice.objects.filter(contract__id=contract_pk).delete()

