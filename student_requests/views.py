from rest_framework import generics, mixins
from rest_framework.views import APIView
from .models import CorrectionTemporaryRequests, TermDropRequest
from .serializers import CorrectionRequestSerializer, CorrectionShowSerializer, TermDropSerializer
from rest_framework.response import Response
from rest_framework import status
from users.models import Student
from  .permissions import IsStudent, IsDeputyEducational
from rest_framework import serializers
from .tasks import send_email_task, alaki
from courses.models import Term, StudentCourse

from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from datetime import datetime

class CreateCorrectionRequestByStudent(generics.GenericAPIView):
    queryset = CorrectionTemporaryRequests.objects.all()
    serializer_class = CorrectionRequestSerializer
    # permission_classes = [IsStudent]

    def get(self, request, pk):
        studnet = Student.objects.get(id=pk)
        return Response({'studnet': f'{studnet.first_name} {studnet.last_name}','details': 'add or remove'}, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['student'] = student
        serializer.save()
        return Response({'detail': 'Pre Request Created'}, status=status.HTTP_201_CREATED)

class DetailCorrectionRequestByStudent(APIView):
    # permission_classes = [IsStudent]
    def get(self, request, pk):
        correction_requests = CorrectionTemporaryRequests.objects.filter(student__id=pk)
        serializer = CorrectionShowSerializer(correction_requests, many=True)
        studnet = Student.objects.get(pk=pk)
        return Response({'Student Name': studnet.first_name,'requests':serializer.data}, status=status.HTTP_200_OK)

class CorrectionShowErrors(APIView):
    def get(self, request, pk):
        errors = {}
        student = Student.objects.get(id=pk)
        add_remove_list = CorrectionTemporaryRequests.objects.filter(student=student)
        print(student.passed_courses.all())
        a = [1,2]
        b = [1 , 2, 3, 4]
        print(all(x in b for x in a))
        for add_remove in add_remove_list:
            errors[add_remove.select_course.course.name] = []
            # print(add_remove.select_course.course.pre_requisites.all() in student.passed_courses.all())
            print(all(prerequisite in student.passed_courses.all() for prerequisite in add_remove.select_course.course.pre_requisites.all()))
        return Response(errors, status=status.HTTP_200_OK)
    



class AssistantRemoveTermList(generics.ListAPIView):
    queryset = TermDropRequest.objects.all()
    serializer_class = TermDropSerializer
    permission_classes = [IsDeputyEducational]
    # def get(self, request):
    #     current_time = datetime.now()
    #     current_term = Term.objects.get(start_course_selection__lt=current_time, end_term__gt=current_time)
    #     print(current_term.name)
    #     return Response('hello', status=status.HTTP_200_OK)
    # def list(self, request, *args, **kwargs):
    #     current_time = datetime.now()
    #     current_term = Term.objects.get(start_course_selection__lt=current_time, end_term__gt=current_time)

    #     print(datetime.now().date() > current_term.end_term)
    #     return super().list(request, *args, **kwargs)

class AssistantRemoveTermStudentDetail(APIView):
    queryset = TermDropRequest.objects.all()
    serializer_class = TermDropSerializer
    permission_classes = [IsDeputyEducational]

    def get(self, request, pk):
        try:
            student = Student.objects.get(id=pk)
            remove_term = TermDropRequest.objects.get(student=student)
            print(remove_term.result)
            serializer = self.serializer_class(remove_term)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            raise serializers.ValidationError('Student Does Not Exist')

    def put(self, request, pk):
        current_time = datetime.now()
        student = Student.objects.get(id=pk)
        remove_term = TermDropRequest.objects.get(student=student)
        studnet_term_drop = TermDropRequest.objects.get(student=student)
        serializer = self.serializer_class(instance=studnet_term_drop ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        accept = serializer.validated_data['accept']
        deputy_educational_comment = serializer.validated_data['deputy_educational_comment']
        if accept :
            # current_term = Term.objects.get(start_course_selection__lt=current_time, end_term__gt=current_time)
            if remove_term.result == 'Without Seniority':
                student.seniority -= 1
                student.save()
            current_term = studnet_term_drop.term
            current_term.students.remove(student)
            StudentCourse.objects.filter(student=student).delete()
            try:
                # send_email_task.delay('Remove Term Response','Your Drop Term request Accepted', EMAIL_HOST_USER, [student.email])
                return Response({'result':'Request Accepted', 'message': deputy_educational_comment}, status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError('Student Email field is Null')
        elif not accept:
            try:
                # send_email_task.delay('Remove Term Response','Your Drop Term request Failed', EMAIL_HOST_USER, [student.email])
                return Response({'result':'Request Failed', 'message': 'deputy_educational_comment'}, status=status.HTTP_200_OK)
            except:
                raise serializers.ValidationError('Student Email field is Null')

