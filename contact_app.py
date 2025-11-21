#!/usr/bin/env python3
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
            New Contact Form Submission:
            
            Name: {form_data['name']}
            Email: {form_data['email']}
            Company: {form_data.get('company', 'Not provided')}
            Service: {form_data['service']}
            Urgency: {form_data['urgency']}
            
            Message:
            {form_data['message']}
            
            ---
            Sent from RF Scanner AI Contact Form
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

@app.route('/contact', methods=['GET'])
def contact_form():
    return render_template('contact.html')

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
        return jsonify({'success': True, 'message': 'Message sent successfully!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to send message. Please try email directly.'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
