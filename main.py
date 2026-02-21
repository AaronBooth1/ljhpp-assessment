#!/usr/bin/env python3
"""
🏢 LJ Hooker Property Partners - Assessment Platform
==================================================
Railway.app Deployment Version - OPTIMIZED FOR NEW CANDIDATES
"""

import os
import sys
import json
import uuid
import threading
import time
import random
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import html

# Get port from environment (Railway requirement)
PORT = int(os.environ.get('PORT', 5000))
ADMIN_EMAIL = 'admin@ljhpp.com'
ADMIN_PASSWORD = 'admin123'

# LJ Hooker Brand Colors - Matching Gamma site
LJ_RED = '#E31E24'
LJ_DARK = '#1A1A1A'
LJ_GRAY = '#6C6C6C'
LJ_LIGHT_GRAY = '#F8F9FA'
LJ_ACCENT = '#FF6B6B'

# 100 General Assessment Questions - Suitable for New/Entry-Level Candidates
BASE_QUESTIONS = [
    {"id": 1, "text": "I enjoy meeting new people and making connections", "category": "social"},
    {"id": 2, "text": "I like to organize my workspace and keep things tidy", "category": "detail"},
    {"id": 3, "text": "I feel comfortable speaking in front of groups", "category": "leadership"},
    {"id": 4, "text": "I enjoy learning new things and skills", "category": "adaptability"},
    {"id": 5, "text": "I prefer to work as part of a team rather than alone", "category": "social"},
    {"id": 6, "text": "I like to double-check my work before submitting it", "category": "detail"},
    {"id": 7, "text": "I often take the initiative to start new projects", "category": "leadership"},
    {"id": 8, "text": "I adapt easily to changes in plans or procedures", "category": "adaptability"},
    {"id": 9, "text": "I enjoy helping others solve their problems", "category": "service"},
    {"id": 10, "text": "I like to research topics thoroughly before making decisions", "category": "analytical"},
    {"id": 11, "text": "I feel energized when working with customers or clients", "category": "social"},
    {"id": 12, "text": "I pay attention to small details that others might miss", "category": "detail"},
    {"id": 13, "text": "I'm comfortable making decisions when others are unsure", "category": "leadership"},
    {"id": 14, "text": "I handle unexpected situations calmly", "category": "adaptability"},
    {"id": 15, "text": "I go out of my way to ensure customer satisfaction", "category": "service"},
    {"id": 16, "text": "I enjoy analyzing information to find patterns", "category": "analytical"},
    {"id": 17, "text": "I build relationships easily with new people", "category": "social"},
    {"id": 18, "text": "I create lists and schedules to stay organized", "category": "detail"},
    {"id": 19, "text": "I'm willing to take charge when leadership is needed", "category": "leadership"},
    {"id": 20, "text": "I see change as an opportunity rather than a problem", "category": "adaptability"},
    {"id": 21, "text": "I genuinely care about helping people achieve their goals", "category": "service"},
    {"id": 22, "text": "I like to gather all the facts before forming opinions", "category": "analytical"},
    {"id": 23, "text": "I enjoy networking and building professional relationships", "category": "social"},
    {"id": 24, "text": "I follow through on commitments and promises", "category": "detail"},
    {"id": 25, "text": "I'm comfortable delegating tasks to others", "category": "leadership"},
    {"id": 26, "text": "I learn new technology and tools quickly", "category": "adaptability"},
    {"id": 27, "text": "I put the needs of others before my own", "category": "service"},
    {"id": 28, "text": "I enjoy solving complex problems step by step", "category": "analytical"},
    {"id": 29, "text": "I remember personal details about people I meet", "category": "social"},
    {"id": 30, "text": "I maintain high standards in everything I do", "category": "detail"},
    {"id": 31, "text": "I inspire others to do their best work", "category": "leadership"},
    {"id": 32, "text": "I thrive in fast-paced, dynamic environments", "category": "adaptability"},
    {"id": 33, "text": "I anticipate what others need before they ask", "category": "service"},
    {"id": 34, "text": "I compare options carefully before making choices", "category": "analytical"},
    {"id": 35, "text": "I enjoy social events and group activities", "category": "social"},
    {"id": 36, "text": "I check my work multiple times to ensure accuracy", "category": "detail"},
    {"id": 37, "text": "I motivate team members during challenging times", "category": "leadership"},
    {"id": 38, "text": "I adjust my approach based on feedback", "category": "adaptability"},
    {"id": 39, "text": "I follow up to make sure people are satisfied", "category": "service"},
    {"id": 40, "text": "I research thoroughly before making recommendations", "category": "analytical"},
    {"id": 41, "text": "I connect well with people from different backgrounds", "category": "social"},
    {"id": 42, "text": "I keep detailed records of important information", "category": "detail"},
    {"id": 43, "text": "I set clear goals and work toward achieving them", "category": "leadership"},
    {"id": 44, "text": "I embrace new challenges with enthusiasm", "category": "adaptability"},
    {"id": 45, "text": "I exceed expectations in customer service", "category": "service"},
    {"id": 46, "text": "I analyze situations from multiple perspectives", "category": "analytical"},
    {"id": 47, "text": "I maintain long-term friendships and relationships", "category": "social"},
    {"id": 48, "text": "I complete tasks thoroughly and completely", "category": "detail"},
    {"id": 49, "text": "I take responsibility for team outcomes", "category": "leadership"},
    {"id": 50, "text": "I stay positive during periods of change", "category": "adaptability"},
    {"id": 51, "text": "I genuinely enjoy helping people succeed", "category": "service"},
    {"id": 52, "text": "I verify information before sharing it with others", "category": "analytical"},
    {"id": 53, "text": "I feel comfortable in social situations", "category": "social"},
    {"id": 54, "text": "I organize my time effectively to meet deadlines", "category": "detail"},
    {"id": 55, "text": "I provide direction when teams need guidance", "category": "leadership"},
    {"id": 56, "text": "I adapt my communication style to different audiences", "category": "adaptability"},
    {"id": 57, "text": "I take pride in delivering excellent service", "category": "service"},
    {"id": 58, "text": "I think through problems logically", "category": "analytical"},
    {"id": 59, "text": "I enjoy collaborating with diverse groups of people", "category": "social"},
    {"id": 60, "text": "I notice when things are out of place or incorrect", "category": "detail"},
    {"id": 61, "text": "I encourage others to share their ideas", "category": "leadership"},
    {"id": 62, "text": "I handle multiple priorities effectively", "category": "adaptability"},
    {"id": 63, "text": "I make sure everyone feels included and valued", "category": "service"},
    {"id": 64, "text": "I gather input from others before making decisions", "category": "analytical"},
    {"id": 65, "text": "I build trust quickly with new acquaintances", "category": "social"},
    {"id": 66, "text": "I create systems to improve efficiency", "category": "detail"},
    {"id": 67, "text": "I lead by example in all situations", "category": "leadership"},
    {"id": 68, "text": "I remain flexible when plans need to change", "category": "adaptability"},
    {"id": 69, "text": "I listen carefully to understand others' needs", "category": "service"},
    {"id": 70, "text": "I consider long-term consequences of decisions", "category": "analytical"},
    {"id": 71, "text": "I make others feel comfortable in conversations", "category": "social"},
    {"id": 72, "text": "I maintain consistent quality in my work", "category": "detail"},
    {"id": 73, "text": "I help resolve conflicts between team members", "category": "leadership"},
    {"id": 74, "text": "I learn from mistakes and improve quickly", "category": "adaptability"},
    {"id": 75, "text": "I go above and beyond to help others", "category": "service"},
    {"id": 76, "text": "I ask thoughtful questions to understand situations", "category": "analytical"},
    {"id": 77, "text": "I enjoy meeting people from different industries", "category": "social"},
    {"id": 78, "text": "I plan ahead to avoid last-minute problems", "category": "detail"},
    {"id": 79, "text": "I communicate vision clearly to others", "category": "leadership"},
    {"id": 80, "text": "I stay calm under pressure", "category": "adaptability"},
    {"id": 81, "text": "I remember what's important to the people I serve", "category": "service"},
    {"id": 82, "text": "I evaluate options objectively", "category": "analytical"},
    {"id": 83, "text": "I enjoy introducing people to each other", "category": "social"},
    {"id": 84, "text": "I review my work carefully before considering it complete", "category": "detail"},
    {"id": 85, "text": "I take initiative to solve problems", "category": "leadership"},
    {"id": 86, "text": "I see opportunities in challenging situations", "category": "adaptability"},
    {"id": 87, "text": "I ensure others feel heard and understood", "category": "service"},
    {"id": 88, "text": "I base my opinions on facts rather than emotions", "category": "analytical"},
    {"id": 89, "text": "I maintain professional relationships over time", "category": "social"},
    {"id": 90, "text": "I document important processes and procedures", "category": "detail"},
    {"id": 91, "text": "I coordinate team efforts effectively", "category": "leadership"},
    {"id": 92, "text": "I adjust my goals based on changing circumstances", "category": "adaptability"},
    {"id": 93, "text": "I celebrate others' successes and achievements", "category": "service"},
    {"id": 94, "text": "I research best practices before implementing solutions", "category": "analytical"},
    {"id": 95, "text": "I connect with people on both personal and professional levels", "category": "social"},
    {"id": 96, "text": "I ensure all aspects of a project are completed properly", "category": "detail"},
    {"id": 97, "text": "I build consensus among team members", "category": "leadership"},
    {"id": 98, "text": "I embrace new ways of doing things", "category": "adaptability"},
    {"id": 99, "text": "I make sure everyone's needs are considered", "category": "service"},
    {"id": 100, "text": "I validate my assumptions with reliable sources", "category": "analytical"}
]

