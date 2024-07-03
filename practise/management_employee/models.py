from django.db import models


# Create your models here.
class Employee(models.Model):
    fullname = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='employee_photos', null=True, blank=True)
    
    def __str__(self):
        return self.fullname