from django.db import models
import datetime

class Stock(models.Model):
    name = models.CharField(max_length=50)
    unit_measure = models.CharField(max_length=10)
    unit_price = models.FloatField()

    def __str__(self):
        return "%s - $%s/%s" % (self.name, self.unit_price, self.unit_measure)

    def purchase_sum(self):
        purchased = Purchase.objects.filter(stock=self,
                                            order__confirm=True)
        sum = 0
        for stock in purchased:
            sum += stock.quantity
        return sum

    def donate_sum(self):
        donated = Donate.objects.filter(stock=self)
        sum = 0
        for stock in donated:
            sum += stock.quantity
        return sum
        
    def distribute_sum(self):
        distributed = Distribute.objects.filter(stock=self)
        sum = 0
        for stock in distributed:
            sum += stock.quantity
        return sum
        
    def transfer_sum(self):
        transferd = Transfer.objects.filter(stock=self)
        sum = 0
        for stock in transferd:
            sum += stock.quantity
        return sum

    def current_amt(self): 
        return self.purchase_sum() + self.donate_sum() - self.transfer_sum() - self.distribute_sum()

    def total_price(self):
        return self.unit_price * self.current_amt()

    def category_slug(self):
        categorys = Category.objects.filter(stock=self)
        slug = ""
        for category in categorys:
            if category != '':
                slug += category.name + ", "
        return slug
        
class Category(models.Model):
    stock = models.ForeignKey(Stock)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['stock__name', 'stock__unit_measure']

        
##################################################
class Destination(models.Model):
    name = models.CharField(max_length=30)
    person_in_charge = models.CharField(max_length=30)
    contact_no = models.IntegerField()

    def __str__(self):
        return self.name

class CommonInfo(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    contact_no = models.IntegerField()

    class Meta:
        abstract = True

class Donor(CommonInfo):
    FM = 'F'
    CLIENT = 'C'
    VOLUNTEER = 'V'
    REGULAR = 'R'
    OTHERS = 'O'
    REFERRAL_TYPES = (
        (FM, 'FM 97.2'),
        (CLIENT, 'SYCC Client'),
        (VOLUNTEER, 'SYCC Volunteer'),
        (REGULAR, 'Regular Donor'),
        (OTHERS, 'Others'),
    )
    mailing = models.BooleanField()
    referral = models.CharField(max_length=1, choices=REFERRAL_TYPES)

    def __str__(self):
        return self.name

class Vendor(CommonInfo):

    def __str__(self):
        return "%s, tel: %s" % (self.name, self.contact_no)

##################################################
class TransitInfo(models.Model):
    date = models.DateField(default=datetime.datetime.now())
    quantity = models.IntegerField()
    stock = models.ForeignKey(Stock)

    class Meta:
        abstract = True

    def cash_value(self):
        return self.quantity * self.stock.unit_price
        
class Distribute(TransitInfo):
    TYPE_A = 'A'
    TYPE_B = 'B'
    TYPE_C = 'C'
    TYPE_D = 'D'
    FAMILY_TYPES = (
        (TYPE_A, 'Type A'),
        (TYPE_B, 'Type B'),
        (TYPE_C, 'Type C'),
        (TYPE_D, 'Type D'),
    )

    family_type = models.CharField(max_length=1, choices=FAMILY_TYPES)

class Transfer(TransitInfo):
    destination = models.ForeignKey(Destination)
    remark = models.CharField(max_length=100)

class Donate(TransitInfo):
    donor = models.ForeignKey(Donor)


class Order(models.Model):
    vendor = models.ForeignKey(Vendor)
    date = models.DateField(default=datetime.datetime.now())
    confirm = models.BooleanField()

    def __str__(self):
        return "%s - %s" % (self.date, self.vendor)
        
    def total_price(self):
        purchase = [item.cash_value() for item in Purchase.objects.filter(order=self)]
        return sum(purchase)
        
    
class Purchase(models.Model):
    order = models.ForeignKey(Order)
    stock = models.ForeignKey(Stock)
    quantity = models.IntegerField()

    def __str__(self):
        return "%s :%s %s" % (self.stock, self.quantity, self.stock.unit_measure)
    
    def cash_value(self):
        return self.quantity * self.stock.unit_price
