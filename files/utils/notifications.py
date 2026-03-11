import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_HOST    = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT    = int(os.getenv("SMTP_PORT", 587))
SMTP_USER    = os.getenv("SMTP_USER", "")
SMTP_PASS    = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM   = os.getenv("EMAIL_FROM", "hello@crafteonlabs.in")
OWNER_EMAIL  = os.getenv("OWNER_EMAIL", "")

TWILIO_SID   = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM  = os.getenv("TWILIO_WHATSAPP_FROM", "")
OWNER_WA     = os.getenv("OWNER_WHATSAPP", "")


# ── EMAIL ──────────────────────────────────────────────────────

def send_email(to: str, subject: str, html_body: str):
    """Send an HTML email. Fails silently in dev if not configured."""
    if not SMTP_USER or not SMTP_PASS:
        print(f"[EMAIL - not configured] To: {to} | Subject: {subject}")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = EMAIL_FROM
        msg["To"]      = to
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, to, msg.as_string())

        print(f"[EMAIL] Sent to {to}")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")


def notify_owner_new_order(order):
    """Email the owner when a new order comes in."""
    subject = f"🖨️ New Order #{order.id} — {order.category}"
    html = f"""
    <h2>New Order Received — Crafteon Labs</h2>
    <table style="font-family:sans-serif;font-size:14px;border-collapse:collapse;">
      <tr><td><b>Order ID</b></td><td>#{order.id}</td></tr>
      <tr><td><b>Name</b></td><td>{order.full_name}</td></tr>
      <tr><td><b>Phone</b></td><td>{order.phone}</td></tr>
      <tr><td><b>Email</b></td><td>{order.email or '—'}</td></tr>
      <tr><td><b>Category</b></td><td>{order.category}</td></tr>
      <tr><td><b>Budget</b></td><td>{order.budget_range or '—'}</td></tr>
      <tr><td><b>Description</b></td><td>{order.description}</td></tr>
    </table>
    <br>
    <p>Log in to the admin dashboard to manage this order.</p>
    """
    send_email(OWNER_EMAIL, subject, html)


def notify_customer_received(order):
    """Email the customer confirming their order was received."""
    if not order.email:
        return
    subject = "We received your order! — Crafteon Labs"
    html = f"""
    <h2>Thanks, {order.full_name}! 🎉</h2>
    <p>We've received your order request and will get back to you on WhatsApp within <b>24 hours</b>.</p>
    <table style="font-family:sans-serif;font-size:14px;border-collapse:collapse;">
      <tr><td><b>Order ID</b></td><td>#{order.id}</td></tr>
      <tr><td><b>Category</b></td><td>{order.category}</td></tr>
      <tr><td><b>Description</b></td><td>{order.description}</td></tr>
    </table>
    <br>
    <p>— Crafteon Labs, Pune 🖨️</p>
    """
    send_email(order.email, subject, html)


def notify_customer_status_update(order):
    """Email customer when their order status changes."""
    if not order.email:
        return
    subject = f"Order #{order.id} Update — {order.status.title()}"
    html = f"""
    <h2>Order Update — Crafteon Labs</h2>
    <p>Hi {order.full_name}, your order status has been updated.</p>
    <table style="font-family:sans-serif;font-size:14px;">
      <tr><td><b>Order ID</b></td><td>#{order.id}</td></tr>
      <tr><td><b>New Status</b></td><td><b>{order.status.upper()}</b></td></tr>
      {"<tr><td><b>Note from us</b></td><td>" + order.admin_notes + "</td></tr>" if order.admin_notes else ""}
    </table>
    <br>
    <p>— Crafteon Labs, Pune 🖨️</p>
    """
    send_email(order.email, subject, html)


# ── WHATSAPP (Twilio) ──────────────────────────────────────────

def send_whatsapp(to: str, message: str):
    """Send a WhatsApp message via Twilio. Fails silently if not configured."""
    if not TWILIO_SID or not TWILIO_TOKEN:
        print(f"[WHATSAPP - not configured] To: {to} | Msg: {message}")
        return
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(body=message, from_=TWILIO_FROM, to=to)
        print(f"[WHATSAPP] Sent to {to}")
    except Exception as e:
        print(f"[WHATSAPP ERROR] {e}")


def whatsapp_owner_new_order(order):
    """WhatsApp the owner on new order."""
    msg = (
        f"🖨️ *New Order #{order.id} — Crafteon Labs*\n\n"
        f"*Name:* {order.full_name}\n"
        f"*Phone:* {order.phone}\n"
        f"*Category:* {order.category}\n"
        f"*Budget:* {order.budget_range or '—'}\n\n"
        f"*Description:*\n{order.description}"
    )
    send_whatsapp(OWNER_WA, msg)
