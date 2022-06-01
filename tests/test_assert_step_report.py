import logging
from unittest import TestCase

import pytest

import pykiso.test_coordinator.assert_step_report as assert_step_report


@pytest.fixture
def test_case():
    tc = TestCase()
    # decorate 2 different assert
    tc.assertTrue = assert_step_report.assert_decorator(tc.assertTrue)
    tc.assertAlmostEqual = assert_step_report.assert_decorator(tc.assertAlmostEqual)

    # Add the step-report parameters
    tc.step_report_header = {}
    tc.step_report_message = ""
    tc.step_report_succeed = True
    tc.step_report_continue_on_error = False

    return tc


def test_assert_step_report_header_error(test_case, caplog):
    test_case.assertTrue = assert_step_report.assert_decorator(test_case.assertTrue)

    with caplog.at_level(logging.ERROR):
        test_case.assertTrue(True)

    assert "'TestCase' object has no attribute 'step_report_header'" in caplog.text


def test_assert_step_report_single_input(mocker, test_case):
    step_result = mocker.patch(
        "pykiso.test_coordinator.assert_step_report.assert_step_report._add_step"
    )

    data_to_test = True
    test_case.assertTrue(data_to_test)

    step_result.assert_called_once_with(
        "TestCase",
        "test_assert_step_report_single_input",
        "",
        "data_to_test",
        "True",
        True,
    )


def test_assert_step_report_no_var_name_test(mocker, test_case):
    step_result = mocker.patch(
        "pykiso.test_coordinator.assert_step_report.assert_step_report._add_step"
    )

    test_case.assertTrue(True)

    step_result.assert_called_once_with(
        "TestCase", "test_assert_step_report_no_var_name_test", "", "True", "True", True
    )


def test_assert_step_report_message(mocker, test_case):
    step_result = mocker.patch(
        "pykiso.test_coordinator.assert_step_report.assert_step_report._add_step"
    )

    data_to_test = True
    test_case.assertTrue(data_to_test, "message")

    step_result.assert_called_once_with(
        "TestCase",
        "test_assert_step_report_message",
        "message",
        "data_to_test",
        "True",
        True,
    )


def test_assert_step_report_multi_input(mocker, test_case):
    step_result = mocker.patch(
        "pykiso.test_coordinator.assert_step_report.assert_step_report._add_step"
    )

    data_to_test = 4
    data_expected = 4.5
    test_case.assertAlmostEqual(
        data_to_test, data_expected, delta=1, msg="Test the step report"
    )

    step_result.assert_called_once_with(
        "TestCase",
        "test_assert_step_report_multi_input",
        "Test the step report",
        "data_to_test",
        "Almost Equal to 4.5; with delta=1",
        4,
    )
