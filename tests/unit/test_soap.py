# -*- coding: utf-8 -*-
# Licensed to Anthony Shaw (anthonyshaw@apache.org) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import workday
from workday.soap import WorkdayResponse, BaseSoapApiClient
import workday.exceptions


bad_params = (
    {1: None},
    {"place": None},
    {"place": 1},
    {"place": dict()},
    {"place": (1,)},
)


@pytest.mark.parametrize("params", bad_params)
def test_workday_response_bad_params(params):
    with pytest.raises(TypeError):
        WorkdayResponse(**params)


def test_properties(test_response_dict):
    wr = WorkdayResponse(
        response=test_response_dict,
        service=None,
        method="Get_Test",
        called_args=(),
        called_kwargs={},
    )
    assert wr.page == 1
    assert wr.total_pages == 2
    assert wr.total_results == 200
    assert wr.page_results == 100
    assert wr.data == {"TestData": [{"TestRecord": 1}]}
    assert wr.references is None
    assert wr.filter is None


@pytest.fixture
def paged_response():
    return (
        {
            "Response_Results": {
                "Page": 1,
                "Total_Pages": 2,
                "Total_Results": 2,
                "Page_Results": 1,
            },
            "Response_Data": {"TestData": [{"TestRecord": 1}]},
        },
        {
            "Response_Results": {
                "Page": 2,
                "Total_Pages": 2,
                "Total_Results": 2,
                "Page_Results": 1,
            },
            "Response_Data": {"TestData": [{"TestRecord": 2}]},
        },
    )


@pytest.fixture
def mock_soap_client(paged_response):
    class test_service(object):
        def Get_Test(self, **kwargs):
            if "Response_Filter" in kwargs and "Page" in kwargs["Response_Filter"]:
                page = kwargs["Response_Filter"]["Page"]
            else:
                page = 1
            return paged_response[page - 1]

    return test_service


def test_paging(paged_response, mock_soap_client):
    page_1 = WorkdayResponse(
        response=paged_response[0],
        service=mock_soap_client(),
        method="Get_Test",
        called_args=(),
        called_kwargs={},
    )
    assert page_1.data == {"TestData": [{"TestRecord": 1}]}
    assert page_1.page == 1
    iterator = iter(page_1)
    assert iterator
    page_2 = next(iterator)
    assert page_2.data == {"TestData": [{"TestRecord": 2}]}
    assert page_2.page == 2
    try:
        next(iterator)
        pytest.fail("Did not raise StopIteration")
    except StopIteration:
        pass


def test_paging_from_page2(paged_response, mock_soap_client):
    page_2 = WorkdayResponse(
        response=paged_response[1],
        service=mock_soap_client(),
        method="Get_Test",
        called_args=(),
        called_kwargs={"Response_Filter": {"Page": 2}},
    )
    assert page_2.data == {"TestData": [{"TestRecord": 2}]}
    assert page_2.page == 2
    iterator = iter(page_2)
    try:
        next(iterator)
        pytest.fail("Did not raise StopIteration")
    except StopIteration:
        pass
