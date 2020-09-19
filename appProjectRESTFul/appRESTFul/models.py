from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class ProductionStatus(models.Model):
    id = models.AutoField(primary_key=True, db_column='production_status_id')
    description = models.CharField(max_length=45, db_column='production_status_description')
    statusId = models.IntegerField(db_column='production_status_active')

    class Meta:
        managed = True
        db_table = 'production_status'

class Item(models.Model):
    id = models.AutoField(primary_key=True, db_column='item_id')
    code = models.CharField(max_length=45, db_column='items_code')
    description = models.CharField(max_length=45, db_column='item_description')
    statusId = models.IntegerField(db_column='item_active')

    class Meta:
        managed = True
        db_table = 'items'
        
class Machine(models.Model):
    id = models.AutoField(primary_key=True, db_column='machine_id')
    name = models.CharField(max_length=9, db_column='machine_name')
    primaryStatusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column='status_id_primary_rm', related_name='primaryStatus')
    secondaryStatusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column='status_id_secondary_rm', related_name='secondaryStatus')
    statusId = models.IntegerField(db_column='machine_active')
    
    @property
    def primaryStatusName(self):
        return self.primaryStatusId.description
    
    @property
    def secondaryStatusName(self):
        return self.secondaryStatusId.description

    class Meta:
        managed = True
        db_table = 'machines'
        
class ProductsProcesses(models.Model):
    id = models.AutoField(primary_key=True, db_column='product_processes_id')
    statusId = models.IntegerField(db_column="product_processes_active")
    stdTime = models.IntegerField(db_column="product_processes_std_time")
    itemId = models.ForeignKey(Item, models.DO_NOTHING, db_column='item_id', related_name='itemName')
    fromStatusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column='from_status_id', related_name='fromStatusName')
    toStatusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column='to_status_id', related_name='toStatusName')
    machineId = models.ForeignKey(Machine, models.DO_NOTHING, db_column='machine_id', related_name='machineName')

    @property
    def fromStatusName(self):
        return self.fromStatusId.description
    
    @property
    def toStatusName(self):
        return self.toStatusId.description
    
    @property
    def itemName(self):
        return self.itemId.description
    
    @property
    def machineName(self):
        return self.machineId.name

    class Meta:
        managed = True
        db_table = 'products_processes'


class UserManager(BaseUserManager):

    def create_user(self, nick_name, password, **extra_fields):

        if not nick_name:
            raise ValueError('The Email must be set')
        username = nick_name
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, nick_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(nick_name, password, **extra_fields)

        
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, db_column="user_id")
    firstName = models.CharField(max_length=30, db_column="first_name")
    lastName = models.CharField(max_length=30, db_column="last_name")
    nick_name = models.CharField(max_length=20, db_column="nick_name", unique=True)
    password = models.TextField()
    salt = models.TextField()
    statusId = models.IntegerField(db_column="state_id")
    createdDate = models.FloatField(blank=True, null=True, db_column="created")
    updatedDate = models.FloatField(blank=True, null=True, db_column="updated")
    
    #Fields inherited from AbstractBaseUser model
    date_of_birth = models.DateField(blank=True, null=True, db_column="date_of_birth")
    picture = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    
    objects = UserManager()

    def __str__(self):
        return self.nick_name


    USERNAME_FIELD = 'nick_name'
    REQUIRED_FIELDS = ['firstName', 'lastName',]


class ChangeoverCost(models.Model):
    id = models.AutoField(primary_key=True, db_column="changeover_cost_id")
    fromStatusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column="from_status", related_name='change_from_status')
    toStatusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column="to_status", related_name='change_to_status')
    time = models.IntegerField(db_column="changeover_cost_time")
    statusId = models.IntegerField(db_column="changeover_cost_active")

    class Meta:
        managed = True
        db_table = 'changeover_cost'


class DowntimeType(models.Model):
    id = models.AutoField(primary_key=True, db_column="downtime_type_id")
    name = models.CharField(max_length=45, db_column="downtime_type_name")
    description = models.CharField(max_length=45, db_column="downtime_type_description")
    subject = models.CharField(max_length=45, db_column="downtime_type")
    statusId = models.CharField(max_length=9, db_column="downtime_active")

    class Meta:
        managed = True
        db_table = 'downtime_type'

        
class OrderDetails(models.Model):
    id = models.IntegerField(primary_key=True, db_column="detail_id")
    orderId = models.IntegerField(db_column="order_id")
    itemId = models.ForeignKey(Item, models.DO_NOTHING, db_column="item")
    quantity = models.IntegerField()
    quantityReceived = models.IntegerField(blank=True, null=True, db_column="quantity_received")
    receivedDate = models.FloatField(blank=True, null=True, db_column="received_date")
    insertedDate = models.FloatField(blank=True, null=True, db_column="inserted")

    class Meta:
        managed = True
        db_table = 'order_details'


class Downtime(models.Model):
    id = models.AutoField(primary_key=True, db_column="downtime_id")
    detailId = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column="detail")
    downtimeTypeId = models.ForeignKey(DowntimeType, models.DO_NOTHING, db_column="downtime_type")
    itemId = models.ForeignKey(Item, models.DO_NOTHING, db_column="item")
    userId = models.ForeignKey(User, models.DO_NOTHING, db_column="user")
    statusId = models.ForeignKey(ProductsProcesses, models.DO_NOTHING, db_column="status")
    startTime = models.FloatField(db_column="downtime_start_time")
    finishTime = models.FloatField(db_column="downtime_finish_time")

    class Meta:
        managed = True
        db_table = 'downtimes'


