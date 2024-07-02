from django.contrib import admin

# Register your models here.
from store.models import Category, Delivery, Item, Cart, OrderItem, Refund, Address, Payment, Coupon, UserProfile


admin.site.register(Category)
admin.site.register(Delivery)
admin.site.register(Item)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(UserProfile)



class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderItem

    list_display = ["__str__", 'ordered']


admin.site.register(OrderItem, OrderAdmin)


def update_refund_request_to_true(model_admin, request, query_set):
    query_set.update(refund_requested=False, refund_granted=True)


update_refund_request_to_true.short_description_message = "Update orders to refund granted"


class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

    list_display = ['__str__',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'billing_address',
                    'shipping_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = ['__str__',
                          'ordered',
                          'billing_address',
                          'shipping_address',
                          'payment',
                          'coupon'
                          ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted'
                   ]
    search_fields = ['user__username', 'reference_code']
    actions = [update_refund_request_to_true]



class RefundAdmin(admin.ModelAdmin):
    class Meta:
        model = Refund
    list_display = ['__str__', 'order']


admin.site.register(Refund, RefundAdmin)
admin.site.register(Cart, CartAdmin)
