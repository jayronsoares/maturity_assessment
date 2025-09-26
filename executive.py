import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Engineering ROI Calculator",
    page_icon="📈",
    layout="wide"
)

# Clean styling
st.markdown("""
<style>
    .big-metric {
        font-size: 3rem;
        font-weight: bold;
        color: #2d5016;
        text-align: center;
    }
    .metric-label {
        font-size: 1.1rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 1rem;
    }
    .highlight-box {
        background: #f0fff4;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #38a169;
        margin: 1rem 0;
    }
    .cost-box {
        background: #fff5f5;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #e53e3e;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Data-Driven Business Health Check")
    st.markdown("**Discover what your current data situation is really costing you**")
    st.markdown("Answer 8 simple questions to see how much revenue you're leaving on the table")
    st.markdown("---")
    
    # Diagnostic-focused form
    with st.form("business_diagnostic"):
        st.subheader("How Data-Driven Is Your Business Really?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer relationship questions
            st.markdown("**Customer Relationships & Sales**")
            
            customer_insight = st.selectbox(
                "Can you predict which customers will churn next month?",
                ["No - we find out when they cancel", 
                 "Sometimes - we guess based on complaints",
                 "Usually - we track some warning signs", 
                 "Yes - we have predictive models"])
            
            cross_sell = st.selectbox(
                "Do you know which products to recommend to each customer?",
                ["No - we use generic recommendations", 
                 "Sometimes - based on purchase history",
                 "Usually - we analyze customer segments", 
                 "Yes - personalized recommendations for each customer"])
            
            pricing_decisions = st.selectbox(
                "How do you set your prices?",
                ["Fixed pricing or gut feeling", 
                 "Check competitors occasionally",
                 "Regular market analysis", 
                 "Dynamic pricing based on real-time data"])
            
            decision_speed = st.selectbox(
                "When opportunities arise, how fast can you analyze and act?",
                ["Days or weeks - need to gather data first", 
                 "Same day if we're lucky",
                 "Within hours with some preparation", 
                 "Immediately - real-time dashboards ready"])
        
        with col2:
            # Operational efficiency questions
            st.markdown("**Operational Efficiency**")
            
            team_time = st.selectbox(
                "How much time do your people spend finding/cleaning data vs using it?",
                ["80% finding data, 20% analyzing", 
                 "60% finding data, 40% analyzing",
                 "40% finding data, 60% analyzing", 
                 "20% finding data, 80% analyzing"])
            
            data_trust = st.selectbox(
                "Do different departments get different numbers for the same metrics?",
                ["Always - creates confusion and arguments", 
                 "Often - we spend time reconciling differences",
                 "Sometimes - mostly consistent", 
                 "Never - single source of truth"])
            
            missed_opportunities = st.selectbox(
                "How often do you miss business opportunities due to slow insights?",
                ["Weekly - competitors beat us regularly", 
                 "Monthly - we're always catching up",
                 "Quarterly - occasional misses", 
                 "Rarely - we're usually first to market"])
            
            revenue_size = st.selectbox(
                "What's your annual revenue range?",
                ["$5-25M", "$25-100M", "$100-500M", "$500M+"])
        
        diagnose = st.form_submit_button("Diagnose My Data Problems", use_container_width=True)
        
        if diagnose:
            # Calculate the "pain score" and missed opportunities
            pain_score = calculate_pain_score(customer_insight, cross_sell, pricing_decisions, 
                                            decision_speed, team_time, data_trust, missed_opportunities)
            
            revenue_base = get_revenue_base(revenue_size)
            opportunity_cost = calculate_opportunity_cost(pain_score, revenue_base)
            
            display_diagnostic_results(pain_score, opportunity_cost, revenue_base, 
                                     customer_insight, cross_sell, team_time, data_trust)

def calculate_pain_score(customer_insight, cross_sell, pricing_decisions, decision_speed, 
                        team_time, data_trust, missed_opportunities):
    # Convert answers to pain points (higher = more pain)
    scores = []
    
    # Each answer gets scored 0-3 (3 = highest pain)
    answer_maps = {
        customer_insight: {"Yes - we have predictive models": 0, "Usually - we track some warning signs": 1, 
                          "Sometimes - we guess based on complaints": 2, "No - we find out when they cancel": 3},
        cross_sell: {"Yes - personalized recommendations for each customer": 0, "Usually - we analyze customer segments": 1,
                    "Sometimes - based on purchase history": 2, "No - we use generic recommendations": 3},
        pricing_decisions: {"Dynamic pricing based on real-time data": 0, "Regular market analysis": 1,
                           "Check competitors occasionally": 2, "Fixed pricing or gut feeling": 3},
        decision_speed: {"Immediately - real-time dashboards ready": 0, "Within hours with some preparation": 1,
                        "Same day if we're lucky": 2, "Days or weeks - need to gather data first": 3},
        team_time: {"20% finding data, 80% analyzing": 0, "40% finding data, 60% analyzing": 1,
                   "60% finding data, 40% analyzing": 2, "80% finding data, 20% analyzing": 3},
        data_trust: {"Never - single source of truth": 0, "Sometimes - mostly consistent": 1,
                    "Often - we spend time reconciling differences": 2, "Always - creates confusion and arguments": 3},
        missed_opportunities: {"Rarely - we're usually first to market": 0, "Quarterly - occasional misses": 1,
                              "Monthly - we're always catching up": 2, "Weekly - competitors beat us regularly": 3}
    }
    
    for answer, score_map in answer_maps.items():
        scores.append(score_map[answer])
    
    return sum(scores) / len(scores)  # Average pain score 0-3

def calculate_opportunity_cost(pain_score, revenue_base):
    # Higher pain = higher opportunity cost
    base_cost_percentage = 0.02 + (pain_score * 0.08)  # 2% to 26% of revenue at risk
    return revenue_base * base_cost_percentage

def display_diagnostic_results(pain_score, opportunity_cost, revenue_base, 
                             customer_insight, cross_sell, team_time, data_trust):
    st.markdown("---")
    
    # Dramatic revelation of the problem
    if pain_score >= 2.5:
        st.error("🚨 CRITICAL: Your data situation is costing you serious money")
        diagnosis = "Data Crisis"
        color = "#e53e3e"
    elif pain_score >= 1.5:
        st.warning("⚠️ WARNING: Significant revenue leakage from data gaps")
        diagnosis = "Data Problems"
        color = "#d69e2e"
    elif pain_score >= 0.5:
        st.info("ℹ️ OPPORTUNITY: Good foundation, but leaving money on the table")
        diagnosis = "Data Opportunities"
        color = "#3182ce"
    else:
        st.success("✅ STRONG: You're ahead of most companies in data maturity")
        diagnosis = "Data Leaders"
        color = "#38a169"
    
    # Show the financial impact
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="big-metric" style="color: {color};">${opportunity_cost:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Annual Revenue at Risk</div>', unsafe_allow_html=True)
    
    with col2:
        monthly_cost = opportunity_cost / 12
        st.markdown(f'<div class="big-metric" style="color: {color};">${monthly_cost:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Monthly Cost of Status Quo</div>', unsafe_allow_html=True)
    
    with col3:
        daily_cost = opportunity_cost / 365
        st.markdown(f'<div class="big-metric" style="color: {color};">${daily_cost:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Daily Revenue Loss</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Specific problem callouts
    st.subheader("Here's What's Costing You Money Right Now:")
    
    problems = []
    
    if customer_insight in ["No - we find out when they cancel", "Sometimes - we guess based on complaints"]:
        problems.append("💸 **Customer Churn Blindness**: You're losing customers without knowing why or when")
    
    if cross_sell in ["No - we use generic recommendations", "Sometimes - based on purchase history"]:
        problems.append("💸 **Missed Sales Opportunities**: Each customer interaction could generate more revenue")
    
    if team_time in ["80% finding data, 20% analyzing", "60% finding data, 40% analyzing"]:
        problems.append("💸 **Team Inefficiency**: Your expensive talent is doing manual work instead of strategic analysis")
    
    if data_trust in ["Always - creates confusion and arguments", "Often - we spend time reconciling differences"]:
        problems.append("💸 **Decision Paralysis**: Inconsistent data slows decisions and creates internal conflict")
    
    for problem in problems[:3]:  # Show top 3 problems
        st.markdown(problem)
    
    if not problems:
        st.success("🎉 **You're doing well!** Your data operations are ahead of most companies.")
    
    # The solution preview
    st.markdown("---")
    st.subheader("What Changes When You Fix This:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="highlight-box">
            <h4 style="color: #22543d; margin-top: 0;">Customer & Revenue Impact</h4>
            <ul>
                <li><strong>Predict and prevent churn</strong> before customers leave</li>
                <li><strong>Personalized recommendations</strong> increase sales per customer</li>
                <li><strong>Dynamic pricing</strong> optimizes revenue in real-time</li>
                <li><strong>Faster market response</strong> beats competitors to opportunities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            <h4 style="color: #22543d; margin-top: 0;">Operational Impact</h4>
            <ul>
                <li><strong>Teams focus on strategy</strong>, not data hunting</li>
                <li><strong>Single source of truth</strong> eliminates confusion</li>
                <li><strong>Real-time dashboards</strong> enable instant decisions</li>
                <li><strong>Automated insights</strong> surface opportunities daily</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ROI calculation
    investment = revenue_base * 0.003
    roi = ((opportunity_cost - investment) / investment) * 100
    
    st.markdown(f"""
    <div class="highlight-box">
        <h3 style="color: #22543d; margin-top: 0;">The Bottom Line</h3>
        <p><strong>Investment needed:</strong> ${investment:,.0f} (0.3% of revenue)</p>
        <p><strong>Annual benefit:</strong> ${opportunity_cost:,.0f}</p>
        <p><strong>ROI:</strong> {roi:.0f}% in first year</p>
        <p><strong>Payback:</strong> {(investment / (opportunity_cost / 12)):.1f} months</p>
    </div>
    """, unsafe_allow_html=True)

def get_revenue_base(annual_revenue):
    revenue_map = {
        "$5-25M": 15_000_000,
        "$25-100M": 62_500_000, 
        "$100-500M": 300_000_000,
        "$500M+": 750_000_000
    }
    return revenue_map[annual_revenue]

def calculate_opportunity(revenue_base, revenue_missed, churn_preventable, pricing_opportunity, team_time):
    # Revenue recovery
    missed_map = {"Under $50K": 300_000, "$50-200K": 1_200_000, "$200-500K": 3_000_000, "$500K+": 6_000_000}
    revenue_recovery = missed_map[revenue_missed]
    
    # Churn prevention 
    churn_map = {"Under 10%": 0.05, "10-25%": 0.175, "25-50%": 0.375, "50%+": 0.6}
    churn_value = revenue_base * 0.15 * churn_map[churn_preventable]  # 15% typical churn, % preventable
    
    # Pricing optimization
    pricing_map = {"Under 5%": 0.025, "5-15%": 0.1, "15-25%": 0.2, "25%+": 0.3}
    pricing_value = revenue_base * pricing_map[pricing_opportunity]
    
    # Productivity gains
    time_map = {"20% gathering, 80% analyzing": 50_000, "40% gathering, 60% analyzing": 200_000,
               "60% gathering, 40% analyzing": 500_000, "80% gathering, 20% analyzing": 1_000_000}
    productivity_value = time_map[team_time]
    
    return revenue_recovery + churn_value + pricing_value + productivity_value

def calculate_current_cost(revenue_base, decision_speed, data_confidence):
    # Cost of slow decisions
    speed_map = {"Within hours": 0, "Same day": 0.002, "2-3 days": 0.005, "1+ weeks": 0.01}
    speed_cost = revenue_base * speed_map[decision_speed]
    
    # Cost of low confidence decisions
    confidence_map = {"Very confident - data-driven": 0, "Confident - good data": 0.003,
                     "Moderate - some data gaps": 0.008, "Low - mostly gut feel": 0.015}
    confidence_cost = revenue_base * confidence_map[data_confidence]
    
    return speed_cost + confidence_cost

def display_results(opportunity, current_cost, investment, revenue_base):
    st.markdown("---")
    st.header("Your Data Engineering ROI")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="big-metric">${opportunity:,.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Annual Revenue Opportunity</div>', unsafe_allow_html=True)
    
    with col2:
        roi = ((opportunity - investment) / investment) * 100
        st.markdown(f'<div class="big-metric">{roi:.0f}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">First Year ROI</div>', unsafe_allow_html=True)
    
    with col3:
        payback = investment / (opportunity / 12)
        st.markdown(f'<div class="big-metric">{payback:.1f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Payback (Months)</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Opportunity breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="highlight-box">
            <h3 style="color: #22543d; margin-top: 0;">What You Gain</h3>
            <p><strong>Annual Revenue Opportunity: ${opportunity:,.0f}</strong></p>
            <ul>
                <li>Faster, more confident decisions</li>
                <li>Prevent customer churn with predictive insights</li>
                <li>Optimize pricing based on data</li>
                <li>Teams focus on analysis, not data gathering</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="cost-box">
            <h3 style="color: #742a2a; margin-top: 0;">What You're Losing Now</h3>
            <p><strong>Annual Cost of Status Quo: ${current_cost:,.0f}</strong></p>
            <ul>
                <li>Slow decisions miss market opportunities</li>
                <li>Poor data leads to wrong choices</li>
                <li>Teams waste time on manual tasks</li>
                <li>Competitors move faster with better data</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Investment summary
    st.subheader("Investment Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Initial Investment", f"${investment:,.0f}")
    with col2:
        st.metric("Annual Support", f"${investment * 0.25:,.0f}")
    with col3:
        st.metric("3-Year Net Benefit", f"${(opportunity * 3 - investment * 1.5):,.0f}")
    
    # Simple projection chart
    create_roi_chart(opportunity, investment)
    
    # Call to action
    st.markdown("---")
    st.subheader("Next Steps")
    
    st.markdown("""
    <div class="highlight-box">
        <h4 style="color: #22543d; margin-top: 0;">Ready to unlock this ROI?</h4>
        <p><strong>Typical Implementation:</strong></p>
        <ol>
            <li><strong>Week 1-2:</strong> Data assessment and quick wins identification</li>
            <li><strong>Month 1-3:</strong> Core data infrastructure and key dashboards</li>
            <li><strong>Month 4-6:</strong> Advanced analytics and predictive capabilities</li>
        </ol>
        <p><strong>Start seeing results in 30 days with our proven methodology.</strong></p>
    </div>
    """, unsafe_allow_html=True)

def create_roi_chart(opportunity, investment):
    years = ['Year 1', 'Year 2', 'Year 3']
    benefits = [opportunity, opportunity * 1.1, opportunity * 1.2]
    costs = [investment, investment * 0.25, investment * 0.25]
    net = [b - c for b, c in zip(benefits, costs)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=years,
        y=benefits,
        name='Annual Benefits',
        marker_color='#38a169'
    ))
    
    fig.add_trace(go.Bar(
        x=years,
        y=costs,
        name='Annual Investment',
        marker_color='#e53e3e'
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=net,
        mode='lines+markers',
        name='Net Benefit',
        line=dict(color='#3182ce', width=3),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title='3-Year ROI Projection',
        xaxis_title='Year',
        yaxis_title='Value ($)',
        height=400,
        plot_bgcolor='white',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()