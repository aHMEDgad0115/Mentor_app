from django.urls import path
from .views import  MentorSignupView,StudentSignupView,CustomAuthToken,LogoutView,MentorOnlyView,StudentOnlyView
from .views import (
    UpdateProfileView,
    MentorSearchView,
    StudentHomePageView,
    StudentCreatedSessionsView,
    MyRequestedToMentorsView,
    RequestMentorshipView,
    CancelRequestView,
    MentorCreatedSessionsView,
    RequestedFromStudentsToMeView,
    AcceptRequestView,
    CancelMentorshipView,
    UpdateSessionView,
    ReviewCreateView,
    MentorReviewsView,
    CashTransferView,
    get_user_Cash,
)


urlpatterns =[
    path('signup/mentor/', MentorSignupView.as_view()),
    path('signup/student/', StudentSignupView.as_view()),
    path('login/',CustomAuthToken.as_view(),name='auth-token'),
    path('logout/',LogoutView.as_view(),name='logout-view'),
    path('mentor/dashboard/',MentorOnlyView.as_view(),name='Mentor-Dashboard'),
    path('student/dashboard/',StudentOnlyView.as_view(),name='Student-Dashboard'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    # Mentor search
    path('mentors/search/', MentorSearchView.as_view(), name='mentor-search'),

    # Student dashboard
    path('student/home/', StudentHomePageView.as_view(), name='student-home'),
    path('student/sessions/created/', StudentCreatedSessionsView.as_view(), name='student-created-sessions'),
    path('student/requests/mentors/', MyRequestedToMentorsView.as_view(), name='student-requests-mentors'),
    path('student/request/mentorship/', RequestMentorshipView.as_view(), name='request-mentorship'),
    path('student/request/cancel/<int:pk>/', CancelRequestView.as_view(), name='cancel-request'),

    # Mentor dashboard
    path('mentor/sessions/created/', MentorCreatedSessionsView.as_view(), name='mentor-created-sessions'),
    path('mentor/requests/students/', RequestedFromStudentsToMeView.as_view(), name='mentor-requests-students'),
    path('mentor/request/accept/<int:pk>/', AcceptRequestView.as_view(), name='accept-request'),
    path('mentor/request/cancel/<int:pk>/', CancelMentorshipView.as_view(), name='cancel-mentorship'),
    path('mentor/session/update/<int:pk>/', UpdateSessionView.as_view(), name='update-session'),

    #Review
    path('student/review/create/', ReviewCreateView.as_view(), name='review-create'),
    path('mentors/<int:mentor_id>/reviews/', MentorReviewsView.as_view(), name='mentor_reviews'),

    #Payment
    path('cash/transfer/', CashTransferView.as_view(), name='cash-transfer'),
    path('cash/', get_user_Cash, name='get-user-cash'),


]