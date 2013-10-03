from django.db import models

class Stock(models.Model):
    description = models.CharField(max_length=50)
    unit_measure = models.CharField(max_length=10)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_sum = models.DecimalField(max_digits=10, decimal_places=2)
    donate_sum = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_sum = models.DecimalField(max_digits=10, decimal_places=2)
    distribute_sum = models.DecimalField(max_digits=10, decimal_places=2)
    # category = models.CharField(max_length=50)
    # Replaced with a table, since this is a many to one relationship
    
    def __str__(self):
        return self.description

    def current_amt(self):
        return self.purchase_sum + self.donate_sum
        - self.transfer_sum - self.distribute_sum

    def total_price(self):
        return self.unit_price * current_amt(self)
        
class Category(models.Model):
    stock = models.ForeignKey(Stock)
    name = models.CharField(max_length=20)
        
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
    # FM = 'F'
    # CLIENT = 'C'
    # VOLUNTEER = 'V'
    # REGULAR = 'R'
    # OTHERS = 'O'
    # REFERRAL_TYPES = (
    #     (FM, 'FM 97.2'),
    #     (CLIENT, 'SYCC Client'),
    #     (VOLUNTEER, 'SYCC Volunteer'),
    #     (REGULAR, 'Regular Donor'),
    #     (OTHERS, 'Others'),
    # )
    mailing = models.BooleanField()
    referral = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class Vendor(CommonInfo):

    def __str__(self):
        return self.name

##################################################
class TransitInfo(models.Model):
    date = models.DateField()
    quantity = models.IntegerField()

    class Meta:
        abstract = True
        
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

    stock = models.ForeignKey(Stock)
    family_type = models.CharField(max_length=1, choices=FAMILY_TYPES)

class Transfer(TransitInfo):
    stock = models.ForeignKey(Stock)
    destination = models.ForeignKey(Destination)

class Donate(TransitInfo):
    stock = models.ForeignKey(Stock)
    donor = models.ForeignKey(Donor)

class Purchase(TransitInfo):
    stock = models.ForeignKey(Stock)
    vendor = models.ForeignKey(Vendor)
    confirm = models.BooleanField()
    
