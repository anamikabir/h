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


class TestListGroupsOpenGroups(object):

    def test_returns_all_open_groups_for_authority(self, list_groups_service, factories):
        o_groups = [factories.OpenGroup(authority='foo.com'),
                    factories.OpenGroup(authority='foo.com')]
        o_group_names = {o_group.name for o_group in o_groups}

        groups = list_groups_service.open_groups(authority='foo.com')

        assert {group['name'] for group in groups} == o_group_names

    def test_no_groups_from_mismatched_authority(self, list_groups_service, factories):
        factories.OpenGroup(authority='foo.com')
        factories.OpenGroup(authority='foo.com')

        groups = list_groups_service.open_groups(authority='bar.com')

        assert groups == []

    def test_returns_groups_from_default_authority(self, list_groups_service):
        groups = list_groups_service.open_groups()

        assert groups[0]['id'] == '__world__'


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