# In-memory storage for cloud deployment
candidates_data = []
results_data = []

# Create randomized question set for each session
QUESTIONS = BASE_QUESTIONS.copy()
random.shuffle(QUESTIONS)

def calculate_scores(responses):
    """Calculate comprehensive personality scores"""
    scores = {
        'leadership': 0, 'analytical': 0, 'social': 0, 'detail': 0,
        'adaptability': 0, 'service': 0
    }
    
    for response in responses:
        qid = response['question_id']
        value = response['value']
        
        # Find question category
        question = next((q for q in BASE_QUESTIONS if q['id'] == qid), None)
        if question:
            category = question['category']
            if category in scores:
                scores[category] += value
    
    return scores

def generate_comprehensive_profile(scores):
    """Generate detailed personality profile with real estate role matching"""
    
    # Calculate percentiles (approximately 16-17 questions per category * 5 max = 80-85 max per category)
    max_scores = {
        'leadership': 85, 'analytical': 85, 'social': 85, 'detail': 85, 'adaptability': 85, 'service': 85
    }
    
    percentiles = {}
    for trait, score in scores.items():
        percentiles[trait] = min(100, (score / max_scores[trait]) * 100)
    
    # Determine primary traits (top 3)
    sorted_traits = sorted(percentiles.items(), key=lambda x: x[1], reverse=True)
    primary_traits = [trait for trait, score in sorted_traits[:3]]
    
    # Real Estate Role matching with weighted scoring
    role_matches = []
    
    # Sales Agent (High social, service, adaptability)
    sales_score = (percentiles['social'] * 0.35 + percentiles['service'] * 0.25 + 
                  percentiles['adaptability'] * 0.25 + percentiles['leadership'] * 0.15)
    role_matches.append(('Sales Agent', sales_score))
    
    # Property Manager (High detail, service, analytical)
    pm_score = (percentiles['detail'] * 0.35 + percentiles['service'] * 0.25 + 
               percentiles['analytical'] * 0.25 + percentiles['adaptability'] * 0.15)
    role_matches.append(('Property Manager', pm_score))
    
    # Team Leader/Principal (High leadership, social, service)
    leader_score = (percentiles['leadership'] * 0.4 + percentiles['social'] * 0.25 + 
                   percentiles['service'] * 0.25 + percentiles['analytical'] * 0.1)
    role_matches.append(('Team Leader/Principal', leader_score))
    
    # Client Relations Specialist (High service, social, adaptability)
    crm_score = (percentiles['service'] * 0.4 + percentiles['social'] * 0.3 + 
                percentiles['adaptability'] * 0.2 + percentiles['detail'] * 0.1)
    role_matches.append(('Client Relations Specialist', crm_score))
    
    # Administrative Support (High detail, service, analytical)
    admin_score = (percentiles['detail'] * 0.4 + percentiles['service'] * 0.3 + 
                  percentiles['analytical'] * 0.2 + percentiles['adaptability'] * 0.1)
    role_matches.append(('Administrative Support', admin_score))
    
    # Business Development (High social, leadership, adaptability)
    bd_score = (percentiles['social'] * 0.35 + percentiles['leadership'] * 0.3 + 
               percentiles['adaptability'] * 0.25 + percentiles['service'] * 0.1)
    role_matches.append(('Business Development', bd_score))
    
    # Sort by fit score
    role_matches.sort(key=lambda x: x[1], reverse=True)
    top_roles = role_matches[:3]
    
    # Generate personality type based on primary trait
    primary_trait = primary_traits[0]
    personality_types = {
        'leadership': 'Natural Leader',
        'analytical': 'Thoughtful Analyst', 
        'social': 'People Connector',
        'detail': 'Quality Focused',
        'adaptability': 'Flexible Achiever',
        'service': 'Helper & Supporter'
    }
    
    personality_type = personality_types.get(primary_trait, 'Well-Rounded Professional')
    
    # Generate detailed insights
    strengths = []
    development_areas = []
    management_style = ""
    
    # Leadership insights
    if percentiles['leadership'] >= 70:
        strengths.append("Natural leadership potential and team coordination abilities")
        management_style += "Thrives with autonomy and leadership opportunities. "
    elif percentiles['leadership'] <= 30:
        development_areas.append("Leadership confidence and team coordination skills")
        management_style += "Benefits from clear direction and mentorship in leadership. "
    
    # Social insights
    if percentiles['social'] >= 70:
        strengths.append("Excellent people skills and relationship building abilities")
    elif percentiles['social'] <= 30:
        development_areas.append("Interpersonal communication and networking skills")
    
    # Service insights
    if percentiles['service'] >= 70:
        strengths.append("Strong customer service orientation and helping mindset")
    elif percentiles['service'] <= 30:
        development_areas.append("Customer service focus and support skills")
    
    # Detail insights
    if percentiles['detail'] >= 70:
        strengths.append("Strong attention to detail and organizational skills")
    elif percentiles['detail'] <= 30:
        development_areas.append("Attention to detail and organizational systems")
    
    # Adaptability insights
    if percentiles['adaptability'] >= 70:
        strengths.append("Excellent adaptability and learning agility")
    elif percentiles['adaptability'] <= 30:
        development_areas.append("Flexibility and adaptation to change")
    
    # Analytical insights
    if percentiles['analytical'] >= 70:
        strengths.append("Strong analytical thinking and problem-solving skills")
    elif percentiles['analytical'] <= 30:
        development_areas.append("Analytical thinking and systematic problem-solving")
    
    return {
        'personality_type': personality_type,
        'primary_traits': primary_traits,
        'percentiles': percentiles,
        'top_roles': top_roles,
        'strengths': strengths,
        'development_areas': development_areas,
        'management_style': management_style.strip()
    }

class LJHPPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            path = urlparse(self.path).path
            
            if path == '/':
                self.serve_home()
            elif path == '/assessment':
                self.serve_assessment()
            elif path == '/admin':
                self.serve_admin()
            elif path == '/dashboard':
                self.serve_dashboard()
            elif path == '/export':
                self.export_csv()
            else:
                self.send_error(404)
                
        except Exception as e:
            print(f"GET Error: {e}")
            self.send_error(500)
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            path = urlparse(self.path).path
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            if path == '/submit_assessment':
                self.handle_assessment_submission(post_data)
            elif path == '/admin_login':
                self.handle_admin_login(post_data)
            else:
                self.send_error(404)
                
        except Exception as e:
            print(f"POST Error: {e}")
            self.send_error(500)
    
    def serve_home(self):
        """Serve LJ Hooker branded home page with optimized fonts"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>LJ Hooker Property Partners - Assessment Platform</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-weight: 400;
            line-height: 1.6;
            background: linear-gradient(135deg, {LJ_RED} 0%, {LJ_DARK} 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }}
        
        .container {{
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 600px;
            width: 90%;
        }}
        
        .logo {{
            width: 100px;
            height: 100px;
            background: {LJ_RED};
            border-radius: 20px;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 2px;
            box-shadow: 0 10px 20px rgba(227, 30, 36, 0.3);
        }}
        
        h1 {{ 
            color: {LJ_DARK}; 
            margin-bottom: 10px; 
            font-size: 2.5em; 
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        
        .subtitle {{ 
            color: {LJ_GRAY}; 
            margin-bottom: 30px; 
            font-size: 1.2em; 
            font-weight: 400;
        }}
        
        .btn {{
            background: {LJ_RED};
            color: white;
            padding: 18px 40px;
            border: none;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 15px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(227, 30, 36, 0.3);
            font-family: inherit;
        }}
        
        .btn:hover {{ 
            background: #c41e22; 
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(227, 30, 36, 0.4);
        }}
        
        .btn-secondary {{ 
            background: {LJ_DARK}; 
        }}
        
        .btn-secondary:hover {{ 
            background: #333; 
        }}
        
        .status {{
            background: linear-gradient(135deg, {LJ_LIGHT_GRAY} 0%, #e9ecef 100%);
            color: {LJ_DARK};
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            border-left: 5px solid {LJ_RED};
            font-weight: 400;
        }}
        
        .status strong {{
            font-weight: 600;
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .feature {{
            padding: 20px;
            background: {LJ_LIGHT_GRAY};
            border-radius: 10px;
            border-top: 3px solid {LJ_RED};
        }}
        
        .feature-icon {{ 
            font-size: 24px; 
            margin-bottom: 10px; 
        }}
        
        .feature-title {{ 
            font-weight: 600; 
            color: {LJ_DARK}; 
            margin-bottom: 5px; 
            font-size: 16px;
        }}
        
        .feature-desc {{ 
            font-size: 14px; 
            color: {LJ_GRAY}; 
            font-weight: 400;
        }}
        
        .cloud-badge {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
            margin-bottom: 20px;
            display: inline-block;
            font-size: 14px;
        }}
        
        /* Font optimization for different devices */
        @media screen and (-webkit-min-device-pixel-ratio: 2) {{
            body {{
                -webkit-font-smoothing: subpixel-antialiased;
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 30px 20px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .subtitle {{
                font-size: 1.1em;
            }}
            
            .btn {{
                padding: 15px 30px;
                font-size: 16px;
                margin: 10px 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="cloud-badge">🌐 LIVE ON RAILWAY!</div>
        <div class="logo">LJ</div>
        <h1>LJ Hooker Property Partners</h1>
        <p class="subtitle">Professional Assessment Platform</p>
        
        <div class="status">
            <strong>🟢 Cloud Platform Ready</strong><br>
            100-question comprehensive assessment • Real estate role matching • Secure cloud storage<br>
            <small>Powered by LJHPP Assessment Engine v3.0 - Railway Edition</small>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">📋</div>
                <div class="feature-title">100 Questions</div>
                <div class="feature-desc">Comprehensive assessment</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Role Matching</div>
                <div class="feature-desc">6 real estate careers</div>
            </div>
            <div class="feature">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Mobile Ready</div>
                <div class="feature-desc">Works on all devices</div>
            </div>
            <div class="feature">
                <div class="feature-icon">☁️</div>
                <div class="feature-title">Cloud Hosted</div>
                <div class="feature-desc">Always accessible</div>
            </div>
        </div>
        
        <a href="/assessment" class="btn">🚀 Start Assessment</a>
        <a href="/admin" class="btn btn-secondary">📊 Admin Dashboard</a>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_assessment(self):
        """Serve comprehensive assessment form with optimized fonts"""
        questions_html = ""
        for i, question in enumerate(QUESTIONS, 1):
            questions_html += f"""
                <div class="question">
                    <div class="question-number">{i}/100</div>
                    <p class="question-text">{html.escape(question['text'])}</p>
                    <div class="scale">
                        <span class="scale-label">Strongly Disagree</span>
                        <div class="scale-options">
                            <div class="scale-option">
                                <input type="radio" name="q{question['id']}" value="1" required>
                                <label>1</label>
                            </div>
                            <div class="scale-option">
                                <input type="radio" name="q{question['id']}" value="2" required>
                                <label>2</label>
                            </div>
                            <div class="scale-option">
                                <input type="radio" name="q{question['id']}" value="3" required>
                                <label>3</label>
                            </div>
                            <div class="scale-option">
                                <input type="radio" name="q{question['id']}" value="4" required>
                                <label>4</label>
                            </div>
                            <div class="scale-option">
                                <input type="radio" name="q{question['id']}" value="5" required>
                                <label>5</label>
                            </div>
                        </div>
                        <span class="scale-label">Strongly Agree</span>
                    </div>
                </div>
            """
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>LJHPP Professional Assessment</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-weight: 400;
            line-height: 1.6;
            background: {LJ_LIGHT_GRAY};
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }}
        
        .header {{
            background: linear-gradient(135deg, {LJ_RED} 0%, {LJ_DARK} 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-weight: 600;
            font-size: 2.2em;
            letter-spacing: -0.02em;
        }}
        
        .header p {{
            font-weight: 400;
            opacity: 0.9;
        }}
        
        .container {{ 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 30px; 
        }}
        
        .candidate-info {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid {LJ_RED};
        }}
        
        .candidate-info h3 {{
            font-weight: 600;
            color: {LJ_DARK};
            margin-bottom: 20px;
        }}
        
        .form-group {{ 
            margin-bottom: 20px; 
        }}
        
        .form-group input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            font-weight: 400;
            transition: border-color 0.3s ease;
        }}
        
        .form-group input:focus {{
            border-color: {LJ_RED};
            outline: none;
            box-shadow: 0 0 0 3px rgba(227, 30, 36, 0.1);
        }}
        
        .question {{
            background: white;
            margin: 20px 0;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid {LJ_RED};
            position: relative;
        }}
        
        .question-number {{
            position: absolute;
            top: 15px;
            right: 20px;
            background: {LJ_RED};
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .question-text {{ 
            color: {LJ_DARK}; 
            margin-bottom: 20px; 
            font-size: 18px; 
            font-weight: 500;
            padding-right: 80px;
            line-height: 1.5;
        }}
        
        .scale {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 15px 0;
            flex-wrap: wrap;
        }}
        
        .scale-label {{ 
            font-weight: 600; 
            color: {LJ_GRAY}; 
            font-size: 14px;
            min-width: 120px;
        }}
        
        .scale-options {{
            display: flex;
            gap: 20px;
            margin: 10px 0;
        }}
        
        .scale-option {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }}
        
        .scale-option input {{ 
            margin: 0;
            transform: scale(1.3);
            accent-color: {LJ_RED};
        }}
        
        .scale-option label {{ 
            font-size: 14px; 
            color: {LJ_GRAY};
            font-weight: 600;
        }}
        
        .btn {{
            background: {LJ_RED};
            color: white;
            padding: 18px 40px;
            border: none;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(227, 30, 36, 0.3);
            font-family: inherit;
        }}
        
        .btn:hover {{ 
            background: #c41e22; 
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(227, 30, 36, 0.4);
        }}
        
        .btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }}
        
        .submit-section {{ 
            text-align: center; 
            margin: 40px 0;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .progress {{
            background: #e9ecef;
            height: 12px;
            border-radius: 6px;
            margin: 20px 0;
            overflow: hidden;
            position: sticky;
            top: 120px;
            z-index: 99;
        }}
        
        .progress-bar {{
            background: linear-gradient(90deg, {LJ_RED} 0%, {LJ_ACCENT} 100%);
            height: 100%;
            border-radius: 6px;
            transition: width 0.3s ease;
            width: 0%;
        }}
        
        .progress-text {{
            text-align: center;
            margin-top: 10px;
            color: {LJ_GRAY};
            font-weight: 600;
        }}
        
        @media (max-width: 768px) {{
            .scale {{ 
                flex-direction: column; 
                gap: 15px; 
            }}
            
            .scale-options {{ 
                justify-content: center; 
            }}
            
            .scale-label {{ 
                min-width: auto; 
            }}
            
            .question-text {{ 
                padding-right: 0; 
            }}
            
            .question-number {{ 
                position: static; 
                margin-bottom: 10px; 
            }}
            
            .container {{
                padding: 20px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 LJHPP Professional Assessment</h1>
        <p>Comprehensive Personality & Real Estate Role Fit Analysis</p>
    </div>
    
    <div class="container">
        <div class="progress">
            <div class="progress-bar" id="progress"></div>
        </div>
        <div class="progress-text" id="progressText">0 of 100 questions completed</div>
        
        <form method="POST" action="/submit_assessment" id="assessmentForm">
            <div class="candidate-info">
                <h3>👤 Candidate Information</h3>
                <div class="form-group">
                    <input type="text" name="name" placeholder="Full Name" required>
                </div>
                <div class="form-group">
                    <input type="email" name="email" placeholder="Email Address" required>
                </div>
                <div class="form-group">
                    <input type="text" name="position" placeholder="Position Applied For" required>
                </div>
            </div>
            
            {questions_html}
            
            <div class="submit-section">
                <button type="submit" class="btn" id="submitBtn" disabled>📊 Complete Assessment</button>
                <p style="margin-top: 15px; color: {LJ_GRAY};" id="submitText">Please answer all questions to submit</p>
            </div>
        </form>
    </div>
    
    <script>
        const form = document.getElementById('assessmentForm');
        const progressBar = document.getElementById('progress');
        const progressText = document.getElementById('progressText');
        const submitBtn = document.getElementById('submitBtn');
        const submitText = document.getElementById('submitText');
        const totalQuestions = 100;
        
        form.addEventListener('change', function() {{
            const answered = document.querySelectorAll('input[type="radio"]:checked').length;
            const progress = (answered / totalQuestions) * 100;
            
            progressBar.style.width = progress + '%';
            progressText.textContent = `${{answered}} of ${{totalQuestions}} questions completed`;
            
            if (answered === totalQuestions) {{
                submitBtn.disabled = false;
                submitBtn.style.background = '{LJ_RED}';
                submitBtn.textContent = '🎉 Submit Complete Assessment';
                submitText.textContent = 'All questions answered - ready to submit!';
                submitText.style.color = '{LJ_RED}';
            }} else {{
                submitBtn.disabled = true;
                submitBtn.style.background = '#ccc';
                submitBtn.textContent = `📊 Complete Assessment (${{answered}}/${{totalQuestions}})`;
                submitText.textContent = `Please answer all questions to submit (${{totalQuestions - answered}} remaining)`;
                submitText.style.color = '{LJ_GRAY}';
            }}
        }});
        
        form.addEventListener('submit', function(e) {{
            const answered = document.querySelectorAll('input[type="radio"]:checked').length;
            if (answered < totalQuestions) {{
                e.preventDefault();
                alert(`Please answer all ${{totalQuestions}} questions before submitting. You have answered ${{answered}} questions.`);
                return false;
            }}
            
            submitBtn.textContent = '⏳ Processing Assessment...';
            submitBtn.disabled = true;
            submitText.textContent = 'Calculating your personality profile...';
        }});
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_admin(self):
        """Serve admin login page with hidden credentials"""
        query = urlparse(self.path).query
        error_msg = ""
        if 'error=1' in query:
            error_msg = '<div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: 500;">❌ Invalid credentials. Please try again.</div>'
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>LJHPP Admin Login</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-weight: 400;
            line-height: 1.6;
            background: linear-gradient(135deg, {LJ_RED} 0%, {LJ_DARK} 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }}
        
        .login-container {{
            background: white;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            max-width: 400px;
            width: 90%;
        }}
        
        .logo {{
            width: 80px;
            height: 80px;
            background: {LJ_RED};
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            font-weight: 600;
        }}
        
        h2 {{ 
            text-align: center; 
            color: {LJ_DARK}; 
            margin-bottom: 30px; 
            font-weight: 600;
            font-size: 1.8em;
        }}
        
        .form-group {{ 
            margin-bottom: 20px; 
        }}
        
        .form-group input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            font-weight: 400;
            transition: border-color 0.3s ease;
        }}
        
        .form-group input:focus {{
            border-color: {LJ_RED};
            outline: none;
            box-shadow: 0 0 0 3px rgba(227, 30, 36, 0.1);
        }}
        
        .btn {{
            width: 100%;
            background: {LJ_RED};
            color: white;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.3s ease;
            font-family: inherit;
        }}
        
        .btn:hover {{ 
            background: #c41e22; 
        }}
        
        .back-link {{
            text-align: center;
            margin-top: 20px;
        }}
        
        .back-link a {{
            color: {LJ_GRAY};
            text-decoration: none;
            font-weight: 400;
        }}
        
        .credentials {{
            background: {LJ_LIGHT_GRAY};
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
            color: {LJ_GRAY};
            text-align: center;
            font-weight: 400;
        }}
        
        .credentials strong {{
            font-weight: 600;
            color: {LJ_DARK};
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🔐</div>
        <h2>Admin Dashboard</h2>
        
        {error_msg}
        
        <div class="credentials">
            <strong>Secure Admin Access</strong><br>
            Please enter your admin credentials
        </div>
        
        <form method="POST" action="/admin_login">
            <div class="form-group">
                <input type="email" name="email" placeholder="Admin Email Address" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Admin Password" required>
            </div>
            <button type="submit" class="btn">🚀 Access Dashboard</button>
        </form>
        <div class="back-link">
            <a href="/">← Back to Home</a>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def handle_assessment_submission(self, post_data):
        """Handle comprehensive assessment submission"""
        try:
            # Parse form data
            data = parse_qs(post_data)
            
            # Extract candidate info
            candidate = {
                'id': str(uuid.uuid4()),
                'name': data.get('name', [''])[0],
                'email': data.get('email', [''])[0],
                'position': data.get('position', [''])[0],
                'timestamp': datetime.now().isoformat()
            }
            
            # Extract responses
            responses = []
            for key, value in data.items():
                if key.startswith('q'):
                    question_id = int(key[1:])
                    responses.append({
                        'question_id': question_id,
                        'value': int(value[0])
                    })
            
            # Calculate scores and generate profile
            scores = calculate_scores(responses)
            profile = generate_comprehensive_profile(scores)
            
            # Save data to memory
            candidates_data.append(candidate)
            results_data.append({
                'candidate_id': candidate['id'],
                'responses': responses,
                'scores': scores,
                'profile': profile,
                'timestamp': candidate['timestamp']
            })
            
            # Show comprehensive results
            self.show_comprehensive_results(candidate, scores, profile)
            
        except Exception as e:
            print(f"Assessment submission error: {e}")
            self.send_error(500)
    
    def show_comprehensive_results(self, candidate, scores, profile):
        """Show comprehensive assessment results with optimized fonts"""
        
        # Generate role recommendations HTML
        roles_html = ""
        for i, (role, score) in enumerate(profile['top_roles'], 1):
            color = LJ_RED if i == 1 else '#ffc107' if i == 2 else '#6c757d'
            roles_html += f"""
                <div class="role-item">
                    <div class="role-rank" style="background: {color};">#{i}</div>
                    <div class="role-info">
                        <div class="role-name">{html.escape(role)}</div>
                        <div class="role-score">{score:.1f}% match</div>
                        <div class="role-bar">
                            <div class="role-fill" style="width: {score}%; background: {color};"></div>
                        </div>
                    </div>
                </div>
            """
        
        # Generate strengths HTML
        strengths_html = ""
        for strength in profile['strengths']:
            strengths_html += f'<li>{html.escape(strength)}</li>'
        
        # Generate development areas HTML
        development_html = ""
        for area in profile['development_areas']:
            development_html += f'<li>{html.escape(area)}</li>'
        
        # Generate trait scores HTML
        traits_html = ""
        for trait, percentile in profile['percentiles'].items():
            color = LJ_RED if percentile >= 70 else '#ffc107' if percentile >= 40 else '#6c757d'
            traits_html += f"""
                <div class="trait-item">
                    <div class="trait-name">{trait.replace('_', ' ').title()}</div>
                    <div class="trait-bar">
                        <div class="trait-fill" style="width: {percentile}%; background: {color};"></div>
                    </div>
                    <div class="trait-score">{percentile:.0f}%</div>
                </div>
            """
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>LJHPP Assessment Results</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-weight: 400;
            line-height: 1.6;
            background: {LJ_LIGHT_GRAY};
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }}
        
        .header {{
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-weight: 600;
            font-size: 2.5em;
            letter-spacing: -0.02em;
        }}
        
        .container {{ 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 30px; 
        }}
        
        .result-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid {LJ_RED};
        }}
        
        .result-section h3 {{
            font-weight: 600;
            color: {LJ_DARK};
            margin-bottom: 20px;
            font-size: 1.4em;
        }}
        
        .personality-type {{
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, {LJ_RED} 0%, {LJ_ACCENT} 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 30px;
        }}
        
        .personality-type h2 {{
            font-size: 2.5em;
            margin-bottom: 15px;
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        
        .traits-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            margin: 25px 0;
        }}
        
        .trait-item {{
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px;
            background: {LJ_LIGHT_GRAY};
            border-radius: 10px;
        }}
        
        .trait-name {{
            min-width: 120px;
            font-weight: 600;
            color: {LJ_DARK};
        }}
        
        .trait-bar {{
            flex: 1;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .trait-fill {{
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
        }}
        
        .trait-score {{
            min-width: 50px;
            font-weight: 600;
            color: {LJ_DARK};
        }}
        
        .roles-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin: 25px 0;
        }}
        
        .role-item {{
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px;
            background: {LJ_LIGHT_GRAY};
            border-radius: 10px;
            border-left: 4px solid {LJ_RED};
        }}
        
        .role-rank {{
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 18px;
        }}
        
        .role-info {{ 
            flex: 1; 
        }}
        
        .role-name {{
            font-weight: 600;
            color: {LJ_DARK};
            font-size: 18px;
            margin-bottom: 5px;
        }}
        
        .role-score {{
            color: {LJ_GRAY};
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 500;
        }}
        
        .role-bar {{
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .role-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        
        .btn {{
            background: {LJ_RED};
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            transition: all 0.3s ease;
            font-family: inherit;
            font-weight: 500;
        }}
        
        .btn:hover {{ 
            background: #c41e22; 
            transform: translateY(-2px);
        }}
        
        .actions {{ 
            text-align: center; 
            margin-top: 40px; 
        }}
        
        ul {{ 
            padding-left: 25px; 
        }}
        
        li {{ 
            margin: 8px 0; 
            color: {LJ_DARK}; 
            font-weight: 400;
        }}
        
        .management-style {{
            background: linear-gradient(135deg, {LJ_LIGHT_GRAY} 0%, #e9ecef 100%);
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
        
        .disclaimer {{
            background: #fff3cd;
            color: #856404;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
            font-size: 14px;
            font-weight: 400;
        }}
        
        .disclaimer strong {{
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎉 Assessment Complete!</h1>
        <p>Comprehensive Results for {html.escape(candidate['name'])}</p>
    </div>
    
    <div class="container">
        <div class="personality-type">
            <h2>{html.escape(profile['personality_type'])}</h2>
            <p style="font-size: 1.2em; opacity: 0.9;">Your primary professional profile</p>
        </div>
        
        <div class="result-section">
            <h3>🎯 Best Real Estate Role Matches</h3>
            <div class="roles-grid">
                {roles_html}
            </div>
        </div>
        
        <div class="result-section">
            <h3>📊 Personality Trait Analysis</h3>
            <div class="traits-grid">
                {traits_html}
            </div>
        </div>
        
        <div class="result-section">
            <h3>💪 Key Strengths</h3>
            <ul>
                {strengths_html if strengths_html else '<li>Well-rounded professional capabilities</li>'}
            </ul>
        </div>
        
        <div class="result-section">
            <h3>📈 Development Opportunities</h3>
            <ul>
                {development_html if development_html else '<li>Continue building on existing strengths</li>'}
            </ul>
        </div>
        
        <div class="result-section">
            <h3>👥 Recommended Management Style</h3>
            <div class="management-style">
                <p>{html.escape(profile['management_style']) if profile['management_style'] else 'Flexible management approach based on individual strengths and development areas.'}</p>
            </div>
        </div>
        
        <div class="disclaimer">
            <strong>📋 Assessment Disclaimer:</strong> This assessment provides indicative personality insights for recruitment screening purposes. Results are not clinical evaluations and should be used alongside other selection criteria. Individual performance may vary regardless of assessment results.
        </div>
        
        <div class="actions">
            <a href="/" class="btn">🏠 Home</a>
            <a href="/assessment" class="btn">🔄 Take Again</a>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def handle_admin_login(self, post_data):
        """Handle admin login"""
        try:
            data = parse_qs(post_data)
            email = data.get('email', [''])[0]
            password = data.get('password', [''])[0]
            
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                self.serve_dashboard()
            else:
                self.send_response(302)
                self.send_header('Location', '/admin?error=1')
                self.end_headers()
                
        except Exception as e:
            print(f"Admin login error: {e}")
            self.send_error(500)
    
    def serve_dashboard(self):
        """Serve comprehensive admin dashboard with optimized fonts"""
        try:
            # Generate statistics
            today = datetime.now().strftime('%Y-%m-%d')
            today_count = len([c for c in candidates_data if c['timestamp'][:10] == today])
            this_month = datetime.now().strftime('%Y-%m')
            month_count = len([c for c in candidates_data if c['timestamp'][:7] == this_month])
            
            # Generate recent candidates table
            candidates_html = ""
            for candidate in candidates_data[-15:]:  # Show last 15
                # Find corresponding result
                result = next((r for r in results_data if r['candidate_id'] == candidate['id']), None)
                personality_type = result['profile']['personality_type'] if result else 'N/A'
                top_role = result['profile']['top_roles'][0][0] if result and result['profile']['top_roles'] else 'N/A'
                
                candidates_html += f"""
                    <tr>
                        <td>{html.escape(candidate['name'])}</td>
                        <td>{html.escape(candidate['email'])}</td>
                        <td>{html.escape(candidate['position'])}</td>
                        <td>{html.escape(personality_type)}</td>
                        <td>{html.escape(top_role)}</td>
                        <td>{candidate['timestamp'][:10]}</td>
                    </tr>
                """
            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>LJHPP Admin Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            font-weight: 400;
            line-height: 1.6;
            background: {LJ_LIGHT_GRAY};
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            text-rendering: optimizeLegibility;
        }}
        
        .header {{
            background: linear-gradient(135deg, {LJ_DARK} 0%, {LJ_RED} 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-weight: 600;
            font-size: 2.2em;
            letter-spacing: -0.02em;
        }}
        
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 30px; 
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 4px solid {LJ_RED};
        }}
        
        .stat-number {{
            font-size: 48px;
            font-weight: 700;
            color: {LJ_RED};
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: {LJ_GRAY};
            font-size: 16px;
            font-weight: 500;
        }}
        
        .candidates-section {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .section-header {{
            background: {LJ_DARK};
            color: white;
            padding: 25px;
            font-size: 20px;
            font-weight: 600;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: {LJ_LIGHT_GRAY};
            color: {LJ_DARK};
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
            font-size: 14px;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            color: {LJ_DARK};
            font-size: 14px;
            font-weight: 400;
        }}
        
        tr:hover {{ 
            background: {LJ_LIGHT_GRAY}; 
        }}
        
        .btn {{
            background: {LJ_RED};
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            transition: all 0.3s ease;
            font-family: inherit;
            font-weight: 500;
        }}
        
        .btn:hover {{ 
            background: #c41e22; 
            transform: translateY(-2px);
        }}
        
        .btn-secondary {{ 
            background: {LJ_DARK}; 
        }}
        
        .btn-secondary:hover {{ 
            background: #333; 
        }}
        
        .actions {{ 
            text-align: center; 
            margin-top: 30px; 
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px;
            color: {LJ_GRAY};
        }}
        
        .empty-state-icon {{ 
            font-size: 48px; 
            margin-bottom: 20px; 
        }}
        
        .empty-state h3 {{
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .cloud-badge {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 600;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 LJHPP Admin Dashboard <span class="cloud-badge">☁️ RAILWAY</span></h1>
        <p>Assessment Management & Analytics</p>
    </div>
    
    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(candidates_data)}</div>
                <div class="stat-label">Total Candidates</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(results_data)}</div>
                <div class="stat-label">Completed Assessments</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{today_count}</div>
                <div class="stat-label">Today's Assessments</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{month_count}</div>
                <div class="stat-label">This Month</div>
            </div>
        </div>
        
        <div class="candidates-section">
            <div class="section-header">📋 Recent Assessment Results</div>
            {f'''
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Position</th>
                        <th>Personality Type</th>
                        <th>Best Role Match</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {candidates_html}
                </tbody>
            </table>
            ''' if candidates_data else '''
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <h3>No assessments completed yet</h3>
                <p>Assessment results will appear here after candidates complete the evaluation</p>
            </div>
            '''}
        </div>
        
        <div class="actions">
            <a href="/" class="btn">🏠 Home</a>
            <a href="/export" class="btn btn-secondary">📥 Export CSV</a>
            <a href="/assessment" class="btn btn-secondary">🧪 Test Assessment</a>
        </div>
    </div>
</body>
</html>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            print(f"Dashboard error: {e}")
            self.send_error(500)
    
    def export_csv(self):
        """Export candidate data as CSV"""
        try:
            # Create CSV content
            csv_content = "Name,Email,Position,Personality Type,Leadership,Analytical,Social,Detail,Adaptability,Service,Top Role,Role Fit %,Second Role,Third Role,Date\n"
            
            for candidate in candidates_data:
                result = next((r for r in results_data if r['candidate_id'] == candidate['id']), None)
                if result:
                    scores = result['scores']
                    profile = result['profile']
                    top_roles = profile['top_roles']
                    
                    role1 = top_roles[0] if len(top_roles) > 0 else ('N/A', 0)
                    role2 = top_roles[1] if len(top_roles) > 1 else ('N/A', 0)
                    role3 = top_roles[2] if len(top_roles) > 2 else ('N/A', 0)
                    
                    csv_content += f'"{candidate["name"]}","{candidate["email"]}","{candidate["position"]}","{profile["personality_type"]}",{scores["leadership"]},{scores["analytical"]},{scores["social"]},{scores["detail"]},{scores["adaptability"]},{scores["service"]},"{role1[0]}",{role1[1]:.1f},"{role2[0]}","{role3[0]}",{candidate["timestamp"][:10]}\n'
            
            self.send_response(200)
            self.send_header('Content-type', 'text/csv; charset=utf-8')
            self.send_header('Content-Disposition', f'attachment; filename="ljhpp_assessments_{datetime.now().strftime("%Y%m%d")}.csv"')
            self.end_headers()
            self.wfile.write(csv_content.encode('utf-8'))
            
        except Exception as e:
            print(f"CSV export error: {e}")
            self.send_error(500)

def start_server():
    """Start the assessment server for cloud deployment"""
    try:
        print(f"""
🚀 LJHPP Assessment Platform - Railway Edition
==========================================

🔧 System Check:
   ✅ Python {sys.version.split()[0]}
   ✅ 100 Questions Loaded & Randomized (Entry-Level Friendly)
   ✅ Cloud Storage Ready
   ✅ LJ Hooker Branding Applied
   ✅ Real Estate Role Matching Active
   ✅ Font Optimization Applied
   ✅ Security Enhanced

🌐 Server Configuration:
   📍 Port: {PORT}
   🔐 Admin: Secure Login Required

🛑 Starting server...
==========================================
        """)
        
        # Start server
        server = HTTPServer(('0.0.0.0', PORT), LJHPPHandler)
        print("🟢 Railway server started successfully!")
        server.serve_forever()
        
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == '__main__':
    print("🏢 LJ Hooker Property Partners")
    print("🎯 Professional Assessment Platform")
    print("☁️ Railway Deployment Version - Optimized for New Candidates")
    print("=" * 50)
    start_server()