class DowntimesHistory(models.Model):
    id = models.AutoField(primary_key=True, db_column="downtime_id")
    detailId = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column="detail")
    downtimeTypeId = models.ForeignKey(DowntimeType, models.DO_NOTHING, db_column="downtime_type")
    itemId = models.ForeignKey(Item, models.DO_NOTHING, db_column="item")
    userId = models.ForeignKey(User, models.DO_NOTHING, db_column="user")
    statusId = models.ForeignKey(ProductsProcesses, models.DO_NOTHING, db_column="status")
    startTime = models.FloatField(db_column="downtime_start_time")
    finishTime = models.FloatField(db_column="downtime_finish_time")

    class Meta:
        managed = True
        db_table = 'downtimes_history'
        

class MachineUser(models.Model):
    id = models.AutoField(primary_key=True, db_column="machine_user_id")
    userId = models.ForeignKey(User, models.DO_NOTHING, db_column="user")
    machineId = models.ForeignKey(Machine, models.DO_NOTHING, db_column="machine")
    statusId = models.IntegerField(db_column="machine_user_active")

    class Meta:
        managed = True
        db_table = 'machine_user'


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True, db_column="order_status_id")
    description = models.CharField(max_length=45, db_column="order_status_description")
    statusId = models.IntegerField(db_column="order_status_active")

    class Meta:
        managed = True
        db_table = 'order_status'


class Order(models.Model):
    id = models.IntegerField(primary_key=True, db_column="order_id")
    customerName = models.CharField(max_length=50, db_column="order_customer_name")
    dueDate = models.FloatField(db_column="order_due_date")
    partiallyCancel = models.IntegerField(blank=True, null=True, db_column="partially_cancel")
    statusId = models.ForeignKey(OrderStatus, models.DO_NOTHING, blank=True, null=True, db_column="order_status")
    isBackOrder = models.IntegerField(blank=True, null=True, db_column="is_back_order")
    createdDate = models.FloatField(blank=True, null=True, db_column="created")
    modifiedDate = models.FloatField(blank=True, null=True, db_column="modified")
    insertedDate = models.FloatField(blank=True, null=True, db_column="inserted")
    priorityStatusId = models.IntegerField(blank=True, null=True, db_column="priority_status")

    class Meta:
        managed = True
        db_table = 'orders'


class OrdersHistory(models.Model):
    id = models.AutoField(primary_key=True, db_column="order_id")
    orderNumber = models.CharField(max_length=15, db_column="order_number")
    itemId = models.IntegerField(db_column="item_id")
    customerName = models.CharField(max_length=50, db_column="order_customer_name")
    dueDate = models.FloatField(db_column="order_due_date")
    newDueDate = models.FloatField(blank=True, null=True, db_column="order_new_due_date")
    quantity = models.IntegerField(db_column="order_quantity")
    quantityReceived = models.IntegerField(blank=True, null=True, db_column="order_quantity_received")
    receivedDate = models.FloatField(blank=True, null=True, db_column="order_received_date")
    statusId = models.ForeignKey(OrderStatus, models.DO_NOTHING, blank=True, null=True, db_column="order_status")
    scheduleTime = models.FloatField(blank=True, null=True, db_column="schedule_time")

    class Meta:
        managed = True
        db_table = 'orders_history'


class Production(models.Model):
    id = models.AutoField(primary_key=True, db_column="production_id")
    detailId = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column="detail")
    itemId = models.ForeignKey(Item, models.DO_NOTHING, db_column="item")
    userId = models.ForeignKey(User, models.DO_NOTHING, db_column="user")
    statusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column="status")
    startTime = models.FloatField(db_column="production_start_time")
    finishTime = models.FloatField(db_column="production_finish_time")
    unitsManufactured = models.IntegerField(db_column="production_units_manufactured")

    class Meta:
        managed = True
        db_table = 'production'


class ProductionHistory(models.Model):
    id = models.AutoField(primary_key=True, db_column="production_id")
    detailId = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column="detail")
    itemId = models.ForeignKey(Item, models.DO_NOTHING, db_column="item")
    userId = models.ForeignKey(User, models.DO_NOTHING, db_column="user")
    statusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column="status")
    startTime = models.FloatField(db_column="production_start_time")
    finishTime = models.FloatField(db_column="production_finish_time")
    unitsManufactured = models.IntegerField(db_column="production_units_manufactured")

    class Meta:
        managed = True
        db_table = 'production_history'


class Schedule(models.Model):
    id = models.AutoField(primary_key=True, db_column="schedule_id")
    orderItemProcess = models.CharField(max_length=15, db_column="order_item_process")
    detailId = models.ForeignKey(OrderDetails, models.DO_NOTHING, db_column="detail")
    statusId = models.ForeignKey(ProductionStatus, models.DO_NOTHING, db_column="status")
    manufacturingDate = models.FloatField(db_column="manufacturing_date")
    creationDate = models.FloatField(db_column="creation_date")
    quantity = models.IntegerField(db_column="order_quantity")

    class Meta:
        managed = True
        db_table = 'schedule'



