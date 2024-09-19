from django.test import TestCase
from .models import AnnualBudget, Plan, Project, Invoice, AttachedDocument, BudgetItem, InvoiceType, MonthlyReport
from django.utils import timezone

class AnnualBudgetModelTest(TestCase):
    def setUp(self):
        # Create an AnnualBudget instance
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="IT Group",
            office="Office of Management",
            office_unit="Central Office",
            income_budget=100000.00,
            operational_expense=50000.00,
            procurement_expense=30000.00,
        )

    def test_annual_budget_creation(self):
        self.assertEqual(self.annual_budget.year, 2567)
        self.assertEqual(self.annual_budget.work_group, "IT Group")
        self.assertEqual(self.annual_budget.income_budget, 100000.00)

class PlanModelTest(TestCase):
    def setUp(self):
        # Create an AnnualBudget and Plan instance
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="Development Group",
            office="Planning Office",
            office_unit="North Office",
            income_budget=150000.00,
            operational_expense=80000.00,
            procurement_expense=40000.00,
        )
        self.plan = Plan.objects.create(
            annual_budget=self.annual_budget,
            plan_name="Development Plan",
            plan_code="DEV123",
            income_budget=150000.00,
            operational_expense=80000.00,
            procurement_expense=40000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )

    def test_plan_creation(self):
        self.assertEqual(self.plan.plan_name, "Development Plan")
        self.assertEqual(self.plan.annual_budget.year, 2567)

class ProjectModelTest(TestCase):
    def setUp(self):
        # Create an AnnualBudget, Plan, and Project instance
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="Infrastructure Group",
            office="Infrastructure Office",
            office_unit="East Office",
            income_budget=200000.00,
            operational_expense=120000.00,
            procurement_expense=60000.00,
        )
        self.plan = Plan.objects.create(
            annual_budget=self.annual_budget,
            plan_name="Infrastructure Plan",
            plan_code="INFRA456",
            income_budget=200000.00,
            operational_expense=120000.00,
            procurement_expense=60000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )
        self.project = Project.objects.create(
            annual_budget=self.annual_budget,
            project_name="Bridge Construction",
            plan=self.plan,
            project_code="BRIDGE001",
            income_budget=200000.00,
            operational_expense=120000.00,
            procurement_expense=60000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )

    def test_project_creation(self):
        self.assertEqual(self.project.project_name, "Bridge Construction")
        self.assertEqual(self.project.plan.plan_name, "Infrastructure Plan")

class InvoiceModelTest(TestCase):
    def setUp(self):
        # Create an AnnualBudget and Invoice instance
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="Finance Group",
            office="Finance Office",
            office_unit="West Office",
            income_budget=250000.00,
            operational_expense=150000.00,
            procurement_expense=70000.00,
        )
        self.invoice = Invoice.objects.create(
            annual_budget=self.annual_budget,
            invoice_number="INV123456",
            invoice_date=timezone.now(),
            total_amount=5000.00,
            vat=7.00,
            payer_name="John Doe",
            supplier_name="ABC Supply Ltd.",
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.invoice_number, "INV123456")
        self.assertEqual(self.invoice.total_amount, 5000.00)
        self.assertEqual(self.invoice.supplier_name, "ABC Supply Ltd.")

class AttachedDocumentModelTest(TestCase):
    def setUp(self):
        # Create an AnnualBudget, Invoice, and AttachedDocument instance
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="Legal Group",
            office="Legal Office",
            office_unit="North East Office",
            income_budget=300000.00,
            operational_expense=180000.00,
            procurement_expense=80000.00,
        )
        self.invoice = Invoice.objects.create(
            annual_budget=self.annual_budget,
            invoice_number="INV654321",
            invoice_date=timezone.now(),
            total_amount=10000.00,
            vat=7.00,
            payer_name="Jane Doe",
            supplier_name="XYZ Suppliers",
        )
        self.document = AttachedDocument.objects.create(
            invoice=self.invoice,
            document_name="Contract Document",
            document_image="path/to/image.jpg",
        )

    def test_attached_document_creation(self):
        self.assertEqual(self.document.document_name, "Contract Document")
        self.assertEqual(self.document.invoice.invoice_number, "INV654321")

class BudgetItemModelTest(TestCase):
    def setUp(self):
        # Create AnnualBudget, Plan, Project, and BudgetItem instance
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="Health Group",
            office="Health Office",
            office_unit="Central Office",
            income_budget=500000.00,
            operational_expense=300000.00,
            procurement_expense=100000.00,
        )
        self.plan = Plan.objects.create(
            annual_budget=self.annual_budget,
            plan_name="Healthcare Plan",
            plan_code="HEALTH001",
            income_budget=500000.00,
            operational_expense=300000.00,
            procurement_expense=100000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )
        self.project = Project.objects.create(
            annual_budget=self.annual_budget,
            project_name="Hospital Construction",
            plan=self.plan,
            project_code="HOSPITAL001",
            income_budget=500000.00,
            operational_expense=300000.00,
            procurement_expense=100000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )
        self.budget_item = BudgetItem.objects.create(
            project=self.project,
            item_name="Construction Equipment",
            income_budget=200000.00,
            procurement_expense=50000.00,
            group="Infrastructure",
        )

    def test_budget_item_creation(self):
        self.assertEqual(self.budget_item.item_name, "Construction Equipment")
        self.assertEqual(self.budget_item.project.project_name, "Hospital Construction")

class InvoiceTypeModelTest(TestCase):
    def setUp(self):
        # Create an InvoiceType instance
        self.invoice_type = InvoiceType.objects.create(
            type_name="Standard Invoice",
        )

    def test_invoice_type_creation(self):
        self.assertEqual(self.invoice_type.type_name, "Standard Invoice")

class MonthlyReportModelTest(TestCase):
    def setUp(self):
        # Create instances for testing MonthlyReport
        self.annual_budget = AnnualBudget.objects.create(
            year=2567,
            work_group="Education Group",
            office="Education Office",
            office_unit="South Office",
            income_budget=600000.00,
            operational_expense=400000.00,
            procurement_expense=150000.00,
        )
        self.plan = Plan.objects.create(
            annual_budget=self.annual_budget,
            plan_name="Education Plan",
            plan_code="EDU123",
            income_budget=600000.00,
            operational_expense=400000.00,
            procurement_expense=150000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )
        self.project = Project.objects.create(
            annual_budget=self.annual_budget,
            project_name="School Renovation",
            plan=self.plan,
            project_code="SCHOOL001",
            income_budget=600000.00,
            operational_expense=400000.00,
            procurement_expense=150000.00,
            contract_start_date=timezone.now(),
            contract_end_date=timezone.now(),
        )
        self.budget_item = BudgetItem.objects.create(
            project=self.project,
            item_name="Building Materials",
            income_budget=300000.00,
            procurement_expense=100000.00,
            group="Infrastructure",
        )
        self.monthly_report = MonthlyReport.objects.create(
            budget_item=self.budget_item,
            month=9,
            year=2567,
            progress="On track with the construction",
        )

    def test_monthly_report_creation(self):
        self.assertEqual(self.monthly_report.budget_item.item_name, "Building Materials")
        self.assertEqual(self.monthly_report.month, 9)
        self.assertEqual(self.monthly_report.progress, "On track with the construction")
