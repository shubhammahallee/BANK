import random
import time
from bank.db import get_connection

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(mobile, otp):
    masked = "XXXXXX" + str(mobile)[-4:]
    print("\n" + "~" * 40)
    print(f"  📱 OTP sent to +91-{masked}")
    print(f"  [DEMO MODE] Your OTP is: {otp}")
    print("~" * 40)

def verify_otp(mobile):
    otp = generate_otp()
    send_otp(mobile, otp)
    expiry   = time.time() + 120
    attempts = 3
    while attempts > 0:
        entered = input("  Enter OTP (6 digits): ").strip()
        if time.time() > expiry:
            print("  ❌ OTP expired.")
            return False
        if entered == otp:
            print("  ✅ OTP verified!")
            return True
        attempts -= 1
        print(f"  ❌ Wrong OTP. {attempts} attempt(s) left.")
    print("  🔒 OTP verification failed.")
    return False

def login():
    conn     = get_connection()
    c        = conn.cursor()
    attempts = 3
    while attempts > 0:
        print("\n" + "-" * 40)
        username = input("  User ID  : ").strip()
        password = input("  Password : ").strip()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            conn.close()
            print(f"\n  👋 Hello, {user[1]}!")
            if verify_otp(user[5]):
                print(f"\n  ✅ Login Successful! Welcome, {user[1]} 🎉")
                return user
            else:
                print("  ❌ Login failed — OTP not verified.")
                return None
        attempts -= 1
        print(f"  ❌ Invalid credentials. {attempts} attempt(s) left.")
    conn.close()
    print("\n  🔒 Account locked. Too many failed attempts.\n")
    return None
