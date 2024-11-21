from django.test import TestCase
from unittest.mock import patch
from admin_panel.tasks import save_daily_report
from admin_panel.models import DailyReport

class SaveDailyReportTaskTests(TestCase):

    @patch('admin_panel.tasks.DailyReport.create_report')
    def test_save_daily_report_called(self, mock_create_report):
        """Testa se a task save_daily_report chama create_report corretamente"""
        save_daily_report.apply()

        mock_create_report.assert_called_once()
        
    def test_save_daily_report_creates_report(self):
        """Testa se o método create_report realmente cria um DailyReport"""
        save_daily_report.apply()
        self.assertEqual(DailyReport.objects.count(), 1)