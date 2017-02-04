from django.contrib import admin
from .models import Post, Comment, Contact

class ContactAdmin(admin.ModelAdmin):

    list_display= ["name","sent_date"]



# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact, ContactAdmin)
