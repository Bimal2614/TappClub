from datetime import datetime, date
from importlib.metadata import requires
from dateutil.relativedelta import relativedelta
from .permission import IsPaid
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import (
    SocialMediaSerializer,
    Registration_serializer,
    Changeprofileserializer,
    membershipserializer,
    W9form,
)
from rest_framework.response import Response
from .models import Profile, SocialMedia, referral, saveContect, ForgotPass, History, Membership, WNineForm
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import SavecontectSerializers, Historyserializer
import uuid
import jwt
from django.conf import settings

# from django.db.models import F
from .serializers import profileserializer

# from user.serializers import UserSerializer
from user.utils import generate_access_token, generate_refresh_token
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)

User = get_user_model()

# Register

@api_view(["POST"])
def registration_view(request):
    if request.method == "POST":
        if not "email" in request.data:
            return Response(
                {"error": "User email not provided"}, status=status.HTTP_404_NOT_FOUND
            )
        if "referred_by" in request.data:
            try:
                usere_referrer = User.objects.get(
                    referralCode=request.data.get("referred_by")
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User Referrer does not exists"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        serializer = Registration_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data["response"] = "Response Created"
            # data['username'] = account.username
            data["email"] = account.email
            data["user_id"] = account.id
            user = User.objects.get(id=account.id)
            # user.is_subscribed = True
            # user.save()
            validated_date = datetime.now() + relativedelta(days=+7)
            model = Membership(user=user, validate_till=validated_date)
            model.save()
            # send_mail("Link to activate account", f"This is Tapp club{token_varify(user)}", settings.EMAIL_HOST_USER, [user.email,])
            if "referred_by" in request.data:
                try:
                    usere_referrer = User.objects.get(
                        referralCode=request.data.get("referred_by")
                    )
                    try:
                        referralUser = referral.objects.get(user_referee=usere_referrer)
                        level = referralUser.level
                    except:
                        level = 0
                    referealModel = referral(
                        user_referrer=usere_referrer, user_referee=user, level=level + 1
                    )
                    referealModel.save()

                except Exception as a:
                    print(a)
                    return Response(
                        {"error": "User Referrer does not exists"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                parents(request, user)

            # user.referralCode = request.data['referralCode'] if 'referralCode' in request.data else None
            # user.user_name = request.data['user_name'] if 'user_name' in request.data else None
            # profile = Profile(Name = request.data['name'], Profilepic=request.data['profile_pic'], JobTitle = request.data['job_Title'] if 'job_Title' in request.data else None, PhoneNum = request.data['phone_num'],Linkdin = request.data['linkdin'] if 'linkdin' in request.data else '', Twitter = request.data['twitter'] if 'twitter' in request.data else  '', BusinessName = request.data['business_name'] if 'business_name' in request.data  else None, PicOrVideo = request.data['picOrvideo'], Email = request.data['email'], user = user)
            # profile.save()
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            data["access_token"] = access_token
            data["refresh_token"] = refresh_token
        else:
            data = serializer.errors
        return Response(data)

# Profile : Get, Post, Put, Delete


class AddProfile(APIView):

    permission_classes = [IsAuthenticated, IsPaid]

    def post(self, request):
        try:
            if Profile.objects.filter(user_name=request.data["user_name"]).exists():
                return Response(
                    {"error": " username exists"}, status=status.HTTP_400_BAD_REQUEST
                )
            if Profile.objects.filter(
                user=request.user, is_business=request.data["is_business"]
            ).exists():
                return Response(
                    {"error": " user exists"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Profile.DoesNotExist:
            pass
        # if (
        #     not User.objects.get(email=request.user.email).is_subscribed
        # ) and request.data.get("is_business"):
        #     return Response(
        #         {"error": "This is For subscribed user only"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        serializer = profileserializer(data=request.data)
        if serializer.is_valid():
            # token = request.headers.get('Authorization').split()
            # payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class GetProfile(APIView):

    permission_classes = [IsAuthenticated, IsPaid]

    def get(self, request):
        """
        required
        """
        try:
            # token = request.headers.get('Authorization').split()
            # payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
            personal = request.data.get("is_business")
            # print(personal, "is_business")
            model = Profile.objects.get(user=request.user, is_business=personal)
        except Exception as e:
            return Response({"error": "Not created"}, status=status.HTTP_404_NOT_FOUND)
        serializer = profileserializer(model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        is_business = request.data.get("is_business")
        model = Profile.objects.get(user=request.user, is_business=is_business)
        serializer = Changeprofileserializer(model, request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            token = request.headers.get("Authorization").split()
            payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_404_NOT_FOUND
            )
        is_business = request.data.get("is_business")
        model = Profile.objects.get(user=payload["user_id"], is_business=is_business)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Social Media: 
class SocialMediaView(APIView):
    permission_classes = [IsAuthenticated, IsPaid]
    # def get(self, request):
    #     try:
    #         token = request.headers.get('Authorization').split()
    #         payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
    #         model = SocialMedia.objects.filter(user= payload['user_id'])
    #         # model2 = User.objects.get(id=payload['user_id'])
    #     except Exception as e:
    #         return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = profileserializer(model, many= True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = SocialMediaSerializer(data=request.data)
        # user_profile = request.data['profile_id']
        is_business = request.data["is_business"]
        try:
            profile = Profile.objects.get(user=request.user, is_business=is_business)
            if SocialMedia.objects.filter(
                user_profile=profile, platform=request.data.get("platform")
            ).exists():
                return Response(status=status.HTTP_201_CREATED)
        except Exception as a:
            print(a)
            return Response(
                {"error": "You have to first create Profile"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # print(serializer, "serializer")
        if serializer.is_valid():
            serializer.save(user_profile=profile)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SocialMediaV(APIView):

    permission_classes = [IsAuthenticated, IsPaid]

    def get(self, request):
        is_business = request.data["is_business"]
        profile = Profile.objects.get(user=request.user, is_business=is_business)
        model = SocialMedia.objects.filter(user_profile=profile)
        serializer = SocialMediaSerializer(model, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        model = SocialMedia.objects.get(id=pk)
        # print(model)
        serializer = SocialMediaSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        model = SocialMedia.objects.get(id=pk)
        # print(model)
        model.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)




def parents(request, user):

    count = 6
    referralCode = request.data.get("referred_by")
    while count > 0:
        user_referrer = User.objects.get(referralCode=referralCode)
        sub_user = Membership.objects.get(user=user_referrer)
        if user_referrer.is_subscribed and sub_user.validate_till >= date.today():
            user_referrer.total_earned += 10
            user_referrer.save()
        try:
            user = referral.objects.get(user_referee=user_referrer)
            referralCode_ = User.objects.get(
                email=user.user_referrer.email
            ).referralCode
            referralCode = referralCode_
            # print(referralCode.referralCode  , "user")

        except Exception as e:
            break
        count -= 1


# except User.DoesNotExist:
#     return Response({"error": "User Referrer does not exists"}, status = status.HTTP_404_NOT_FOUND)

# def token_varify(object_user):
#     link = uuid.uuid4()
#     varificationLink = f"user/varify/{link}"
#     profile = verifyProfile(user=object_user, token = link)
#     profile.save()
#     return varificationLink

class HistoryView(APIView):

    def get(self ,request):
        try:
            history = []
            model = History.objects.filter(user = request.user)
            serializers = Historyserializer(model, many =True)
            for i in serializers.data:
                profile = Profile.objects.get(id=i.get('saved'))
                serializer = profileserializer(profile)
                name = "TappClub"
                if not serializer.data.get("name") == "":
                    name = serializer.data.get("name")
                history.append(
                    {
                            # "User_ispaid": i.user_id.is_subscribed,
                            "Name": name,
                            # "Profile_id": serializer.data.get("id"),
                            "is_business":serializer.data.get("is_business"),
                            "User_name": serializer.data.get("my_name"), 
                            "profilePic": serializer.data.get("profilepic"),
                            "user_name": serializer.data.get("user_name"),
                        }
                )

            return Response({"Userhistory": history}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({"error": exception}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def varify(request, slug):

#     try:
#         instance = verifyProfile.objects.get(token=slug)
#         user = User.objects.get(email = instance.user.email)
#         if user.is_verified == True:
#             return Response("You have already verified your account")
#         instance.is_verified = True
#         user.is_verified = True
#         user.save()
#         instance.save()
#     except:
#         return Response({'error': 'Something wrong with Link'})
#     return Response(status=status.HTTP_200_OK)


class forgot_password(APIView):
    def post(self, request):
        email = str(request.data.get("email")).lower()
        # print(email)
        # if ForgotPass.objects.filter(email = email).exists():
        # ForgotPass.objects.filter(email = email).delete()
        link = uuid.uuid4()
        # print(link)
        # print(email)
        varificationLink = f"user/varify_forgot_password/{link}"
        try:
            user = User.objects.get(email=email)
            user = ForgotPass(email=email, user=user, token=link)
            user.save()
            return Response(
                {"varification_Link": varificationLink}, status=status.HTTP_200_OK
            )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def varify_forgot_password(request, slug):
    try:
        # print(request.data)
        new_password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        if not len(new_password) > 0:
            return Response({"error": "len(password) must be > 1"})
        if new_password == confirm_password:
            print("Hey")
            user = ForgotPass.objects.get(token=slug)
            # print(user)
            instance = User.objects.get(email=user.email)
            instance.set_password(new_password)
            instance.save()
            ForgotPass(user=instance).delete()
        else:
            return Response({"error": "password must be same"})
    except:
        return Response({"error": "Invalid Link"})
    return Response(status=status.HTTP_200_OK)


# Back Office :Get and W9form #ToDo


class Office(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        members_list = []
        ids = []
        user = User.objects.get(email=request.user.email).total_earned
        mlm_users(0, request.user, ids, members_list)
        # for i in range(len(ids)):
        #     user = User.objects.get(email=ids[i])
        #     mlm_users(user, ids, members_list)
        # while True:
        #     user = request.user
        #     try:
        #         member = referral.objects.filter(user_referrer=user)
        #         for i in member:
        #             try:
        #                 print(i)
        #                 ids.append(i.user_referee.email)
        #                 serializer = ReferralSerializer(i)
        #                 members_list.append(serializer.data)
        #             except:
        #                 break
        #         else:
        #             break

        #     except:
        #         break
        # print(ids)
        return Response({"members": members_list, "total_income": user}, status=status.HTTP_200_OK)

class formVie(APIView):
    permission_classes = [IsAuthenticated, IsPaid]  

    def post(self, request):
        serializer = W9form(data=request.data)
        if serializer.is_valid():
            if not WNineForm.objects.filter(user = request.user).exists():
                serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            model = WNineForm.objects.filter(user = request.user).first()
            serializer = W9form(model)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_Bad_REQUEST)

    def put(self, request):
        model = WNineForm.objects.filter(user = request.user).first()
        serializer = W9form(model, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# Save connections

class SaveContectView(APIView):

    permission_classes = [IsAuthenticated, IsPaid]

    def post(self, request):
        # print(request.data)
        try:
            if saveContect.objects.get(
                user_id=request.user, profile_id=request.data.get("profile_id")
            ):
                return Response(status=status.HTTP_201_CREATED)
        except saveContect.DoesNotExist:
            serializers = SavecontectSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save(user_id=request.user)
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            # user = User.objects.get(id=request.user)
            # print(user.id)
            model = saveContect.objects.filter(user_id=request.user)
            print(request.user)
            list_profile = []
            for i in model:

                id = i.profile_id.id
                print(i.user_id)
                profile = Profile.objects.get(id=id)
                pro_ser = profileserializer(profile)
                name = 'TappClub'
                if not pro_ser.data.get("name") == "":
                    name = pro_ser.data.get("name")
                list_profile.append(
                        {
                            # "User_ispaid": i.user_id.is_subscribed,
                            "Name": name,
                            "Profile_id": pro_ser.data.get("id"),
                            "is_business":pro_ser.data.get("is_business"),
                            "User_name": pro_ser.data.get("my_name"), 
                            "profilePic": pro_ser.data.get("profilepic"),
                            "user_name": pro_ser.data.get("user_name"),
                        }
                )

            # print(list_profile, "List of profiles are")
            return Response({"saved_contect": list_profile}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Exists"}, status=status.HTTP_404_NOT_FOUND)
 
    # def delete(self, request):
    #     data = saveContect.objects.get(user_id = request.user, profile_id = request.data.get('profile_id'))
    #     data.delete()
    #     return Response(status=status.HTTP_200_OK)


# Membership date

class MembershipView(APIView):
    permission_classes = [IsAuthenticated, IsPaid]

    def get(self, request):
        try:
            model = Membership.objects.get(user=request.user)
            serialize = membershipserializer(model)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

def mlm_users(id, user, ids, members_list):
    member = referral.objects.filter(user_referrer=user)
    for i in member:
        try:
            ids.append(i.user_referee.email)
            try:
                profile = Profile.objects.get(user = i.user_referee, is_business = False)
                serielizer = profileserializer(profile)
                pic = serielizer.data.get('profilepic')
                if serielizer.data.get("name") != "":
                    name = serielizer.data.get('name')
                else:
                    name = 'TappClub'
                # pic = profile.profilepic
            #     name = profile.name if profile.name else 'TappClub'
            #     print("Try")
            except:
                pic = '/static/default.jpg'
                name = 'TappClub'
                # print("Except")
            # serializer = ReferralSerializer(i)

            members_list.append({"name": name,
                                  "pic": pic,
                                  "email":i.user_referee.email,
                                  "is_paid": i.user_referee.is_subscribed})

        except Exception as e:
            print(e)
    else:
        try:
            user = User.objects.get(email=ids[id])
            id += 1
            mlm_users(id, user, ids, members_list)
        except Exception as e:
            print(e)
            return ids


# return ids


# try:
#     print(i)
#     if Profile.objects.filter(user = i.user_referee, is_business = False).exists():
#         print("Hey")
#         profile = Profile.objects.get(user = i.user_referee, is_business = False)
#     else:
#         print(i.referee)
#         profile = Profile.objects.get(user = i.user_referee, is_business = True)
#         print(profile)
#     ids.append({"user": profile.user_name, "profile":profile.profilepic, "is_varified": i.user_referee.is_subscribed})
#     # serializer = ReferralSerializer(i)
#     members_list.append(i.user_referee.email)
# except Exception as e:
#     print(e)

class UserPersonalLink(APIView):
    def get(self, request, pk):
        try:
            model = Profile.objects.get(user_name=pk)
            serializer = profileserializer(model)
            user = False
            if request.user.is_authenticated:
                if not History.objects.filter(user=request.user, saved = model).exists():
                    history = History(user=request.user, saved = model)
                    history.save()
                if saveContect.objects.filter(user_id=request.user, profile_id= model).exists():
                    
                    user= True

            return Response({"profile": serializer.data, "is_saved":user}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Invalid user name"}, status=status.HTTP_404_NOT_FOUND
            )


# User from access
# try:
#     token = request.headers.get('Authorization').split()
#     payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
# except Exception:
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
