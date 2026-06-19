from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView

from .models import Student, Profile, LoanApplication, EligibilityResult, LoanRecommendation
from .permissions import (
    CanViewOwnApplicationOrAdminUpdate,
    HasProfileRole,
    IsAdminOrOwnObject,
    IsAdminOrSelfProfile,
    IsAdminRole,
    is_admin,
)
from .serializers import (
    ApplicationStatusUpdateSerializer,
    EligibilityResultSerializer,
    LoanApplicationSerializer,
    LoanRecommendationSerializer,
    ProfileSerializer,
    StudentSerializer,
)


class AdminStudentListView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminRole]


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [HasProfileRole]

    def get_queryset(self):
        if is_admin(self.request):
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrSelfProfile]


class LoanApplicationListView(ListAPIView):
    serializer_class = LoanApplicationSerializer
    permission_classes = [HasProfileRole]

    def get_queryset(self):
        if is_admin(self.request):
            return LoanApplication.objects.all()
        return LoanApplication.objects.filter(applicant=self.request.user.profile)


class LoanApplicationDetailView(RetrieveUpdateAPIView):
    queryset = LoanApplication.objects.all()
    permission_classes = [CanViewOwnApplicationOrAdminUpdate]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ApplicationStatusUpdateSerializer
        return LoanApplicationSerializer


class EligibilityResultListView(ListAPIView):
    serializer_class = EligibilityResultSerializer
    permission_classes = [HasProfileRole]

    def get_queryset(self):
        if is_admin(self.request):
            return EligibilityResult.objects.all()
        return EligibilityResult.objects.filter(profile=self.request.user.profile)


class EligibilityResultDetailView(RetrieveAPIView):
    queryset = EligibilityResult.objects.all()
    serializer_class = EligibilityResultSerializer
    permission_classes = [IsAdminOrOwnObject]


class LoanRecommendationListView(ListAPIView):
    serializer_class = LoanRecommendationSerializer
    permission_classes = [HasProfileRole]

    def get_queryset(self):
        if is_admin(self.request):
            return LoanRecommendation.objects.all()
        return LoanRecommendation.objects.filter(profile=self.request.user.profile)


class LoanRecommendationDetailView(RetrieveAPIView):
    queryset = LoanRecommendation.objects.all()
    serializer_class = LoanRecommendationSerializer
    permission_classes = [IsAdminOrOwnObject]
