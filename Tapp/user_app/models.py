import profile
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):

    profilepic = models.ImageField(upload_to='profilepic', default='../static/default.jpg')
    name = models.CharField(max_length=150, blank=True)  
    user_name = models.CharField(max_length=10, unique=True)
    profession = models.CharField(max_length=200, blank = True)
    aboutMe = models.TextField(blank=True)
    address = models.TextField(blank=True)
    # PicOrVideo = models.FileField(upload_to='media/PicOrVideo', blank= True)
    is_business = models.BooleanField()
    contact_no = models.CharField(max_length=13,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    my_role = models.CharField(max_length=200, blank=True)
    my_name = models.CharField(max_length=100, blank=True, default ="")

    class Meta:
        unique_together = [['user', 'is_business']]

    def __str__(self):
        return self.name + " | " + self.user_name + " | " + str(self.user.email)

class WNineForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=200)
    Business_name = models.CharField(max_length=500)
    Tax_classification = models.CharField(max_length=100)
    PayeeCode = models.CharField(max_length=100, blank=True)
    FATCA = models.CharField(max_length=100) 
    Address = models.TextField()
    Address2 = models.TextField()
    List_account_number = models.CharField(max_length= 200, blank=True)
    Social_security_Taxt_Number = models.CharField(max_length=100)

    class Meta:
        unique_together = [['user', 'Social_security_Taxt_Number']]

    def __str__(self) -> str:
        return self.user.email

class SocialMedia(models.Model):
    platform = models.CharField(max_length=20, blank = False, null= True)
    addofplt = models.CharField(max_length=2083, null=True, blank = False)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="socialMedia")
 
    class Meta:
        unique_together = [['user_profile', 'platform']]

    def __str__(self):
        return  str(self.platform) + " | "+ str(self.user_profile)

class referral(models.Model):

    user_referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrar")
    user_referee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='referee')
    level = models.IntegerField(default=0)

    def __str__(self):
        return "referrer : {0}, referee: {1}".format(self.user_referrer.email, self.user_referee.email)

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Member")
    # start_date = m odels.DateField()
    validate_till = models.DateField()
# class verifyProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token = models.CharField(max_length=100)
#     is_varified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email) + " 's membership is validated till : |" + str(self.validate_till)

class ForgotPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    email = models.EmailField()
    is_varified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_saver')
    saved = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'user_saved')

    def __str__(self):
        return str(self.user.email) + "| " + str(self.saved.user_name)
class saveContect(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_saver")
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='to_save', unique=True)

    class Meta:
        unique_together = ['user_id', 'profile_id']

    def __str__(self):
        return self.user_id.email + "    has saved   - Id" + str(self.profile_id.id)


# Personal: Name, Links of Social Media accounts, Profile Pic, Phone Num, Bio, Profession, email
# Business: Business Name, Logo, Social Accounts, Contact No, About, Business Title like (text tile, Angadiya), email
# -Atyare aatli field rakhu 6u
# class Subscription(models.Model):
#     user = models.ForeignKey()
     
# class WNineForm(models.Model):
#     user 

# class saved_contacts(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     saved_user = models.ForeignKey(User, on_delete=models.CASCADE)
 