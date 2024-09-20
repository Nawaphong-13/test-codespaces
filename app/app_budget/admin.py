from django.contrib import admin
from .models import (
    BudgetYear, Plan, Project, Category, BudgetItem,
    MonthlyPlan, File, Image, TypeInvoice, Invoice
)
from image_uploader_widget.admin import ImageUploaderInline


@admin.register(BudgetYear)
class BudgetYearAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'department', 'office', 'allocated_budget', 'created_at', 'updated_at')
    search_fields = ('fiscal_year', 'department', 'section', 'office')
    list_filter = ('fiscal_year', 'department')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'plan_code', 'fiscal_year', 'allocated_budget', 'created_at', 'updated_at')
    search_fields = ('plan_name', 'plan_code')
    list_filter = ('fiscal_year',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_code', 'fiscal_year', 'plan', 'project_status', 'created_at', 'updated_at')
    search_fields = ('project_name', 'project_code')
    list_filter = ('fiscal_year', 'project_status')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_at', 'updated_at')
    search_fields = ('category_name',)

@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('budget_item_name', 'project', 'allocated_budget', 'category', 'created_at', 'updated_at')
    search_fields = ('budget_item_name', 'project__project_name')
    list_filter = ('project', 'category')

@admin.register(MonthlyPlan)
class MonthlyPlanAdmin(admin.ModelAdmin):
    list_display = ('budget_item', 'month', 'year', 'planned_amount', 'actual_amount', 'created_at', 'updated_at')
    search_fields = ('budget_item__budget_item_name',)
    list_filter = ('month', 'year')

# @admin.register(File)
# class FileAdmin(admin.ModelAdmin):
#     list_display = ('file_name_original', 'file_type', 'file_size', 'created_at')
#     search_fields = ('file_name_original',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_at')
    search_fields = ('file_nfileame_original',)

@admin.register(TypeInvoice)
class TypeInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_type_name', 'created_at', 'updated_at')
    search_fields = ('invoice_type_name',)

# # Create the File inline admin
# class FileInline(admin.TabularInline):
#     model = Invoice
#     extra = 1  # Number of empty file slots to display

# # Create the Image inline admin
# class ImageInline(admin.TabularInline):
#     model = Invoice.attached_images.through
#     extra = 1  # Number of empty image slots to display

class ImageInline(ImageUploaderInline):
    model = Image
    
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'fiscal_year', 'invoice_type', 'total_amount_due', 'approval_date', 'created_at', 'updated_at')
    search_fields = ('invoice_number', 'fiscal_year__fiscal_year', 'contractor_name')
    list_filter = ('fiscal_year', 'invoice_type')
    
    # # Add the inlines for File and Image
    inlines = [ImageInline]
