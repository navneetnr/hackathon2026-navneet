import random
import time
import json
from datetime import datetime
from pathlib import Path

# Tool functions
def get_order(order_id):
    print(f"  [TOOL] Fetching order {order_id}")
    time.sleep(0.5)
    return {"order_id": order_id, "status": "delivered", "amount": 1000}

def get_customer(email):
    print(f"  [TOOL] Fetching customer {email}")
    time.sleep(0.5)
    return {"email": email, "tier": "gold"}

def check_refund_eligibility(order_id, status, tier):
    print(f"  [TOOL] Checking eligibility")
    time.sleep(0.5)
    return {"eligible": True, "reason": "Within policy"}

def issue_refund(order_id, amount, tier):
    print(f"  [TOOL] Issuing refund ${amount}")
    time.sleep(0.5)
    return {"success": True}

def send_reply(ticket_id, message, email):
    print(f"  [TOOL] Sending reply to {email}")
    time.sleep(0.5)
    return {"success": True}

def escalate(ticket_id, summary, priority, reason):
    print(f"  [TOOL] Escalating ticket {ticket_id}")
    return {"success": True}

class SupportAgent:
    def process_ticket(self, ticket):
        ticket_id = ticket["id"]
        print(f"\n🧠 Processing {ticket_id}")
        
        try:
            order = get_order(ticket["order_id"])
            customer = get_customer(ticket["customer_email"])
            eligibility = check_refund_eligibility(order["order_id"], order["status"], customer["tier"])
            
            if eligibility["eligible"]:
                issue_refund(order["order_id"], order["amount"], customer["tier"])
                send_reply(ticket_id, "Refund processed", ticket["customer_email"])
                action = "refund_processed"
                confidence = 0.85
            else:
                escalate(ticket_id, "Not eligible", "medium", "Policy")
                action = "escalated"
                confidence = 0.35
        except Exception as e:
            print(f"  Error: {e}")
            action = "error"
            confidence = 0.2
        
        print(f"  ✅ {action} (confidence: {confidence:.0%})")
        return {"ticket_id": ticket_id, "action": action, "confidence": confidence}

# Main
print("="*60)
print("🤖 AI SUPPORT AGENT - HACKATHON 2026")
print("="*60)

tickets = [
    {"id": "T1", "issue": "refund", "order_id": "101", "customer_email": "a@b.com"},
    {"id": "T2", "issue": "delivery", "order_id": "102", "customer_email": "c@d.com"},
    {"id": "T3", "issue": "wrong product", "order_id": "103", "customer_email": "e@f.com"}
]

agent = SupportAgent()
results = []
for ticket in tickets:
    result = agent.process_ticket(ticket)
    results.append(result)

print(f"\n✅ Processed {len(results)} tickets")
