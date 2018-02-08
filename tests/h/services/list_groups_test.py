# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mock
import pytest

from h.services.list_groups import ListGroupsService


class TestListGroupsService(object):
    def test_service_exists(self, db_session, pyramid_request):
        svc = ListGroupsService(
            session=db_session,
            request_authority=pyramid_request.authority,
            route_url=pyramid_request.route_url
        )

        assert isinstance(svc, ListGroupsService)


@pytest.fixture
def pyramid_request(pyramid_request):
    pyramid_request.route_url = mock.Mock(return_value='/group/a')
    return pyramid_request
