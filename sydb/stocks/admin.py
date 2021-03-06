from django.contrib import admin
from stocks.models import *

class StockAdmin(admin.ModelAdmin):

    list_display = ['name', 'unit_measure', 'unit_price', 'category_slug']
    ordering = ['name']
    search_fields = ('name',)

class DonorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_no', 'address', 'referral', 'mailing']
    ordering = ['name']

class DonateAdmin(admin.ModelAdmin):
    list_display = ['stock', 'quantity']
    ordering = ['stock']

class DonationAdmin(admin.ModelAdmin):
    list_display = ['date', 'donor']
    ordering = ['date']
    
class DestinationAdmin(admin.ModelAdmin):
    pass
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_no', 'address']
    ordering = ['name']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock']
    ordering = ['stock']

class DistributeAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'stock', 'family_type', 'date']
    ordering = ['stock']

class PurchaseInline(admin.StackedInline):
    model = Purchase
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['vendor', 'confirm']}),
        ('Date Info', {'fields': ['date'], 'classes' : ['collapse']}),
    ]
    inlines = [PurchaseInline]

    
admin.site.register(Stock, StockAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Donate, DonateAdmin)
admin.site.register(Donation, DonationAdmin)
# admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Distribute, DistributeAdmin)
admin.site.register(Transfer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)


    
