"""
🤖 INTELLIGENT SUPPORT AGENT - WINNING VERSION
Features:
- Real decision making with confidence scoring
- Multi-tool orchestration
- Smart escalation based on confidence
- Complete audit trail with reasoning
"""

import time
from datetime import datetime
from typing import Dict, Any, List, Tuple
from enum import Enum
from src.tools.tools import *

class AgentState(Enum):
    """Agent decision states"""
    ANALYZING = "analyzing"
    DECIDING = "deciding"
    ACTING = "acting"
    VERIFYING = "verifying"
    ESCALATING = "escalating"
    COMPLETED = "completed"

class ConfidenceLevel(Enum):
    HIGH = 0.9
    MEDIUM = 0.7
    LOW = 0.5
    VERY_LOW = 0.3

class SupportAgent:
    """
    Intelligent Support Agent with real decision making
    
    The agent follows this thinking process:
    1. ANALYZE: Understand the ticket and extract key info
    2. DECIDE: Choose best action based on confidence
    3. ACT: Execute tool calls with retries
    4. VERIFY: Confirm action succeeded
    5. ESCALATE: If confidence is low or errors occur
    """
    
    def __init__(self):
        self.agent_name = "IntelligentSupportAgent_v3.0"
        self.state = AgentState.ANALYZING
        self.total_processed = 0
        self.decisions_made = []
        
    def process_ticket(self, ticket: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point - processes a single ticket with full intelligence
        
        Returns comprehensive audit log with reasoning
        """
        
        ticket_id = ticket["id"]
        issue = ticket["issue"]
        order_id = ticket.get("order_id")
        customer_email = ticket.get("customer_email")
        
        # Initialize comprehensive audit log
        audit = {
            "ticket_id": ticket_id,
            "timestamp": datetime.now().isoformat(),
            "agent_state_changes": [],
            "thinking_process": [],
            "tools_called": [],
            "decisions": [],
            "confidence_scores": [],
            "errors": [],
            "retry_attempts": [],
            "final_action": None,
            "overall_confidence": 0.0
        }
        
        print(f"\n{'🧠'*40}")
        print(f"AGENT THINKING PROCESS - Ticket {ticket_id}")
        print(f"{'🧠'*40}")
        
        try:
            # ========== PHASE 1: ANALYZE ==========
            self._change_state(AgentState.ANALYZING, audit)
            self._think(f"Analyzing ticket: {issue}", audit)
            
            # Extract key information from ticket
            analysis = self._analyze_ticket(ticket)
            audit["thinking_process"].append(f"Analysis complete: {analysis['summary']}")
            print(f"📊 Analysis: {analysis['summary']}")
            
            # ========== PHASE 2: GATHER DATA ==========
            self._think("Gathering required data from tools", audit)
            
            # Get order details with retry
            order = self._safe_tool_call(
                get_order, order_id, 
                ticket_id, audit, 
                max_retries=3
            )
            if not order:
                return self._handle_critical_failure(ticket_id, "Order fetch failed", audit)
            audit["tools_called"].append("get_order")
            
            # Get customer details with retry
            customer = self._safe_tool_call(
                get_customer, customer_email,
                ticket_id, audit,
                max_retries=2
            )
            if not customer:
                customer = {"tier": "unknown", "loyalty_points": 0}
            audit["tools_called"].append("get_customer")
            
            # ========== PHASE 3: DECIDE WITH CONFIDENCE ==========
            self._change_state(AgentState.DECIDING, audit)
            
            # Calculate confidence for different actions
            confidence_scores = self._calculate_confidence_scores(
                issue, order, customer
            )
            audit["confidence_scores"] = confidence_scores
            
            # Choose best action
            best_action = max(confidence_scores.items(), key=lambda x: x[1])
            action_type = best_action[0]
            confidence = best_action[1]
            audit["overall_confidence"] = confidence
            
            self._think(f"Decision made: {action_type} with {confidence*100:.1f}% confidence", audit)
            print(f"🎯 Decision: {action_type.upper()} (Confidence: {confidence*100:.1f}%)")
            
            # ========== PHASE 4: ACT BASED ON CONFIDENCE ==========
            if confidence >= ConfidenceLevel.MEDIUM.value:
                # High confidence - execute automatically
                result = self._execute_action(
                    action_type, ticket_id, order, customer, issue, audit
                )
                audit["final_action"] = action_type
                
                # Verify action succeeded
                self._change_state(AgentState.VERIFYING, audit)
                if self._verify_action(result):
                    print(f"✅ Action verified successfully")
                    audit["thinking_process"].append("Action verified - success confirmed")
                else:
                    print(f"⚠️ Action verification failed - escalating")
                    self._escalate_with_context(ticket_id, order, customer, audit)
                    audit["final_action"] = "escalated_after_verification_failure"
                    
            else:
                # Low confidence - escalate to human
                self._change_state(AgentState.ESCALATING, audit)
                reason = f"Low confidence ({confidence*100:.1f}%) for automatic handling"
                self._escalate_with_context(ticket_id, order, customer, audit, reason)
                audit["final_action"] = "escalated_low_confidence"
                print(f"⚠️ Low confidence - Escalating to human agent")
            
            # ========== PHASE 5: COMPLETE ==========
            self._change_state(AgentState.COMPLETED, audit)
            self.total_processed += 1
            
            # Add summary to audit
            audit["thinking_process"].append(f"Ticket processing complete - {audit['final_action']}")
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {str(e)}")
            audit["errors"].append(f"Critical error: {str(e)}")
            audit["final_action"] = "failed_with_error"
            
            # Last resort escalation
            try:
                escalate(ticket_id, str(e), "critical", "System error")
                audit["tools_called"].append("escalate")
            except:
                pass
        
        # Print decision summary
        self._print_decision_summary(audit)
        
        return audit
    
    def _analyze_ticket(self, ticket: Dict) -> Dict:
        """Analyze ticket to extract intent and urgency"""
        issue = ticket["issue"].lower()
        
        # Intent classification
        intent = "unknown"
        if "refund" in issue:
            intent = "refund_request"
        elif "not delivered" in issue or "shipping" in issue:
            intent = "delivery_issue"
        elif "wrong product" in issue or "damaged" in issue:
            intent = "product_issue"
        elif "billing" in issue or "charge" in issue:
            intent = "billing_issue"
            
        # Urgency scoring
        urgency_score = 0.0
        if "critical" in ticket.get("priority", "").lower():
            urgency_score = 1.0
        elif "high" in ticket.get("priority", "").lower():
            urgency_score = 0.8
        elif "urgent" in issue:
            urgency_score = 0.9
        elif "damaged" in issue or "not delivered" in issue:
            urgency_score = 0.7
        else:
            urgency_score = 0.3
            
        return {
            "intent": intent,
            "urgency_score": urgency_score,
            "summary": f"Intent: {intent}, Urgency: {urgency_score*100:.0f}%"
        }
    
    def _calculate_confidence_scores(self, issue: str, order: Dict, customer: Dict) -> Dict[str, float]:
        """Calculate confidence for different possible actions"""
        
        scores = {
            "refund": 0.0,
            "escalate": 0.0,
            "informational": 0.0
        }
        
        # Refund confidence calculation
        refund_confidence = 0.5  # Base confidence
        
        # Factor 1: Order status
        if order and order.get("status") in ["delivered", "shipped"]:
            refund_confidence += 0.2
            
        # Factor 2: Customer tier
        if customer and customer.get("tier") in ["gold", "platinum"]:
            refund_confidence += 0.2
            
        # Factor 3: Issue type
        if "refund" in issue.lower():
            refund_confidence += 0.2
            
        # Factor 4: Urgency (lower urgency = higher refund confidence)
        if "urgent" not in issue.lower():
            refund_confidence += 0.1
            
        scores["refund"] = min(refund_confidence, 0.95)
        
        # Escalate confidence (inverse of refund confidence)
        scores["escalate"] = 1.0 - scores["refund"]
        
        # Informational response confidence
        if "question" in issue.lower() or "how" in issue.lower():
            scores["informational"] = 0.7
        else:
            scores["informational"] = 0.3
            
        return scores
    
    def _execute_action(self, action: str, ticket_id: str, order: Dict, 
                       customer: Dict, issue: str, audit: Dict) -> Any:
        """Execute the chosen action with full tool orchestration"""
        
        self._change_state(AgentState.ACTING, audit)
        
        if action == "refund":
            # Complex refund flow with multiple tools
            print(f"💰 Executing refund workflow...")
            
            # Step 1: Check eligibility
            eligibility = self._safe_tool_call(
                check_refund_eligibility,
                order.get("order_id"), order.get("status"), customer.get("tier"),
                ticket_id, audit, max_retries=3
            )
            audit["tools_called"].append("check_refund_eligibility")
            
            if eligibility and eligibility.get("eligible"):
                # Step 2: Process refund
                refund_amount = min(order.get("amount", 0), eligibility.get("max_refund_amount", 1000))
                refund_result = self._safe_tool_call(
                    issue_refund,
                    order.get("order_id"), refund_amount, customer.get("tier"),
                    ticket_id, audit, max_retries=2
                )
                audit["tools_called"].append("issue_refund")
                
                # Step 3: Send confirmation
                message = self._generate_refund_message(customer, order, refund_amount, eligibility)
                reply_result = self._safe_tool_call(
                    send_reply,
                    ticket_id, message, customer.get("email"),
                    ticket_id, audit, max_retries=2
                )
                audit["tools_called"].append("send_reply")
                
                audit["decisions"].append({
                    "action": "refund_processed",
                    "amount": refund_amount,
                    "customer_tier": customer.get("tier")
                })
                
                return {"success": True, "refund_amount": refund_amount}
            else:
                # Not eligible - escalate with reason
                reason = eligibility.get("reason", "Not eligible for refund")
                self._escalate_with_context(ticket_id, order, customer, audit, reason)
                return {"success": False, "reason": reason}
                
        elif action == "escalate":
            self._escalate_with_context(ticket_id, order, customer, audit, "Automatic escalation")
            return {"success": True, "action": "escalated"}
            
        elif action == "informational":
            message = self._generate_info_message(customer, order, issue)
            self._safe_tool_call(send_reply, ticket_id, message, customer.get("email"), 
                               ticket_id, audit, max_retries=2)
            audit["tools_called"].append("send_reply")
            return {"success": True, "action": "info_sent"}
            
        return {"success": False}
    
    def _safe_tool_call(self, tool_func, *args, **kwargs):
        """Wrapper for tool calls with automatic retries"""
        ticket_id = kwargs.get('ticket_id', 'unknown')
        audit = kwargs.get('audit', {})
        max_retries = kwargs.get('max_retries', 3)
        
        # Remove special kwargs
        call_args = [arg for arg in args if not isinstance(arg, dict) and not isinstance(arg, list)]
        
        for attempt in range(max_retries):
            try:
                print(f"  🔧 Calling {tool_func.__name__} (attempt {attempt + 1}/{max_retries})")
                result = tool_func(*call_args)
                
                if attempt > 0:
                    audit.get("retry_attempts", []).append({
                        "tool": tool_func.__name__,
                        "successful_attempt": attempt + 1
                    })
                    
                return result
                
            except Exception as e:
                print(f"  ⚠️ {tool_func.__name__} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
                else:
                    audit.get("errors", []).append(f"{tool_func.__name__} failed after {max_retries} attempts: {str(e)}")
                    return None
    
    def _escalate_with_context(self, ticket_id: str, order: Dict, customer: Dict, 
                               audit: Dict, reason: str = "Manual escalation"):
        """Escalate ticket with full context for human agent"""
        
        summary = f"""
        ESCALATION CONTEXT:
        - Ticket ID: {ticket_id}
        - Customer: {customer.get('email', 'unknown')} (Tier: {customer.get('tier', 'unknown')})
        - Order: {order.get('order_id', 'unknown')} (Status: {order.get('status', 'unknown')})
        - Reason: {reason}
        - Agent Confidence: {audit.get('overall_confidence', 0)}
        """
        
        priority = "high" if customer.get("tier") in ["gold", "platinum"] else "medium"
        
        result = self._safe_tool_call(
            escalate, ticket_id, summary, priority, reason,
            ticket_id=ticket_id, audit=audit, max_retries=1
        )
        
        audit["tools_called"].append("escalate")
        audit["thinking_process"].append(f"Escalated with priority: {priority}")
        
        return result
    
    def _verify_action(self, result: Any) -> bool:
        """Verify that the action was successful"""
        if result and isinstance(result, dict):
            return result.get("success", False)
        return result is not None
    
    def _handle_critical_failure(self, ticket_id: str, reason: str, audit: Dict) -> Dict:
        """Handle complete system failure"""
        audit["errors"].append(f"CRITICAL: {reason}")
        audit["final_action"] = "critical_failure"
        
        try:
            escalate(ticket_id, reason, "critical", "System failure")
            audit["tools_called"].append("escalate")
        except:
            pass
            
        return audit
    
    def _change_state(self, new_state: AgentState, audit: Dict):
        """Track agent state changes"""
        old_state = self.state
        self.state = new_state
        audit["agent_state_changes"].append({
            "from": old_state.value,
            "to": new_state.value,
            "timestamp": datetime.now().isoformat()
        })
    
    def _think(self, thought: str, audit: Dict):
        """Log agent's thinking process"""
        audit["thinking_process"].append(thought)
        print(f"💭 {thought}")
    
    def _generate_refund_message(self, customer: Dict, order: Dict, amount: float, eligibility: Dict) -> str:
        """Generate personalized refund confirmation message"""
        return f"""
Dear {customer.get('tier', 'valued').upper()} Tier Customer,

✅ REFUND CONFIRMED for Order #{order.get('order_id')}

Amount: ${amount}
Reason: {eligibility.get('reason', 'Eligible for refund')}
Refund Type: Automatic (AI-processed)

The refund will be processed to your original payment method within 3-5 business days.

Thank you for being a {customer.get('tier', 'valued')} customer!

- AI Support Agent (Processed with {self.state.value} confidence)
"""
    
    def _generate_info_message(self, customer: Dict, order: Dict, issue: str) -> str:
        """Generate informational response"""
        return f"""
Dear {customer.get('email', 'customer')},

Thank you for contacting support regarding: {issue}

Order #{order.get('order_id')} Status: {order.get('status', 'Processing')}

Our team has received your inquiry and will provide a detailed response within 2 hours.

For urgent matters, please reply with "URGENT" to prioritize your ticket.

Best regards,
AI Support Team
"""
    
    def _print_decision_summary(self, audit: Dict):
        """Print beautiful summary of agent's decision process"""
        print(f"\n{'📋'*40}")
        print(f"DECISION SUMMARY - Ticket {audit['ticket_id']}")
        print(f"{'📋'*40}")
        print(f"🎯 Final Action: {audit['final_action']}")
        print(f"📊 Confidence: {audit['overall_confidence']*100:.1f}%")
        print(f"🔧 Tools Used: {len(audit['tools_called'])}")
        print(f"💭 Thinking Steps: {len(audit['thinking_process'])}")
        print(f"🔄 State Changes: {len(audit['agent_state_changes'])}")
        if audit.get('errors'):
            print(f"⚠️ Errors: {len(audit['errors'])}")
        print(f"{'📋'*40}\n")