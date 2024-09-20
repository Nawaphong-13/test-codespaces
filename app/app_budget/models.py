from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PILImage
from io import BytesIO
import os, random, string

class BudgetYear(models.Model):
    fiscal_year = models.CharField(max_length=255, verbose_name="ปีงบประมาณ")
    department = models.CharField(max_length=255, verbose_name="กลุ่มงาน")
    section = models.CharField(max_length=255, verbose_name="กองงาน")
    office = models.CharField(max_length=255, verbose_name="สำนักงาน")
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณได้รับจัดสรร")
    operating_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบดำเนินการ")
    procurement_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณซื้อจ้าง")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_budget_years", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_budget_years", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    def __str__(self):
        return self.fiscal_year

class Plan(models.Model):
    fiscal_year = models.ForeignKey(BudgetYear, on_delete=models.CASCADE, verbose_name="ปีงบประมาณ")
    plan_name = models.CharField(max_length=500, verbose_name="ชื่อแผนงาน")
    plan_code = models.CharField(max_length=100, verbose_name="รหัสแผนงาน")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณได้รับจัดสรร")
    operating_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบดำเนินการ")
    procurement_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณซื้อจ้าง")
    contract_sign_date = models.DateField(verbose_name="วันลงนามสัญญาจ้าง")
    contract_end_date = models.DateField(verbose_name="วันสิ้นสุดสัญญา")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_plans", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_plans", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")
    sort_order = models.IntegerField(default=500, verbose_name="ลำดับการจัดเรียง")

    def __str__(self):
        return self.plan_name


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'กำลังวางแผน'),
        ('in_progress', 'กำลังดำเนินการ'),
        ('completed', 'เสร็จสิ้น'),
        ('paused', 'ระงับชั่วคราว'),
        ('canceled', 'ยกเลิก'),
    ]
    fiscal_year = models.ForeignKey(BudgetYear, on_delete=models.CASCADE, verbose_name="ปีงบประมาณ")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name="แผนงาน")
    project_name = models.CharField(max_length=500, verbose_name="ชื่อโครงการ")
    project_code = models.CharField(max_length=100, verbose_name="รหัสโครงการ")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณได้รับจัดสรร")
    operating_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบดำเนินการ")
    procurement_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณซื้อจ้าง")
    contract_sign_date = models.DateField(verbose_name="วันลงนามสัญญาจ้าง")
    contract_end_date = models.DateField(verbose_name="วันสิ้นสุดสัญญา")
    project_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='planning', verbose_name="สถานะโครงการ")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_projects", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_projects", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")
    sort_order = models.IntegerField(default=500, verbose_name="ลำดับการจัดเรียง")

    def __str__(self):
        return self.project_name


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="ชื่อกลุ่มของรายการงบ")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_categories", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_categories", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    def __str__(self):
        return self.category_name


class BudgetItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('main_item', 'หัวข้อหลัก'),
        ('sub_item', 'หัวข้อย่อย'),
        ('budget_item', 'รายการงบ'),
    ]
    SUB_ITEM_CHOICES = [
        ('none', 'ไม่มี'),
        ('sub_by_item', 'ย่อยรายรายการ'),
        ('sub_by_month', 'ย่อยรายเดือน'),
        ('sub_by_day', 'ย่อยรายวัน'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="โครงการ")
    budget_item_name = models.CharField(max_length=500, verbose_name="ชื่อรายการงบ")
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณได้รับจัดสรร")
    operating_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบดำเนินการ")
    procurement_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="งบประมาณซื้อจ้าง")
    contract_sign_date = models.DateField(verbose_name="วันลงนามสัญญาจ้าง")
    contract_end_date = models.DateField(verbose_name="วันสิ้นสุดสัญญา")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="กลุ่มของรายการงบ")
    main_budget_item = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="รายการงบหลัก")
    item_type = models.CharField(max_length=50, choices=ITEM_TYPE_CHOICES, default='main_item', verbose_name="ประเภทของรายการงบ")
    sub_item_type = models.CharField(max_length=50, choices=SUB_ITEM_CHOICES, default='none', verbose_name="ประเภทของรายการย่อย")
    sort_number = models.CharField(max_length=255, verbose_name="หมายเลขลำดับ")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_budget_items", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_budget_items", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    def __str__(self):
        return self.budget_item_name

MONTH_CHOICES = [
        (1, "มกราคม"), (2, "กุมภาพันธ์"), (3, "มีนาคม"), (4, "เมษายน"),
        (5, "พฤษภาคม"), (6, "มิถุนายน"), (7, "กรกฎาคม"), (8, "สิงหาคม"),
        (9, "กันยายน"), (10, "ตุลาคม"), (11, "พฤศจิกายน"), (12, "ธันวาคม")
    ]

class MonthlyPlan(models.Model):
    budget_item = models.ForeignKey(BudgetItem, on_delete=models.CASCADE, verbose_name="รายการงบ")
    month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, verbose_name="เดือน")
    year = models.PositiveIntegerField(verbose_name="ปี")
    planned_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="แผนสำหรับเดือนนั้น")
    actual_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="ผลที่ได้สำหรับเดือนนั้น")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_monthly_plans", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_monthly_plans", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    def __str__(self):
        return f"{self.budget_item} - {self.month} {self.year}"

