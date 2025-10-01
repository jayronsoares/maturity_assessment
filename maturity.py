import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Business Data Health Diagnostic - DataDoctor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    .stRadio > label {
        font-weight: 600;
        font-size: 1.1rem;
        color: #1f2937;
    }
    .stTextInput > label {
        font-weight: 600;
        color: #1f2937;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .reportview-container {
        background: #f8fafc;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_report' not in st.session_state:
    st.session_state.show_report = False

# Questions data structure
questions = [
    {
        'id': 'reporting_time',
        'category': 'time',
        'question': 'How long does it take your team to produce key business reports?',
        'subtitle': 'Weekly sales, month-end close, performance dashboards - from request to delivery',
        'options': [
            {'value': 'minutes', 'label': 'Minutes to 1 hour', 'risk': 'low'},
            {'value': 'hours', 'label': '2-8 hours', 'risk': 'low'},
            {'value': 'day', 'label': '1-2 days', 'risk': 'medium', 'cost': 16},
            {'value': 'days', 'label': '3-5 days', 'risk': 'high', 'cost': 40},
            {'value': 'week', 'label': 'More than a week', 'risk': 'critical', 'cost': 80}
        ],
        'follow_up': 'How many people are involved in creating these reports?',
        'follow_up_type': 'number',
        'follow_up_label': 'Number of people',
        'follow_up_help': 'Enter the number of team members'
    },
    {
        'id': 'manual_work',
        'category': 'cost',
        'question': 'How much time does your team spend on manual data work each week?',
        'subtitle': 'Copying data between systems, fixing errors, reconciling spreadsheets, manual entry',
        'options': [
            {'value': 'none', 'label': 'Almost none (< 2 hours/week)', 'risk': 'low'},
            {'value': 'some', 'label': '5-10 hours/week', 'risk': 'medium', 'hours': 7.5},
            {'value': 'significant', 'label': '15-25 hours/week', 'risk': 'high', 'hours': 20},
            {'value': 'substantial', 'label': '30-40 hours/week', 'risk': 'high', 'hours': 35},
            {'value': 'extreme', 'label': 'More than 40 hours/week', 'risk': 'critical', 'hours': 50}
        ],
        'follow_up': 'What is the average hourly cost of these team members?',
        'follow_up_type': 'number',
        'follow_up_label': 'Hourly rate (USD)',
        'follow_up_help': 'Enter dollar amount without symbols (e.g., 75)'
    },
    {
        'id': 'data_accuracy',
        'category': 'risk',
        'question': 'How often do you discover errors in reports or make decisions based on incorrect data?',
        'subtitle': 'Wrong numbers, outdated data, different reports showing different numbers',
        'options': [
            {'value': 'rarely', 'label': 'Rarely or never', 'risk': 'low'},
            {'value': 'monthly', 'label': 'A few times per month', 'risk': 'medium', 'frequency': 3},
            {'value': 'weekly', 'label': 'Weekly', 'risk': 'high', 'frequency': 4},
            {'value': 'daily', 'label': 'Multiple times per week', 'risk': 'high', 'frequency': 12},
            {'value': 'constant', 'label': 'Almost daily', 'risk': 'critical', 'frequency': 20}
        ],
        'follow_up': 'Approximately how much does a bad-data decision cost?',
        'follow_up_type': 'number',
        'follow_up_label': 'Cost per incident (USD)',
        'follow_up_help': 'Rough estimate in dollars (e.g., 1000)'
    },
    {
        'id': 'decision_speed',
        'category': 'revenue',
        'question': 'When you need to answer an urgent business question, how quickly can you get reliable data?',
        'subtitle': 'Example: "Which customers haven\'t ordered in 60 days?" or "What\'s inventory for product X?"',
        'options': [
            {'value': 'instant', 'label': 'Within minutes', 'risk': 'low'},
            {'value': 'same_day', 'label': 'Same day (few hours)', 'risk': 'low'},
            {'value': 'next_day', 'label': '1-2 days', 'risk': 'medium', 'delay': 1.5},
            {'value': 'several_days', 'label': '3-5 days', 'risk': 'high', 'delay': 4},
            {'value': 'week_plus', 'label': 'A week or more', 'risk': 'critical', 'delay': 7}
        ],
        'follow_up': 'How many time-sensitive opportunities or issues come up per month?',
        'follow_up_type': 'number',
        'follow_up_label': 'Opportunities per month',
        'follow_up_help': 'Approximate number (e.g., 10)'
    },
    {
        'id': 'data_silos',
        'category': 'cost',
        'question': 'How many different systems contain critical business data that don\'t talk to each other?',
        'subtitle': 'CRM, ERP, accounting software, Excel files, departmental databases',
        'options': [
            {'value': '1-2', 'label': '1-2 systems (well integrated)', 'risk': 'low'},
            {'value': '3-5', 'label': '3-5 systems', 'risk': 'medium', 'systems': 4},
            {'value': '6-10', 'label': '6-10 systems', 'risk': 'high', 'systems': 8},
            {'value': '11-15', 'label': '11-15 systems', 'risk': 'high', 'systems': 13},
            {'value': '15+', 'label': 'More than 15 systems', 'risk': 'critical', 'systems': 20}
        ],
        'follow_up': 'How many hours per week are spent combining data from these sources?',
        'follow_up_type': 'number',
        'follow_up_label': 'Hours per week',
        'follow_up_help': 'Estimated hours (e.g., 15)'
    },
    {
        'id': 'compliance_audit',
        'category': 'risk',
        'question': 'How confident are you in your ability to pass an audit or prove compliance?',
        'subtitle': 'Can you show where data came from, who changed it, and prove accuracy?',
        'options': [
            {'value': 'very_confident', 'label': 'Very confident - full audit trail', 'risk': 'low'},
            {'value': 'mostly_confident', 'label': 'Mostly confident', 'risk': 'low'},
            {'value': 'somewhat_confident', 'label': 'Somewhat confident', 'risk': 'medium', 'exposure': 50000},
            {'value': 'not_confident', 'label': 'Not very confident', 'risk': 'high', 'exposure': 150000},
            {'value': 'worried', 'label': 'Seriously concerned', 'risk': 'critical', 'exposure': 500000}
        ],
        'follow_up': 'Are you subject to specific compliance requirements?',
        'follow_up_type': 'text',
        'follow_up_label': 'Compliance requirements',
        'follow_up_help': 'e.g., SOX, GDPR, HIPAA, or enter "None"'
    }
]

def calculate_findings():
    findings = {
        'total_annual_cost': 0,
        'time_wasted': 0,
        'risk_exposure': 0,
        'critical_issues': [],
        'opportunities': []
    }
    
    # Reporting time calculations
    if 'reporting_time' in st.session_state.answers:
        answer = st.session_state.answers['reporting_time']
        option = next((o for o in questions[0]['options'] if o['value'] == answer['value']), None)
        if option and 'cost' in option and answer.get('follow_up'):
            people = int(float(answer['follow_up']))
            hours_per_report = option['cost']
            reports_per_year = 52
            avg_cost_per_hour = 75
            annual_cost = hours_per_report * people * reports_per_year * avg_cost_per_hour
            findings['total_annual_cost'] += annual_cost
            findings['time_wasted'] += hours_per_report * reports_per_year
            if option['risk'] in ['high', 'critical']:
                findings['critical_issues'].append({
                    'area': 'Report Generation Time',
                    'impact': f"${annual_cost:,.0f}/year in productivity costs",
                    'detail': f"{people} people spending {hours_per_report} hours per report, {reports_per_year} times/year"
                })
                findings['opportunities'].append({
                    'area': 'Automated Reporting',
                    'potential': f"Save ${int(annual_cost * 0.8):,.0f}/year by automating report generation",
                    'improvement': '80-90% time reduction'
                })
    
    # Manual work calculations
    if 'manual_work' in st.session_state.answers:
        answer = st.session_state.answers['manual_work']
        option = next((o for o in questions[1]['options'] if o['value'] == answer['value']), None)
        if option and 'hours' in option and answer.get('follow_up'):
            hourly_rate = float(answer['follow_up'])
            weekly_hours = option['hours']
            annual_cost = weekly_hours * 52 * hourly_rate
            findings['total_annual_cost'] += annual_cost
            findings['time_wasted'] += weekly_hours * 52
            if weekly_hours >= 15:
                findings['critical_issues'].append({
                    'area': 'Manual Data Processing',
                    'impact': f"${annual_cost:,.0f}/year in labor costs",
                    'detail': f"{weekly_hours} hours/week at ${hourly_rate:,.0f}/hour"
                })
                findings['opportunities'].append({
                    'area': 'Data Pipeline Automation',
                    'potential': f"Save ${int(annual_cost * 0.75):,.0f}/year through automation",
                    'improvement': '75% reduction in manual work'
                })
    
    # Data accuracy calculations
    if 'data_accuracy' in st.session_state.answers:
        answer = st.session_state.answers['data_accuracy']
        option = next((o for o in questions[2]['options'] if o['value'] == answer['value']), None)
        if option and 'frequency' in option and answer.get('follow_up'):
            cost_per_incident = float(answer['follow_up'])
            monthly_incidents = option['frequency']
            annual_cost = cost_per_incident * monthly_incidents * 12
            findings['risk_exposure'] += annual_cost
            if option['risk'] in ['high', 'critical']:
                findings['critical_issues'].append({
                    'area': 'Data Quality Issues',
                    'impact': f"${annual_cost:,.0f}/year in bad decisions and rework",
                    'detail': f"{monthly_incidents} incidents/month at ${cost_per_incident:,.0f} each"
                })
                findings['opportunities'].append({
                    'area': 'Data Quality Framework',
                    'potential': f"Prevent ${int(annual_cost * 0.7):,.0f}/year in errors",
                    'improvement': '70-90% reduction in data errors'
                })
    
    # Decision speed calculations
    if 'decision_speed' in st.session_state.answers:
        answer = st.session_state.answers['decision_speed']
        option = next((o for o in questions[3]['options'] if o['value'] == answer['value']), None)
        if option and 'delay' in option and answer.get('follow_up'):
            opportunities_per_month = int(float(answer['follow_up']))
            avg_opportunity_value = 5000
            opportunities_lost = opportunities_per_month * 0.2
            annual_cost = opportunities_lost * 12 * avg_opportunity_value
            findings['risk_exposure'] += annual_cost
            if option['risk'] in ['high', 'critical']:
                findings['critical_issues'].append({
                    'area': 'Slow Decision Making',
                    'impact': f"${annual_cost:,.0f}/year in missed opportunities",
                    'detail': f"{option['delay']}-day delays on {opportunities_per_month} monthly opportunities"
                })
                findings['opportunities'].append({
                    'area': 'Real-Time Analytics',
                    'potential': f"Capture ${int(annual_cost * 0.6):,.0f}/year in faster decisions",
                    'improvement': 'Decision time from days to minutes'
                })
    
    # Data silos calculations
    if 'data_silos' in st.session_state.answers:
        answer = st.session_state.answers['data_silos']
        option = next((o for o in questions[4]['options'] if o['value'] == answer['value']), None)
        if option and 'systems' in option and answer.get('follow_up'):
            hours_per_week = float(answer['follow_up'])
            annual_cost = hours_per_week * 52 * 75
            findings['total_annual_cost'] += annual_cost
            findings['time_wasted'] += hours_per_week * 52
            if option['systems'] >= 6:
                findings['critical_issues'].append({
                    'area': 'Data Silos & Integration',
                    'impact': f"${annual_cost:,.0f}/year in integration labor",
                    'detail': f"{option['systems']} disconnected systems, {hours_per_week} hours/week to reconcile"
                })
                findings['opportunities'].append({
                    'area': 'Unified Data Platform',
                    'potential': f"Save ${int(annual_cost * 0.7):,.0f}/year with integrated data",
                    'improvement': 'Single source of truth across all systems'
                })
    
    # Compliance audit calculations
    if 'compliance_audit' in st.session_state.answers:
        answer = st.session_state.answers['compliance_audit']
        option = next((o for o in questions[5]['options'] if o['value'] == answer['value']), None)
        if option and 'exposure' in option:
            findings['risk_exposure'] += option['exposure']
            if option['risk'] in ['high', 'critical']:
                compliance = answer.get('follow_up', 'regulatory requirements')
                findings['critical_issues'].append({
                    'area': 'Compliance & Audit Risk',
                    'impact': f"${option['exposure']:,.0f} potential exposure",
                    'detail': f"Inadequate audit trail for {compliance}"
                })
                findings['opportunities'].append({
                    'area': 'Data Governance & Compliance',
                    'potential': f"Mitigate ${option['exposure']:,.0f} in compliance risk",
                    'improvement': 'Full audit trail and regulatory compliance'
                })
    
    return findings

def show_report():
    findings = calculate_findings()
    total_impact = findings['total_annual_cost'] + findings['risk_exposure']
    
    # Container for professional layout
    st.markdown("<div style='background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
    
    st.markdown("# Business Data Health Report")
    st.caption(f"Confidential Assessment  •  {datetime.now().strftime('%B %d, %Y')}")
    st.divider()
    
    # Total Impact Section
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-left: 4px solid #dc2626; padding: 2rem; border-radius: 0.75rem; margin: 2rem 0;'>
        <h2 style='color: #991b1b; margin-bottom: 1rem; font-size: 1.5rem;'>Total Annual Impact Identified</h2>
        <div style='font-size: 3rem; font-weight: 800; color: #dc2626; margin-bottom: 1rem;'>
            ${total_impact:,.0f}
        </div>
        <p style='color: #6b7280; font-size: 0.95rem;'>Estimated annual cost and risk exposure from data challenges</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Annual Costs", f"${findings['total_annual_cost']:,.0f}")
    with col2:
        st.metric("Risk Exposure", f"${findings['risk_exposure']:,.0f}")
    with col3:
        st.metric("Hours Wasted", f"{int(findings['time_wasted']):,} hrs/year")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Critical Issues
    if findings['critical_issues']:
        st.markdown("### Critical Issues Identified")
        st.markdown("<p style='color: #6b7280; margin-bottom: 1.5rem;'>High-impact areas requiring immediate attention</p>", unsafe_allow_html=True)
        
        for issue in findings['critical_issues']:
            st.markdown(f"""
            <div style='background: #fff; border: 2px solid #fed7aa; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1rem;'>
                <h4 style='color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.1rem;'>{issue['area']}</h4>
                <p style='color: #dc2626; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 1rem;'>{issue['impact']}</p>
                <p style='color: #6b7280; margin: 0; font-size: 0.9rem;'>{issue['detail']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Opportunities
    if findings['opportunities']:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Revenue & Cost Reduction Opportunities")
        st.markdown("<p style='color: #6b7280; margin-bottom: 1.5rem;'>Potential improvements with modern data solutions</p>", unsafe_allow_html=True)
        
        for opp in findings['opportunities']:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #86efac; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1rem;'>
                <h4 style='color: #1f2937; margin: 0 0 0.5rem 0; font-size: 1.1rem;'>{opp['area']}</h4>
                <p style='color: #059669; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 1rem;'>{opp['potential']}</p>
                <p style='color: #6b7280; margin: 0; font-size: 0.9rem;'>{opp['improvement']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Bottom Line
    roi_percent = int((total_impact * 0.6) / (total_impact * 0.15) * 100) if total_impact > 0 else 0
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-left: 4px solid #3b82f6; padding: 2rem; border-radius: 0.75rem; margin: 2rem 0;'>
        <h3 style='color: #1e40af; margin-bottom: 1rem;'>Bottom Line</h3>
        <p style='color: #374151; margin-bottom: 1.5rem; line-height: 1.8; font-size: 1rem;'>
            Based on your responses, your organization is facing <strong>${total_impact:,.0f}</strong> in 
            annual costs and risk exposure due to data challenges. The good news: most of this is preventable 
            with the right data infrastructure and processes.
        </p>
        <div style='background: white; border-radius: 0.75rem; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='color: #6b7280; margin-bottom: 0.5rem; font-size: 0.9rem;'>Estimated First-Year ROI with Data Solutions</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: #3b82f6; margin-bottom: 0.5rem;'>
                {roi_percent}% ROI
            </div>
            <div style='color: #6b7280; font-size: 0.9rem;'>Typical 6-8 month payback period</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); color: white; padding: 2.5rem; border-radius: 0.75rem; margin: 2rem 0;'>
        <h2 style='color: white; margin-bottom: 1.5rem; font-size: 1.75rem;'>Ready to Transform Your Data Operations?</h2>
        <p style='opacity: 0.95; margin-bottom: 2rem; font-size: 1.05rem; line-height: 1.7;'>
            Let's discuss a strategic data solution tailored to your business. Our solutions can help you:
        </p>
        <div style='background: rgba(255,255,255,0.1); border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem;'>
            <div style='margin-bottom: 1rem; display: flex; align-items: start;'>
                <span style='font-size: 1.5rem; margin-right: 1rem;'>💰</span>
                <span>Recover <strong>${int(findings['total_annual_cost'] * 0.7):,.0f}</strong> annually in productivity costs</span>
            </div>
            <div style='margin-bottom: 1rem; display: flex; align-items: start;'>
                <span style='font-size: 1.5rem; margin-right: 1rem;'>🛡️</span>
                <span>Mitigate <strong>${findings['risk_exposure']:,.0f}</strong> in risk exposure</span>
            </div>
            <div style='display: flex; align-items: start;'>
                <span style='font-size: 1.5rem; margin-right: 1rem;'>⚡</span>
                <span>Enable data-driven decisions in <strong>minutes instead of days</strong></span>
            </div>
        </div>
        <div style='border-top: 1px solid rgba(255,255,255,0.2); padding-top: 2rem;'>
            <p style='font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem;'>Schedule a 30-Minute Strategy Call</p>
            <p style='opacity: 0.9; margin-bottom: 1.5rem;'>No obligation. We'll discuss your specific situation and potential solutions.</p>
            <div style='display: flex; flex-wrap: wrap; gap: 2rem; font-size: 1rem;'>
                <div><strong>Email:</strong> jayron.soares@gayaanalytics.com.br</div>
                <div><strong>Phone:</strong> +55(21) 98983-8805</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Start New Assessment", use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.session_state.show_report = False
            st.rerun()
    with col2:
        if st.button("Download Report (PDF)", use_container_width=True, disabled=True):
            st.info("PDF download coming soon")

def show_question():
    current_q = questions[st.session_state.current_question]
    
    # Professional container
    st.markdown("""
    <div style='background: white; padding: 2.5rem; border-radius: 1rem; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin: 2rem auto; max-width: 900px;'>
    """, unsafe_allow_html=True)
    
    # Header with progress
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Business Data Health Diagnostic")
    with col2:
        st.markdown(f"<p style='text-align: right; color: #6b7280; margin-top: 0.5rem;'>Question {st.session_state.current_question + 1} of {len(questions)}</p>", unsafe_allow_html=True)
    
    progress_percent = (st.session_state.current_question + 1) / len(questions)
    st.progress(progress_percent)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Question with icon
    category_icons = {
        'revenue': '📈',
        'cost': '💰',
        'risk': '🛡️',
        'time': '⏱️'
    }
    icon = category_icons.get(current_q['category'], '📋')
    
    st.markdown(f"## {icon} {current_q['question']}")
    st.markdown(f"<p style='color: #6b7280; font-size: 1rem; margin-bottom: 2rem;'>{current_q['subtitle']}</p>", unsafe_allow_html=True)
    
    # Get current answer
    current_answer = st.session_state.answers.get(current_q['id'], {})
    
    # Options with better styling
    selected_option = None
    for idx, opt in enumerate(current_q['options']):
        is_selected = current_answer.get('value') == opt['value']
        
        # Risk badge styling
        risk_colors = {
            'low': ('background: #d1fae5; color: #065f46;', 'Healthy'),
            'medium': ('background: #fef3c7; color: #92400e;', 'Attention'),
            'high': ('background: #fed7aa; color: #9a3412;', 'High Impact'),
            'critical': ('background: #fecaca; color: #991b1b;', 'Critical')
        }
        risk_style, risk_label = risk_colors.get(opt.get('risk', 'low'), ('', ''))
        
        button_style = f"""
        <div style='
            border: 2px solid {"#3b82f6" if is_selected else "#e5e7eb"};
            background: {"#eff6ff" if is_selected else "white"};
            padding: 1.25rem;
            border-radius: 0.75rem;
            margin-bottom: 1rem;
            cursor: pointer;
            transition: all 0.2s;
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-weight: 500; color: #1f2937;'>{opt['label']}</span>
                <span style='{risk_style} padding: 0.25rem 0.75rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 600;'>
                    {risk_label}
                </span>
            </div>
        </div>
        """
        
        if st.button(opt['label'], key=f"opt_{current_q['id']}_{idx}", use_container_width=True):
            if current_q['id'] not in st.session_state.answers:
                st.session_state.answers[current_q['id']] = {}
            st.session_state.answers[current_q['id']]['value'] = opt['value']
            selected_option = opt['value']
            st.rerun()
    
    # Follow-up question if option selected
    if current_answer.get('value'):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: #eff6ff; border: 1px solid #bfdbfe; padding: 1.5rem; border-radius: 0.75rem;'>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**{current_q['follow_up']}**")
        
        if current_q['follow_up_type'] == 'number':
            current_val = current_answer.get('follow_up', '')
            
            follow_up_text = st.text_input(
                current_q['follow_up_label'],
                value=current_val,
                placeholder=current_q['follow_up_help'],
                key=f"followup_{current_q['id']}",
                help=current_q['follow_up_help']
            )
            
            # Validate and store
            if follow_up_text:
                try:
                    # Remove common formatting characters
                    cleaned = follow_up_text.replace(',', '').replace('$', '').replace(' ', '').strip()
                    float(cleaned)  # Validate it's a number
                    st.session_state.answers[current_q['id']]['follow_up'] = cleaned
                except ValueError:
                    st.error("⚠️ Please enter a valid number")
                    st.session_state.answers[current_q['id']]['follow_up'] = None
            else:
                st.session_state.answers[current_q['id']]['follow_up'] = None
        else:
            follow_up_value = st.text_input(
                current_q['follow_up_label'],
                value=current_answer.get('follow_up', ''),
                placeholder=current_q['follow_up_help'],
                key=f"followup_{current_q['id']}",
                help=current_q['follow_up_help']
            )
            st.session_state.answers[current_q['id']]['follow_up'] = follow_up_value if follow_up_value else None
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("← Previous", use_container_width=True, type="secondary"):
                st.session_state.current_question -= 1
                st.rerun()
        else:
            st.markdown("")  # Empty space for alignment
    
    with col2:
        can_proceed = (
            current_q['id'] in st.session_state.answers and
            st.session_state.answers[current_q['id']].get('value') and
            st.session_state.answers[current_q['id']].get('follow_up')
        )
        
        if st.session_state.current_question < len(questions) - 1:
            if st.button("Next Question →", use_container_width=True, disabled=not can_proceed, type="primary"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Generate Report 📊", use_container_width=True, disabled=not can_proceed, type="primary"):
                st.session_state.show_report = True
                st.rerun()
    
    # Privacy notice
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🔒 Your responses are confidential and used only to generate your personalized report")

# Main app logic
if st.session_state.show_report:
    show_report()
else:
    show_question()
