from django.contrib import admin

from apps.deals.models import Gem, Customer, Deal


@admin.register(Gem)
class GemAdmin(admin.ModelAdmin):
    model = Gem
    list_display = ['name', ]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['username', ]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    model = Deal
    list_display = ['customer', 'item', 'total', 'quantity']
