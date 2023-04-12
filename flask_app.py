"""
file: twilio_msg.py
description: Driver code for twilio messaging service & AI connections
language: python3
author: Aravind
"""

from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import openai
import re


openai.api_key = ""  # supply your API key however you choose

SECRET_KEY = 'xzAMtIhuCZsiNIw3NuxAVDCbsI9VDfyy'
app = Flask(__name__)
app.config.from_object(__name__)


# Test route
@app.route('/')
def index():
    return 'Web App with Python Flask! Reloaded !!'


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Body
    # data = request.get_json()
    # body = data['Body']
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()
    choice = body.split(" ", 1)[0].lower()
    if choice == "about":
        resp.message(
            "You have reached MedText, a SMS-based application"
            "for providing AI input on your medical symptoms")
        return str(resp)

    # Open-AI connection
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": body}])
    response = completion.choices[0].message.content
    response = re.sub("As an AI language model, ", "", response)
    resp.message(response)
    xml_response = resp
    print(xml_response)
    return Response(str(xml_response), mimetype="application/xml")


if __name__ == "__main__":
    app.run(debug=True, port=6000)
