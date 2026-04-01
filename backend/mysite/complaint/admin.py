from django.contrib import admin
from .models import Complaint, ElectricityComplaint, RoadComplaint, GarbageComplaint, WaterComplaint

# -----------------------------
# Main Complaint Admin
# -----------------------------
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "citizen_name_display",
        "citizen_email_display",
        "citizen_phone_display",
        "category",
        "authority",
        "ml_status",
        "confidence",
        "status",
        "created_at",
        "latitude",
        "longitude",
        "map_link",
    )

    list_filter = ("category", "authority", "status", "ml_status", "created_at")

    search_fields = (
        "description",
        "citizen__fullname",
        "citizen__email",
        "citizen__phone",
        "category",
        "authority",
    )

    # -----------------------------
    # Display citizen info from FK
    # -----------------------------
    def citizen_name_display(self, obj):
        return obj.citizen.fullname if obj.citizen else "-"
    citizen_name_display.short_description = "Citizen Name"

    def citizen_email_display(self, obj):
        return obj.citizen.email if obj.citizen else "-"
    citizen_email_display.short_description = "Citizen Email"

    def citizen_phone_display(self, obj):
        return obj.citizen.phone if obj.citizen else "-"
    citizen_phone_display.short_description = "Citizen Phone"

    def map_link(self, obj):
        if obj.latitude and obj.longitude:
                return f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
        return "-"
    map_link.short_description = "Map Location"


# Register main complaint admin
admin.site.register(Complaint, ComplaintAdmin)


# -----------------------------
# Proxy Models for Category Filters
# -----------------------------
class CategoryAdmin(ComplaintAdmin):
    category_value = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.category_value:
            return qs.filter(category__iexact=self.category_value)
        return qs


class ElectricityComplaintAdmin(CategoryAdmin):
    category_value = "electricity"


class RoadComplaintAdmin(CategoryAdmin):
    category_value = "road"


class GarbageComplaintAdmin(CategoryAdmin):
    category_value = "garbage"


class WaterComplaintAdmin(CategoryAdmin):
    category_value = "water"


# Register proxy models
admin.site.register(ElectricityComplaint, ElectricityComplaintAdmin)
admin.site.register(RoadComplaint, RoadComplaintAdmin)
admin.site.register(GarbageComplaint, GarbageComplaintAdmin)
admin.site.register(WaterComplaint, WaterComplaintAdmin)
