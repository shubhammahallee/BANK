from bank.db      import init_db
from bank.auth    import login
from bank.account import BankAccount

def main():
    init_db()
    print("\n" + "=" * 40)
    print("      WELCOME TO UNIVERSAL BANK")
    print("=" * 40)
    user = login()
    if user:
        account = BankAccount(user)
        account.menu()

if __name__ == "__main__":
    main()
