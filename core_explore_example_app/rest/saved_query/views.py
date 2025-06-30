""" REST Views for Saved Queries
"""

from django.http import Http404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import core_explore_example_app.components.saved_query.api as saved_query_api
from core_explore_example_app.rest.saved_query.serializers import (
    SavedQuerySerializer,
)
from core_main_app.commons import exceptions


@extend_schema(
    tags=["Saved Query"],
    description="Get all SavedQuery",
)
class SavedQueryList(APIView):
    """Get all SavedQuery"""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Get all SavedQuery",
        description="Retrieve a list of all SavedQuery, filtered by owner and template",
        parameters=[
            OpenApiParameter(
                name="user_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by user ID",
            ),
            OpenApiParameter(
                name="template_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by template ID",
            ),
        ],
        responses={
            200: SavedQuerySerializer(many=True),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request):
        """Get all SavedQuery, can be filtered by owner and template
        Url Parameters:
            template: template_id
            user_id: document_title
        Examples:
            ../saved/query/
            ../saved/query/?user_id=[id]
            ../saved/query/?template_id=[id]
            ../saved/query/?user_id=[id]&template_id=[id]
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of saved queries
            - code: 500
              content: Internal server error
        """
        try:
            saved_query_list = saved_query_api.get_all()
            # Apply filters
            user_id = self.request.query_params.get("user_id", None)
            if user_id is not None:
                saved_query_list = saved_query_list.filter(user_id=user_id)
            template_id = self.request.query_params.get("template_id", None)
            if template_id is not None:
                saved_query_list = saved_query_list.filter(
                    template=str(template_id)
                )
            # Serialize object
            return_value = SavedQuerySerializer(saved_query_list, many=True)
            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Saved Query"],
    description="Get a SavedQuery",
)
class SavedQueryDetail(APIView):
    """Get a SavedQuery"""

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        """Get SavedQuery from db
        Args:
            pk: ObjectId
        Returns:
            SavedQuery
        """
        try:
            return saved_query_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    @extend_schema(
        summary="Retrieve a SavedQuery",
        description="Retrieve a SavedQuery by ID",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="SavedQuery ID",
            ),
        ],
        responses={
            200: SavedQuerySerializer,
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    def get(self, request, pk):
        """Retrieve a SavedQuery
        Args:
            request: HTTP request
            pk: ObjectId
        Returns:
            - code: 200
              content: SavedQuery
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            saved_query_object = self.get_object(pk)
            # Serialize object
            return_value = SavedQuerySerializer(saved_query_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {"message": "Saved Query not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Delete a SavedQuery",
        description="Delete a SavedQuery by ID",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="SavedQuery ID",
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
        """Delete a SavedQuery
        Args:
            request: HTTP request
            pk: ObjectId
        Returns:
            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            saved_query_object = self.get_object(pk)
            # if the user is owner or super user
            if (
                str(request.user.id) != saved_query_object.user_id
                and not request.user.is_staff
            ):
                return Response(status=status.HTTP_403_FORBIDDEN)
            # Remove the saved query
            saved_query_api.delete(saved_query_object)
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {"message": "Saved Query not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
