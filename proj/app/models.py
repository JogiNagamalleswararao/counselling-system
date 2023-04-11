from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# app/models.py


class Login(models.Model):
    uid = models.CharField(max_length=30, primary_key=True,unique=True)
    password = models.CharField(max_length=255)
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    parent = models.BooleanField(default=False)

    def __str__(self):
        return self.uid

class Student(models.Model):
    uid = models.CharField(max_length=30,primary_key=True,unique=True)
    email = models.EmailField(max_length=255)
    password=models.CharField(max_length=255,default=f"{uid}")
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    branch = models.CharField(max_length=50)
    sec = models.CharField(max_length=10)
    mobile_num = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    mentor_name = models.CharField(max_length=50)

    def __str__(self):
        return self.uid


class Parent(models.Model):
    uid = models.CharField(max_length=30,primary_key=True,unique=True)
    Fname = models.CharField(max_length=100)
    Lname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    Email = models.EmailField()
    password=models.CharField(max_length=255,default=f"{uid}")
    mobile_num = models.CharField(max_length=100)
    mentor_name = models.CharField(max_length=100)
    
    
    def __str__(self) -> str:
        return self.uid

class Teacher(models.Model):
    uid = models.CharField(max_length=30,primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    Email = models.EmailField()
    password=models.CharField(max_length=255,default=f"{uid}")
    dep = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    des = models.CharField(max_length=100,default="None")
    def __str__(self) -> str:
        return self.uid



class Mentor(models.Model):
    student_uid = models.CharField(max_length=30,primary_key=True,unique=True)
    teacher_uid = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.teacher_uid} , {self.student_uid} "



class Fee(models.Model):
    student_uid = models.CharField(max_length=30,primary_key=True,unique=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee_pending = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Fee Details for {self.student.uid}:{self.student.fname} {self.student.lname}"

class ParentRequest(models.Model):
    # parent = models.CharField(max_length=30,primary_key=True,unique=True)
    teacher = models.CharField(max_length=30)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='requests',default=0,primary_key=True,unique=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='requests',default=0)
    message = models.TextField(blank=True,null=True)

    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.parent) + ' - ' +str(self.teacher) 
    
class Link(models.Model):
    uid = models.CharField(max_length=30,primary_key=True)
    link = models.CharField(max_length=255)
    # parent=Email = models.EmailField()

    def __str__(self):
        return str(self.uid) 
