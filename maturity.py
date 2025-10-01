import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Business Data Health Diagnostic - DataDoctor",
    page_icon="🏥",
    layout="wide"
)

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
        'follow_up_label': 'Number of people'
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
        'follow_up_label': 'Hourly rate ($)'
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
        'follow_up': 'Approximately how much does a bad-data decision cost? (rough estimate)',
        'follow_up_type': 'number',
        'follow_up_label': 'Cost per incident ($)'
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
        'follow_up_label': 'Opportunities per month'
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
        'follow_up_label': 'Hours per week'
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
        'follow_up': 'Are you subject to specific compliance requirements? (SOX, GDPR, HIPAA, etc.)',
        'follow_up_type': 'text',
        'follow_up_label': 'Compliance requirements (or "None")'
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
            people = int(answer['follow_up']) if answer['follow_up'] else 1
            hours_per_report = option['cost']
            reports_per_year = 52
            avg_cost_per_hour = 75
            annual_cost = hours_per_report * people * reports_per_year * avg_cost_per_hour
            findings['total_annual_cost'] += annual_cost
            findings['time_wasted'] += hours_per_report * reports_per_year
            if option['risk'] in ['high', 'critical']:
                findings['critical_issues'].append({
                    'area': 'Report Generation Time',
                    'impact': f"${annual_cost:,}/year in productivity costs",
                    'detail': f"{people} people spending {hours_per_report} hours per report, {reports_per_year} times/year"
                })
                findings['opportunities'].append({
                    'area': 'Automated Reporting',
                    'potential': f"Save ${int(annual_cost * 0.8):,}/year by automating report generation",
                    'improvement': '80-90% time reduction'
                })
    
    # Manual work calculations
    if 'manual_work' in st.session_state.answers:
        answer = st.session_state.answers['manual_work']
        option = next((o for o in questions[1]['options'] if o['value'] == answer['value']), None)
        if option and 'hours' in option and answer.get('follow_up'):
            hourly_rate = float(answer['follow_up']) if answer['follow_up'] else 75
            weekly_hours = option['hours']
            annual_cost = weekly_hours * 52 * hourly_rate
            findings['total_annual_cost'] += annual_cost
            findings['time_wasted'] += weekly_hours * 52
            if weekly_hours >= 15:
                findings['critical_issues'].append({
                    'area': 'Manual Data Processing',
                    'impact': f"${annual_cost:,}/year in labor costs",
                    'detail': f"{weekly_hours} hours/week at ${hourly_rate}/hour"
                })
                findings['opportunities'].append({
                    'area': 'Data Pipeline Automation',
                    'potential': f"Save ${int(annual_cost * 0.75):,}/year through automation",
                    'improvement': '75% reduction in manual work'
                })
    
    # Data accuracy calculations
    if 'data_accuracy' in st.session_state.answers:
        answer = st.session_state.answers['data_accuracy']
        option = next((o for o in questions[2]['options'] if o['value'] == answer['value']), None)
        if option and 'frequency' in option and answer.get('follow_up'):
            cost_per_incident = float(answer['follow_up']) if answer['follow_up'] else 1000
            monthly_incidents = option['frequency']
            annual_cost = cost_per_incident * monthly_incidents * 12
            findings['risk_exposure'] += annual_cost
            if option['risk'] in ['high', 'critical']:
                findings['critical_issues'].append({
                    'area': 'Data Quality Issues',
                    'impact': f"${annual_cost:,}/year in bad decisions and rework",
                    'detail': f"{monthly_incidents} incidents/month at ${cost_per_incident:,} each"
                })
                findings['opportunities'].append({
                    'area': 'Data Quality Framework',
                    'potential': f"Prevent ${int(annual_cost * 0.7):,}/year in errors",
                    'improvement': '70-90% reduction in data errors'
                })
    
    # Decision speed calculations
    if 'decision_speed' in st.session_state.answers:
        answer = st.session_state.answers['decision_speed']
        option = next((o for o in questions[3]['options'] if o['value'] == answer['value']), None)
        if option and 'delay' in option and answer.get('follow_up'):
            opportunities_per_month = int(answer['follow_up']) if answer['follow_up'] else 5
            avg_opportunity_value = 5000
            opportunities_lost = opportunities_per_month * 0.2
            annual_cost = opportunities_lost * 12 * avg_opportunity_value
            findings['risk_exposure'] += annual_cost
            if option['risk'] in ['high', 'critical']:
                findings['critical_issues'].append({
                    'area': 'Slow Decision Making',
                    'impact': f"${annual_cost:,}/year in missed opportunities",
                    'detail': f"{option['delay']}-day delays on {opportunities_per_month} monthly opportunities"
                })
                findings['opportunities'].append({
                    'area': 'Real-Time Analytics',
                    'potential': f"Capture ${int(annual_cost * 0.6):,}/year in faster decisions",
                    'improvement': 'Decision time from days to minutes'
                })
    
    # Data silos calculations
    if 'data_silos' in st.session_state.answers:
        answer = st.session_state.answers['data_silos']
        option = next((o for o in questions[4]['options'] if o['value'] == answer['value']), None)
        if option and 'systems' in option and answer.get('follow_up'):
            hours_per_week = float(answer['follow_up']) if answer['follow_up'] else 10
            annual_cost = hours_per_week * 52 * 75
            findings['total_annual_cost'] += annual_cost
            findings['time_wasted'] += hours_per_week * 52
            if option['systems'] >= 6:
                findings['critical_issues'].append({
                    'area': 'Data Silos & Integration',
                    'impact': f"${annual_cost:,}/year in integration labor",
                    'detail': f"{option['systems']} disconnected systems, {hours_per_week} hours/week to reconcile"
                })
                findings['opportunities'].append({
                    'area': 'Unified Data Platform',
                    'potential': f"Save ${int(annual_cost * 0.7):,}/year with integrated data",
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
                    'impact': f"${option['exposure']:,} potential exposure",
                    'detail': f"Inadequate audit trail for {compliance}"
                })
                findings['opportunities'].append({
                    'area': 'Data Governance & Compliance',
                    'potential': f"Mitigate ${option['exposure']:,} in compliance risk",
                    'improvement': 'Full audit trail and regulatory compliance'
                })
    
    return findings

