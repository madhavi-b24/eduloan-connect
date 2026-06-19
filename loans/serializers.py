from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Student, Bank, LoanBid, Profile, LoanApplication, EligibilityResult, LoanRecommendation

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class LoanBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanBid
        fields = '__all__'


class StudentRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Profile.objects.create(user=user, role=Profile.ROLE_STUDENT)
        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'role': Profile.ROLE_STUDENT,
        }


class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        username = username_or_email
        if username_or_email and '@' in username_or_email:
            user = User.objects.filter(email=username_or_email).first()
            username = user.username if user else username_or_email

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid username/email or password.")

        if not hasattr(user, 'profile') or user.profile.role != Profile.ROLE_STUDENT:
            raise serializers.ValidationError("Only student accounts can log in here.")

        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'username',
            'email',
            'role',
            'phone',
            'apaar_id',
            'course',
            'family_income',
            'academic_score',
            'legacy_student',
        )
        read_only_fields = fields


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = (
            'id',
            'applicant',
            'legacy_student',
            'loan_product',
            'requested_amount',
            'requested_tenure_years',
            'status',
            'remarks',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ('status',)


class EligibilityResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityResult
        fields = (
            'id',
            'profile',
            'loan_product',
            'application',
            'eligible',
            'score',
            'reasons',
            'created_at',
        )
        read_only_fields = fields


class LoanRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRecommendation
        fields = (
            'id',
            'profile',
            'loan_product',
            'application',
            'rank',
            'score',
            'estimated_emi',
            'total_repayment',
            'reason',
            'created_at',
        )
        read_only_fields = fields
