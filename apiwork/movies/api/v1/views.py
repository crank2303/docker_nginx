"""This is module with views of api v1."""
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    """Mixin class for pages."""

    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        """Get queryset about movie.

        Returns:
            queryset: Queryset from Filmwork with genre, actor, writer, director

        """
        queryset = self.model.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg(
                'persons__full_name', distinct=True, filter=Q(personfilmwork__role='actor')),
            directors=ArrayAgg(
                'persons__full_name', distinct=True, filter=Q(personfilmwork__role='director')),
            writers=ArrayAgg(
                'persons__full_name', distinct=True, filter=Q(personfilmwork__role='writer')),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        """Make Json.

        Returns:
            json: Data of movies

        """
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """View of all movies."""

    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get data of response.

        Returns:
            context: Json with list of movies with params and params of page

        """
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """View of one movie."""

    pk_url_kwarg = 'pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get data of response.

        Returns:
            context: Json with params of one movie

        """
        queryset = self.get_queryset()
        queryset_film = queryset.filter(id__icontains=self.kwargs[self.pk_url_kwarg])
        context = {
            'id': [item['id'] for item in queryset_film][0],
            'title': [item['title'] for item in queryset_film][0],
            'description': [item['description'] for item in queryset_film][0],
            'creation_date': [item['creation_date'] for item in queryset_film][0],
            'rating': [item['rating'] for item in queryset_film][0],
            'type': [item['type'] for item in queryset_film][0],
            'genres': [item['genres'] for item in queryset_film][0],
            'actors': [item['actors'] for item in queryset_film][0],
            'directors': [item['directors'] for item in queryset_film][0],
            'writers': [item['writers'] for item in queryset_film][0],
        }
        return context
