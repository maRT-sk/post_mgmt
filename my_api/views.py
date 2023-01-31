import json
import requests

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


def fetch_from_ext_api(resource: str, key: str) -> dict:
    """ function which gets data from external api - jsonplaceholder.typicode.com """
    URL = f"https://jsonplaceholder.typicode.com/{resource}/{key}"
    response_API = requests.get(URL)
    data = json.loads(response_API.text)
    return data


def create_post(data: dict) -> None:
    """ function to create a new post in the database """
    Post(id=data['id'], user_id=data['userId'], title=data['title'], body=data['body']).save()


class MyApiView(APIView):

    def post(self, request, *args, **kwargs):

        # check if user_id exists via external API; create a new post using posted query params  + return JsonResponse
        if fetch_from_ext_api('users', request.query_params['user_id']):
            try:
                data = {'id'     : request.query_params['id'],
                        'user_id': request.query_params['user_id'],
                        'title'  : request.query_params['title'],
                        'body'   : request.query_params['body']}
            except KeyError:
                return JsonResponse(data=None, status=status.HTTP_400_BAD_REQUEST, safe=False)
            serializer = PostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"user_id": ["user with this id does not exist."]}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id=None, *args, **kwargs):

        # get post by post id from query params or request URL
        if 'id' in request.query_params or post_id is not None:
            pk = post_id if post_id is not None else request.query_params['id']
            try:
                post = Post.objects.get(id=pk)
            # if the post does not exist in the db, it will be fetched from the external api
            except ObjectDoesNotExist:
                fetched_data = fetch_from_ext_api('posts', pk)
                if fetched_data:
                    create_post(fetched_data)
                    post = Post.objects.get(id=pk)
                else:
                    return JsonResponse({"id": ["error: Post does not exist"]}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(post)

        # get all posts by user_id from query params
        elif 'user_id' in request.query_params:
            post = Post.objects.filter(user_id=request.query_params['user_id'])
            serializer = PostSerializer(post, many=True)

        # get all posts in the db
        else:
            all_posts = Post.objects.all()
            serializer = PostSerializer(all_posts, many=True)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'indent': 2})

    # delete a post by id from query params or request URL
    def delete(self, request, post_id=None, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id if post_id is not None else request.query_params['id'])
            post.delete()
            return JsonResponse({"id": ["ok: object has been deleted"]}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return JsonResponse({"id": ["error: ObjectDoesNotExist"]}, status=status.HTTP_404_NOT_FOUND)

    # edit an existing post
    def patch(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
            data = {'title': request.query_params['title'],
                    'body' : request.query_params['body']}
        except (ObjectDoesNotExist, KeyError):
            return JsonResponse(data=None, status=status.HTTP_400_BAD_REQUEST, safe=False)
        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
