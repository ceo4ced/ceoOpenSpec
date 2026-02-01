"""
CXA Agent - Chief Experience/Communications Agent
Handles all external communications: email, phone, scheduling, and contacts.

Commands:
    cxa.email     - Email management and routing
    cxa.phone     - Phone communications (via Twilio)
    cxa.schedule  - Calendar and scheduling
    cxa.contacts  - Contact management
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'packages'))
from factory_core.agent import BaseAgent


class CXAAgent(BaseAgent):
    """
    CXA Agent - Chief Experience/Communications Agent.

    Responsibilities:
    - Single email address management (hello@company.com)
    - Email routing to appropriate C-Suite agents
    - Phone communications via Twilio
    - Calendar and scheduling
    - Contact management
    """

    # Email routing rules
    EMAIL_ROUTING = [
        # Legal (highest priority)
        (["subpoena", "lawsuit", "legal notice", "attorney"], "CLO", "critical"),
        (["attorney", "counsel", "legal"], "CLO", "high"),

        # Press/Media
        (["interview", "press", "journalist", "media", "reporter"], "CMO", "high"),

        # Investor
        (["invest", "funding", "valuation", "venture", "vc"], "CFO", "high"),

        # Technical
        (["bug", "error", "not working", "broken", "api"], "CTO", "normal"),

        # Support
        (["help", "support", "issue", "problem"], "COO", "normal"),

        # Sales/Partnership
        (["pricing", "demo", "trial", "purchase"], "CMO", "normal"),
        (["partner", "collaborate", "integration"], "CEO", "normal"),

        # Finance
        (["invoice", "payment", "receipt"], "CFO", "normal"),

        # HR
        (["job", "resume", "apply", "position", "hiring"], "COO", "low"),
    ]

    def __init__(self, factory_id: Optional[str] = None):
        super().__init__("CXA", "Chief Experience Agent", factory_id)
        self.memory_path = self._get_memory_path()
        self.logs_path = self._get_logs_path()

    def _get_memory_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CXA" / ".cxa" / "memory"

    def _get_logs_path(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "C-Suites" / "CXA" / "logs"

    def _get_project_root(self) -> Path:
        return Path(__file__).parent.parent.parent.parent

    def _log_session(self, log_type: str, data: Dict[str, Any]) -> bool:
        try:
            self.logs_path.mkdir(parents=True, exist_ok=True)
            date_str = datetime.utcnow().strftime("%Y-%m-%d")

            # Use subdirectories for different log types
            if log_type in ["email", "emails"]:
                log_dir = self.logs_path / "emails"
            elif log_type in ["call", "calls"]:
                log_dir = self.logs_path / "calls"
            else:
                log_dir = self.logs_path

            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"{log_type}-{date_str}.md"

            with open(log_path, 'a') as f:
                f.write(f"\n\n---\n\n# {log_type.title()} Session\n\n")
                f.write(f"**Date**: {datetime.utcnow().isoformat()}Z\n\n")
                f.write(json.dumps(data, indent=2))
            return True
        except Exception as e:
            self.logger.error(f"Could not log session: {e}")
            return False

    def _route_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Determine routing for incoming email."""
        sender = email.get("from", "")
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()
        combined = subject + " " + body

        for keywords, agent, priority in self.EMAIL_ROUTING:
            if any(kw in combined for kw in keywords):
                return {
                    "route_to": agent,
                    "reason": f"Keyword match: {keywords[0]}",
                    "priority": priority
                }

        # Unknown - queue for human
        return {
            "route_to": "HUMAN",
            "reason": "Could not determine routing",
            "priority": "normal"
        }

    # =========================================================================
    # CXA.EMAIL - Email management
    # =========================================================================

    def cxa_email(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Email management and routing.
        """
        action = payload.get("action", "check")

        if action == "check":
            # Check inbox status (would connect to Gmail API in production)
            return {
                "message": "Email inbox status",
                "unread": 0,
                "pending_routing": 0,
                "pending_response": 0,
                "note": "Gmail API integration required for production"
            }

        elif action == "route":
            email = payload.get("email", {})
            if not email:
                return {"error": "Email data required"}

            routing = self._route_email(email)

            self._log_session("email", {
                "action": "route",
                "from": email.get("from"),
                "subject": email.get("subject"),
                "routed_to": routing["route_to"],
                "priority": routing["priority"]
            })

            return {
                "message": "Email routed",
                "routing": routing,
                "email_preview": {
                    "from": email.get("from"),
                    "subject": email.get("subject")
                }
            }

        elif action == "respond":
            email_id = payload.get("email_id")
            response = payload.get("response")
            approved_by = payload.get("approved_by")

            if not all([email_id, response]):
                return {"error": "email_id and response required"}

            # Log the response
            self._log_session("email", {
                "action": "respond",
                "email_id": email_id,
                "approved_by": approved_by,
                "sent": datetime.utcnow().isoformat()
            })

            return {
                "message": "Response queued",
                "email_id": email_id,
                "note": "Gmail API integration required to send"
            }

        elif action == "search":
            query = payload.get("query", "")
            return {
                "message": f"Email search for: {query}",
                "results": [],
                "note": "Gmail API integration required for search"
            }

        return {"error": f"Unknown action: {action}"}

    # =========================================================================
    # CXA.PHONE - Phone communications
    # =========================================================================

    def cxa_phone(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phone communications via Twilio.
        """
        action = payload.get("action", "status")

        if action == "status":
            return {
                "message": "Phone system status",
                "configured": False,
                "number": None,
                "calls_today": 0,
                "voicemails": 0,
                "note": "Twilio integration required for production"
            }

        elif action == "call":
            to_number = payload.get("to")
            message = payload.get("message")

            if not to_number:
                return {"error": "Phone number required"}

            self._log_session("call", {
                "action": "outbound_call",
                "to": to_number,
                "initiated": datetime.utcnow().isoformat()
            })

            return {
                "message": "Call initiated",
                "to": to_number,
                "status": "pending",
                "note": "Twilio integration required to complete call"
            }

        elif action == "sms":
            to_number = payload.get("to")
            message = payload.get("message")

            if not all([to_number, message]):
                return {"error": "Phone number and message required"}

            self._log_session("call", {
                "action": "sms",
                "to": to_number,
                "message_preview": message[:50]
            })

            return {
                "message": "SMS queued",
                "to": to_number,
                "note": "Twilio integration required to send"
            }

        return {"error": f"Unknown action: {action}"}

    # =========================================================================
    # CXA.SCHEDULE - Calendar and scheduling
    # =========================================================================

    def cxa_schedule(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calendar and scheduling management.
        """
        action = payload.get("action", "view")

        if action == "view":
            date = payload.get("date", datetime.utcnow().strftime("%Y-%m-%d"))
            return {
                "message": f"Schedule for {date}",
                "events": [],
                "availability": "Open",
                "note": "Google Calendar integration required"
            }

        elif action == "book":
            event = payload.get("event", {})
            return {
                "message": "Meeting booking requested",
                "event": event,
                "status": "pending_confirmation",
                "note": "Requires human confirmation for external meetings"
            }

        elif action == "availability":
            date_range = payload.get("date_range", "this_week")
            return {
                "message": f"Availability for {date_range}",
                "slots": [],
                "note": "Google Calendar integration required"
            }

        return {"error": f"Unknown action: {action}"}

    # =========================================================================
    # CXA.CONTACTS - Contact management
    # =========================================================================

    def cxa_contacts(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Contact management.
        """
        action = payload.get("action", "list")

        if action == "list":
            return {
                "message": "Contact list",
                "contacts": [],
                "total": 0,
                "note": "Contacts stored in BigQuery in production"
            }

        elif action == "add":
            contact = payload.get("contact", {})
            if not contact.get("email") and not contact.get("phone"):
                return {"error": "Email or phone required"}

            self._log_session("contacts", {
                "action": "add",
                "contact": {
                    "name": contact.get("name"),
                    "email": contact.get("email"),
                    "phone": contact.get("phone")
                }
            })

            return {
                "message": "Contact added",
                "contact": contact
            }

        elif action == "search":
            query = payload.get("query", "")
            return {
                "message": f"Contact search for: {query}",
                "results": []
            }

        elif action == "lookup":
            email = payload.get("email")
            phone = payload.get("phone")

            return {
                "message": "Contact lookup",
                "found": False,
                "contact": None,
                "note": "BigQuery integration required for lookup"
            }

        return {"error": f"Unknown action: {action}"}


# Cloud Function Entry Point
def entry_point(request):
    request_json = request.get_json(silent=True)
    if not request_json:
        return {"error": "JSON body required"}, 400

    command = request_json.get("command")
    payload = request_json.get("payload", {})
    factory_id = request_json.get("factory_id")

    if not command:
        return {"error": "Command required"}, 400

    agent = CXAAgent(factory_id=factory_id)
    result = agent.run(command, payload)
    return result


if __name__ == "__main__":
    import sys
    agent = CXAAgent()

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [payload_json]")
        print("Commands: cxa.email, cxa.phone, cxa.schedule, cxa.contacts")
        sys.exit(1)

    command = sys.argv[1]
    payload = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = agent.run(command, payload)
    print(json.dumps(result, indent=2))
