# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from h.services.list_groups import ListGroupsService


class TestListGroupsPrivateGroups(object):

    @pytest.mark.parametrize('attribute', [
        ('id'),
        ('name'),
        ('public'),
        ('scoped'),
        ('type')
    ])
    def test_returns_formatted_groups(self, list_groups_service, factories, attribute):
        user = factories.User()
        user.groups = [factories.Group()]

        groups = list_groups_service.private_groups(user)

        assert attribute in groups[0]

    def test_returns_private_groups_only(self, list_groups_service, factories):
        user = factories.User()
        user.groups = [factories.Group(), factories.Group(), factories.Group()]

        groups = list_groups_service.private_groups(user)

        assert len(groups) == 3
        for group in groups:
            assert group['type'] == 'private'

    def test_returns_empty_when_user_no_private_groups(self, list_groups_service, factories):
        user = factories.User()

        groups = list_groups_service.private_groups(user)

        assert groups == []

    def test_returns_no_groups_for_no_user(self, list_groups_service):

        groups = list_groups_service.private_groups(user=None)

        assert groups == []


@pytest.fixture
def pyramid_request(pyramid_request):
    pyramid_request.route_url = mock.Mock(return_value='/group/a')
    return pyramid_request


@pytest.fixture
def list_groups_service(pyramid_request, db_session):
    return ListGroupsService(
        session=db_session,
        request_authority=pyramid_request.authority,
        route_url=pyramid_request.route_url
    )
