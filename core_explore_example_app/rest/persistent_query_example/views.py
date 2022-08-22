""" REST views for the Persistent Query Example.
"""
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
import core_explore_example_app.components.persistent_query_example.api as persistent_query_example_api
from core_explore_example_app.rest.persistent_query_example.serializers import (
    PersistentQueryExampleSerializer,
    PersistentQueryExampleAdminSerializer,
)


class AdminPersistentQueryExampleList(APIView):
    """List all persistent query example, or create a new one."""

    permission_classes = (IsAdminUser,)
    serializer = PersistentQueryExampleAdminSerializer

    def get(self, request):
        """Get all user persistent query example

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of persistent query example
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            # Get object
            object_list = persistent_query_example_api.get_all(request.user)

            # Serialize object
            serializer = self.serializer(object_list, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create a persistent query example

        Parameters:

            {
                "content": "{}",
                "templates": ["5ea99316d26ebc48e475c60a"],
                "name": "persistent_query_example"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created persistent query example
            - code: 400
              content: Validation error
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            # Build serializer
            serializer = self.serializer(
                data=request.data, context={"request": request}
            )

            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersistentQueryExampleList(APIView):
    """List all persistent query example or create one"""

    permission_classes = (IsAuthenticated,)
    serializer = PersistentQueryExampleSerializer

    def get(self, request):
        """Get all user persistent query example

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of persistent query example
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """

        try:
            # Get object
            object_list = persistent_query_example_api.get_all_by_user(request.user)

            # Serialize object
            serializer = self.serializer(object_list, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create a new persistent query example

        Parameters:

            {
                "content": "{}",
                "templates": ["5ea99316d26ebc48e475c60a"],
                "name": "persistent_query_example"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created data
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
        """

        try:
            # Build serializer
            serializer = self.serializer(
                data=request.data, context={"request": request}
            )

            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersistentQueryExampleDetail(APIView):
    """Persistent query example detail"""

    permission_classes = (IsAuthenticated,)
    serializer = PersistentQueryExampleSerializer

    def get(self, request, pk):
        """Retrieve persistent query example from database

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:
            - code: 200
              content: persistent query example
            - code: 403
              content: Forbidden
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            persistent_query_example = persistent_query_example_api.get_by_id(
                pk, request.user
            )

            # Serialize object
            serializer = self.serializer(persistent_query_example)

            # Return response
            return Response(serializer.data)

        except exceptions.DoesNotExist:
            content = {"message": "Object not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        """Update a persistent query example

        Parameters:
            {
                "content": "{}",
                "templates": ["5ea99316d26ebc48e475c60a"],
                "name": null
            }

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            - code: 200
              content: Updated data
            - code: 400
              content: Validation error
            - code: 403
              content: Forbidden
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            persistent_query_example = persistent_query_example_api.get_by_id(
                pk, request.user
            )

            # Build serializer
            serializer = self.serializer(
                instance=persistent_query_example,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            # Validate and save persistent query example
            serializer.is_valid(True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Persistent query example not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete a persistent query example

        Args:
            request: HTTP request
            pk: ObjectId

        Returns:
            - code: 204
              content: Deletion success
            - code: 403
              content: Authentication error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            persistent_query_example = persistent_query_example_api.get_by_id(
                pk, request.user
            )

            # delete object
            persistent_query_example_api.delete(persistent_query_example, request.user)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except exceptions.DoesNotExist:
            content = {"message": "Persistent query example not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PersistentQueryExampleByName(APIView):
    """Persistent query example detail"""

    permission_classes = (IsAuthenticated,)
    serializer = PersistentQueryExampleSerializer

    def get(self, request, name):
        """Retrieve persistent query example from database

        Args:

            request: HTTP request
            name: name

        Returns:
            - code: 200
              content: persistent query example
            - code: 403
              content: Forbidden
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            persistent_query_example = persistent_query_example_api.get_by_name(
                name, request.user
            )

            # Serialize object
            serializer = self.serializer(persistent_query_example)

            # Return response
            return Response(serializer.data)
        except exceptions.DoesNotExist:
            content = {"message": "Persistent query example not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
