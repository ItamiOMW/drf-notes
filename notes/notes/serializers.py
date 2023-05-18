from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'user_id', 'title', 'content', 'date_updated',)

    def create(self, validated_data):
        user_id = self.context['user_id']
        return Note.objects.create(user_id=user_id, **validated_data)
