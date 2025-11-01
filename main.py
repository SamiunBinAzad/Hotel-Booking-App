import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id":str})
df_cards = pd.read_csv("cards.csv", dtype = str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype= str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book_hotel(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel has been available"""
        availability =  df.loc[df["id"] == self.hotel_id , "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object


    def generate_ticket(self):
        content = f"""
        Thanks! Here are your booking data:
        Name : {self.the_customer_name}
        Hotel name : {self.hotel.name}
        """
        return content

    @property
    def the_customer_name(self):
        name = self.customer_name.strip()
        name = name.title()
        return name

    @staticmethod
    def convert(amount):
        return amount * 1.2



class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder , cvc):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_ID = input("Enter ID: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number = "1234")
    if credit_card.validate(expiration = "12/26", holder = "JOHN SMITH", cvc = "123"):
        if credit_card.authenticate(given_password = "mypass"):
            hotel.book_hotel()
            name = input("Enter name: ")
            reservation = ReservationTicket(customer_name = name, hotel_object = hotel)
            reservation.generate_ticket()
            print(reservation.generate_ticket())
        else:
            print("Credit Card authentication failed")
    else:
        print("Invalid Payment")
else:
    print("Hotel is not available")

