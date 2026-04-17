#!/usr/bin/env python3
"""
Hackathon 2026 - AI Customer Support Agent
Automated ticket processing system with intelligent decision making
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from src.workflows.ticket_processor import process_tickets
from src.agent.agent import SupportAgent

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ["logs", "data", "src/agent", "src/tools", "src/workflows"]
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def load_tickets(file_path="data/tickets.json"):
    """Load tickets from JSON file"""
    try:
        with open(file_path, 'r') as f:
            tickets = json.load(f)
        print(f"✅ Loaded {len(tickets)} tickets from {file_path}")
        return tickets
    except FileNotFoundError:
        print(f"❌ Tickets file not found: {file_path}")
        print("Creating sample tickets...")
        
        # Create sample tickets if file doesn't exist
        sample_tickets = [
            {
                "id": "T001",
                "issue": "refund request",
                "order_id": "ORD-001",
                "customer_email": "sample@example.com"
            }
        ]
        
        with open(file_path, 'w') as f:
            json.dump(sample_tickets, f, indent=2)
        
        return sample_tickets

def save_results(results, file_path="logs/audit_log.json"):
    """Save processing results to audit log"""
    audit_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tickets": len(results),
        "results": results
    }
    
    with open(file_path, 'w') as f:
        json.dump(audit_data, f, indent=2)
    
    print(f"✅ Results saved to {file_path}")

def print_agent_info():
    """Print agent capabilities"""
    agent = SupportAgent()
    stats = agent.get_stats()
    
    print("\n" + "="*60)
    print("🤖 AI SUPPORT AGENT SYSTEM")
    print("="*60)
    print(f"Agent: {stats['agent_name']}")
    print(f"Tools Available: {', '.join(stats['tools_available'])}")
    print(f"Features:")
    print("  ✅ Intelligent decision making")
    print("  ✅ Automatic refund processing")
    print("  ✅ Customer tier recognition")
    print("  ✅ Smart escalation system")
    print("  ✅ Concurrent ticket processing")
    print("  ✅ Retry logic with fallbacks")
    print("  ✅ Comprehensive audit logging")
    print("="*60 + "\n")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI Customer Support Agent')
    parser.add_argument('--tickets', type=str, default='data/tickets.json',
                       help='Path to tickets JSON file')
    parser.add_argument('--output', type=str, default='logs/audit_log.json',
                       help='Path for audit log output')
    parser.add_argument('--workers', type=int, default=5,
                       help='Number of concurrent workers')
    parser.add_argument('--no-concurrent', action='store_true',
                       help='Disable concurrent processing')
    
    args = parser.parse_args()
    
    # Setup
    setup_directories()
    
    # Print header
    print("\n" + "🎯"*30)
    print("HACKATHON 2026 - AI CUSTOMER SUPPORT AGENT")
    print("🎯"*30)
    
    # Print agent info
    print_agent_info()
    
    # Load tickets
    tickets = load_tickets(args.tickets)
    
    if not tickets:
        print("❌ No tickets to process. Exiting.")
        sys.exit(1)
    
    # Process tickets
    print("🚀 Starting ticket processing...\n")
    
    try:
        results = process_tickets(
            tickets, 
            use_concurrency=not args.no_concurrent,
            max_workers=args.workers
        )
        
        # Save results
        save_results(results, args.output)
        
        # Print final summary
        print("\n" + "🏆"*30)
        print("PROCESSING COMPLETE")
        print("🏆"*30)
        
        # Show some results
        print("\n📋 Sample Results:")
        for i, result in enumerate(results[:3]):  # Show first 3 results
            print(f"\n  Ticket {i+1}: {result.get('ticket_id', 'Unknown')}")
            print(f"    Action: {result.get('final_action', 'unknown')}")
            print(f"    Tools Used: {len(result.get('tools_called', []))}")
            if result.get('errors'):
                print(f"    Errors: {len(result.get('errors', []))}")
        
        if len(results) > 3:
            print(f"\n  ... and {len(results)-3} more tickets processed")
        
        print("\n✅ Check logs/audit_log.json for complete details")
        print("\n🎉 Hackathon project ready for demo!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()