class TypeInvoice(models.Model):
    invoice_type_name = models.CharField(max_length=255, verbose_name="ชื่อประเภทใบแจ้งหนี้")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_invoice_types", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_invoice_types", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    def __str__(self):
        return self.invoice_type_name


class Invoice(models.Model):
    fiscal_year = models.ForeignKey(BudgetYear, null=True, blank=True, on_delete=models.CASCADE, verbose_name="ปีงบประมาณ")
    invoice_type = models.ForeignKey(TypeInvoice, null=True, blank=True, on_delete=models.CASCADE, verbose_name="ประเภทใบแจ้งหนี้")
    invoice_number = models.CharField(max_length=255, verbose_name="เลขที่ใบแจ้งหนี้")
    invoice_date = models.DateField(null=True, blank=True, verbose_name="วันที่แจ้งหนี้")
    total_amount_due = models.PositiveIntegerField(default=0, verbose_name="รวมเงินที่ต้องชำระ")
    approval_date = models.DateField(null=True, blank=True, verbose_name="วันที่อนุมัติ")
    approver_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="ผู้ขออนุมัติ")
    contractor_name = models.CharField(null=True, blank=True, max_length=255, verbose_name="ชื่อผู้รับจ้าง")
    details = models.TextField(null=True, blank=True, verbose_name="รายละเอียด")
    invoice_month = models.PositiveSmallIntegerField(choices=MONTH_CHOICES, default=1, verbose_name="รายการงบเดือน")
    invoice_year = models.PositiveIntegerField(default=2567, verbose_name="รายการงบปี")
    # attached_file = models.ForeignKey('File', null=True, blank=True, on_delete=models.CASCADE, verbose_name="เอกสารแนบ")
    # attached_image = models.ForeignKey('Image', null=True, blank=True, on_delete=models.CASCADE, verbose_name="รูปภาพประกอบ")

    
    budget_item = models.ForeignKey(BudgetItem, null=True, blank=True, on_delete=models.CASCADE, verbose_name="รายการงบ")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_invoice", verbose_name="ผู้เพิ่มข้อมูล")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="edited_invoice", verbose_name="ผู้แก้ไขข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไขล่าสุด")

    def __str__(self):
        return self.invoice_number

class File(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/files/%Y/%m/%d/', null=True, blank=True, verbose_name='ไฟล์ที่เกี่ยวข้อง')
    file_name_original = models.CharField(max_length=255, verbose_name="ชื่อไฟล์เดิม")
    file_type = models.CharField(max_length=50, verbose_name="ประเภทไฟล์")
    file_size = models.PositiveIntegerField(verbose_name="ขนาดไฟล์")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_files", verbose_name="ผู้เพิ่มข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")

    def __str__(self):
        return self.file_name_original

class Image(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="images", on_delete=models.CASCADE)
    file = models.ImageField(upload_to='uploads/images/%Y/%m/%d/', null=True, blank=True, verbose_name='รูปภาพประกอบ')
    file_name_original = models.CharField(max_length=255, verbose_name="ชื่อไฟล์เดิม")
    file_type = models.CharField(max_length=50, verbose_name="ประเภทไฟล์")
    file_size = models.PositiveIntegerField(verbose_name="ขนาดไฟล์")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="added_images", verbose_name="ผู้เพิ่มข้อมูล")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")

    class Meta:
        verbose_name = 'รูปภาพประกอบ'
        verbose_name_plural = 'รูปภาพประกอบ'

    def save(self, *args, **kwargs):
        if self.file:
            self.file_type = self.file.file.content_type
            self.file_size = self.file.size
            # Save original file name before renaming
            count = Image.objects.filter(file_name_original=self.file.name).count()
            if count > 0:
                base_name, extension = os.path.splitext(self.file.name)
                self.file_name_original = f"{base_name}({count}){extension}"
            else:
                self.file_name_original = self.file.name
            self.process_image()
        super().save(*args, **kwargs)
    
    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        random_str = ''.join(random.choices(characters, k=length))
        return random_str

    def process_image(self):
        if self.file:
            # Open the image
            img = PILImage.open(self.file)
            # Convert to RGB if image has alpha channel
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Resize the image
            # Calculate new dimensions (20% of original size)
            original_width, original_height = img.size
            new_width = int(original_width * 1)
            new_height = int(original_height * 1)
            output_size = (new_width, new_height)
            # Resize the image
            img.thumbnail(output_size, PILImage.Resampling.LANCZOS)
            # Convert image back to InMemoryUploadedFile to save to ImageField
            image_io = BytesIO()
            img.save(image_io, format='WEBP', quality=80)
            image_io.seek(0)
            # Set the image field to the new resized image
            self.file = InMemoryUploadedFile(
                image_io, 'ImageField', f"{self.generate_random_string(12)}.webp", 'image/webp', image_io.getbuffer().nbytes, None
            )
            
    def __str__(self):
        return f"self.file_name_original"