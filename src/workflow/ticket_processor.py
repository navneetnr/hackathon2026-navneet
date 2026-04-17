from concurrent.futures import ThreadPoolExecutor, as_completed
from src.agent.agent import SupportAgent
import time
from datetime import datetime

class TicketProcessor:
    """Process tickets concurrently with intelligent workflow"""
    
    def __init__(self, max_workers=5):
        self.agent = SupportAgent()
        self.max_workers = max_workers
        self.processing_stats = {
            "start_time": None,
            "end_time": None,
            "total_tickets": 0,
            "successful": 0,
            "failed": 0
        }
    
    def process_tickets(self, tickets):
        """Process multiple tickets concurrently"""
        print(f"\n{'🚀'*30}")
        print(f"🎯 Starting ticket processing workflow")
        print(f"📊 Total tickets: {len(tickets)}")
        print(f"⚡ Max concurrent workers: {self.max_workers}")
        print(f"{'🚀'*30}\n")
        
        self.processing_stats["start_time"] = datetime.now()
        self.processing_stats["total_tickets"] = len(tickets)
        
        results = []
        
        # Method 1: Using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tickets for processing
            future_to_ticket = {
                executor.submit(self.agent.process_ticket, ticket): ticket 
                for ticket in tickets
            }
            
            # Process completed futures as they finish
            for future in as_completed(future_to_ticket):
                ticket = future_to_ticket[future]
                try:
                    result = future.result(timeout=30)  # 30 second timeout per ticket
                    results.append(result)
                    self.processing_stats["successful"] += 1
                    print(f"📈 Progress: {self.processing_stats['successful']}/{len(tickets)} completed")
                except Exception as e:
                    print(f"❌ Ticket {ticket.get('id', 'unknown')} failed: {str(e)}")
                    self.processing_stats["failed"] += 1
                    results.append({
                        "ticket_id": ticket.get("id", "unknown"),
                        "error": str(e),
                        "final_action": "failed"
                    })
        
        self.processing_stats["end_time"] = datetime.now()
        
        # Print summary
        self._print_summary()
        
        return results
    
    def process_tickets_batch(self, tickets, batch_size=3):
        """Process tickets in batches (alternative to concurrency)"""
        print(f"\n📦 Processing tickets in batches of {batch_size}")
        
        all_results = []
        for i in range(0, len(tickets), batch_size):
            batch = tickets[i:i+batch_size]
            print(f"\n📋 Batch {i//batch_size + 1}: Processing {len(batch)} tickets")
            batch_results = self.process_tickets(batch)
            all_results.extend(batch_results)
            time.sleep(1)  # Small delay between batches
        
        return all_results
    
    def _print_summary(self):
        """Print processing statistics"""
        duration = (self.processing_stats["end_time"] - self.processing_stats["start_time"]).total_seconds()
        
        print(f"\n{'📊'*30}")
        print(f"PROCESSING SUMMARY")
        print(f"{'📊'*30}")
        print(f"✅ Total Tickets: {self.processing_stats['total_tickets']}")
        print(f"✅ Successful: {self.processing_stats['successful']}")
        print(f"❌ Failed: {self.processing_stats['failed']}")
        print(f"⏱️  Total Time: {duration:.2f} seconds")
        print(f"⚡ Average per ticket: {duration/self.processing_stats['total_tickets']:.2f} seconds")
        print(f"🎯 Success Rate: {(self.processing_stats['successful']/self.processing_stats['total_tickets']*100):.1f}%")
        print(f"{'📊'*30}\n")

# Simple function-based interface for backward compatibility
def process_tickets(tickets, use_concurrency=True, max_workers=5):
    """Simple function to process tickets"""
    processor = TicketProcessor(max_workers=max_workers)
    
    if use_concurrency:
        return processor.process_tickets(tickets)
    else:
        return processor.process_tickets_batch(tickets)