import random
import time
from functools import wraps
from datetime import datetime

# Retry decorator for tool calls
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    print(f"[ATTEMPT {attempt + 1}/{max_attempts}] {func.__name__}")
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"✅ {func.__name__} succeeded on attempt {attempt + 1}")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                    if attempt < max_attempts - 1:
                        print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
            raise Exception(f"{func.__name__} failed after {max_attempts} attempts: {last_exception}")
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def get_order(order_id):
    """Fetch order details by ID"""
    print(f"[TOOL] 🔍 Fetching order {order_id}")
    
    # Simulate different order statuses
    statuses = ["delivered", "shipped", "processing", "cancelled", "delivered"]
    amounts = [500, 1000, 1500, 2000, 2500]
    
    # Simulate occasional timeout (10% chance)
    if random.random() < 0.1:
        time.sleep(2)  # Simulate slow response
        raise Exception("Order service timeout")
    
    return {
        "order_id": order_id,
        "status": random.choice(statuses),
        "amount": random.choice(amounts),
        "order_date": "2024-01-15",
        "items": random.randint(1, 5)
    }

@retry(max_attempts=2, delay=0.5)
def get_customer(email):
    """Fetch customer details by email"""
    print(f"[TOOL] 👤 Fetching customer {email}")
    
    # Simulate customer tiers
    tiers = ["gold", "silver", "bronze", "platinum"]
    
    # Simulate occasional failure (15% chance)
    if random.random() < 0.15:
        raise Exception("Customer database connection failed")
    
    return {
        "email": email,
        "tier": random.choice(tiers),
        "loyalty_points": random.randint(100, 5000),
        "member_since": "2023-01-01"
    }

@retry(max_attempts=3, delay=1)
def check_refund_eligibility(order_id, order_status, customer_tier):
    """Check if order is eligible for refund"""
    print(f"[TOOL] 🔄 Checking refund eligibility for order {order_id}")
    
    # Simulate complex business logic
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
    elif order_status == "cancelled":
        eligible = False
        reason = "Order already cancelled"
    else:
        eligible = False
        reason = "Order still processing"
    
    # Gold/Platinum customers get special treatment
    if customer_tier in ["gold", "platinum"] and not eligible:
        eligible = True
        reason = f"Courtesy refund for {customer_tier} tier customer"
    
    return {
        "eligible": eligible,
        "reason": reason,
        "max_refund_amount": 1000 if eligible else 0
    }

@retry(max_attempts=2, delay=1)
def issue_refund(order_id, amount, customer_tier):
    """Process refund for customer"""
    print(f"[TOOL] 💰 Issuing refund of ${amount} for order {order_id}")
    
    # Simulate refund processing
    if random.random() < 0.1:
        raise Exception("Payment gateway timeout")
    
    refund_id = f"REF_{order_id}_{int(time.time())}"
    
    # Different processing times based on tier
    processing_days = 1 if customer_tier in ["gold", "platinum"] else 3
    
    return {
        "success": True,
        "refund_id": refund_id,
        "amount": amount,
        "processing_days": processing_days,
        "message": f"Refund of ${amount} initiated successfully"
    }

@retry(max_attempts=2, delay=0.5)
def send_reply(ticket_id, message, customer_email):
    """Send reply to customer"""
    print(f"[TOOL] 📧 Sending reply to ticket {ticket_id}")
    
    # Simulate email sending
    if random.random() < 0.05:
        raise Exception("Email service unavailable")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "success": True,
        "ticket_id": ticket_id,
        "message_sent": message,
        "sent_to": customer_email,
        "timestamp": timestamp
    }

@retry(max_attempts=1, delay=0)
def escalate(ticket_id, summary, priority, reason):
    """Escalate ticket to human agent"""
    print(f"[TOOL] 🚨 Escalating ticket {ticket_id} with {priority} priority")
    
    escalation_id = f"ESC_{ticket_id}_{int(time.time())}"
    
    return {
        "success": True,
        "escalation_id": escalation_id,
        "assigned_team": "Senior Support",
        "response_time": "1 hour" if priority == "high" else "4 hours",
        "priority": priority,
        "reason": reason
    }