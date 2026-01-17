from django.contrib import admin

from .models import Material, Basket, SystemLog, EmailLog


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "unit_price",
        "unit",
        "quantity",
        "user"
    )
    list_editable = ("name", "unit_price", "quantity")
    list_filter = ("name", "unit_price", "quantity") # to filter by ONE name / unit_price / quantity
    ordering = ("id", ) # to change the way how displays (to change order)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "material",
        "status",
        "count"
    )
    list_editable = ("user", "material", "status", "count")
    list_filter = ("user", "status", "count")
    ordering = ("id", )


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "level", "message")
    list_filter = ("level", "created_at")
    search_fields = ("message", )
    ordering = ("-created_at", )

    readonly_fields = ("created_at", "level", "message")


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("id", "to_email", "subject")
    list_filter = ("to_email", )
    readonly_fields = ("to_email", "subject")
