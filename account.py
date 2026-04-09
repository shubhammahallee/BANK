from bank.db import get_connection, DB_FILE
from bank.auth import verify_otp

class BankAccount:
    def __init__(self, user_data):
        self.id           = user_data[0]
        self.name         = user_data[1]
        self.acc_num      = user_data[2]
        self.branch       = user_data[3]
        self.ifsc_code    = user_data[4]
        self.mobile       = user_data[5]
        self.__balance    = user_data[8]
        self.credit_count = user_data[9]
        self.debit_count  = user_data[10]

    def __save(self):
        conn = get_connection()
        c    = conn.cursor()
        c.execute(
            "UPDATE users SET balance=?, credit_count=?, debit_count=? WHERE id=?",
            (self.__balance, self.credit_count, self.debit_count, self.id)
        )
        conn.commit()
        conn.close()

    def check_balance(self):
        print("\n" + "=" * 40)
        print("          ACCOUNT DETAILS")
        print("=" * 40)
        print(f"  Account Holder : {self.name}")
        print(f"  Account Number : {self.acc_num}")
        print(f"  Branch         : {self.branch}")
        print(f"  IFSC Code      : {self.ifsc_code}")
        print(f"  Mobile         : +91-XXXXXX{str(self.mobile)[-4:]}")
        print("-" * 40)
        if self.__balance == 0:
            print("  bhai paise nahi the to acc kyu khola 😄")
        else:
            print(f"  Account Balance: ₹ {self.__balance:,.2f}")
        print("=" * 40)

    def credit(self):
        amount = float(input("  Enter amount to credit: ₹ "))
        self.__balance += amount
        self.credit_count += 1
        self.__save()
        print(f"  ✅ ₹{amount:,.2f} credited! New balance: ₹{self.__balance:,.2f}")

    def debit(self):
        amount = float(input("  Enter amount to debit: ₹ "))
        if amount > self.__balance:
            print("  ❌ Insufficient balance!")
            return
        print(f"  🔐 OTP required to debit ₹{amount:,.2f}")
        if verify_otp(self.mobile):
            self.__balance -= amount
            self.debit_count += 1
            self.__save()
            print(f"  ✅ ₹{amount:,.2f} debited! New balance: ₹{self.__balance:,.2f}")
        else:
            print("  ❌ Transaction cancelled.")

    def saving(self):
        print("\n" + "-" * 40)
        principal = float(input("  Enter deposit amount: ₹ "))
        time_yrs  = float(input("  Enter time (in years): "))
        rate      = 0.08
        amount    = principal * (1 + rate) ** time_yrs
        interest  = amount - principal
        print("-" * 40)
        print("      SAVING ACCOUNT SUMMARY")
        print("-" * 40)
        print(f"  Principal : ₹ {principal:,.2f}")
        print(f"  Time      : {time_yrs} years @ 8% p.a.")
        print(f"  Interest  : ₹ {interest:,.2f}")
        print(f"  Total     : ₹ {amount:,.2f}")
        print("-" * 40)

    def current(self):
        print("\n" + "-" * 40)
        principal = float(input("  Enter deposit amount: ₹ "))
        time_yrs  = float(input("  Enter time (in years): "))
        rate      = 0.05
        amount    = principal * (1 + rate) ** time_yrs
        interest  = amount - principal
        print("-" * 40)
        print("      CURRENT ACCOUNT SUMMARY")
        print("-" * 40)
        print(f"  Principal : ₹ {principal:,.2f}")
        print(f"  Time      : {time_yrs} years @ 5% p.a.")
        print(f"  Interest  : ₹ {interest:,.2f}")
        print(f"  Total     : ₹ {amount:,.2f}")
        print("-" * 40)

    def menu(self):
        while True:
            print("\n" + "=" * 40)
            print("           MAIN MENU")
            print("=" * 40)
            print("  1. Check Balance")
            print("  2. Credit Amount")
            print("  3. Debit Amount        🔐 OTP")
            print("  4. Saving Account Calculator")
            print("  5. Current Account Calculator")
            print("  6. Logout")
            print("=" * 40)
            choice = input("  Enter choice (1-6): ").strip()
            if   choice == "1": self.check_balance()
            elif choice == "2": self.credit()
            elif choice == "3": self.debit()
            elif choice == "4": self.saving()
            elif choice == "5": self.current()
            elif choice == "6":
                print(f"\n  Goodbye, {self.name}! Thank you for banking with us 🙏\n")
                break
            else:
                print("  ⚠️  Invalid choice. Enter 1-6.")
