# ai_pipeline_project/functions.py
from typing import List, Dict, Any

def get_invoices(month: str) -> List[Dict[str, Any]]:
    """Fetch invoices for the specified month."""
    return [
        {"id": 1, "amount": 1200, "month": month},
        {"id": 2, "amount": 800, "month": month}
    ]

def summarize_invoices(invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize total and count of provided invoices."""
    total = sum(inv.get("amount", 0) for inv in invoices)
    return {"total": total, "count": len(invoices)}

def send_email(to: str, subject: str, body: str) -> bool:
    """Send a simulated email with subject and body."""
    print(f"[Email] To: {to}\nSubject: {subject}\nBody:\n{body}")
    return True

def create_calendar_event(title: str, date: str, time: str) -> Dict[str, Any]:
    """Create a mock calendar event."""
    return {"id": "evt123", "title": title, "date": date, "time": time}

def write_summary_to_file(content: str, filename: str = "summary.txt") -> bool:
    """Write a text summary to a file (simulated)."""
    print(f"[File Write] Filename: {filename}\nContent:\n{content}")
    return True
