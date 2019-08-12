from django.db import models
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import *
from django.dispatch import receiver
from django.utils import timezone, six

from django.contrib.auth.models import User,AbstractBaseUser,AbstractUser
# Create your models here.

TYPEMODEL=(("Mammography","M"),("Numirique","N"),)

class ModelVersion(models.Model):
    version = models.IntegerField()
    accuracy = models.FloatField()
    date = models.DateTimeField()
    time = models.DurationField()
    typem = models.CharField(choices=TYPEMODEL,max_length=25)
    file = models.FileField(upload_to='mod/', verbose_name="")

#doctor user
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True,null=True)
    specialty=models.CharField(max_length=250)
    establishment=models.CharField(max_length=100)
    #phone_establishment=models.CharField(max_length=15,)
    photo=models.FileField(upload_to='images/', default="images/default.jpg", verbose_name="")

    def get_teen_mammographys(self):
        list = Mammography.objects.raw("select m.id,m.user_id,m.mammography from AideCan_Mammography m where m.id not in (select d.mammography_id from AideCan_Diagnostic d where D.user_id =="+str(self.id)+") ORDER BY RANDOM()")[:1]
        return list
    def get_non_labled_mammogrphies(self):
        list = Mammography.objects.raw("select m.id,m.user_id,m.mammography from AideCan_Mammography m where m.user_id =="+str(self.id)+" and m.id not in (select d.mammography_id from AideCan_Diagnostic d where D.user_id =="+str(self.id)+")")
        return list

    #TODO:: -last 10 diagnostics - all diagnostics - all mammography added



#mamography

class Mammography(models.Model):
    user=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    mammography=models.FileField(upload_to='images/', null=True, verbose_name="")






BACKGROUND_TISSUE = (

    ("F","Fatty"),
    ("G","Fatty-glandular"),
    ("D","Dense-glandular"),
)

ABNORMALITY_PRESENT=(

    ("CALC" , "Calcification"),
    ("CIRC" , "Well - defined / circumscribed masses"),
    ("SPIC" , "Spiculated masses"),
    ("MISC" , "Other, ill - defined masses"),
    ("ARCH" , "Architectural distortion"),
    ("ASYM" ,"Asymmetry"),
    ("NORM" , "Normal"),
)

SEVERITY_OF_ABNORMALITY=(

    ("M","Malignant"),
    ("B","Benign"),

)


#diagnostic
class Diagnostic(models.Model):
    mammography=models.ForeignKey(Mammography,on_delete=models.CASCADE)
    user=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    #rate=models.FloatField()
    background_tissue=models.CharField(choices=BACKGROUND_TISSUE,max_length=16)
    abnormality_present=models.CharField(choices=ABNORMALITY_PRESENT,max_length=40)
    Severity_of_abnormality=models.CharField(choices=SEVERITY_OF_ABNORMALITY,max_length=10,null=True,blank=True)
    Cercle=models.TextField(null=True,blank=True)
    comment=models.TextField(null=True,blank=True)
    date=models.DateField(default=timezone.now().date())





