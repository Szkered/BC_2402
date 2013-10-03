from django.contrib import admin
from stocks.models import *

class StockAdmin(admin.ModelAdmin):

    list_display = ['description', 'unit_measure', 'unit_price',
                    'current_amt'
    ]
    ordering = ['description']
    search_fields = ('description',)

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


    
