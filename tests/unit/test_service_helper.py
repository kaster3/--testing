from datetime import datetime
from unittest.mock import patch

import pytest

from app.service_layer.service_helper import ServiceHelper


class TestServiceHelper:
    @pytest.mark.parametrize(
        "date, expected_output",
        [
            ("2025-12-31", None),
            ("2026-01-01", None),
            ("2022-12-30", "Ошибка: Дедлайн не может быть в прошлом.\n"),
            ("   ", "Ошибка: Неверный формат даты. Ожидается формат 'YYYY-MM-DD'.\n"),
            ("Декабрь", "Ошибка: Неверный формат даты. Ожидается формат 'YYYY-MM-DD'.\n"),
            ("2013.02.11", "Ошибка: Неверный формат даты. Ожидается формат 'YYYY-MM-DD'.\n"),
        ],
    )
    def test_validate_data(self, date: str, expected_output: str, service_helper: ServiceHelper) -> None:
        with patch("builtins.input", return_value=date):
            if expected_output:
                with patch("builtins.print") as mock_print:
                    service_helper.validate_date()
                    mock_print.assert_called_once_with(expected_output)
            else:
                result = service_helper.validate_date()
                assert result == datetime.strptime(date, "%Y-%m-%d")

    @pytest.mark.parametrize(
        "title, expected_output",
        [
            ("Бег", None),
            ("Ужин", None),
            ("", "Ошибка: Название задачи не может быть пустым.\n"),
            ("    ", "Ошибка: Название задачи не может быть пустым.\n"),
        ],
    )
    def test_validate_title(self, title: str, expected_output: str, service_helper: ServiceHelper) -> None:
        with patch("builtins.input", return_value=title):
            if expected_output:
                with patch("builtins.print") as mock_print:
                    service_helper.validate_title()
                    mock_print.assert_called_once_with(expected_output)
            else:
                result = service_helper.validate_title()
                assert result == title.strip()
