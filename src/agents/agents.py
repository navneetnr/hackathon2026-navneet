import time
from datetime import datetime
from src.tools.tools import *

class SupportAgent:
    """Intelligent customer support agent that makes decisions using tools"""
    
    def __init__(self):
        self.agent_name = "AutoSupport v2.0"
        self.total_tickets_processed = 0
        self.success_rate = 0
        
    def process_ticket(self, ticket):
        """Process a single support ticket with intelligent decision making"""
        ticket_id = ticket["id"]
        issue = ticket["issue"]
        order_id = ticket.get("order_id", "unknown")
        customer_email = ticket.get("customer_email", "customer@example.com")
        
        print(f"\n{'='*60}")
        print(f"🤖 Agent {self.agent_name} processing ticket {ticket_id}")
        print(f"📝 Issue: {issue}")
        print(f"🆔 Order ID: {order_id}")
        print(f"{'='*60}")
        
        audit_log = {
            "ticket_id": ticket_id,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "tools_called": [],
            "decisions": [],
            "errors": [],
            "final_action": None
        }
        
        try:
            # STEP 1: Fetch order details
            print(f"\n📋 STEP 1: Fetching order information...")
            order = get_order(order_id)
            audit_log["steps"].append("Order fetched successfully")
            audit_log["tools_called"].append("get_order")
            print(f"   ✅ Order status: {order['status']}, Amount: ${order['amount']}")
            
            # STEP 2: Get customer information
            print(f"\n👤 STEP 2: Retrieving customer profile...")
            customer = get_customer(customer_email)
            audit_log["steps"].append("Customer info retrieved")
            audit_log["tools_called"].append("get_customer")
            print(f"   ✅ Customer tier: {customer['tier']}, Points: {customer['loyalty_points']}")
            
            # STEP 3: Check refund eligibility
            print(f"\n🔄 STEP 3: Checking refund eligibility...")
            eligibility = check_refund_eligibility(
                order_id, 
                order["status"], 
                customer["tier"]
            )
            audit_log["steps"].append("Refund eligibility checked")
            audit_log["tools_called"].append("check_refund_eligibility")
            print(f"   ✅ Eligible: {eligibility['eligible']}")
            print(f"   📝 Reason: {eligibility['reason']}")
            
            # STEP 4: Intelligent decision making
            print(f"\n🧠 STEP 4: Making decision...")
            
            if eligibility["eligible"] and eligibility["max_refund_amount"] > 0:
                # Process refund
                refund_amount = min(order["amount"], eligibility["max_refund_amount"])
                print(f"   💰 Processing refund of ${refund_amount}...")
                
                refund_result = issue_refund(order_id, refund_amount, customer["tier"])
                audit_log["tools_called"].append("issue_refund")
                audit_log["steps"].append(f"Refund processed: ${refund_amount}")
                
                # Send confirmation to customer
                message = f"Dear {customer['tier']} tier customer,\n\n"
                message += f"We have processed a refund of ${refund_amount} for order {order_id}.\n"
                message += f"Refund ID: {refund_result['refund_id']}\n"
                message += f"Amount will reflect in {refund_result['processing_days']} business days.\n\n"
                message += f"Reason: {eligibility['reason']}\n"
                message += "Thank you for your patience."
                
                reply_result = send_reply(ticket_id, message, customer_email)
                audit_log["tools_called"].append("send_reply")
                audit_log["steps"].append("Customer notified")
                
                final_action = "refund_processed"
                audit_log["decisions"].append({
                    "action": final_action,
                    "refund_amount": refund_amount,
                    "customer_tier": customer["tier"]
                })
                print(f"   ✅ Refund completed successfully!")
                
            else:
                # Not eligible - escalate with context
                summary = f"Refund request for order {order_id}. "
                summary += f"Order status: {order['status']}. "
                summary += f"Eligibility check failed. Reason: {eligibility['reason']}"
                
                priority = "high" if customer["tier"] in ["gold", "platinum"] else "medium"
                
                escalation_result = escalate(ticket_id, summary, priority, eligibility["reason"])
                audit_log["tools_called"].append("escalate")
                audit_log["steps"].append(f"Ticket escalated with {priority} priority")
                
                # Still send a reply explaining the situation
                message = f"Dear {customer['tier']} tier customer,\n\n"
                message += f"We've reviewed your refund request for order {order_id}.\n"
                message += f"Unfortunately, it's not eligible for automatic refund because: {eligibility['reason']}\n\n"
                message += f"Your ticket has been escalated to our senior support team (ID: {escalation_result['escalation_id']}).\n"
                message += f"Expected response time: {escalation_result['response_time']}\n\n"
                message += "We'll get back to you shortly."
                
                send_reply(ticket_id, message, customer_email)
                audit_log["tools_called"].append("send_reply")
                
                final_action = "escalated"
                audit_log["decisions"].append({
                    "action": final_action,
                    "priority": priority,
                    "reason": eligibility["reason"]
                })
                print(f"   ⚠️ Ticket escalated - not eligible for automatic refund")
            
            audit_log["final_action"] = final_action
            self.total_tickets_processed += 1
            
        except Exception as e:
            # Handle any unexpected errors
            error_msg = f"Critical error processing ticket: {str(e)}"
            print(f"   ❌ {error_msg}")
            audit_log["errors"].append(error_msg)
            
            # Escalate immediately
            try:
                escalate(ticket_id, error_msg, "critical", "System error")
                audit_log["tools_called"].append("escalate")
                audit_log["final_action"] = "error_escalation"
            except:
                audit_log["final_action"] = "failed"
        
        print(f"\n✅ Ticket {ticket_id} processing complete")
        print(f"   Action: {audit_log['final_action']}")
        print(f"   Tools used: {len(audit_log['tools_called'])}")
        
        return audit_log
    
    def get_stats(self):
        """Get agent performance statistics"""
        return {
            "agent_name": self.agent_name,
            "total_processed": self.total_tickets_processed,
            "tools_available": ["get_order", "get_customer", "check_refund_eligibility", 
                               "issue_refund", "send_reply", "escalate"]
        }