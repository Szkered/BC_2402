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

class DonorAdmin(admin.ModelAdmin):
    pass

# class DonateAdmin(admin.ModelAdmin):
#     # fieldsets = {
#     #     ('Donor Info': {'fields': ['quantity']}),
#     #     ('Date Info': {'fields': ['date']}),
#     # }
#     # inlines = [StockInline]
#     pass
    
class DestinationAdmin(admin.ModelAdmin):
    pass
    
class VendorAdmin(admin.ModelAdmin):
    pass
    
    
    
admin.site.register(Stock, StockAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Donate)
admin.site.register(Purchase)
admin.site.register(Distribute)
admin.site.register(Transfer)
admin.site.register(Category)


    
