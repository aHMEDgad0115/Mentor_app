from rest_framework import generics,status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UpdateUserSerializer,UserSerializers,MentorSignupSerializer,StudentSignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsStudentUser,IsMentorUser
from mentor_api.models import User,Mentor,Student,Session,Request
from .serializers import MentorSerializer,StudentSerializer,RequestSerializer,SessionSerializer






class MentorSignupView(generics.GenericAPIView):
    serializer_class = MentorSignupSerializer
    def post(self, request,*args,**kwargs):
        serializer=self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            'user':UserSerializers(user,context= self.get_serializer_context()).data,
            'token':Token.objects.get(user= user).key,
            'message':'Account Create Successfuly'
        })

    


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)

        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_student':user.is_student
        })



class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)




class StudentSignupView(generics.GenericAPIView):
    serializer_class = StudentSignupSerializer
    def post(self, request,*args,**kwargs):
        serializer=self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            'user':UserSerializers(user,context= self.get_serializer_context()).data,
            'token':Token.objects.get(user= user).key,
            'message':'Account Create Successfuly'
        })




class StudentOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsStudentUser]
    serializer_class =UserSerializers

    def get_object(self):
        return self.request.user
    



class MentorOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsMentorUser]
    serializer_class =UserSerializers

    def get_object(self):
        return self.request.user    
    






class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer



class MentorSearchView(generics.ListAPIView):
    serializer_class = MentorSerializer

    def get_queryset(self):
        queryset = Mentor.objects.all()
        track = self.request.query_params.get('track')
        name = self.request.query_params.get('name')

        if track:
            queryset = queryset.filter(track=track)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
    


class StudentHomePageView(generics.ListAPIView):
    serializer_class = MentorSerializer

    def get_queryset(self):
        return Mentor.objects.all()

class MyCreatedSessionsView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(student=user.student)

class MyRequestedToMentorsView(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(student=user.student)

class RequestMentorshipView(generics.CreateAPIView):
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        student = request.user.student
        mentor = Mentor.objects.get(pk=request.data['mentor_id'])
        
        request_obj = Request(student=student, mentor=mentor)
        request_obj.save()

        return Response(status=status.HTTP_201_CREATED)

class CancelRequestView(generics.DestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer    
    permission_classes=[permissions.IsAuthenticated]





class MyCreatedSessionsView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(mentor=user.mentor)

class RequestedFromStudentsToMeView(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Request.objects.filter(mentor=user.mentor)

class AcceptRequestView(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accepted = True
        instance.save()

        session = Session(mentor=instance.mentor, student=instance.student, request=instance)
        session.save()

        return Response(status=status.HTTP_200_OK)

class CancelMentorshipView(generics.DestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]


class UpdateSessionView(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes=[permissions.IsAuthenticated&IsMentorUser]

    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()