# ⚡ Market Analyst AI
### The Transparent Product Intelligence Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=LangChain&logoColor=white)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=OpenAI&logoColor=white)](https://openai.com/)
[![Apify](https://img.shields.io/badge/Apify-97D700?style=flat&logo=Apify&logoColor=white)](https://apify.com/)

**Market Analyst AI** is an autonomous agentic workflow designed to validate product ideas with **strict financial rigor**. Unlike standard chatbots that hallucinate numbers, this engine scrapes real-time data, performs category-specific tax research (GST/VAT), and calculates a precise Unit Economics Waterfall to determine the *real* Net Profit of a product.

---

## 🚀 Key Features

### 🧠 Multi-Agent Architecture
The system employs a swarm of specialized AI agents to triangulate data:
- **🕵️ Agent 1 (Demand):** Analyzes Google Trends & Search Volume.
- **⚔️ Agent 2 (Competition):** Scrapes Amazon/Google Shopping for real-time pricing & rival density.
- **🏭 Agent 3 (Supply Chain):** Estimates sourcing costs via Alibaba/Indiamart logic.
- **⚖️ Agent 4 (Compliance):** Research & validates specific Tax/VAT slabs (e.g., 18% GST for Electronics in India).
- **🧠 Agent 5 (Strategy):** Synthesizes all data into a "Viability Score" and strategic thesis.

### 💰 Strict Financial Waterfall
Most tools stop at Gross Margin. Market Analyst AI calculates the **Net Profit**:
- **Dynamic COGS:** Estimates manufacturing costs based on hardware/software category benchmarks.
- **Tax Reality:** automatically detects if a product falls under specific tax brackets (e.g., 0% for Books vs 18% for Smart Rings).
- **"The 7% Reality":** Intentionally conservative logic to warn users about "tight margin" traps in dropshipping/hardware.

### 🌍 Dual-Market Support
- **🇬🇧 United Kingdom:** Support for GBP (£), VAT rules, and local shipping estimates.
- **🇮🇳 India:** Support for INR (₹), GST slabs, and local market dynamics.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Orchestration:** LangChain
- **LLM:** OpenAI GPT-4o
- **Data Acquisition:**
  - **Apify:** Amazon Product Scraper
  - **Serper.dev:** Google Search & Shopping API

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/nirumutha/Market_Analyst_AI.git](https://github.com/nirumutha/Market_Analyst_AI.git)
   ### 2. Install Dependencies
```bash
pip install -r requirements.txt
