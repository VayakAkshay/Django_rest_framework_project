from django.shortcuts import render
from .models import Posts,LikeData
from .serializer import PostSerializer, LikeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,action
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['GET'])
def All_Posts(request):
    try:
        post_data = Posts.objects.all()
        serializers = PostSerializer(post_data,many = True)
        return Response({
            "status":200,
            "Message":"All Posts Data",
            "data":serializers.data
        })
    except Exception as e:
        return Response({
            "status": 404,
            "Message": "Something went wrong"
        })

class PostViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.filter(private = False).all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['GET'])
    def get(self, request):
        current_user = request.user
        public_data = Posts.objects.filter(private = False).all().values()
        private_data = Posts.objects.filter(user_id = request.user.id).filter(private = True).values()
        my_data = []
        for i in public_data:
            my_data.append(i)
        for i in private_data:
            my_data.append(i)
        return Response({
            "Message":"All posts data",
            "Data":my_data
        })

    def list(self, request, *args, **kwargs):
        current_user = request.user
        return super().list(request, *args, **kwargs)


    def put(self,request):
        current_userdata = User.objects.filter(username = request.user).values()[0]
        data  = request.data
        obj = Posts.objects.get(post_id = data.get("id"))
        check_data = Posts.objects.filter(post_id = data.get("id")).values()[0]
        if current_userdata["id"] == check_data["user_id_id"]:
            return Response({
                "Message":"You cannot change the data"
            })
        else:
            update_serializer = PostSerializer(obj,data=data,partial = True)
            if update_serializer.is_valid():
                update_serializer.save()
                return Response({
                    "status":200,
                    "message":"Data Successfully Updated",
                    "data":update_serializer.data,
                })
            else:
                return Response({
                    "status":400,
                    "message":"Something went wrong",
                    "data":update_serializer.errors,
                })

    def delete(self,request):
        data  = request.data
        current_userdata = User.objects.filter(username = request.user).values()[0]
        check_data = Posts.objects.filter(post_id = data.get("id")).values()[0]
        if current_userdata["id"] == check_data["user_id_id"]:
            return Response({
                "Message":"You cannot delete the data"
            })
        else:
            Posts.objects.get(post_id = data.get("id")).delete()
            return Response({
                "Data":"Data successfully Deleted"
            })

class LikeViewset(viewsets.ModelViewSet):
    queryset = LikeData.objects.all()
    serializer_class = LikeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def post(self,request):
        data  = request.data
        add_likes = Posts.objects.filter(post_id = data["post_id"]).values()[0]["total_likes"] + 1
        Posts.objects.filter(post_id = data["post_id"]).update(total_likes = add_likes)
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message":"Data successfully Saved",
                "data":serializer.data
            })
        else:
            return Response({
                "Message":"Please enter valid details"
            })


    def put(self,request):
        data  = request.data
        obj = LikeData.objects.get(like_id = data.get("id"))
        update_serializer = LikeSerializer(obj,data=data,partial = True)
        if update_serializer.is_valid():
            update_serializer.save()
            return Response({
                "status":200,
                "message":"Data Successfully Updated",
                "data":update_serializer.data,
            })
        else:
            return Response({
                "status":400,
                "message":"Something went wrong",
                "data":update_serializer.errors,
            })

    def delete(self,request):
        data  = request.data
        obj = LikeData.objects.get(post_id = data.get("id")).delete()
        return Response({
            "Data":"Data successfully Deleted"
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self,request):
        data  = request.data
        obj = User.objects.get(id = data.get("id"))
        update_serializer = UserSerializer(obj,data=data,partial = True)
        if update_serializer.is_valid():
            update_serializer.save()
            return Response({
                "status":200,
                "message":"Data Successfully Updated",
                "data":update_serializer.data,
            })
        else:
            return Response({
                "status":400,
                "message":"Something went wrong",
                "data":update_serializer.errors,
            })

    def delete(self,request):
        data  = request.data
        obj = User.objects.get(id = data.get("id")).delete()
        return Response({
            "Data":"Data successfully Deleted"
        })
