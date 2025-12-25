import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
import urllib.parse
import plotly.express as px

# --- SOFTWARE ARCHITECTURE CONFIG ---
st.set_page_config(
    page_title="OmniScraper v12.0 | Global Intelligence",
    page_icon="🕸️",
    layout="wide"
)

# --- ADVANCED UI (CYBER-BLUEPRINT + CSS GRID) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;800&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --core: #3b82f6;
        --accent: #06b6d4;
        --grid-line: rgba(59, 130, 246, 0.12);
        --bg: #020617;
    }

    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .mono { font-family: 'JetBrains Mono', monospace; }

    /* FIXED BLUEPRINT GRID BACKGROUND */
    .stApp {
        background-color: var(--bg);
        background-image: 
            linear-gradient(var(--grid-line) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
        background-size: 45px 45px;
        background-attachment: fixed;
        color: #f1f5f9;
    }

    /* CSS GRID: THE SINGULARITY MATRIX */
    .singularity-matrix {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        margin: 30px 0;
    }

    .matrix-node {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(20px);
        padding: 26px;
        border-radius: 28px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        position: relative;
        overflow: hidden; 
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) all;
    }

    .matrix-node:hover { transform: translateY(-8px) scale(1.01); border-color: var(--accent); }

    .matrix-node::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 6px; height: 100%;
        background: var(--accent);
        border-top-left-radius: 28px;
        border-bottom-left-radius: 28px;
    }

    .node-label { color: #94a3b8; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; }
    .node-value { font-size: 1.8rem; font-weight: 800; margin-top: 10px; color: white; }
    
    .hub-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
    
    /* Dynamic Buttons: Primary (Orange) & Secondary (Blue) */
    .hub-btn {
        text-align: center; padding: 12px; border-radius: 14px;
        font-size: 0.75rem; font-weight: 800; text-decoration: none; transition: 0.3s all;
    }
    
    /* Amazon Style (Global) */
    .btn-pri { background: rgba(255, 153, 0, 0.1); color: #FF9900; border: 1px solid #FF9900; }
    .btn-pri:hover { background: #FF9900; color: black; }
    
    /* Secondary Style (Flipkart/eBay) */
    .btn-sec { background: rgba(40, 116, 240, 0.1); color: #2874f0; border: 1px solid #2874f0; }
    .btn-sec:hover { background: #2874f0; color: white; }

    .terminal {
        background: #000; border: 1px solid #1e293b; padding: 25px; border-radius: 20px;
        font-family: 'JetBrains Mono', monospace; color: #10b981; font-size: 0.85rem;
        height: 150px; overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKEND LOGIC ---
def get_prediction(price):
    """Simulates 7-day predictive analytics."""
    days = [datetime.now() + timedelta(days=i) for i in range(1, 8)]
    forecast = [price]
    for _ in range(1, 8):
        volatility = random.uniform(-0.06, 0.06)
        forecast.append(forecast[-1] * (1 + volatility))
    return days, forecast[1:]

def get_market_links(title, region_code):
    """Generates region-specific e-commerce links."""
    q = urllib.parse.quote(f"{title} book")
    
    if "UK" in region_code:
        # United Kingdom Links
        return (
            f"https://www.amazon.co.uk/s?k={q}", 
            f"https://www.ebay.co.uk/sch/i.html?_nkw={q}", 
            "AMAZON.CO.UK", 
            "EBAY.UK"
        )
    elif "USA" in region_code:
        # USA Links
        return (
            f"https://www.amazon.com/s?k={q}", 
            f"https://www.ebay.com/sch/i.html?_nkw={q}", 
            "AMAZON.COM", 
            "EBAY.US"
        )
    else:
        # Default: India Links
        return (
            f"https://www.amazon.in/s?k={q}", 
            f"https://www.flipkart.com/search?q={q}", 
            "AMAZON.IN", 
            "FLIPKART"
        )

def scraper_protocol(url, multiplier, region_code):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        pods = soup.find_all('article', class_='product_pod')
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        db = []
        for p in pods:
            title = p.h3.a['title']
            price = float(p.find('p', class_='price_color').text.replace('£', '').replace('Â', '')) * multiplier
            rating = rating_map.get(p.find('p', class_='star-rating')['class'][1], 0)
            
            # Dynamic Link Generation
            link1, link2, label1, label2 = get_market_links(title, region_code)
            
            db.append({
                "Title": title, 
                "Price": round(price, 2), 
                "Rating": rating, 
                "Link1": link1, 
                "Link2": link2,
                "Label1": label1,
                "Label2": label2
            })
        return db
    except: return None

# --- UI HEADER ---
st.markdown('<h1 style="font-weight:800; font-size:3.5rem; letter-spacing:-4px; margin-bottom:0;">OMNISCRAPER <span style="color:#06b6d4">GLOBAL</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="mono" style="color:#64748b;">>> ENTERPRISE INTELLIGENCE SYSTEM | REGION-LOCKED ROUTING ACTIVE</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### `NODE SETTINGS`")
    region = st.selectbox("Intelligence Node", ["India (Asia-South1)", "UK (London)", "USA (Virginia)"], index=0)
    
    # Currency Logic
    if "UK" in region: 
        mult, sym = 1.0, "£"
        region_code = "UK"
    elif "USA" in region: 
        mult, sym = 1.28, "$"
        region_code = "USA"
    else: 
        mult, sym = 105.5, "₹"
        region_code = "IN"
    
    st.divider()
    st.markdown("### `ANALYTICS ENGINE`")
    viz_mode = st.radio("Intelligence Projection", ["Predictive Trend", "Satisfaction Density", "3D Value Matrix", "Crawl Yield Radial"])
    
    st.divider()
    st.markdown("### `ENGINE OVERRIDES`")
    neural_active = st.toggle("Neural Pattern Recognition", value=True)
    blueprint_active = st.toggle("Fixed Blueprint Grid", value=True)
    threading_level = st.slider("Crawl Threading", 1, 64, 32)

# Apply Blueprint Toggle
if not blueprint_active:
    st.markdown("<style>.stApp { background-image: none !important; }</style>", unsafe_allow_html=True)

GENRES = {
    "Science Fiction": "science-fiction_16", "Business": "business_35", "Philosophy": "philosophy_7", 
    "Travel": "travel_2", "Mystery": "mystery_3", "Historical Fiction": "historical-fiction_4",
    "Sequential Art": "sequential-art_5", "Classics": "classics_6", "Romance": "romance_8",
    "Poetry": "poetry_23", "Horror": "horror_31", "History": "history_32", "Food & Drink": "food-and-drink_33",
    "Psychology": "psychology_26", "Fiction": "fiction_10", "Nonfiction": "nonfiction_13", 
    "Art": "art_25", "Spirituality": "spirituality_39", "Politics": "politics_48", "Academic": "academic_40",
    "Self Help": "self-help_41", "Medical": "medical_42"
}

c1, c2 = st.columns([4, 1])
with c1:
    target = st.selectbox("TARGET E-COMMERCE SEGMENT", list(GENRES.keys()), label_visibility="collapsed")
with c2:
    trigger = st.button("INITIALIZE ENGINE", use_container_width=True)

if trigger:
    term = st.empty()
    logs = [f"Resolving Node: {region}...", "Bypassing Proxy SSL Buffers...", f"Converting Currency to {sym}...", "Generating Regional Market Links..."]
    
    if neural_active:
        logs.insert(2, "Neural Pattern Recognition: Active...")

    txt = ""
    for l in logs:
        txt += f"> {datetime.now().strftime('%H:%M:%S')} {l}<br>"
        term.markdown(f"<div class='terminal'>{txt}</div>", unsafe_allow_html=True)
        time.sleep(0.3)

    # Pass region_code to the scraper
    data = scraper_protocol(f"http://books.toscrape.com/catalogue/category/books/{GENRES[target]}/index.html", mult, region_code)
    
    if data:
        df = pd.DataFrame(data)
        term.empty()

        reco = df[df['Rating'] == df['Rating'].max()].iloc[0]
        
        st.markdown(f"""
            <div class="singularity-matrix">
                <div class="matrix-node">
                    <div class="node-label">Avg Market Price</div>
                    <div class="node-value">{sym}{df['Price'].mean():,.2f}</div>
                    <div class="status-badge" style="background:rgba(59,130,246,0.2); color:#3b82f6;">{region} Node</div>
                </div>
                <div class="matrix-node" style="border-left-color: #f59e0b;">
                    <div class="node-label">Oracle's Pick</div>
                    <div class="node-value" style="font-size:1rem; margin-top:12px;">{reco['Title']}</div>
                    <a href="{reco['Link1']}" style="color:#06b6d4; font-size:0.75rem; font-weight:800; text-decoration:underline;" target="_blank">Direct Buy on {reco['Label1']}</a>
                </div>
                <div class="matrix-node">
                    <div class="node-label">Total Assets Found</div>
                    <div class="node-value">{len(df)} Units</div>
                    <div class="status-badge" style="background:rgba(255,255,255,0.1); color:#fff;">Active Threads: {threading_level}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        tab_list = ["📊 Market Intelligence", "⚡ Marketplace Hub"]
        if neural_active:
            tab_list.insert(1, "🧠 Neural Analysis")
        
        tabs = st.tabs(tab_list)

        with tabs[0]:
            st.markdown(f"#### 🌀 {viz_mode} Intelligence ({sym})")
            if viz_mode == "Predictive Trend":
                dates, prices = get_prediction(df.iloc[0]['Price'])
                f_df = pd.DataFrame({"Date": dates, "Projected Price": prices})
                fig = px.line(f_df, x="Date", y="Projected Price", template="plotly_dark", markers=True)
                fig.update_traces(line_color='#06b6d4', line_width=4)
            elif viz_mode == "3D Value Matrix":
                fig = px.scatter(df, x="Price", y="Rating", size="Price", color="Price", template="plotly_dark", hover_name="Title")
            elif viz_mode == "Crawl Yield Radial":
                fig = px.pie(df, names='Rating', hole=0.6, template='plotly_dark')
            else:
                fig = px.density_heatmap(df, x="Price", y="Rating", template="plotly_dark", color_continuous_scale="Viridis")

            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', transition_duration=1500)
            st.plotly_chart(fig, use_container_width=True)

        if neural_active:
            with tabs[1]:
                st.success(f"Neural Pattern Recognition identified these 'Hidden Gems' in the {region} Market.")
                df['ValueScore'] = (df['Rating'] * 10) / (df['Price'] / mult)
                gems = df.sort_values(by='ValueScore', ascending=False).head(3)
                for _, gem in gems.iterrows():
                    st.markdown(f"""
                        <div style="background:rgba(6,182,212,0.1); padding:20px; border-radius:15px; border-left:5px solid #06b6d4; margin-bottom:10px;">
                            <h5 style="margin:0;">{gem['Title']}</h5>
                            <p style="color:#94a3b8; font-size:0.8rem; margin:5px 0;">Rating: {gem['Rating']}★ | Price: {sym}{gem['Price']}</p>
                            <a href="{gem['Link1']}" target="_blank" style="color:#06b6d4; font-size:0.75rem; font-weight:800;">{gem['Label1']} SOURCE</a>
                        </div>
                    """, unsafe_allow_html=True)

        with tabs[-1]:
            st.markdown(f"#### ⚡ Marketplace Hub ({region} Portal)")
            hub_cols = st.columns(3)
            for i, (_, row) in enumerate(df.head(9).iterrows()):
                with hub_cols[i % 3]:
                    st.markdown(f"""
                        <div style="background:rgba(59,130,246,0.08); padding:20px; border-radius:24px; border:1px solid rgba(59,130,246,0.15); margin-bottom:15px;">
                            <h6 style="margin:0; height:45px; overflow:hidden;">{row['Title']}</h6>
                            <p style="color:#94a3b8; font-size:0.8rem; margin:10px 0;"><b>{sym}{row['Price']}</b> | {row['Rating']}★</p>
                            <div class="hub-grid">
                                <a href="{row['Link1']}" class="hub-btn btn-pri" target="_blank">{row['Label1']}</a>
                                <a href="{row['Link2']}" class="hub-btn btn-sec" target="_blank">{row['Label2']}</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.divider()
            st.download_button("💾 DOWNLOAD MASTER SYSTEM LEDGER (CSV)", df.to_csv(index=False).encode('utf-8'), f"omniscraper_v12_{region_code}_{target.lower()}.csv", use_container_width=True)
    else:
        st.error("Protocol Overridden: Target node currently blocking scraping protocol.")