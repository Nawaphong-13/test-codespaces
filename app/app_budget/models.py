from django.db import models

# Model for งบประมาณประจำปี (Annual Budget)
class AnnualBudget(models.Model):
    year = models.IntegerField(verbose_name="ปีงบประมาณ")  # Budget year (e.g., 2567)
    work_group = models.CharField(max_length=255, verbose_name="กลุ่มงาน")  # Work group
    office = models.CharField(max_length=255, verbose_name="กองงาน")  # Office
    office_unit = models.CharField(max_length=255, verbose_name="สำนักงาน")  # Office unit
    income_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณได้รายได้จักสรร")  # Income budget (Auto fill)
    operational_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบดำเนินการ")  # Expense budget (Auto fill)
    procurement_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณ จัดซื้อ/จ้าง")  # Procurement budget (Auto fill)

    def __str__(self):
        return f"Annual Budget {self.year}"


# Model for แผนงาน (Plans)
class Plan(models.Model):
    annual_budget = models.ForeignKey(AnnualBudget, on_delete=models.CASCADE, verbose_name="ปีงบประมาณ")  # ForeignKey to AnnualBudget
    plan_name = models.CharField(max_length=255, verbose_name="ชื่อแผนงาน")  # Plan name
    plan_code = models.CharField(max_length=100, verbose_name="รหัสแผนงาน")  # Plan code
    income_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณได้รายได้จักสรร")  # Income budget (Auto fill)
    operational_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบดำเนินการ")  # Expense budget (Auto fill)
    procurement_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณ จัดซื้อ/จ้าง")  # Procurement budget (Auto fill)
    contract_start_date = models.DateField(verbose_name="วันลงนามสัญญาจ้าง")  # Contract start date
    contract_end_date = models.DateField(verbose_name="วันสิ้นสุดสัญญา")  # Contract end date

    def __str__(self):
        return self.plan_name


# Model for โครงการ (Project)
class Project(models.Model):
    annual_budget = models.ForeignKey(AnnualBudget, on_delete=models.CASCADE, verbose_name="ปีงบประมาณ")  # ForeignKey to AnnualBudget
    project_name = models.CharField(max_length=255, verbose_name="ชื่อโครงการ")  # Project name
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name="แผนงาน")  # ForeignKey to Plan
    project_code = models.CharField(max_length=100, verbose_name="รหัสโครงการ")  # Project code
    income_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณได้รายได้จักสรร")  # Income budget (Auto fill)
    operational_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบดำเนินการ")  # Expense budget (Auto fill)
    procurement_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณ จัดซื้อ/จ้าง")  # Procurement budget (Auto fill)
    contract_start_date = models.DateField(verbose_name="วันลงนามสัญญาจ้าง")  # Contract start date
    contract_end_date = models.DateField(verbose_name="วันสิ้นสุดสัญญา")  # Contract end date

    def __str__(self):
        return self.project_name


# Model for ใบแจ้งหนี้ (Invoice)
class Invoice(models.Model):
    annual_budget = models.ForeignKey(AnnualBudget, on_delete=models.CASCADE, verbose_name="ปีงบประมาณ")  # ForeignKey to AnnualBudget
    invoice_number = models.CharField(max_length=255, verbose_name="เลขที่ใบแจ้งหนี้")  # Invoice number
    invoice_date = models.DateField(verbose_name="วันที่ใบแจ้งหนี้")  # Invoice date
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="รวมสินค้าชิ้นราคารวม")  # Total amount
    vat = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="ภาษีมูลค่าเพิ่ม")  # VAT
    payer_name = models.CharField(max_length=255, verbose_name="ชื่อผู้อนุมัติ/ผู้จ่ายเงิน")  # Payer name
    supplier_name = models.CharField(max_length=255, verbose_name="ชื่อผู้รับจ้าง")  # Supplier name

    def __str__(self):
        return self.invoice_number


# Model for เอกสารแนบ (Attached Document)
class AttachedDocument(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, verbose_name="เอกสารแนบ")  # ForeignKey to Invoice
    document_name = models.CharField(max_length=255, verbose_name="ชื่อเอกสารแนบ")  # Document name
    document_image = models.ImageField(upload_to='documents/', verbose_name="รูปภาพประกอบ")  # Document image

    def __str__(self):
        return self.document_name


# Model for รายการงบ (Budget Item)
class BudgetItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="โครงการ")  # ForeignKey to Project
    item_name = models.CharField(max_length=255, verbose_name="ชื่อรายการงบ")  # Item name
    income_budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณได้รายได้จักสรร")  # Income budget (Auto fill)
    procurement_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="งบประมาณ จัดซื้อ/จ้าง")  # Procurement expense (Auto fill)
    group = models.CharField(max_length=255, verbose_name="กลุ่มรายการงบ")  # Budget group

    def __str__(self):
        return self.item_name


# Model for ประเภทใบแจ้งหนี้ (Invoice Type)
class InvoiceType(models.Model):
    type_name = models.CharField(max_length=255, verbose_name="ชื่อประเภทใบแจ้งหนี้")  # Type name

    def __str__(self):
        return self.type_name


# Model for แผนผล (Monthly Report)
class MonthlyReport(models.Model):
    budget_item = models.ForeignKey(BudgetItem, on_delete=models.CASCADE, verbose_name="รายการงบ")  # ForeignKey to BudgetItem
    month = models.IntegerField(verbose_name="เดือน")  # Month
    year = models.IntegerField(verbose_name="ปี")  # Year
    progress = models.TextField(verbose_name="แผน")  # Plan

    def __str__(self):
        return f"Report for {self.budget_item} in {self.month}/{self.year}"
