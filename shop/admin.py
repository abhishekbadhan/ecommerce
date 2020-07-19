from django.contrib import admin
from .models import product, contacts,orderupdate,Post,Blogcomment


# admin.site.register(product)
admin.site.register(contacts)
admin.site.register(orderupdate)
admin.site.register(Post)
admin.site.register((Blogcomment))


@admin.register(product)
class productAdmin(admin.ModelAdmin):
    class Media :
        js = ('description.js')