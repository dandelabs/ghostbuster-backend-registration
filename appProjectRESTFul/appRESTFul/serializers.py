from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


class ProductionStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionStatus
        fields = ('id',
                  'description',
                  'statusId')


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id',
                  'code',
                  'description',
                  'statusId')


class MachinesSerializer(serializers.ModelSerializer):

    primaryStatusName = serializers.ReadOnlyField()
    secondaryStatusName = serializers.ReadOnlyField()

    class Meta:
        model = Machine
        fields = ('id',
                  'name',
                  'statusId',
                  'primaryStatusId',
                  'secondaryStatusId',
                  'primaryStatusName',
                  'secondaryStatusName')


class ProductsProcessesSerializer(serializers.ModelSerializer):

    fromStatusName = serializers.ReadOnlyField()
    toStatusName = serializers.ReadOnlyField()
    itemName = serializers.ReadOnlyField()
    machineName = serializers.ReadOnlyField()
    
    class Meta:
        model = ProductsProcesses
        fields = ('id',
                  'itemId',
                  'statusId',
                  'fromStatusId',
                  'toStatusId',
                  'machineId',
                  'stdTime',
                  'machineId',
                  'fromStatusName',
                  'toStatusName',
                  'itemName',
                  'machineName')

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'firstName',
                  'lastName',
                  'nick_name',
                  'salt',
                  'statusId',
                  'createdDate',
                  'updatedDate',
                  'password',
                  'date_of_birth')

        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('auth_token',)

    def create(self, validated_data):
        try:
            user = super(UsersSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

    def update(self, instance, validated_data):
        user = super(UsersSerializer, self).update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class ChangeOverSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeoverCost
        fields = ('id',
                  'fromStatusId',
                  'toStatusId',
                  'time',
                  'statusId')


class DowntimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DowntimeType
        fields = ('id',
                  'name',
                  'description',
                  'subject',
                  'statusId')


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ('id',
                  'orderId',
                  'itemId',
                  'quantity',
                  'quantityReceived',
                  'receivedDate',
                  'insertedDate',)


class DowntimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Downtime
        fields = ('id',
                  'detailId',
                  'downtimeTypeId',
                  'itemId',
                  'userId',
                  'statusId',
                  'startTime',
                  'finishTime',)


class DowntimesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DowntimesHistory
        fields = ('id',
                  'detailId',
                  'downtimeTypeId',
                  'itemId',
                  'userId',
                  'statusId',
                  'startTime',
                  'finishTime',)


class MachineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineUser
        fields = ('id',
                  'userId',
                  'machineId',
                  'statusId')


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('id',
                  'description',
                  'statusId')


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
                  'customerName',
                  'dueDate',
                  'partiallyCancel',
                  'statusId',
                  'isBackOrder',
                  'createdDate',
                  'modifiedDate',
                  'insertedDate',
                  'priorityStatusId',)


class OrdersHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersHistory
        fields = ('id',
                  'orderNumber',
                  'itemId',
                  'customerName',
                  'dueDate',
                  'newDueDate',
                  'quantity',
                  'quantityReceived',
                  'receivedDate',
                  'statusId',
                  'scheduleTime',)


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ('id',
                  'detailId',
                  'itemId',
                  'userId',
                  'statusId',
                  'startTime',
                  'finishTime',
                  'unitsManufactured',)


class ProductionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionHistory
        fields = ('id',
                  'detailId',
                  'itemId',
                  'userId',
                  'statusId',
                  'startTime',
                  'finishTime',
                  'unitsManufactured',)


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id',
                  'orderItemProcess',
                  'detailId',
                  'statusId',
                  'manufacturingDate',
                  'creationDate',
                  'quantity',)
