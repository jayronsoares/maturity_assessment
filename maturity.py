import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Data Engineering ROI Assessment",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean professional styling
st.markdown("""
<style>
    .stMetric > label {
        font-size: 0.9rem;
        color: #4a5568;
        font-weight: 500;
    }
    .stMetric > div > div {
        font-size: 1.8rem;
        color: #2d3748;
        font-weight: 700;
    }
    .main > div {
        padding-top: 2rem;
    }
    h1 {
        color: #2d3748;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .stSelectbox > label {
        font-weight: 500;
        color: #4a5568;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Data Engineering ROI Assessment")
    st.markdown("**Quantify the business impact of data engineering investments**")
    st.markdown("---")
    
    # Initialize session state
    if 'roi_assessment_completed' not in st.session_state:
        st.session_state.roi_assessment_completed = False
    if 'business_inputs' not in st.session_state:
        st.session_state.business_inputs = {}
    
    # Clean sidebar navigation
    with st.sidebar:
        st.header("Assessment Navigation")
        page = st.selectbox("Select Section:", 
                          ["Business Assessment", "ROI Analysis", "Executive Summary", "Implementation Guide"])
        
        if st.session_state.roi_assessment_completed:
            st.success("Assessment Completed")
            if st.button("Reset Assessment"):
                st.session_state.roi_assessment_completed = False
                st.session_state.business_inputs = {}
                st.rerun()
    
    # Route to pages
    if page == "Business Assessment":
        business_assessment_page()
    elif page == "ROI Analysis":
        roi_analysis_page()
    elif page == "Executive Summary":
        executive_summary_page()
    else:
        implementation_guide_page()

def business_assessment_page():
    st.header("Business Data-Driven Opportunities Assessment")
    st.write("Identify how better data capabilities can improve your decision-making, sales performance, and revenue growth")
    
    with st.form("business_assessment_form"):
        # Company Profile Section
        st.subheader("Company Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            annual_revenue = st.number_input("Annual Revenue ($M)", min_value=1, max_value=50000, value=50)
            employees = st.number_input("Number of Employees", min_value=10, max_value=100000, value=250)
            data_users = st.number_input("Decision Makers & Analysts", min_value=5, max_value=5000, value=50)
        
        with col2:
            industry = st.selectbox("Industry Sector", 
                                  ["E-commerce/Retail", "B2B Software/SaaS", "Manufacturing", 
                                   "Financial Services", "Healthcare", "Media/Marketing", "Other"])
            avg_customer_value = st.number_input("Average Customer Lifetime Value ($)", 
                                                min_value=100, max_value=1000000, value=25000)
            churn_rate = st.slider("Annual Customer Churn Rate (%)", min_value=0, max_value=50, value=15)
        
        # Decision-Making & Data Gaps
        st.subheader("Current Decision-Making Challenges")
        col1, col2 = st.columns(2)
        
        with col1:
            decision_delay = st.selectbox("How long to get data for critical business decisions?",
                                        ["Real-time (minutes)", "Same day", "2-3 days", "1 week", "2+ weeks"])
            missed_opportunities = st.number_input("Monthly revenue lost due to slow insights ($K)", 
                                                 min_value=0, max_value=10000, value=200)
            data_quality_issues = st.selectbox("How often do data quality issues impact decisions?",
                                             ["Daily", "Weekly", "Monthly", "Rarely"])
        
        with col2:
            decision_confidence = st.selectbox("Confidence level in business decisions due to data availability",
                                             ["Very low - guessing often", "Low - limited data", 
                                              "Medium - some good data", "High - comprehensive data"])
            bad_decisions = st.number_input("Monthly cost of poor decisions due to data gaps ($K)", 
                                          min_value=0, max_value=5000, value=150)
            competitive_insights = st.selectbox("Ability to respond to market/competitor changes",
                                              ["Very slow - weeks/months", "Slow - days", 
                                               "Moderate - same day", "Fast - real-time"])
        
        # Revenue & Sales Opportunities
        st.subheader("Revenue Growth Opportunities")
        col1, col2 = st.columns(2)
        
        with col1:
            customer_insights = st.selectbox("Current ability to predict customer behavior",
                                           ["No predictive capability", "Basic reporting only", 
                                            "Some analytics", "Advanced predictive models"])
            cross_sell_potential = st.slider("Potential increase in sales with better customer insights (%)", 
                                            min_value=0, max_value=100, value=25)
            churn_prevention = st.slider("Preventable churn with predictive analytics (%)", 
                                       min_value=0, max_value=80, value=30)
        
        with col2:
            pricing_strategy = st.selectbox("Current pricing strategy approach",
                                          ["Fixed pricing", "Manual adjustments", 
                                           "Basic analytics", "Dynamic data-driven pricing"])
            pricing_optimization = st.slider("Revenue increase potential from data-driven pricing (%)", 
                                            min_value=0, max_value=50, value=15)
            market_response = st.slider("Faster market response advantage (weeks)", 
                                      min_value=0, max_value=26, value=8)
        
        # Operational Efficiency Through Data
        st.subheader("Operational Efficiency Gaps")
        col1, col2 = st.columns(2)
        
        with col1:
            manual_reporting = st.slider("% of time spent on manual reporting vs strategic analysis", 
                                       min_value=20, max_value=90, value=70)
            process_optimization = st.selectbox("Current approach to operational optimization",
                                              ["Manual/intuition-based", "Occasional analysis", 
                                               "Regular monitoring", "Real-time optimization"])
            cost_reduction_potential = st.slider("Operational cost reduction through data insights (%)", 
                                                min_value=0, max_value=50, value=20)
        
        with col2:
            inventory_forecasting = st.selectbox("Inventory/resource planning accuracy",
                                                ["Poor - frequent stockouts/overstock", "Fair - some issues", 
                                                 "Good - well managed", "Excellent - optimized"])
            employee_productivity = st.slider("Productivity increase with better data access (%)", 
                                             min_value=0, max_value=100, value=35)
            new_revenue_streams = st.number_input("Potential new revenue from data insights ($K monthly)", 
                                                min_value=0, max_value=2000, value=100)
        
        # Implementation Context
        st.subheader("Implementation Context")
        col1, col2 = st.columns(2)
        
        with col1:
            data_culture = st.selectbox("Current data-driven culture",
                                      ["Decisions based on gut feeling", "Some data used occasionally", 
                                       "Data informs most decisions", "Fully data-driven organization"])
            change_readiness = st.selectbox("Organization's readiness for data-driven transformation",
                                          ["High resistance to change", "Some resistance", 
                                           "Generally open to change", "Eager for innovation"])
        
        with col2:
            executive_support = st.selectbox("Leadership commitment to becoming data-driven",
                                           ["Minimal interest", "Some interest", "Moderate support", 
                                            "Strong champion", "Top strategic priority"])
            competitive_position = st.selectbox("Competitive position in data usage",
                                              ["Far behind industry", "Slightly behind", "Average", 
                                               "Slightly ahead", "Industry leader"])
        
        # Technical Context (simplified)
        st.subheader("Current Data Capabilities")
        col1, col2 = st.columns(2)
        
        with col1:
            data_accessibility = st.selectbox("How easily can teams access needed data?",
                                            ["Very difficult - requires IT help", "Difficult - complex process", 
                                             "Moderate - some self-service", "Easy - self-service available"])
            data_integration = st.selectbox("Data integration across business functions",
                                          ["Siloed systems", "Some integration", 
                                           "Well integrated", "Fully unified data"])
        
        with col2:
            analytics_maturity = st.selectbox("Current analytics capabilities",
                                            ["Basic reporting only", "Standard dashboards", 
                                             "Advanced analytics", "AI/ML capabilities"])
            system_reliability = st.selectbox("Data system reliability for business decisions",
                                            ["Unreliable - frequent issues", "Sometimes unreliable", 
                                             "Generally reliable", "Highly reliable"])
        
        # Submit button
        submit_button = st.form_submit_button("Calculate Business Impact", use_container_width=True)
        
        if submit_button:
            inputs = {
                'annual_revenue': annual_revenue, 'employees': employees, 'data_users': data_users,
                'industry': industry, 'avg_customer_value': avg_customer_value, 'churn_rate': churn_rate,
                'decision_delay': decision_delay, 'missed_opportunities': missed_opportunities,
                'data_quality_issues': data_quality_issues, 'decision_confidence': decision_confidence,
                'bad_decisions': bad_decisions, 'competitive_insights': competitive_insights,
                'customer_insights': customer_insights, 'cross_sell_potential': cross_sell_potential,
                'churn_prevention': churn_prevention, 'pricing_strategy': pricing_strategy,
                'pricing_optimization': pricing_optimization, 'market_response': market_response,
                'manual_reporting': manual_reporting, 'process_optimization': process_optimization,
                'cost_reduction_potential': cost_reduction_potential, 'inventory_forecasting': inventory_forecasting,
                'employee_productivity': employee_productivity, 'new_revenue_streams': new_revenue_streams,
                'data_culture': data_culture, 'change_readiness': change_readiness,
                'executive_support': executive_support, 'competitive_position': competitive_position,
                'data_accessibility': data_accessibility, 'data_integration': data_integration,
                'analytics_maturity': analytics_maturity, 'system_reliability': system_reliability
            }
            
            st.session_state.business_inputs = inputs
            st.session_state.roi_assessment_completed = True
            st.success("Assessment completed! Navigate to ROI Analysis to see how data engineering can drive your business results.")

def roi_analysis_page():
    if not st.session_state.roi_assessment_completed:
        st.warning("Please complete the Business Assessment first.")
        return
    
    inputs = st.session_state.business_inputs
    roi_data = calculate_roi_metrics(inputs)
    
    st.header("Revenue Impact Analysis")
    
    # Key Metrics Dashboard using native Streamlit
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Annual Revenue Opportunity", f"${roi_data['annual_opportunity']:,.0f}")
    with col2:
        st.metric("Current State Annual Cost", f"${roi_data['current_cost']:,.0f}")
    with col3:
        st.metric("3-Year ROI Potential", f"{roi_data['roi_percentage']:.0f}%")
    with col4:
        st.metric("Payback Period", f"{roi_data['payback_months']:.1f} months")
    
    st.markdown("---")
    
    # Revenue Opportunity Breakdown
    st.subheader("Revenue Opportunity Breakdown")
    create_revenue_breakdown_chart(roi_data)
    
    # 5-Year Financial Projection
    st.subheader("5-Year Financial Projection")
    create_financial_projection(roi_data)
    
    # Current vs Future State Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current State Annual Costs")
        st.write(f"**Lost revenue from delays:** ${roi_data['delay_cost']:,.0f}")
        st.write(f"**Poor decision costs:** ${roi_data['decision_cost']:,.0f}")
        st.write(f"**Customer churn:** ${roi_data['churn_cost']:,.0f}")
        st.write(f"**Inefficient operations:** ${roi_data['efficiency_cost']:,.0f}")
        st.write(f"**Total Annual Cost:** ${roi_data['current_cost']:,.0f}")
    
    with col2:
        st.subheader("Future State Revenue Gains")
        st.write(f"**Increased cross-sell/upsell:** ${roi_data['cross_sell_gain']:,.0f}")
        st.write(f"**Reduced churn:** ${roi_data['churn_prevention_value']:,.0f}")
        st.write(f"**Pricing optimization:** ${roi_data['pricing_gain']:,.0f}")
        st.write(f"**New revenue streams:** ${roi_data['new_revenue']:,.0f}")
        st.write(f"**Total Annual Opportunity:** ${roi_data['annual_opportunity']:,.0f}")
    
    st.markdown("---")
    
    # Investment Requirements
    st.subheader("Estimated Investment Requirements")
    investment_data = calculate_investment_requirements(inputs)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Data Migration & Setup", f"${investment_data['migration']:,.0f}")
    with col2:
        st.metric("Implementation & Integration", f"${investment_data['implementation']:,.0f}")
    with col3:
        st.metric("Annual Support & Maintenance", f"${investment_data['annual_support']:,.0f}")

def executive_summary_page():
    if not st.session_state.roi_assessment_completed:
        st.warning("Please complete the Business Assessment first.")
        return
    
    inputs = st.session_state.business_inputs
    roi_data = calculate_roi_metrics(inputs)
    
    st.header("Executive Summary")
    st.subheader("Business Case: Data Engineering Investment")
    
    # Financial Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current State Annual Cost")
        st.metric("Total Annual Cost", f"${roi_data['current_cost']:,.0f}")
        st.write(f"- Revenue delays: ${roi_data['delay_cost']:,.0f}")
        st.write(f"- Poor decisions: ${roi_data['decision_cost']:,.0f}")
        st.write(f"- Customer churn: ${roi_data['churn_cost']:,.0f}")
        st.write(f"- Inefficiencies: ${roi_data['efficiency_cost']:,.0f}")
    
    with col2:
        st.subheader("Annual Revenue Opportunity")
        st.metric("Total Opportunity", f"${roi_data['annual_opportunity']:,.0f}")
        st.write(f"- Cross-sell increase: ${roi_data['cross_sell_gain']:,.0f}")
        st.write(f"- Churn prevention: ${roi_data['churn_prevention_value']:,.0f}")
        st.write(f"- Pricing optimization: ${roi_data['pricing_gain']:,.0f}")
        st.write(f"- New revenue streams: ${roi_data['new_revenue']:,.0f}")
    
    st.markdown("---")
    
    # Key Financial Metrics
    st.subheader("Key Financial Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("3-Year ROI", f"{roi_data['roi_percentage']:.0f}%")
    with col2:
        st.metric("Payback Period", f"{roi_data['payback_months']:.1f} months")
    with col3:
        st.metric("Net Annual Benefit", f"${(roi_data['annual_opportunity'] - roi_data['current_cost']):,.0f}")
    
    st.markdown("---")
    
    # Strategic Benefits
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Competitive Advantages")
        st.write(f"- {inputs['market_response']} weeks faster time-to-market")
        st.write(f"- {inputs['employee_productivity']}% productivity increase")
        st.write(f"- {inputs['churn_prevention']}% churn reduction capability")
    
    with col2:
        st.subheader("Risk Mitigations")
        st.write("- Regulatory compliance automation")
        st.write("- Reduced business continuity risk")
        st.write("- Future-proofed scalable architecture")
    
    st.markdown("---")
    
    # Next Steps
    st.subheader("Recommended Next Steps")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Immediate Actions (30 days):**")
        st.write("1. Detailed technical assessment")
        st.write("2. Stakeholder alignment workshop")
        st.write("3. Pilot project identification")
        st.write("4. Vendor evaluation process")
    
    with col2:
        st.write("**Implementation Timeline (6-12 months):**")
        st.write("1. Phase 1: Quick wins & data quality")
        st.write("2. Phase 2: Core infrastructure migration")
        st.write("3. Phase 3: Advanced analytics capabilities")
        st.write("4. Phase 4: Optimization & scaling")

def implementation_guide_page():
    st.header("Data Engineering Implementation Guide")
    
    if not st.session_state.roi_assessment_completed:
        st.info("Complete the Business Assessment first to see customized recommendations.")
        st.markdown("---")
    
    # Professional Services Approach
    st.subheader("Professional Services Approach")
    
    # Phase 1
    with st.expander("Phase 1: Foundation & Quick Wins (Weeks 1-8)"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Key Objectives:**")
            st.write("- Data quality assessment and improvements")
            st.write("- Critical data pipeline automation")
            st.write("- Basic monitoring implementation")
            st.write("- Quick ROI demonstrations")
        
        with col2:
            st.write("**Deliverables:**")
            st.write("- Technical assessment report")
            st.write("- Data quality improvement plan")
            st.write("- Automated business reports")
            st.write("- Performance dashboards")
        
        st.write("**Investment Allocation:** 25% of total project cost")
    
    # Phase 2
    with st.expander("Phase 2: Core Infrastructure (Weeks 9-20)"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Key Objectives:**")
            st.write("- Modern data platform implementation")
            st.write("- Legacy system migration")
            st.write("- Security and compliance framework")
            st.write("- Scalable architecture deployment")
        
        with col2:
            st.write("**Deliverables:**")
            st.write("- Production data platform")
            st.write("- Migrated critical data sources")
            st.write("- Security controls")
            st.write("- Technical documentation")
        
        st.write("**Investment Allocation:** 50% of total project cost")
    
    # Phase 3
    with st.expander("Phase 3: Advanced Capabilities (Weeks 21-32)"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Key Objectives:**")
            st.write("- Real-time processing implementation")
            st.write("- Advanced analytics enablement")
            st.write("- Self-service capabilities")
            st.write("- Performance optimization")
        
        with col2:
            st.write("**Deliverables:**")
            st.write("- Real-time data pipelines")
            st.write("- Self-service tools")
            st.write("- Predictive analytics framework")
            st.write("- Optimized performance")
        
        st.write("**Investment Allocation:** 25% of total project cost")
    
    st.markdown("---")
    
    # Risk Mitigation
    st.subheader("Risk Mitigation & Success Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Critical Success Factors")
        st.write("- Executive sponsorship for change management")
        st.write("- Cross-functional business and IT collaboration")
        st.write("- Phased delivery with incremental value")
        st.write("- Comprehensive user training programs")
        st.write("- Strong data governance framework")
    
    with col2:
        st.subheader("Risk Mitigation Strategies")
        st.write("- Start with pilot projects in low-risk areas")
        st.write("- Maintain parallel systems during transition")
        st.write("- Implement comprehensive testing protocols")
        st.write("- Establish clear rollback procedures")
        st.write("- Continuous performance monitoring")
    
    st.markdown("---")
    
    # Investment Planning
    if st.session_state.roi_assessment_completed:
        st.subheader("Investment Planning Framework")
        inputs = st.session_state.business_inputs
        roi_data = calculate_roi_metrics(inputs)
        investment_data = calculate_investment_requirements(inputs)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Phase 1: Foundation", f"${investment_data['migration']:,.0f}")
        with col2:
            st.metric("Phase 2 & 3: Implementation", f"${investment_data['implementation']:,.0f}")
        with col3:
            st.metric("Annual Benefit Target", f"${roi_data['annual_opportunity']:,.0f}")
    
    # Technology Recommendations
    st.subheader("Technology Platform Recommendations")
    
    platforms = {
        "Cloud Infrastructure": "AWS, Microsoft Azure, Google Cloud Platform",
        "Data Processing": "Apache Spark, Databricks, AWS Glue, Azure Data Factory", 
        "Data Storage": "Snowflake, Amazon Redshift, BigQuery, Azure Synapse",
        "Orchestration": "Apache Airflow, Prefect, AWS Step Functions"
    }
    
    for category, options in platforms.items():
        st.write(f"**{category}:** {options}")

# Helper functions for calculations
def calculate_roi_metrics(inputs):
    annual_revenue = inputs['annual_revenue'] * 1_000_000
    churn_rate = inputs['churn_rate'] / 100
    
    # Calculate current costs
    delay_cost = inputs['missed_opportunities'] * 12 * 1000
    decision_cost = inputs['bad_decisions'] * 12 * 1000
    churn_cost = (annual_revenue * churn_rate) * 0.7
    efficiency_cost = (annual_revenue * 0.15) * (inputs['manual_reporting'] / 100)  # Fixed: use 'manual_reporting' instead of 'data_preparation_time'
    
    current_cost = delay_cost + decision_cost + churn_cost + efficiency_cost
    
    # Calculate revenue opportunities
    cross_sell_gain = annual_revenue * (inputs['cross_sell_potential'] / 100)
    churn_prevention_value = churn_cost * (inputs['churn_prevention'] / 100)
    pricing_gain = annual_revenue * (inputs['pricing_optimization'] / 100)
    new_revenue = inputs['new_revenue_streams'] * 12 * 1000
    operational_savings = (annual_revenue * 0.2) * (inputs['cost_reduction_potential'] / 100)  # Fixed: use 'cost_reduction_potential' instead of 'operational_efficiency'
    productivity_value = (inputs['data_users'] * 100_000) * (inputs['employee_productivity'] / 100)
    
    annual_opportunity = cross_sell_gain + churn_prevention_value + pricing_gain + new_revenue + operational_savings + productivity_value
    
    # Calculate ROI
    initial_investment = annual_revenue * 0.002
    annual_support = initial_investment * 0.3
    three_year_benefit = annual_opportunity * 3 * 1.05
    three_year_investment = initial_investment + (annual_support * 2)
    roi_percentage = ((three_year_benefit - three_year_investment) / three_year_investment) * 100
    payback_months = (initial_investment / (annual_opportunity / 12))
    
    return {
        'annual_opportunity': annual_opportunity, 'current_cost': current_cost,
        'roi_percentage': roi_percentage, 'payback_months': payback_months,
        'delay_cost': delay_cost, 'decision_cost': decision_cost,
        'churn_cost': churn_cost, 'efficiency_cost': efficiency_cost,
        'cross_sell_gain': cross_sell_gain, 'churn_prevention_value': churn_prevention_value,
        'pricing_gain': pricing_gain, 'new_revenue': new_revenue,
        'operational_savings': operational_savings, 'productivity_value': productivity_value,
        'initial_investment': initial_investment, 'annual_support': annual_support
    }

def calculate_investment_requirements(inputs):
    annual_revenue = inputs['annual_revenue'] * 1_000_000
    migration_cost = annual_revenue * 0.001
    implementation_cost = annual_revenue * 0.0015
    annual_support = (migration_cost + implementation_cost) * 0.25
    
    return {
        'migration': migration_cost,
        'implementation': implementation_cost,
        'annual_support': annual_support
    }

def create_revenue_breakdown_chart(roi_data):
    categories = ['Cross-sell/Upsell', 'Churn Prevention', 'Pricing Optimization', 
                 'New Revenue Streams', 'Operational Savings', 'Productivity Gains']
    
    values = [roi_data['cross_sell_gain'], roi_data['churn_prevention_value'], 
             roi_data['pricing_gain'], roi_data['new_revenue'],
             roi_data['operational_savings'], roi_data['productivity_value']]
    
    colors = ['#38a169', '#4299e1', '#d69e2e', '#805ad5', '#ed8936', '#38b2ac']
    
    fig = go.Figure(data=[go.Bar(x=categories, y=values, marker_color=colors,
                                text=[f'${v:,.0f}' for v in values], textposition='auto')])
    
    fig.update_layout(title="Annual Revenue Opportunity by Category",
                     xaxis_title="Revenue Category", yaxis_title="Annual Value ($)",
                     height=500, showlegend=False, plot_bgcolor='white')
    
    st.plotly_chart(fig, use_container_width=True)

def create_financial_projection(roi_data):
    years = list(range(1, 6))
    annual_benefit = roi_data['annual_opportunity']
    initial_investment = roi_data['initial_investment']
    annual_support = roi_data['annual_support']
    
    cumulative_benefits = [sum([annual_benefit * (1.05 ** (i - 1)) for i in range(1, year + 1)]) for year in years]
    cumulative_investment = [initial_investment + (annual_support * (year - 1)) if year > 1 else initial_investment for year in years]
    net_benefit = [cb - ci for cb, ci in zip(cumulative_benefits, cumulative_investment)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=cumulative_benefits, mode='lines+markers',
                            name='Cumulative Benefits', line=dict(color='#38a169', width=3)))
    fig.add_trace(go.Scatter(x=years, y=cumulative_investment, mode='lines+markers',
                            name='Cumulative Investment', line=dict(color='#e53e3e', width=3)))
    fig.add_trace(go.Scatter(x=years, y=net_benefit, mode='lines+markers',
                            name='Net Benefit', line=dict(color='#d69e2e', width=3)))
    
    fig.update_layout(title="5-Year Financial Projection", xaxis_title="Year", yaxis_title="Value ($)",
                     height=500, hovermode='x unified', plot_bgcolor='white')
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()