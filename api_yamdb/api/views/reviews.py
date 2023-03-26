from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers.reviews import CommentSerializer, ReviewSerializer
from reviews.models import Review
from titles.models import Title
from users.permissions import IsAuthorOrAdminOrModerator


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        rating = title.reviews.aggregate(Avg('score'))
        title.rating = int(rating.get('score__avg'))
        title.save()

    def perform_update(self, serializer):
        self.perform_create(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminOrModerator,
    )
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comment.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
