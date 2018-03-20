""" REST Views for Saved Queries
"""
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import core_explore_example_app.components.saved_query.api as saved_query_api
from core_explore_example_app.rest.saved_query.serializers import SavedQuerySerializer
from core_main_app.commons import exceptions


class SavedQueryList(APIView):
    """ Get all SavedQuery
    """
    def get(self, request):
        """ Get all Save Query, can be filtered by owner and template

        GET /rest/saved/query/
        GET /rest/saved/query/?user_id=<id>
        GET /rest/saved/query/?template_id=<id>
        GET /rest/saved/query/?user_id=<id>&template_id=<id>

        Args:
            request:

        Returns:

        """
        try:
            saved_query_list = saved_query_api.get_all()

            # Apply filters
            user_id = self.request.query_params.get('user_id', None)
            if user_id is not None:
                saved_query_list = saved_query_list.filter(user_id=user_id)
            template_id = self.request.query_params.get('template_id', None)
            if template_id is not None:
                saved_query_list = saved_query_list.filter(template=str(template_id))

            # Serialize object
            return_value = SavedQuerySerializer(saved_query_list, many=True)
            # Return response
            return Response(return_value.data)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SavedQueryDetail(APIView):
    """" Get an SavedQuery
    """

    def get_object(self, pk):
        """ Retrieve a saved query

        Args:
            pk:

        Returns:

        """
        try:
            return saved_query_api.get_by_id(pk)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Get saved query by its id.

        GET /rest/saved/query/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            saved_query_object = self.get_object(pk)
            # Serialize object
            return_value = SavedQuerySerializer(saved_query_object)
            # Return response
            return Response(return_value.data)
        except Http404:
            content = {'message': 'Saved Query not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """ Delete Saved query by its id.

        DELETE /rest/saved/query/pk

        Args:
            request:
            pk:

        Returns:

        """
        try:
            # Get object
            saved_query_object = self.get_object(pk)
            # if the user is owner or super user
            if str(request.user.id) != saved_query_object.user_id and not request.user.is_superuser:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # Remove the saved query
            saved_query_api.delete(saved_query_object)
            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            content = {'message': 'Saved Query not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': api_exception.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
