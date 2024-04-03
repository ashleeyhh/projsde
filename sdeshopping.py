from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLite database engine
engine = create_engine('sqlite:///shopping_cart.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

    carts = relationship('Cart', backref='user', lazy='dynamic')

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    cart_items = relationship('CartItem', backref='cart', lazy='dynamic')

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

class ShoppingCart:
    def add_item_to_cart(self, user_id, item_id, quantity=1):
        user = session.query(User).filter_by(id=user_id).first()
        item = session.query(Item).filter_by(id=item_id).first()
        if user and item:
            cart = user.carts.first()  # Assuming a user has only one cart for simplicity
            if not cart:
                cart = Cart(user_id=user_id)
                session.add(cart)
            cart_item = session.query(CartItem).filter_by(cart_id=cart.id, item_id=item_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(cart_id=cart.id, item_id=item.id, quantity=quantity)
                session.add(cart_item)
            session.commit()
            return True
        return False

    def remove_item_from_cart(self, user_id, item_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            cart = user.carts.first()
            if cart:
                cart_item = session.query(CartItem).filter_by(cart_id=cart.id, item_id=item_id).first()
                if cart_item:
                    session.delete(cart_item)
                    session.commit()
                    return True
        return False

    def calculate_cart_total(self, user_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            cart = user.carts.first()
            if cart:
                total = sum(cart_item.item.price * cart_item.quantity for cart_item in cart.cart_items)
                return total
        return 0

# Example usage
shopping_cart = ShoppingCart()

# Adding items to cart
shopping_cart.add_item_to_cart(user_id=1, item_id=1, quantity=2)
shopping_cart.add_item_to_cart(user_id=1, item_id=2, quantity=1)

# Removing item from cart
shopping_cart.remove_item_from_cart(user_id=1, item_id=2)

# Calculating cart total
total_price = shopping_cart.calculate_cart_total(user_id=1)
print(f"Total Price: ${total_price}")

# Close the session
session.close()
