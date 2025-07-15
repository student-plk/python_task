import streamlit as st
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from instagrapi import Client as InstaClient

st.set_page_config(page_title="Communication Dashboard", layout="centered")
st.title("📡 Communication Dashboard – By PLK")

st.markdown("---")

# ------------------ SEND SMS ------------------
st.subheader("📩 Send SMS")

with st.form("sms_form"):
    twilio_sid = st.text_input("Twilio SID", type="password")
    twilio_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Twilio Phone Number (with +country code)")
    recipient_number = st.text_input("Recipient Phone Number (with +country code)")
    sms_body = st.text_input("Message Text", value="Hello from Python, I am PLK!")
    sms_submit = st.form_submit_button("Send SMS")

    if sms_submit:
        try:
            client = Client(twilio_sid, twilio_token)
            message = client.messages.create(
                body=sms_body,
                from_=twilio_number,
                to=recipient_number
            )
            st.success(f"✅ SMS sent! SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ SMS Error: {e}")


# ------------------ MAKE CALL ------------------
st.subheader("📞 Make a Call")

with st.form("call_form"):
    call_sid = st.text_input("Twilio SID (Call)", type="password")
    call_token = st.text_input("Twilio Auth Token (Call)", type="password")
    call_from = st.text_input("Twilio Phone Number (Call)")
    call_to = st.text_input("Recipient Phone Number (Call)")
    call_msg = st.text_area("Call Message", value="Hello! This is a Python-Twilio call. Have a great day!")
    call_submit = st.form_submit_button("Make Call")

    if call_submit:
        try:
            call_client = Client(call_sid, call_token)
            twiml = f'<Response><Say>{call_msg}</Say></Response>'
            call = call_client.calls.create(
                to=call_to,
                from_=call_from,
                twiml=twiml
            )
            st.success(f"✅ Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Call Error: {e}")


# ------------------ SEND EMAIL ------------------
st.subheader("📧 Send Email")

with st.form("email_form"):
    sender_email = st.text_input("Your Gmail Address")
    app_password = st.text_input("App Password", type="password")
    receiver_email = st.text_input("Receiver Email")
    subject = st.text_input("Subject", value="Test Email from Python")
    plain_text = st.text_input("Plain Text Message", value="Hi, how are you?")
    html_content = st.text_area("HTML Message", value="<h2>Hello!</h2><p>This is a test email from Streamlit + Python.</p>")
    email_submit = st.form_submit_button("Send Email")

    if email_submit:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email

            msg.attach(MIMEText(plain_text, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Email Error: {e}")


# ------------------ INSTAGRAM POST ------------------
st.subheader("📸 Instagram Auto Post")

with st.form("insta_form"):
    insta_user = st.text_input("Instagram Username")
    insta_pass = st.text_input("Instagram Password", type="password")
    caption = st.text_input("Caption", value="Automated post from Streamlit + Python ❤️")
    uploaded_img = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    insta_submit = st.form_submit_button("Post to Instagram")

    if insta_submit:
        if uploaded_img is None:
            st.warning("⚠️ Please upload an image to post.")
        else:
            try:
                with open("temp_insta_img.jpg", "wb") as f:
                    f.write(uploaded_img.read())

                cl = InstaClient()
                cl.login(insta_user, insta_pass)
                cl.photo_upload("temp_insta_img.jpg", caption)
                st.success("✅ Instagram post uploaded!")
            except Exception as e:
                st.error(f"❌ Instagram Error: {e}")
