from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('title',)
        model = Review

    def validate(self, attrs):
        title_id = self.context.get('view').kwargs.get('title_id')
        if (self.context.get('view').action == 'create') and (
                Review.objects.filter(
                    author=self.context.get('request').user,
                    title__id=title_id).exists()
        ):
            raise serializers.ValidationError(
                'Нельзя оставить второй комментарий'
            )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('review',)
        model = Comment
