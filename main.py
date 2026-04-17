import json
from pathlib import Path
from src.agent.agent import SupportAgent

def main():
    print("\n" + "="*60)
    print("🚀 AI CUSTOMER SUPPORT AGENT - HACKATHON 2026")
    print("="*60 + "\n")
    
    # Create data directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Create sample tickets if they don't exist
    tickets_file = "data/tickets.json"
    if not Path(tickets_file).exists():
        sample_tickets = [
            {
                "id": "T001",
                "issue": "refund request - product defective",
                "order_id": "ORD-001",
                "customer_email": "john.doe@example.com"
            },
            {
                "id": "T002",
                "issue": "order not delivered",
                "order_id": "ORD-002",
                "customer_email": "jane.smith@example.com"
            },
            {
                "id": "T003",
                "issue": "wrong product received",
                "order_id": "ORD-003",
                "customer_email": "bob.wilson@example.com"
            }
        ]
        with open(tickets_file, "w") as f:
            json.dump(sample_tickets, f, indent=2)
        print(f"✅ Created sample tickets in {tickets_file}\n")
    
    # Load tickets
    with open(tickets_file, "r") as f:
        tickets = json.load(f)
    
    print(f"📋 Loaded {len(tickets)} tickets\n")
    
    # Process tickets
    agent = SupportAgent()
    results = []
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n📌 Ticket {i}/{len(tickets)}")
        result = agent.process_ticket(ticket)
        results.append(result)
    
    # Save audit log
    audit_file = "logs/audit_log.json"
    with open(audit_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 PROCESSING COMPLETE!")
    print("="*60)
    print(f"✅ Total tickets processed: {len(results)}")
    print(f"📊 Audit log saved to: {audit_file}")
    
    # Calculate success rate
    successful = sum(1 for r in results if r['action'] == 'refund_processed')
    escalated = sum(1 for r in results if r['action'] == 'escalated')
    print(f"💰 Refunds processed: {successful}")
    print(f"⚠️ Tickets escalated: {escalated}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
