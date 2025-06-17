import random
import time

def activate_paynessta(appointment_id, customer_name, mobile, email):
    print(f"📅 Appointment #{appointment_id} scheduled for {customer_name}.")
    print("✅ Step 1: Appointment marked as availed.")
    print(f"📨 Step 2: Sending Paynessta payment link to {mobile} (SMS), {email} (Email), and WhatsApp...")
    
    # Simulate sending delay
    time.sleep(1)
    
    payment_link = f"https://wellnessta.com/paynessta/pay/{random.randint(10000, 99999)}"
    print(f"🔗 Payment link generated: {payment_link}")
    
    # Simulate client action
    time.sleep(2)
    print("💳 Customer is making the payment...")
    
    # Simulate payment success
    time.sleep(1)
    print("✅ Payment received successfully!")
    print(f"📥 Confirmation sent to registered mobile and email for appointment #{appointment_id}.")
    print("💸 Amount will be settled in T+2 days.\n")


# Example usage
activate_paynessta(appointment_id=12345, customer_name="Aisha Sharma", mobile="+91-9876543210", email="aisha@example.com")
# this is the change