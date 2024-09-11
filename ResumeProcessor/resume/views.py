from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer
from pyresparser import ResumeParser
import os
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser

class ResumeExtractionView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file type
        if not resume_file.name.endswith(('.pdf', '.docx')):
            return Response({"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the file temporarily
        file_path = os.path.join(settings.MEDIA_ROOT, resume_file.name)
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in resume_file.chunks():
                    destination.write(chunk)

            # Parse the resume using pyresparser
            data = ResumeParser(file_path).get_extracted_data()

            # Extract necessary details
            first_name = data.get('name', '').split()[0]
            email = data.get('email')
            mobile_number = data.get('mobile_number')

            if not (first_name and email and mobile_number):
                return Response({"error": "Could not extract required information"}, status=status.HTTP_400_BAD_REQUEST)

            # Save to the database
            candidate = Candidate(first_name=first_name, email=email, mobile_number=mobile_number)
            candidate.save()

            # Serialize the response
            serializer = CandidateSerializer(candidate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)  # Clean up after parsing
