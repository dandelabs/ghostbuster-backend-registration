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
    class Meta:
        model = Machine
        fields = ('id',
                  'name',
                  'statusIdPrimary',
                  'statusIdSecondary',
                  'statusId')
        
class ProductsProcessesSerializer(serializers.ModelSerializer):                
    class Meta:
        model = ProductsProcesses
        fields = ('id',
                  'itemId',
                  'fromStatusId',
                  'toStatusId',
                  'machineId',
                  'stdTime', 
                  'machineId')
        
class UsersSerializer(serializers.ModelSerializer):                
    class Meta:
        model = User
        fields = ('id',
                  'firstName',
                  'lastName',
                  'nick_name',
                  'password',
                  'salt',
                  'statusId',
                  'createdDate',
                  'updatedDate')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super(UsersSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
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