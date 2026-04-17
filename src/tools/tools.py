import random
import time
from functools import wraps
from datetime import datetime

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    print(f"  [Attempt {attempt + 1}/{max_attempts}]")
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"  ✅ Succeeded on attempt {attempt + 1}")
                    return result
                except Exception as e:
                    print(f"  ❌ Failed: {str(e)}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    else:
                        raise
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def get_order(order_id):
    print(f"  [TOOL] Fetching order {order_id}")
    statuses = ["delivered", "shipped", "processing", "cancelled"]
    amounts = [500, 1000, 1500, 2000]
    
    if random.random() < 0.1:
        raise Exception("Order service timeout")
    
    return {
        "order_id": order_id,
        "status": random.choice(statuses),
        "amount": random.choice(amounts)
    }

@retry(max_attempts=2, delay=0.5)
def get_customer(email):
    print(f"  [TOOL] Fetching customer {email}")
    tiers = ["gold", "silver", "bronze", "platinum"]
    
    if random.random() < 0.15:
        raise Exception("Customer database connection failed")
    
    return {
        "email": email,
        "tier": random.choice(tiers),
        "loyalty_points": random.randint(100, 5000)
    }

@retry(max_attempts=3, delay=1)
def check_refund_eligibility(order_id, order_status, customer_tier):
    print(f"  [TOOL] Checking refund eligibility")
    
    if random.random() < 0.2:
        raise Exception("Refund eligibility service timeout")
    
    eligible = False
    reason = ""
    
    if order_status == "delivered":
        eligible = True
        reason = "Within 30-day return window"
    elif order_status == "shipped":
        eligible = True
        reason = "Order not yet delivered - can cancel"
    else:
        eligible = False
        reason = "Order not eligible for refund"
    
    if customer_tier in ["gold", "platinum"] and not eligible:
        eligible = True
        reason = f"Courtesy refund for {customer_tier} customer"
    
    return {
        "eligible": eligible,
        "reason": reason,
        "max_refund_amount": 1000 if eligible else 0
    }

@retry(max_attempts=2, delay=1)
def issue_refund(order_id, amount, customer_tier):
    print(f"  [TOOL] Issuing refund of ${amount}")
    
    if random.random() < 0.1:
        raise Exception("Payment gateway timeout")
    
    return {
        "success": True,
        "refund_id": f"REF_{order_id}_{int(time.time())}",
        "amount": amount,
        "processing_days": 1 if customer_tier in ["gold", "platinum"] else 3
    }

@retry(max_attempts=2, delay=0.5)
def send_reply(ticket_id, message, customer_email):
    print(f"  [TOOL] Sending reply to {customer_email}")
    
    if random.random() < 0.05:
        raise Exception("Email service unavailable")
    
    return {
        "success": True,
        "ticket_id": ticket_id,
        "sent_to": customer_email,
        "timestamp": datetime.now().isoformat()
    }

@retry(max_attempts=1, delay=0)
def escalate(ticket_id, summary, priority, reason):
    print(f"  [TOOL] 🚨 Escalating ticket {ticket_id} with {priority} priority")
    
    return {
        "success": True,
        "escalation_id": f"ESC_{ticket_id}_{int(time.time())}",
        "assigned_team": "Senior Support",
        "response_time": "1 hour" if priority == "high" else "4 hours"
    }
