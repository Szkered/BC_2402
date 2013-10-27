from django.contrib import admin
from stocks.models import *

class StockAdmin(admin.ModelAdmin):

    list_display = ['name', 'unit_measure', 'unit_price',
                    'current_amt', 'total_price', 'category_slug'
    ]
    ordering = ['name']
    search_fields = ('name',)

# class StockInline(admin.TabularInline):
#     model = Stock
#     extra = 1

class PurchaseAdmin(admin.ModelAdmin):

    list_display = ['date', 'stock', 'vendor', 'quantity', 'total_price', 'confirm']
    ordering = ['date']
    search_fields = ('date',)
    

class DonorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_no', 'address', 'referral', 'mailing']
    ordering = ['name']

class DonateAdmin(admin.ModelAdmin):
    list_display = ['stock', 'quantity', 'donor', 'date']
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
    
admin.site.register(Stock, StockAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Donate, DonateAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Distribute, DistributeAdmin)
admin.site.register(Transfer)
admin.site.register(Category, CategoryAdmin)


    
