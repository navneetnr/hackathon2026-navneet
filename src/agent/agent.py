import json
import time
from pathlib import Path
from datetime import datetime
from src.tools.tools import *

class SupportAgent:
    def __init__(self):
        print("🤖 Initializing Support Agent...")
        self.memory_file = "logs/agent_memory.json"
        self.memory = self._load_memory()
    
    def _load_memory(self):
        if Path(self.memory_file).exists():
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return {"tickets_processed": [], "customer_history": {}}
        return {"tickets_processed": [], "customer_history": {}}
    
    def _save_memory(self):
        Path("logs").mkdir(exist_ok=True)
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def process_ticket(self, ticket):
        ticket_id = ticket.get("id", "unknown")
        order_id = ticket.get("order_id", "unknown")
        customer_email = ticket.get("customer_email", "unknown@example.com")
        issue = ticket.get("issue", "")
        
        print(f"\n{'='*50}")
        print(f"📝 Processing Ticket: {ticket_id}")
        print(f"   Issue: {issue}")
        print(f"{'='*50}")
        
        reasoning = []
        tools_used = []
        confidence = 0.5
        
        try:
            # Tool 1: Get order
            print("\n  Step 1: Fetching order...")
            order = get_order(order_id)
            tools_used.append("get_order")
            reasoning.append(f"Order status: {order['status']}, Amount: ${order['amount']}")
            print(f"  ✓ Order found: {order['status']}")
            
            # Tool 2: Get customer
            print("\n  Step 2: Fetching customer...")
            customer = get_customer(customer_email)
            tools_used.append("get_customer")
            reasoning.append(f"Customer tier: {customer['tier']}")
            print(f"  ✓ Customer: {customer['tier']} tier")
            
            # Tool 3: Check eligibility
            print("\n  Step 3: Checking refund eligibility...")
            eligibility = check_refund_eligibility(order_id, order['status'], customer['tier'])
            tools_used.append("check_refund_eligibility")
            reasoning.append(f"Eligible: {eligibility['eligible']} - {eligibility['reason']}")
            print(f"  ✓ Eligibility: {eligibility['eligible']}")
            
            if eligibility['eligible']:
                confidence = 0.85
                
                # Tool 4: Issue refund
                print("\n  Step 4: Processing refund...")
                refund = issue_refund(order_id, order['amount'], customer['tier'])
                tools_used.append("issue_refund")
                reasoning.append(f"Refund issued: ${order['amount']}")
                print(f"  ✓ Refund processed: ${order['amount']}")
                
                # Tool 5: Send reply
                print("\n  Step 5: Sending confirmation...")
                message = f"Your refund of ${order['amount']} for order {order_id} has been approved."
                send_reply(ticket_id, message, customer_email)
                tools_used.append("send_reply")
                reasoning.append("Customer notified")
                print(f"  ✓ Confirmation sent")
                
                action = "refund_processed"
                
            else:
                confidence = 0.35
                
                # Tool 5: Escalate
                print("\n  Step 4: Escalating ticket...")
                escalate(ticket_id, "Not eligible for refund", "medium", eligibility['reason'])
                tools_used.append("escalate")
                reasoning.append(f"Escalated: {eligibility['reason']}")
                print(f"  ✓ Ticket escalated")
                
                action = "escalated"
            
        except Exception as e:
            print(f"\n  ❌ Error: {str(e)}")
            confidence = 0.2
            action = "error"
            reasoning.append(f"Error: {str(e)}")
            
            try:
                escalate(ticket_id, str(e), "high", "System error")
                tools_used.append("escalate")
            except:
                pass
        
        # Save to memory
        self.memory["tickets_processed"].append({
            "ticket_id": ticket_id,
            "action": action,
            "confidence": confidence,
            "tools_used": tools_used,
            "timestamp": datetime.now().isoformat()
        })
        
        if customer_email not in self.memory["customer_history"]:
            self.memory["customer_history"][customer_email] = []
        self.memory["customer_history"][customer_email].append({
            "ticket_id": ticket_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_memory()
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"✅ Final Result for {ticket_id}")
        print(f"   Action: {action}")
        print(f"   Confidence: {confidence:.0%}")
        print(f"   Tools used: {len(tools_used)}")
        print(f"{'='*50}\n")
        
        return {
            "ticket_id": ticket_id,
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "tools_used": tools_used
        }
