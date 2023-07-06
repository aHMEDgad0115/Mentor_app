from rest_framework import generics,status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UpdateUserSerializer,UserSerializers,MentorSignupSerializer,StudentSignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsStudentUser,IsMentorUser
from mentor_api.models import User,Mentor,Student,Session,Request,Review
from .serializers import CashTransferSerializer,MentorSerializer,StudentSerializer,RequestSerializer,SessionSerializer
from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer
from rest_framework.decorators import api_view

import logging
logger = logging.getLogger(__name__)





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
            'message':'Account Created Successfuly'
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
    serializer_class = UserSerializers
    def get_queryset(self):
        print("get_queryset web")
        queryset = User.objects.filter(is_mentor=True)
        track = self.request.query_params.get('track')
        username = self.request.query_params.get('username')

        if track:
            queryset = queryset.filter(track=track)
        if username:
            queryset = queryset.filter(username=username)

        return queryset
    

############################################################################################
class StudentHomePageView(generics.ListAPIView):
    serializer_class = UserSerializers

    def get_queryset(self):
        
        queryset = User.objects.filter(is_mentor=True)
        return queryset


class RequestMentorshipView(generics.CreateAPIView):
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        #logger.debug(request.data)
        student = Student.objects.get(user=request.user)
        mentor = Mentor.objects.get(pk=request.data['mentor_id'])
        request_obj = Request(student=student, mentor=mentor)
        request_obj.save()

        return Response(status=status.HTTP_201_CREATED)

class MyRequestedToMentorsView(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]
 
    def get_queryset(self):
        user = Student.objects.get(user=self.request.user)
        return Request.objects.filter(student=user)

class CancelRequestView(generics.DestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer    
    permission_classes=[permissions.IsAuthenticated]


class StudentCreatedSessionsView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        student = Student.objects.get(user = self.request.user)
        return Session.objects.filter(student = student)

############################################################################################

class RequestedFromStudentsToMeView(generics.ListAPIView):
    serializer_class = RequestSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        mentor =  Student.objects.get(user=self.request.user)
        return Request.objects.filter(mentor)

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



class MentorCreatedSessionsView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        mentor =  Mentor.objects.get( user = self.request.user)
        return Session.objects.filter(mentor = mentor)

class UpdateSessionView(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes=[permissions.IsAuthenticated&IsMentorUser]

    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        session_id = kwargs['session_id']
        session = get_object_or_404(self.queryset, id=session_id)
        session.start_time = request.data['start_time']
        session.duration = request.data['duration']
        session.zoom_link = request.data['zoom_link']

        session.save()

        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)

   





##########################################################################################

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class MentorReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        mentor_id = self.kwargs['mentor_id']  
        return Review.objects.filter(mentor=mentor_id)
    








###########################################################################################

class CashTransferView(generics.CreateAPIView):
    serializer_class = CashTransferSerializer

    def create(self, request, *args, **kwargs):
        student = self.request.user
        mentor_id = request.data.get('mentor_id')
        price = request.data.get('price')

        try:
            mentor = User.objects.get(id=mentor_id, is_mentor=True)
        except User.DoesNotExist:
            return Response({'error': 'Mentor not found'}, status=status.HTTP_404_NOT_FOUND)

        if student.cash < price:
            return Response({'error': 'Insufficient Cash'}, status=status.HTTP_400_BAD_REQUEST)

        student.cash -= price
        mentor.cash += price

        student.save()
        mentor.save()

        return Response({'message': 'Money transferred successfully'}, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def get_user_Cash(request):
    user = request.user
    cash = user.cash
    return Response({'Cash': cash}, status=status.HTTP_200_OK)