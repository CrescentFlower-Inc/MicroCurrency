from sqlmodel import Field, Relationship, SQLModel, Session, select

class Currency(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shortname: str = Field(index=True)
    fullname: str = Field(index=True)
    symbol: str = Field()
    managers: str = Field()

    def __init__(self, shortname, fullname, symbol, managers): # TODO: make a base model or something in order to avoid this repetitiveness
        self.shortname = shortname
        self.fullname = fullname
        self.symbol = symbol
        self.managers = managers

    def create_transaction(self, session: Session, receiver: int, sender: int, amount: float):
        if sender == receiver:
            return False, "Can't send funds to self!"
        
        if amount <= 0:
            return False, "Can't send 0 or less funds!"
        bal = self.get_balance(session, sender)

        if amount > bal and not sender == 0: # ID 0 should be reserved for ADMINISTRATOR and partial manager use ONLY!
            return False, "Insufficient funds!"

        transaction = Transaction(sender, receiver, self.id, amount)
        session.add(transaction)
        session.commit()
        session.refresh(transaction)

        return True, transaction
    
    def get_balance(self, session: Session, user: int):
        statement = select(Transaction).where(Transaction.sid==user or Transaction.rid==user)
        history = session.exec(statement)
        amt = 0
        for t in history:
            if t.rid == user:
                amt += t.amount
            else:
                amt -= t.amount
        
        return amt



class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    sid: int = Field() # ID of sender
    rid: int = Field() # ID of receiver
    # currency: Currency = Relationship(back_populates="currency")
    cid: int = Field() # currency ID, TODO: figure out relationships
    amount: float = Field() # amount sent in transaction

    def __init__(self, sid, rid, cid, amount):
        self.sid = sid
        self.rid = rid 
        self.cid = cid 
        self.amount = amount