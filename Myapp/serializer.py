from rest_framework import serializers
from .models import Posts, LikeData
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Posts
        fields = ["post_id","title","description","content","creation_date","private","user_id","total_likes"]

    def validate(self, validated_data):
        title = validated_data["title"]
        if len(title) > 20:
            raise serializers.ValidationError("Please Enter Short title")
        return validated_data



class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LikeData
        fields = '__all__'
        # depth = 1