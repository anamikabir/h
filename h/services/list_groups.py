# -*- coding: utf-8 -*-

from __future__ import unicode_literals


class ListGroupsService(object):

    """
    A service for providing filtered lists of groups.

    This service filters groups by user session, scope, etc.

    ALl public methods return a list of relevant groups,
    as dicts (see _group_model) for consumption by e.g. API services.
    """

    def __init__(self, session, request_authority, route_url):
        """
        Create a new list_groups service.

        :param _session: the SQLAlchemy session object
        :param _request_authority: the authority to use as a default
        :param _route_url: a callable for generating URLs for app routes
        """
        self._session = session
        self._route_url = route_url
        self._request_authority = request_authority

    def _sort(self, groups):
        """Sort a list of groups."""

    def all_groups(self, user=None, authority=None, document_uri=None):
        """
        Return a list of groups relevant to this session/profile (i.e. user).

        Return a list of groups filtered on user, authority, document_uri.
        Include all types of relevant groups (open and private).
        """

    def open_groups(self, authority=None, document_uri=None):
        """
        Return all matching open groups for the authority and target URI.

        Return matching open groups for the authority (or request_authority
        default), filtered by scope as per ``document_uri``.
        """

    def private_groups(self, user):
        """Return this user's private groups per user.groups."""

    def _group_model(self, group):
        """Return dict representing group for API use."""


def list_groups_factory(context, request):
    """Return a ListGroupsService instance for the passed context and request."""
    return ListGroupsService(session=request.db,
                             request_authority=request.authority,
                             route_url=request.route_url)
