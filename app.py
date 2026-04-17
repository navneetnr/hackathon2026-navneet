import streamlit as st
import json
from pathlib import Path
from src.agent.agent import SupportAgent
import pandas as pd

st.set_page_config(page_title="AI Support Agent", layout="wide")

st.title("🤖 AI Customer Support Agent Dashboard")

# Load or create tickets
tickets_file = "data/tickets.json"

if not Path(tickets_file).exists():
    sample_tickets = [
        {"id": "T001", "issue": "refund request - defective", "order_id": "ORD-1", "customer_email": "a@test.com"},
        {"id": "T002", "issue": "order not delivered", "order_id": "ORD-2", "customer_email": "b@test.com"},
        {"id": "T003", "issue": "wrong product", "order_id": "ORD-3", "customer_email": "c@test.com"}
    ]
    Path("data").mkdir(exist_ok=True)
    with open(tickets_file, "w") as f:
        json.dump(sample_tickets, f, indent=2)

with open(tickets_file, "r") as f:
    tickets = json.load(f)

st.subheader("📋 Tickets")
st.json(tickets)

# Run button
if st.button("🚀 Run AI Agent"):
    agent = SupportAgent()
    results = []

    for ticket in tickets:
        result = agent.process_ticket(ticket)
        results.append(result)

    # Save results
    Path("logs").mkdir(exist_ok=True)
    with open("logs/audit_log.json", "w") as f:
        json.dump(results, f, indent=2)

    st.success("✅ Processing Complete!")

    # Convert to dataframe
    df = pd.DataFrame(results)

    st.subheader("📊 Results Table")
    st.dataframe(df)

    # Dashboard charts
    st.subheader("📈 Analytics Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Actions Distribution")
        st.bar_chart(df["action"].value_counts())

    with col2:
        st.write("### Confidence Scores")
        st.line_chart(df["confidence"])

    # Metrics
    st.subheader("📌 Key Metrics")

    total = len(df)
    refunds = len(df[df["action"] == "refund_processed"])
    escalations = len(df[df["action"] == "escalated"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", total)
    col2.metric("Refunds", refunds)
    col3.metric("Escalations", escalations)