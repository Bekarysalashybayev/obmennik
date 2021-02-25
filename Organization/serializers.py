from rest_framework import serializers

from .models import *


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('code', 'fio')


class OperationSerializer(serializers.ModelSerializer):
    valuta = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    contract = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = ('contract', 'valuta', 'category', 'sum')

    def get_valuta(self, obj):
        return obj.code_valuta.name

    def get_category(self, obj):
        return obj.category.name

    def get_contract(self, obj):
        return ContractSerializer(obj.contract).data

class ContractSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ('pk', 'date', 'client')

    def get_client(self, obj):
        return UserInfoSerializer(obj.code_client).data