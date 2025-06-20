import unittest
import json
from model_engine import ModelEngine

class TestModelEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = ModelEngine()

    def assertPlanMatches(self, user_query, expected_steps):
        plan_json = self.engine.plan_sequence(user_query)
        actual_plan = json.loads(plan_json)
        self.assertEqual(actual_plan, expected_steps)

    def test_query_invoices_email(self):
        user_query = "Get invoices for March, summarize them, and email me the report."
        expected = [
            {"function": "get_invoices", "args": {"month": "March"}},
            {"function": "summarize_invoices", "args": {"invoices": "<output_of_get_invoices>"}},
            {"function": "send_email", "args": {
                "to": "me@example.com",
                "subject": "Invoice Summary",
                "body": "<output_of_summarize_invoices>"
            }}
        ]
        self.assertPlanMatches(user_query, expected)

    def test_query_create_calendar_event(self):
        user_query = "Create a calendar event called 'Meeting' on 2025-07-01 at 09:00."
        expected = [
            {"function": "create_calendar_event", "args": {
                "title": "Meeting",
                "date": "2025-07-01",
                "time": "09:00"
            }}
        ]
        self.assertPlanMatches(user_query, expected)

    def test_query_invoice_summary_to_file(self):
        user_query = "Generate invoice summary for June and save to a file."
        expected = [
            {"function": "get_invoices", "args": {"month": "June"}},
            {"function": "summarize_invoices", "args": {"invoices": "<output_of_get_invoices>"}},
            {"function": "write_summary_to_file", "args": {
                "content": "<output_of_summarize_invoices>",
                "filename": "summary.txt"
            }}
        ]
        self.assertPlanMatches(user_query, expected)

    def test_query_combined_email_and_file(self):
        user_query = "Summarize invoices for March and send me the result in an email and save it as a file."
        expected = [
            {"function": "get_invoices", "args": {"month": "March"}},
            {"function": "summarize_invoices", "args": {"invoices": "<output_of_get_invoices>"}},
            {"function": "send_email", "args": {
                "to": "me@example.com",
                "subject": "Invoice Summary",
                "body": "<output_of_summarize_invoices>"
            }},
            {"function": "write_summary_to_file", "args": {
                "content": "<output_of_summarize_invoices>",
                "filename": "summary.txt"
            }}
        ]
        self.assertPlanMatches(user_query, expected)

    def test_query_no_match(self):
        user_query = "Tell me a joke"
        with self.assertRaises(ValueError):
            self.engine.plan_sequence(user_query)

if __name__ == "__main__":
    unittest.main()
