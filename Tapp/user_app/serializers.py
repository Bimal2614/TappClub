from rest_framework import serializers
from .models import Membership, Profile, SocialMedia, saveContect, referral, History, WNineForm
# from django.conf import settings

# User = settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()



class Registration_serializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
 
    def save(self):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        # if not self.validated_data['email']:
        #     raise serializers.ValidatioError('email is must')
        if password != confirm_password:
            raise serializers.ValidationError({'errot': "password must be same"})
        if User.objects.filter(email=str(self.validated_data['email']).lower()).exists():
            raise serializers.ValidationError({'error': "email must not be same"})
        account = User.objects.create_user(self.validated_data['email'], password)
        # account.set_password(password)
        # account.save()

        return account

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        exclude = ['user_profile']

class W9form(serializers.ModelSerializer):

    class Meta:
        model = WNineForm
        exclude = ['user']

class SavecontectSerializers(serializers.ModelSerializer):

    class Meta:
        model = saveContect
        exclude = ['user_id']

class profileserializer(serializers.ModelSerializer):

    socialMedia = SocialMediaSerializer(many= True, read_only = True)
    # to_save = SavecontectSerializers(read_only=True, many= True)

    class Meta:
        model = Profile
        exclude = ['user']

class membershipserializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = "__all__"


class Changeprofileserializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['user_name', 'user', "is_business"]

    # def save(self,user):
    #     user_name = self.validated_data['user_name']
    #     if Profile.objects.get(user_name=user_name).exists():
    #         raise ValueError("username must be unique")
    #     profile = self.validated_data['is_business']
    #     if not profile:
    #         mdl = Profile(name = self.validated_data['name'], profession=self.validated_data['profession'], aboutMe=self.validated_data['aboutMe'],is_business = self.validated_data['is_business'],email = self.validated_data['email'], contact_no = self.validated_data['contact_no'],profilepic=self.validated_data['profilepic'],user=user)
    #         mdl.save()
        # else:
        #     # mdl = Profile(my_role = self.validated_data['my_role'], my_name=self.validated_data['my_name'])
        #     # mdl.save()
        #     pass
        # return mdl
# name = self.validated_data['name'], profession=self.validated_data['profession'],user=user, aboutMe=self.validated_data['aboutMe'],is_business = self.validated_data['is_business'],email = self.validated_data['email'], contact_no = self.validated_data['contact_no'],profilepic=self.validated_data['profilepic'],


class SavecontectSerializersGet(serializers.ModelSerializer):
    
    # to_save = profileserializer(read_only=True)

    class Meta:
        model = saveContect
        fields = [  'profile_id']

class Historyserializer(serializers.ModelSerializer):

    profile = profileserializer(read_only=True)
    class Meta:
        model = History
        fields = ['saved', 'profile']

class Userserializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ['user']




# Registration_serializer
    # if User.objects.filter(user_name=self.validated_data['user_name']).exists():
    #     raise serializers.ValidationError({'error': "user_name must not be same"})
    # try:
    #     if self.validated_data['referred_by']:
    #         referred_by = self.validated_data['referred_by']
    # except Exception:
    #     referred_by = None
    # if User.objects.filter(user_name=self.validated_data['referred_by']).exists():
    #     raise serializers.ValidationError({'error': "referred_by must not be same"})