import streamlit as st
import traceback

# 1. PAGE SETUP
st.set_page_config(page_title="AI Market Analyst", page_icon="⚡", layout="wide")

try:
    from config import get_country_config
    from agents import analyze_market_trends, lookup_tax_rate
    from scraper import get_price_data
    from sourcing_agent import get_wholesale_cost
    from brain import calculate_viability_score
    from validator import get_market_guardrails

    # CUSTOM CSS
    st.markdown("""
    <style>
        .verdict-box { 
            padding: 20px; border-radius: 12px; text-align: center; 
            font-weight: bold; color: white !important; margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        .thesis-box {
            background-color: #e3f2fd; border-left: 6px solid #2196f3;
            padding: 20px; border-radius: 10px; margin-bottom: 25px;
            color: #0d47a1; font-size: 16px; font-weight: 500;
        }
        .strategy-card { 
            background-color: #f0f2f6 !important; color: #000 !important;
            padding: 20px; border-radius: 10px; border-left: 6px solid #007bff; margin-top: 15px; 
        }
        .signal-box {
            background-color: #ffffff; border: 1px solid #e0e0e0;
            padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 8px;
        }
        .signal-val { font-size: 14px; font-weight: 700; color: #333; }
        .signal-label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.5px;}
        
        .finance-item {
            display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px dashed #eee;
        }
        .finance-label { color: #555; font-size: 14px; }
        .finance-value { font-weight: bold; color: #000; }
        .finance-total {
            display: flex; justify-content: space-between; padding: 12px 0; border-top: 2px solid #333; margin-top: 10px; font-weight: 800; font-size: 16px;
        }

        .stTabs [data-baseweb="tab"] { background-color: #e0e0e0 !important; color: #000 !important; font-weight: 600; }
        .stTabs [aria-selected="true"] { background-color: #fff !important; color: #ff4b4b !important; border-top: 3px solid #ff4b4b; }
        
        .source-tag { font-size: 11px; color: #888; text-align: center; margin-top: 50px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

    st.title("⚡ AI Market Analyst")
    st.markdown("### The Transparent Product Intelligence Engine")

    # 2. SIDEBAR
    with st.sidebar:
        st.header("🎯 Mission Control")
        selected_country = st.selectbox("Target Market", ["UK", "INDIA"])
        product_name = st.text_input("Product Idea", placeholder="e.g. Smart Ring")
        config = get_country_config(selected_country)
        st.divider()
        st.info(f"📍 **Region:** {config['country_full']}\n\n💷 **Currency:** {config['currency_symbol']}")
        start_btn = st.button("Initialize Deep Scan 🚀", type="primary", use_container_width=True)

        with st.expander("🛠️ Scoring Methodology"):
            st.caption("""
            **Weighted Multi-Factor Index:**
            - 📈 **Demand (30%):** Search Vol, CAGR, Social Momentum
            - ⚔️ **Competition (25%):** Listings, Price Spread, Dominance
            - 💰 **Economics (25%):** Margins, AOV, LTV Potential
            - 🌏 **Ecosystem (20%):** App Maturity, Retail Trust, Adoption Barriers
            """)

    # 3. MAIN LOGIC
    if start_btn and product_name:
        st.divider()
        
        # PHASE 1: LOADING
        with st.status("🔄 Initializing Universal Market Engine...", expanded=True) as status:
            st.write("⚖️ Agent 0: Calibrating Market Norms...")
            guardrails = get_market_guardrails(product_name, config)
            st.write(f"✅ Target Range: {config['currency_symbol']}{guardrails['min_price']} - {config['currency_symbol']}{guardrails['max_price']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("🕵️ Agent 1: Demand Signals...")
                market_data = analyze_market_trends(product_name, config)
            with col2:
                st.write("⚔️ Agent 2: Competitive Scan...")
                competitor_data = get_price_data(product_name, config, guardrails)
            with col3:
                st.write("🏭 Agent 3: Supply Chain...")
                sourcing_data = get_wholesale_cost(product_name, config)
            
            st.write("⚖️ Agent 4: Tax & Compliance Scan...")
            tax_info = lookup_tax_rate(product_name, config)
            st.caption(f"Detected Tax Slab: {int(tax_info.get('rate', 0.18)*100)}% ({tax_info.get('reason', 'Standard')})")
                
            st.write("🧠 Agent 5: Synthesizing Strategy...")
            verdict = calculate_viability_score(product_name, config, market_data, competitor_data, sourcing_data, tax_info)
            status.update(label="Deep Analysis Complete", state="complete", expanded=False)

        # PHASE 2: DASHBOARD
        st.markdown("---")
        
        # 1. VERDICT SECTION
        v_col, s_col, c_col = st.columns([2, 1, 1])
        with v_col:
            tag = verdict.get('verdict_tag', 'MONITOR')
            if "AGGRESSIVELY" in tag: bg_color = "#28a745"
            elif "CAUTIOUSLY" in tag: bg_color = "#ffc107"
            else: bg_color = "#dc3545"
            st.markdown(f'<div class="verdict-box" style="background-color: {bg_color}; font-size: 24px;">{tag}</div>', unsafe_allow_html=True)
            st.info(f"💡 **Action:** {verdict.get('recommendation')}")

        with s_col:
            final_score = verdict.get('final_score', 0)
            st.metric("Viability Score", f"{final_score}/10")
            st.progress(final_score / 10)

        with c_col:
            conf = verdict.get('confidence_score', 50)
            st.metric("Confidence", f"{conf}%")
            vol = verdict.get('volatility', 'Medium')
            vol_color = "orange" if vol == "Medium" else "red" if vol == "High" else "green"
            st.caption(f"Market Volatility: :{vol_color}[{vol}]")

        # 2. STRATEGIC THESIS
        st.markdown(f"""
        <div class="thesis-box">
            🧠 <b>Strategic Thesis:</b> {verdict.get('strategic_thesis', 'Analysis pending...')}
        </div>
        """, unsafe_allow_html=True)

        # 3. FINANCIALS (SAFE MODE)
        st.markdown("---")
        st.subheader("💰 Profitability Analysis (Estimates)")
        
        fin = verdict.get('financials', {})
        currency = config['currency_symbol']
        
        f_col1, f_col2 = st.columns([1, 1])
        
        with f_col1:
            sell_price = fin.get('sell_price', 0)
            cogs = fin.get('cogs', 0)
            gross_profit = sell_price - cogs
            net_profit = fin.get('net_profit', 0)
            
            # SAFE MODE: Round numbers to avoid "fake precision"
            def safe_num(n): return f"{int(n):,}"
            
            st.markdown(f"""
            <div style="background:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ddd;">
                <div class="finance-item"><span class="finance-label">Avg Market Price</span><span class="finance-value">{currency}{safe_num(sell_price)}</span></div>
                <div class="finance-item"><span class="finance-label" style="color:#d9534f;">- Est. Manufacturing (COGS)</span><span class="finance-value" style="color:#d9534f;">{currency}{safe_num(cogs)}</span></div>
                <div class="finance-item" style="border-top:1px solid #ccc; background:#fff;"><span class="finance-label"><b>= Gross Profit</b></span><span class="finance-value">{currency}{safe_num(gross_profit)}</span></div>
                <div class="finance-item"><span class="finance-label" style="color:#f0ad4e;">- Marketing & Ops Costs</span><span class="finance-value" style="color:#f0ad4e;">{currency}{safe_num(fin.get('marketing_cpa') + fin.get('logistics_cost'))}</span></div>
                <div class="finance-item"><span class="finance-label" style="color:#f0ad4e;">- Est. Tax/VAT</span><span class="finance-value" style="color:#f0ad4e;">{currency}{safe_num(fin.get('tax_rate'))}</span></div>
                <div class="finance-total"><span style="color:#28a745;">= NET PROFIT ESTIMATE</span><span style="color:#28a745;">~ {currency}{safe_num(net_profit)}</span></div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("*Based on category benchmarks. Actual costs may vary.*")
            
        with f_col2:
            st.write("#### 📊 Margin Health")
            
            # Qualitative Health Check instead of just raw numbers
            net_m = fin.get('net_margin_pct', 0)
            
            # Determine color and text
            if net_m > 25: 
                health_color = "#28a745" # Green
                health_text = "Healthy"
            elif net_m > 10: 
                health_color = "#ffc107" # Orange
                health_text = "Tight"
            else:
                health_color = "#dc3545" # Red
                health_text = "Critical"
            
            # FORCE HTML RENDERING (This fixes the ": red[...]" bug)
            st.markdown(f"""
            <div style="font-size: 16px; margin-bottom: 10px;">
                Projected Net Margin: <span style="color: {health_color}; font-weight: bold;">{health_text} (~{net_m}%)</span>
            </div>
            """, unsafe_allow_html=True)
            
            if "note" in fin: st.info(f"ℹ️ **Analyst Note:** {fin['note']}")
            
            if net_m > 0:
                st.progress(min(net_m / 40, 1.0)) 
            else:
                st.error("⚠️ Negative Net Margin projected. High Risk.")

        # 4. STRATEGY
        st.markdown("---")
        st.subheader("🚀 Market Entry Strategy")
        entry = verdict.get('market_entry', {})
        st.markdown(f"""
        <div class="strategy-card">
            <h3>Recommended Path: {entry.get('strategy', 'N/A')}</h3>
            <p>{entry.get('reason', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

        # 5. TRACEABLE SCORING
        st.markdown("---")
        st.subheader("🔍 Logic Breakdown (Triangulated Intelligence)")
        bk = verdict.get('breakdown', {})
        
        def render_pillar(data, pillar_name, help_text):
            c1, c2 = st.columns([1, 4])
            with c1:
                st.metric(f"{pillar_name} Score", f"{data.get('total')}/10", help=help_text)
            with c2:
                st.progress(data.get('total', 0)/10)
                st.caption(f"**Primary Driver:** {data.get('reason', '-')}")
            
            s1, s2, s3 = st.columns(3)
            signals = [data.get('signal_1'), data.get('signal_2'), data.get('signal_3')]
            
            for col, sig in zip([s1, s2, s3], signals):
                if sig:
                    parts = str(sig).split(":", 1)
                    label = parts[0]
                    val = parts[1] if len(parts) > 1 else ""
                    with col:
                        st.markdown(f"""
                        <div class="signal-box">
                            <div class="signal-label">{label}</div>
                            <div class="signal-val">{val}</div>
                        </div>
                        """, unsafe_allow_html=True)

        t1, t2, t3, t4 = st.tabs(["📈 Demand", "⚔️ Competition", "💵 Economics", "🌏 Ecosystem"])
        
        with t1: render_pillar(bk.get('demand', {}), "Demand", "0=Dead, 10=Viral")
        with t2: 
            render_pillar(bk.get('competition', {}), "Competition", "0=Blue Ocean, 10=Bloodbath")
            with st.expander("View Competitor List"): st.dataframe(competitor_data['products'])
        with t3: render_pillar(bk.get('economics', {}), "Economics", "0=Money Pit, 10=Cash Cow")
        with t4: render_pillar(bk.get('culture', {}), "Ecosystem", "0=Impossible, 10=Plug & Play")

        # 6. PROS & CONS
        st.markdown("---")
        col_p, col_c = st.columns(2)
        
        with col_p:
            st.subheader("✅ Advantages")
            for p in verdict.get('pros', []):
                if isinstance(p, dict):
                    bullets = "".join([f"\n- {s}" for s in p.get('specs', [])])
                    st.success(f"**{p.get('title')}**{bullets}")
                else: st.success(p)
        
        with col_c:
            st.subheader("⚠️ Risks")
            for c in verdict.get('cons', []):
                if isinstance(c, dict):
                    bullets = "".join([f"\n- {s}" for s in c.get('specs', [])])
                    st.error(f"**{c.get('title')}**{bullets}")
                else: st.error(c)

        # 7. FOOTER
        st.markdown("---")
        st.markdown("""
        <div class='source-tag'>
        Sources: Google Trends, Google Shopping Sampling, Category Benchmarking, Regulatory Databases.<br>
        Estimations are heuristic-based for strategic planning. Volatility index is AI-projected.
        </div>
        """, unsafe_allow_html=True)

    elif start_btn and not product_name:
        st.warning("Please enter a product name.")

except Exception as e:
    st.error("🚨 SYSTEM CRASHED")
    st.write("The app encountered a critical error. Please show this to the developer:")
    st.code(traceback.format_exc())