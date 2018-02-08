# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from h import models
from h.models import group


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

    def _authority(self, user=None, authority=None):
        """Determine which authority to use.

           Determine the appropriate authority to use for querying groups.
           User's authority will always supersede if present; otherwise provide
           default value—request.authority—if no authority specified.
        """

        if user is not None:
            return user.authority
        return authority or self._request_authority

    def all_groups(self, user=None, authority=None, document_uri=None):
        """
        Return a list of groups relevant to this session/profile (i.e. user).

        Return a list of groups filtered on user, authority, document_uri.
        Include all types of relevant groups (open and private).
        """
        open_groups = self.open_groups(user, authority, document_uri)
        private_groups = self.private_groups(user)

        return open_groups + private_groups

    def open_groups(self, user=None, authority=None, document_uri=None):
        """
        Return all matching open groups for the authority and target URI.

        Return matching open groups for the authority (or request_authority
        default), filtered by scope as per ``document_uri``.
        """

        authority = self._authority(user, authority)
        # TODO This is going to change once scopes and model updates in place
        groups = (self._session.query(models.Group)
                      .filter_by(authority=authority,
                                 readable_by=group.ReadableBy.world)
                      .all())
        return [self._group_model(o_group) for o_group in groups]

    def private_groups(self, user=None):
        """Return this user's private groups per user.groups."""

        if user is None:
            return []
        return [self._group_model(p_group) for p_group in user.groups]

    def _group_model(self, group):
        """
        Return dict representing group for API use.

        Take a Group and return a formatted dict for API consumption.

        :param group: Group model for formatting
        """

        model = {
          'name': group.name,
          'id': group.pubid,
          'public': group.is_public,
          'scoped': False,  # TODO
          'type': 'open' if group.is_public else 'private',  # TODO
          'urls': {}
        }
        if not group.is_public:
            # `url` legacy property support
            model['url'] = self._route_url('group_read',
                                           pubid=group.pubid,
                                           slug=group.slug)
            # `urls` are the future
            model['urls']['group'] = model['url']
        return model


def list_groups_factory(context, request):
    """Return a ListGroupsService instance for the passed context and request."""
    return ListGroupsService(session=request.db,
                             request_authority=request.authority,
                             route_url=request.route_url)
