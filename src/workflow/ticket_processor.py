"""
High-performance ticket processor with concurrency and batch processing
"""

from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from src.agent.agent import SupportAgent
import time
from datetime import datetime
from typing import List, Dict, Any
import json

class TicketProcessor:
    """Enterprise-grade ticket processor with advanced features"""
    
    def __init__(self, max_workers: int = 5, timeout_seconds: int = 60):
        self.agent = SupportAgent()
        self.max_workers = max_workers
        self.timeout_seconds = timeout_seconds
        self.stats = {
            "start_time": None,
            "end_time": None,
            "total_tickets": 0,
            "processed": 0,
            "failed": 0,
            "timeouts": 0,
            "confidence_distribution": {
                "high": 0,    # >0.8
                "medium": 0,  # 0.5-0.8
                "low": 0      # <0.5
            }
        }
    
    def process_tickets_concurrent(self, tickets: List[Dict]) -> List[Dict]:
        """
        Process tickets concurrently with ThreadPoolExecutor
        This is where the magic happens - 30% of hackathon points!
        """
        print(f"\n{'⚡'*40}")
        print(f"CONCURRENT PROCESSING MODE")
        print(f"Workers: {self.max_workers} | Timeout: {self.timeout_seconds}s")
        print(f"Total Tickets: {len(tickets)}")
        print(f"{'⚡'*40}\n")
        
        self.stats["start_time"] = datetime.now()
        self.stats["total_tickets"] = len(tickets)
        
        results = []
        
        # Using ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_ticket = {
                executor.submit(self.agent.process_ticket, ticket): ticket 
                for ticket in tickets
            }
            
            # Process as they complete
            for future in as_completed(future_to_ticket):
                ticket = future_to_ticket[future]
                try:
                    # Get result with timeout
                    result = future.result(timeout=self.timeout_seconds)
                    results.append(result)
                    self.stats["processed"] += 1
                    
                    # Update confidence stats
                    confidence = result.get("overall_confidence", 0)
                    if confidence > 0.8:
                        self.stats["confidence_distribution"]["high"] += 1
                    elif confidence > 0.5:
                        self.stats["confidence_distribution"]["medium"] += 1
                    else:
                        self.stats["confidence_distribution"]["low"] += 1
                    
                    print(f"✅ Completed: {result['ticket_id']} ({self.stats['processed']}/{len(tickets)})")
                    
                except TimeoutError:
                    print(f"⏰ Timeout processing ticket {ticket.get('id', 'unknown')}")
                    self.stats["timeouts"] += 1
                    self.stats["failed"] += 1
                    results.append({
                        "ticket_id": ticket.get("id", "unknown"),
                        "final_action": "timeout",
                        "error": "Processing timeout"
                    })
                    
                except Exception as e:
                    print(f"❌ Failed processing {ticket.get('id', 'unknown')}: {str(e)}")
                    self.stats["failed"] += 1
                    results.append({
                        "ticket_id": ticket.get("id", "unknown"),
                        "final_action": "failed",
                        "error": str(e)
                    })
        
        self.stats["end_time"] = datetime.now()
        self._print_stats()
        
        return results
    
    def process_tickets_sequential(self, tickets: List[Dict]) -> List[Dict]:
        """Fallback sequential processing (for comparison)"""
        print(f"\n{'🐢'*40}")
        print(f"SEQUENTIAL PROCESSING MODE (Fallback)")
        print(f"{'🐢'*40}\n")
        
        self.stats["start_time"] = datetime.now()
        self.stats["total_tickets"] = len(tickets)
        
        results = []
        for i, ticket in enumerate(tickets, 1):
            print(f"Processing {i}/{len(tickets)}: {ticket.get('id')}")
            try:
                result = self.agent.process_ticket(ticket)
                results.append(result)
                self.stats["processed"] += 1
            except Exception as e:
                print(f"❌ Failed: {str(e)}")
                self.stats["failed"] += 1
                results.append({"ticket_id": ticket.get("id"), "error": str(e)})
        
        self.stats["end_time"] = datetime.now()
        self._print_stats()
        
        return results
    
    def _print_stats(self):
        """Print beautiful processing statistics"""
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        
        print(f"\n{'📊'*40}")
        print(f"PROCESSING STATISTICS")
        print(f"{'📊'*40}")
        print(f"✅ Successfully Processed: {self.stats['processed']}/{self.stats['total_tickets']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"⏰ Timeouts: {self.stats['timeouts']}")
        print(f"⏱️  Total Time: {duration:.2f} seconds")
        print(f"⚡ Throughput: {self.stats['processed']/duration:.2f} tickets/second")
        print(f"\n📈 Confidence Distribution:")
        print(f"   High (>80%): {self.stats['confidence_distribution']['high']} tickets")
        print(f"   Medium (50-80%): {self.stats['confidence_distribution']['medium']} tickets")
        print(f"   Low (<50%): {self.stats['confidence_distribution']['low']} tickets")
        print(f"{'📊'*40}\n")

# Convenience function
def process_tickets(tickets: List[Dict], use_concurrency: bool = True, max_workers: int = 5) -> List[Dict]:
    """Main entry point for ticket processing"""
    processor = TicketProcessor(max_workers=max_workers)
    
    if use_concurrency:
        return processor.process_tickets_concurrent(tickets)
    else:
        return processor.process_tickets_sequential(tickets)