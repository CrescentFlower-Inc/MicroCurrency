from sqlmodel import select
from microcurrency.core.db import create_db_and_tables, get_session
from microcurrency.core.models import Currency

create_db_and_tables()
session = get_session()

def create_curr():
    shortname = input("Short name: ")
    fullname = input("Full name: ")
    symbol = input("Symbol: ")
    managers = input("Managers (seperated with ','): ")

    currency = Currency(shortname, fullname, symbol, managers)
    session.add(currency)
    session.commit()
    session.refresh(currency)

    print(f"Added currency, it has id: {currency.id}!")

def create_transaction():
    cid = int(input("Enter in currency ID: "))

    statement = select(Currency).where(Currency.id==cid)
    currency: Currency = session.exec(statement).fetchall()[0]

    sender = int(input("Sender (use 0 for infinite money): "))
    receiver = int(input("Receiver: "))
    amount = float(input("Amount: "))

    success, data = currency.create_transaction(session, receiver, sender, amount)
    if success:
        print("Created transaction succesfully")
        print(f"Transaction ID: {data.id}")
    else:
        print("Failed to make transaction")
        print(f"Reason: {data}")