from django.contrib import admin
from stocks.models import Stock, Donor, Destination, Vendor

class StockAdmin(admin.ModelAdmin):
    list_display = ['description', 'unit_price']
    ordering = ['description']
    search_fields = ('description',)

class DonorAdmin(admin.ModelAdmin):
    pass
    
class DestinationAdmin(admin.ModelAdmin):
    pass
    
class VendorAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(Stock, StockAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Vendor, VendorAdmin)


    
