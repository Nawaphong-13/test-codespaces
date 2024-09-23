from django.contrib import admin
from .models import (
    BudgetYear, Plan, Project, Category, BudgetItem,
    MonthlyPlan, File, Image, TypeInvoice, Invoice
)
from image_uploader_widget.admin import ImageUploaderInline, OrderedImageUploaderInline
from . import forms

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
    fields = ('invoice', 'file_original', 'file_name_original', 'file_type', 'file_size', 'created_at',)
    readonly_fields = ('file_name_original', 'file_type', 'file_size', 'created_at')
    list_display = ('file_name_original', 'file_type', 'file_size', 'created_at')
    search_fields = ('file_name_original',)

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



class ImageInline(OrderedImageUploaderInline):
    model = Image
    # form = forms.ImageForm
    fields = ('file_original', 'order',)


    
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'fiscal_year', 'invoice_type', 'total_amount_due', 'approval_date', 'created_at', 'updated_at')
    search_fields = ('invoice_number', 'fiscal_year__fiscal_year', 'contractor_name')
    list_filter = ('fiscal_year', 'invoice_type')
    
    # Add the inlines for File and Image
    inlines = [ImageInline]

    def save_model(self, request, obj, form, change):
        if not change:  # If the object is being created
            obj.created_by = request.user
        obj.updated_by = request.user  # Always set the updated_by field
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # Check if this is an Image formset
        if formset.model == Image:
            # Delete instances marked for deletion
            for instance in formset.deleted_forms:
                if instance.instance.pk:
                    instance.instance.delete()

            # Iterate through each instance in the formset that is not marked for deletion
            instances = formset.save(commit=False)
            for instance in instances:
                # If the created_by field is empty, set it to the current user
                if not instance.created_by:
                    instance.created_by = request.user
                instance.save()  # Save the instance

            formset.save_m2m()  # Save many-to-many relationships if any

        else:
            # If it's not the Image formset, just save it as usual
            formset.save()




    