def show_report():
    findings = calculate_findings()
    total_impact = findings['total_annual_cost'] + findings['risk_exposure']
    
    st.markdown("# Business Data Health Report")
    st.markdown(f"**Confidential Assessment** - {datetime.now().strftime('%B %d, %Y')}")
    st.divider()
    
    # Total Impact Section
    st.markdown(f"""
    <div style='background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 2rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
        <h2 style='color: #991b1b; margin-bottom: 1rem;'>Total Annual Impact Identified</h2>
        <div style='font-size: 3rem; font-weight: 800; color: #dc2626; margin-bottom: 1.5rem;'>
            ${total_impact:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Annual Costs", f"${findings['total_annual_cost']:,}")
    with col2:
        st.metric("Risk Exposure", f"${findings['risk_exposure']:,}")
    with col3:
        st.metric("Hours Wasted", f"{int(findings['time_wasted']):,} hrs/year")
    
    st.divider()
    
    # Critical Issues
    if findings['critical_issues']:
        st.markdown("## ⚠️ Critical Issues Identified")
        for issue in findings['critical_issues']:
            st.markdown(f"""
            <div style='background-color: #fff; border: 1px solid #fed7aa; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1rem;'>
                <h3 style='color: #1f2937; margin-bottom: 0.5rem;'>{issue['area']}</h3>
                <p style='color: #dc2626; font-weight: 600; margin-bottom: 0.5rem;'>{issue['impact']}</p>
                <p style='color: #6b7280;'>{issue['detail']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Opportunities
    if findings['opportunities']:
        st.markdown("## 📈 Revenue & Cost Reduction Opportunities")
        for opp in findings['opportunities']:
            st.markdown(f"""
            <div style='background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1rem;'>
                <h3 style='color: #1f2937; margin-bottom: 0.5rem;'>{opp['area']}</h3>
                <p style='color: #059669; font-weight: 600; margin-bottom: 0.5rem;'>{opp['potential']}</p>
                <p style='color: #6b7280;'>{opp['improvement']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Bottom Line
    st.markdown(f"""
    <div style='background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 2rem; border-radius: 0.5rem; margin-bottom: 2rem;'>
        <h2 style='color: #1e40af; margin-bottom: 1rem;'>Bottom Line</h2>
        <p style='color: #374151; margin-bottom: 1.5rem; line-height: 1.7;'>
            Based on your responses, your organization is facing <strong>${total_impact:,}</strong> in 
            annual costs and risk exposure due to data challenges. The good news: most of this is preventable.
        </p>
        <div style='background-color: #fff; border-radius: 0.5rem; padding: 1.5rem;'>
            <div style='color: #6b7280; margin-bottom: 0.5rem;'>Estimated First-Year ROI with Data Solutions</div>
            <div style='font-size: 2.5rem; font-weight: 800; color: #3b82f6;'>
                {int((total_impact * 0.6) / (total_impact * 0.15) * 100) if total_impact > 0 else 0}% ROI
            </div>
            <div style='color: #6b7280; margin-top: 0.5rem;'>Typical 6-8 month payback period</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: #fff; padding: 2.5rem; border-radius: 0.75rem;'>
        <h2 style='margin-bottom: 1.5rem;'>Want to Increase Revenue, Decrease Costs, and Avoid Risk?</h2>
        <p style='opacity: 0.95; margin-bottom: 2rem; font-size: 1.05rem;'>
            Let's talk about a strategic data solution tailored to your business. I can help you:
        </p>
        <ul style='list-style: none; padding: 0; margin-bottom: 2rem;'>
            <li style='margin-bottom: 1rem;'>💰 Recover ${int(findings['total_annual_cost'] * 0.7):,} annually in productivity costs</li>
            <li style='margin-bottom: 1rem;'>🛡️ Mitigate ${findings['risk_exposure']:,} in risk exposure</li>
            <li style='margin-bottom: 1rem;'>📈 Enable data-driven decisions in minutes instead of days</li>
        </ul>
        <div style='border-top: 1px solid rgba(255,255,255,0.2); padding-top: 2rem;'>
            <p style='font-size: 1.25rem; font-weight: 600; margin-bottom: 0.75rem;'>Schedule a 30-Minute Strategy Call</p>
            <p style='opacity: 0.9; margin-bottom: 1.5rem;'>No obligation. We'll discuss your specific situation and potential solutions.</p>
            <p>📧 solveproblems@datadoctor.com &nbsp;&nbsp;&nbsp; 📞 (555) 123-4567</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🔄 Start New Assessment"):
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.show_report = False
        st.rerun()

def show_question():
    current_q = questions[st.session_state.current_question]
    
    # Header
    st.markdown(f"### Business Data Health Diagnostic")
    st.progress((st.session_state.current_question + 1) / len(questions))
    st.markdown(f"**Question {st.session_state.current_question + 1} of {len(questions)}**")
    st.divider()
    
    # Question
    category_icons = {
        'revenue': '📈',
        'cost': '💰',
        'risk': '🛡️',
        'time': '📄'
    }
    icon = category_icons.get(current_q['category'], '❓')
    
    st.markdown(f"## {icon} {current_q['question']}")
    st.markdown(f"*{current_q['subtitle']}*")
    st.write("")
    
    # Options
    current_answer = st.session_state.answers.get(current_q['id'], {})
    
    selected_option = st.radio(
        "Select your answer:",
        options=[opt['value'] for opt in current_q['options']],
        format_func=lambda x: next((opt['label'] for opt in current_q['options'] if opt['value'] == x), x),
        index=[opt['value'] for opt in current_q['options']].index(current_answer.get('value')) if current_answer.get('value') else None,
        key=f"radio_{current_q['id']}"
    )
    
    # Update answer
    if selected_option:
        if current_q['id'] not in st.session_state.answers:
            st.session_state.answers[current_q['id']] = {}
        st.session_state.answers[current_q['id']]['value'] = selected_option
        
        # Follow-up question
        st.write("")
        st.markdown(f"**{current_q['follow_up']}**")
        
        if current_q['follow_up_type'] == 'number':
            follow_up_value = st.number_input(
                current_q['follow_up_label'],
                min_value=0.0,
                value=float(current_answer.get('follow_up', 0)) if current_answer.get('follow_up') else 0.0,
                key=f"followup_{current_q['id']}"
            )
            st.session_state.answers[current_q['id']]['follow_up'] = str(follow_up_value) if follow_up_value > 0 else None
        else:
            follow_up_value = st.text_input(
                current_q['follow_up_label'],
                value=current_answer.get('follow_up', ''),
                key=f"followup_{current_q['id']}"
            )
            st.session_state.answers[current_q['id']]['follow_up'] = follow_up_value if follow_up_value else None
    
    # Navigation buttons
    st.write("")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        can_proceed = (
            current_q['id'] in st.session_state.answers and
            st.session_state.answers[current_q['id']].get('value') and
            st.session_state.answers[current_q['id']].get('follow_up')
        )
        
        if st.session_state.current_question < len(questions) - 1:
            if st.button("Next Question ➡️", disabled=not can_proceed):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Generate Report 📊", disabled=not can_proceed):
                st.session_state.show_report = True
                st.rerun()
    
    st.write("")
    st.info("🔒 Your responses are confidential and used only to generate your personalized report")

# Main app logic
if st.session_state.show_report:
    show_report()
else:
    show_question()
