# 🤖 AI Customer Support Agent - Hackathon 2026

## 🎯 Project Overview

An intelligent, autonomous customer support agent that processes support tickets, makes decisions, and takes actions using multiple tools with built-in error handling and concurrency.

## ✨ Features

- **🧠 Intelligent Decision Making**: Agent analyzes tickets and decides best action
- **🔧 Multiple Tool Integration**: 6 different tools for complete support workflow
- **⚡ Concurrent Processing**: Handle multiple tickets simultaneously
- **🔄 Automatic Retry Logic**: Built-in retry mechanism with exponential backoff
- **📊 Comprehensive Audit Logging**: Track every decision and action
- **🎯 Customer Tier Recognition**: Different handling for premium customers
- **🚨 Smart Escalation**: Automatic escalation when needed
- **💪 Error Resilience**: Graceful handling of service failures

## 🛠️ Tools Available

1. `get_order()` - Fetch order details
2. `get_customer()` - Retrieve customer profile
3. `check_refund_eligibility()` - Determine refund eligibility
4. `issue_refund()` - Process refund payments
5. `send_reply()` - Send customer communications
6. `escalate()` - Escalate to human agents

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd hackathon2026-navneet

# Install dependencies
pip install -r requirements.txt

# Run the agent
python main.py