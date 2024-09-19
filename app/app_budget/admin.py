from django.contrib import admin
from .models import AnnualBudget, Plan, Project, Invoice, AttachedDocument, BudgetItem, InvoiceType, MonthlyReport

# Registering AnnualBudget model with Django Admin
@admin.register(AnnualBudget)
class AnnualBudgetAdmin(admin.ModelAdmin):
    list_display = ('year', 'work_group', 'office', 'income_budget', 'operational_expense', 'procurement_expense')
    search_fields = ('year', 'work_group', 'office')
    list_filter = ('year', 'work_group')

# Registering Plan model with Django Admin
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'plan_code', 'annual_budget', 'contract_start_date', 'contract_end_date')
    search_fields = ('plan_name', 'plan_code')
    list_filter = ('annual_budget',)

# Registering Project model with Django Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_code', 'plan', 'annual_budget', 'contract_start_date', 'contract_end_date')
    search_fields = ('project_name', 'project_code')
    list_filter = ('plan', 'annual_budget')

# Registering Invoice model with Django Admin
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_date', 'total_amount', 'payer_name', 'supplier_name')
    search_fields = ('invoice_number', 'payer_name', 'supplier_name')
    list_filter = ('annual_budget',)

# Registering AttachedDocument model with Django Admin
@admin.register(AttachedDocument)
class AttachedDocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'invoice')
    search_fields = ('document_name',)
    list_filter = ('invoice',)

# Registering BudgetItem model with Django Admin
@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'project', 'income_budget', 'procurement_expense', 'group')
    search_fields = ('item_name', 'group')
    list_filter = ('project',)

# Registering InvoiceType model with Django Admin
@admin.register(InvoiceType)
class InvoiceTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
    search_fields = ('type_name',)

# Registering MonthlyReport model with Django Admin
@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('budget_item', 'month', 'year', 'progress')
    search_fields = ('budget_item',)
    list_filter = ('month', 'year')
