"""
file: twilio_msg.py
description: Driver code for twilio messaging service & AI connections
language: python3
author: Aravind
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai


openai.api_key = "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"  # supply your API key however you choose

SECRET_KEY = 'xzAMtIhuCZsiNIw3NuxAVDCbsI9VDfyy'
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Body
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
    resp.message(response)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True, port=9999)
