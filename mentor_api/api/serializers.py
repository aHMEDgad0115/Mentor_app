from rest_framework import  serializers
from mentor_api.models import User, Mentor, Student,Session,Request,Review


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'

class MentorSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Mentor
        fields = ['user','id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        mentor = Mentor.objects.create(user=user, **validated_data)
        return mentor

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Student
        fields = ['user','id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student
class MentorSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model =User
        fields =['username','email','password','password2','first_name','last_name']
        extra_kwargs={
            'password':{'style':{"input_type":"password"},'write_only':True}
        }

    def save(self,**kwargs):
        user=User(
            username= self.validated_data['username'],
            email=self.validated_data['email']
        )    
        password=self.validated_data['password']
        password2= self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':'password does not match'})
        user.set_password(password)
        user.is_mentor= True
        user.save()
        Mentor.objects.create(user=user)
        return user


class StudentSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"},write_only=True)
    class Meta:
        model =User
        fields =['username','email','password','password2','first_name','last_name']
        extra_kwargs={
            'password':{'style':{"input_type":"password"},'write_only':True}
        }

    def save(self,**kwargs):
        user=User(
            username= self.validated_data['username'],
            email=self.validated_data['email']
        )    
        password=self.validated_data['password']
        password2= self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':'password doesnot match'})
        user.set_password(password)
        user.is_student= True
        user.save()
        Student.objects.create(user=user)
        return user    





class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'mentor', 'student', 'accepted']

class SessionSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer()
    student = StudentSerializer()
    request = RequestSerializer()

    class Meta:
        model = Session
        fields = ['mentor', 'student', 'request','start_time','duration','zoom_link']





class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['student', 'mentor', 'rating', 'feedback', 'created_at']



class CashTransferSerializer(serializers.Serializer):
    mentor_id = serializers.IntegerField()
    price = serializers.IntegerField()
