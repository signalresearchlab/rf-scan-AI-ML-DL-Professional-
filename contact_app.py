from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

class ContactForm:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = "signalresearchlab@gmail.com"
        # Use environment variables for security
        self.password = os.getenv('EMAIL_PASSWORD', 'your-app-password')
    
    def send_email(self, form_data):
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = f"New Contact: {form_data['service']} - {form_data['name']}"
            
            # Create email body
            body = f"""
            📧 NEW CONTACT FORM SUBMISSION - Signal Research Lab
            
            Contact Details:
            • Name: {form_data['name']}
            • Email: {form_data['email']}
            • Company: {form_data.get('company', 'Not provided')}
            • Service Needed: {form_data['service']}
            • Urgency Level: {form_data['urgency']}
            
            Project Details:
            {form_data['message']}
            
            ---
            🔗 GitHub: https://github.com/signalresearchlab
            📧 Email: signalresearchlab@gmail.com
            🏢 Signal Research Lab
            
            This message was sent from the RF Scanner AI Contact Form
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

@app.route('/')
def contact_form():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact - Signal Research Lab</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 700px; 
                margin: 50px auto; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .header h1 {
                color: #333;
                margin-bottom: 10px;
            }
            .header p {
                color: #666;
                font-size: 16px;
            }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: bold; color: #333; }
            input, textarea, select { 
                width: 100%; 
                padding: 12px; 
                border: 2px solid #e1e1e1; 
                border-radius: 8px; 
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input:focus, textarea:focus, select:focus {
                border-color: #667eea;
                outline: none;
            }
            button { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 15px 40px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 18px;
                font-weight: bold;
                width: 100%;
                transition: transform 0.2s;
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e1e1e1;
                color: #666;
            }
            .footer a {
                color: #667eea;
                text-decoration: none;
            }
            .success {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📧 Contact Signal Research Lab</h1>
                <p>Get in touch with us for RF consulting, custom development, and security services</p>
            </div>
            
            <form method="POST" action="/submit">
                <div class="form-group">
                    <label for="name">Full Name *</label>
                    <input type="text" id="name" name="name" required placeholder="Enter your full name">
                </div>
                
                <div class="form-group">
                    <label for="email">Email Address *</label>
                    <input type="email" id="email" name="email" required placeholder="your.email@example.com">
                </div>
                
                <div class="form-group">
                    <label for="company">Company/Organization</label>
                    <input type="text" id="company" name="company" placeholder="Your company name (optional)">
                </div>
                
                <div class="form-group">
                    <label for="service">Service Needed *</label>
                    <select id="service" name="service" required>
                        <option value="">Select a service...</option>
                        <option value="rf-consulting">RF Consulting & Analysis</option>
                        <option value="custom-development">Custom Software Development</option>
                        <option value="security-audit">Security Vulnerability Assessment</option>
                        <option value="training">Training & Workshops</option>
                        <option value="technical-support">Technical Support</option>
                        <option value="other">Other Services</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="urgency">Urgency Level</label>
                    <select id="urgency" name="urgency">
                        <option value="low">Low - General Inquiry</option>
                        <option value="medium">Medium - Project Planning</option>
                        <option value="high">High - Urgent Issue</option>
                        <option value="critical">Critical - Emergency Response</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="message">Project Details *</label>
                    <textarea id="message" name="message" rows="6" required 
                        placeholder="Please describe your project requirements, timeline, budget, and any specific RF technologies involved..."></textarea>
                </div>
                
                <button type="submit">🚀 Send Message</button>
            </form>
            
            <div class="footer">
                <p>
                    <strong>Signal Research Lab</strong><br>
                    📧 <a href="mailto:signalresearchlab@gmail.com">signalresearchlab@gmail.com</a> | 
                    🔗 <a href="https://github.com/signalresearchlab" target="_blank">GitHub/signalresearchlab</a>
                </p>
                <p style="font-size: 14px; margin-top: 10px;">
                    We typically respond within 24 hours. For urgent matters, please select "High" or "Critical" urgency.
                </p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit_form():
    form_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'company': request.form.get('company', ''),
        'service': request.form['service'],
        'urgency': request.form['urgency'],
        'message': request.form['message']
    }
    
    contact = ContactForm()
    if contact.send_email(form_data):
        return '''
        <div style="max-width: 600px; margin: 100px auto; padding: 40px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center;">
            <div style="color: #28a745; font-size: 80px; margin-bottom: 20px;">✅</div>
            <h2 style="color: #333; margin-bottom: 20px;">Message Sent Successfully!</h2>
            <p style="color: #666; font-size: 18px; margin-bottom: 30px;">
                Thank you for contacting <strong>Signal Research Lab</strong>. We have received your message and will respond within 24 hours.
            </p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>Your Details:</strong></p>
                <p>Name: ''' + form_data['name'] + '''</p>
                <p>Email: ''' + form_data['email'] + '''</p>
                <p>Service: ''' + form_data['service'] + '''</p>
            </div>
            <a href="/" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                ← Back to Contact Form
            </a>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e1e1e1;">
                <p style="color: #666; font-size: 14px;">
                    🔗 <a href="https://github.com/signalresearchlab" style="color: #667eea;">GitHub/signalresearchlab</a> | 
                    📧 <a href="mailto:signalresearchlab@gmail.com" style="color: #667eea;">signalresearchlab@gmail.com</a>
                </p>
            </div>
        </div>
        '''
    else:
        return '''
        <div style="max-width: 600px; margin: 100px auto; padding: 40px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center;">
            <div style="color: #dc3545; font-size: 80px; margin-bottom: 20px;">❌</div>
            <h2 style="color: #333; margin-bottom: 20px;">Message Failed to Send</h2>
            <p style="color: #666; font-size: 18px; margin-bottom: 30px;">
                We encountered an issue sending your message. Please try one of these alternative methods:
            </p>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p>📧 <strong>Email us directly:</strong> <a href="mailto:signalresearchlab@gmail.com">signalresearchlab@gmail.com</a></p>
                <p>🔗 <strong>Visit our GitHub:</strong> <a href="https://github.com/signalresearchlab">github.com/signalresearchlab</a></p>
            </div>
            <a href="/" style="display: inline-block; background: #6c757d; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold;">
                ← Back to Contact Form
            </a>
        </div>
        '''

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')