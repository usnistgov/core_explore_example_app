""" REST views for the Persistent Query by Example.
"""

from django.db import IntegrityError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import core_explore_example_app.components.persistent_query_example.api as persistent_query_example_api
from core_explore_example_app.rest.persistent_query_example.serializers import (
    PersistentQueryExampleSerializer,
    PersistentQueryExampleAdminSerializer,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions


@extend_schema(
    tags=["Persistent Query by Example"],
    description="List all persistent query by example, or create a new one",
)
class AdminPersistentQueryExampleList(APIView):
    """List all persistent query by example, or create a new one."""

    permission_classes = (IsAdminUser,)
    serializer = PersistentQueryExampleAdminSerializer

    @extend_schema(
        summary="Get all persistent query by example",
        description="Retrieve a list of all persistent query by examples",
        responses={
            200: PersistentQueryExampleAdminSerializer(many=True),
            403: OpenApiResponse(description="Access Forbidden"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        """Get all user persistent query by example
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of persistent query by example
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
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Create a persistent query by example",
        description="Create a new persistent query by example",
        request=PersistentQueryExampleAdminSerializer,
        responses={
            201: PersistentQueryExampleAdminSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Access Forbidden"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Create a persistent query by example",
                summary="Create a new persistent query by example",
                description="Create a new persistent query by example with the provided parameters",
                request_only=True,
                value={
                    "content": "{}",
                    "templates": ["123"],
                    "name": "persistent_query_example",
                },
            ),
        ],
    )
    def post(self, request):
        """Create a persistent query by example
        Parameters:
            {
              "content": "{}",
              "templates": ["123"],
              "name": "persistent_query_example"
            }
        Args:
            request: HTTP request
        Returns:
            - code: 201
              content: Created persistent query by example
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
            serializer.is_valid(raise_exception=True)
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
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Persistent Query by Example"],
    description="List all persistent query by example or create one",
)
class PersistentQueryExampleList(APIView):
    """List all persistent query by example or create one"""

    permission_classes = (IsAuthenticated,)
    serializer = PersistentQueryExampleSerializer

    @extend_schema(
        summary="Get all persistent query by example by user",
        description="Retrieve a list of all persistent query by examples for the current user",
        responses={
            200: PersistentQueryExampleSerializer(many=True),
            403: OpenApiResponse(description="Access Forbidden"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        """Get all user persistent query by example
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of persistent query by example
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            object_list = persistent_query_example_api.get_all_by_user(
                request.user
            )
            # Serialize object
            serializer = self.serializer(object_list, many=True)
            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Create a persistent query by example",
        description="Create a new persistent query by example",
        request=PersistentQueryExampleSerializer,
        responses={
            201: PersistentQueryExampleSerializer,
            400: OpenApiResponse(description="Validation error"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Create a persistent query by example",
                summary="Create a new persistent query by example",
                description="Create a new persistent query by example with the provided parameters",
                request_only=True,
                value={
                    "content": "{}",
                    "templates": ["123"],
                    "name": "persistent_query_example",
                },
            ),
        ],
    )
    def post(self, request):
        """Create a new persistent query by example
        Parameters:
            {
              "content": "{}",
              "templates": ["123"],
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
            serializer.is_valid(raise_exception=True)
            # Save data
            serializer.save()
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Persistent Query by Example"],
    description="Persistent query by example detail",
)
class PersistentQueryExampleDetail(APIView):
    """Persistent query by example detail"""

    permission_classes = (IsAuthenticated,)
    serializer = PersistentQueryExampleSerializer

    @extend_schema(
        summary="Retrieve a persistent query by example",
        description="Retrieve a persistent query by example by ID",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Persistent Query by Example ID",
            ),
        ],
        responses={
            200: PersistentQueryExampleSerializer,
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request, pk):
        """Retrieve persistent query by example from database
        Args:
            request: HTTP request
            pk: ObjectId
        Returns:
            - code: 200
              content: persistent query by example
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
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Update a persistent query by example",
        description="Update a persistent query by example by ID",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Persistent Query by Example ID",
            ),
        ],
        request=PersistentQueryExampleSerializer(partial=True),
        responses={
            200: PersistentQueryExampleSerializer,
            400: OpenApiResponse(description="Validation error"),
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
        examples=[
            OpenApiExample(
                "Update a persistent query by example",
                summary="Update a persistent query by example",
                description="Update a persistent query by example with the provided parameters",
                request_only=True,
                value={
                    "content": "{}",
                    "templates": ["123"],
                    "name": None,
                },
            ),
        ],
    )
    def patch(self, request, pk):
        """Update a persistent query by example
        Parameters:
            {
              "content": "{}",
              "templates": ["123"],
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
            # Validate and save persistent query by example
            serializer.is_valid(raise_exception=True)
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
            content = {"message": "Persistent query by example not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Delete a persistent query by example",
        description="Delete a persistent query by example by ID",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Persistent Query by Example ID",
            ),
        ],
        responses={
            204: None,
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def delete(self, request, pk):
        """Delete a persistent query by example
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
            persistent_query_example_api.delete(
                persistent_query_example, request.user
            )
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except exceptions.DoesNotExist:
            content = {"message": "Persistent query by example not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Persistent Query by Example"],
    description="Persistent query by example detail by name",
)
class PersistentQueryExampleByName(APIView):
    """Persistent query by example detail"""

    permission_classes = (IsAuthenticated,)
    serializer = PersistentQueryExampleSerializer

    @extend_schema(
        summary="Retrieve a persistent query by example by name",
        description="Retrieve a persistent query by example by its name",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Persistent Query by Example name",
            ),
        ],
        responses={
            200: PersistentQueryExampleSerializer,
            403: OpenApiResponse(description="Access Forbidden"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request, name):
        """Retrieve persistent query by example from database
        Args:
            request: HTTP request
            name: name
        Returns:
            - code: 200
              content: persistent query by example
            - code: 403
              content: Forbidden
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            persistent_query_example = (
                persistent_query_example_api.get_by_name(name, request.user)
            )
            # Serialize object
            serializer = self.serializer(persistent_query_example)
            # Return response
            return Response(serializer.data)
        except exceptions.DoesNotExist:
            content = {"message": "Persistent query by example not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except AccessControlError as exception:
            content = {"message": str(exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
