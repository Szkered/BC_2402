from django.db import models
import datetime

class Stock(models.Model):
    name = models.CharField(max_length=50)
    unit_measure = models.CharField(max_length=40)
    unit_price = models.FloatField()

    def __str__(self):
        return "%s - $%s/%s" % (self.name, self.unit_price, self.unit_measure)

    def purchase_sum(self, d):
        purchased = Purchase.objects.filter(stock=self,
                                            order__confirm=True,
                                            order__date__lte=d)
        return sum([stock.quantity for stock in purchased])

    def donate_sum(self, d):
        donated = Donate.objects.filter(stock=self, donation__date__lte=d)
        return sum([stock.quantity for stock in donated])
        
    def distribute_sum(self, d):
        distributed = Distribute.objects.filter(stock=self, date__lte=d)
        return sum([stock.quantity for stock in distributed])
        
    def transfer_sum(self, d):
        transfered = Transfer.objects.filter(stock=self, date__lte=d)
        return sum([stock.quantity for stock in transfered])

    def query_amt(self, q):
        q = q.filter(stock=self)
        return sum([item.quantity for item in q])

    def query_price(self, q):
        q = q.filter(stock=self)
        return "%.2f" % sum([item.cash_value() for item in q])
        
    def current_amt(self, d): 
        return self.purchase_sum(d) + self.donate_sum(d) - self.transfer_sum(d) - self.distribute_sum(d)

    def total_price(self, d):
        return "%.2f" % (self.unit_price * self.current_amt(d))


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
    contact_no = models.IntegerField()
    address = models.CharField(max_length=200)
    
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

    email = models.EmailField()
    mailing = models.BooleanField()
    referral = models.CharField(max_length=1, choices=REFERRAL_TYPES)

    def __str__(self):
        return "%s, tel: %s" % (self.name, self.contact_no)

class Vendor(CommonInfo):
    email = models.EmailField()
    fax = models.IntegerField()
    contact_person_name = models.CharField(max_length=50)
    
    def __str__(self):
        return "%s, tel: %s" % (self.name, self.contact_no)

##################################################
class TransitInfo(models.Model):
    quantity = models.IntegerField()
    stock = models.ForeignKey(Stock)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s :%s %s" % (self.stock, self.quantity, self.stock.unit_measure)
        
    def cash_value(self):
        return float("%.2f" % (self.quantity * self.stock.unit_price))

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
    date = models.DateField(default=datetime.datetime.now())
    family_type = models.CharField(max_length=1, choices=FAMILY_TYPES)

class Transfer(TransitInfo):
    date = models.DateField(default=datetime.datetime.now())
    destination = models.ForeignKey(Destination)
    remark = models.CharField(max_length=100)

class Donation(models.Model):
    donor = models.ForeignKey(Donor)
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return "%s - %s" % (self.date, self.donor)
    
class Donate(TransitInfo):
    donation = models.ForeignKey(Donation)

class Order(models.Model):
    vendor = models.ForeignKey(Vendor)
    date = models.DateField(default=datetime.datetime.now())
    confirm = models.BooleanField()

    def __str__(self):
        return "%s - %s" % (self.date, self.vendor)
        
    def total_price(self):
        purchase = [item.cash_value() for item in Purchase.objects.filter(order=self)]
        return "%.2f" % sum(purchase)
        
    
class Purchase(TransitInfo):
    order = models.ForeignKey(Order)
    price = models.FloatField()

    def purchase_price(self):
        return float("%.2f" % (self.quantity * self.price))
