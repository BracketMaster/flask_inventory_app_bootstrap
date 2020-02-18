from flask_sqlalchemy import SQLAlchemy as sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from tables import GameTable, CartTable
import copy
from datetime import datetime

Base = declarative_base()

#database classes
association_table = Table('association', Base.metadata,
    Column('User', Integer, ForeignKey('user.name')),
    Column('Game', Integer, ForeignKey('game.title'))
)

transcations_vs_games = Table('transcations_vs_games', Base.metadata,
    Column('Timestamp', Integer, ForeignKey('transactions.timestamp')),
    Column('Game', Integer, ForeignKey('game.title'))
)

class Transactions(Base):
    __tablename__ = 'transactions'
    timestamp = Column(String(80), primary_key=True)
    user = Column(String(80))
    cost = Column(Integer)
    cart = relationship("Game",secondary=transcations_vs_games)

class User(Base):
    __tablename__ = 'user'
    name = Column(String(80), primary_key=True)
    password = Column(String(80))
    cart = relationship("Game",secondary=association_table)

class Game(Base):
    __tablename__ = 'game'
    #properties
    title = Column(String(80), unique=True, nullable=False, primary_key=True)
    genre = Column(String(80))
    rating = Column(String(80))
    platform = Column(String(80))
    dev = Column(String(80))
    year = Column(Integer)
    price = Column(Integer)

def record_transaction(user,price):
    user = session.query(User).filter(User.name==user).one()
    transaction = Transactions(user=user.name, cost=price)
    transaction.cart = user.cart
    transaction.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    session.add(transaction)
    session.commit()

#init session
from sqlalchemy import create_engine
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "games.db"))
engine = create_engine(database_file)
from sqlalchemy.orm import sessionmaker
session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)

#cart database functions
def add_to_cart_db(user,game):
    user = session.query(User).filter(User.name==user).one()
    game = session.query(Game).filter(Game.title==game).one()
    user.cart.append(game)
    session.commit()

def clear_cart(user):
    user = session.query(User).filter(User.name==user).one()
    user.cart = []
    session.commit()

def delete_from_cart_db(user,game):
    user = session.query(User).filter(User.name==user).one()
    game = session.query(Game).filter(Game.title==game).one()
    user.cart.remove(game)
    session.commit()

def build_user_cart_table(user):
    user = session.query(User).filter(User.name==user).one()
    cart = user.cart
    return CartTable(cart).__html__()

def current_cart_cost(user):
    user = session.query(User).filter(User.name==user).one()
    cart = user.cart
    if cart == []:
        return 0
    return sum([int(item.price) for item in cart])

#game database functions
def add_game(** kwargs):
    game = Game(**kwargs)
    session.add(game)
    session.commit()

def delete_game(title):
    game = session.query(Game).filter_by(title=title).first()
    session.delete(game)
    session.commit()

def game_titles():
    res = [el.title for el in session.query(Game).all()]
    return res

def game_genres():
    res = session.query(Game.genre).distinct()
    genres =  [(el.genre, el.genre) for el in res]
    return genres

def search_game_db(** kwargs):
    my_query = session.query(Game)

    if 'title' in kwargs.keys():
        if kwargs['title']:
            select = f"%{kwargs['title']}%"
            my_query = my_query.filter(Game.title.ilike(select))

    if 'genre' in kwargs.keys():
        if kwargs['genre']:
            my_query = my_query.filter(Game.genre==kwargs['genre'])

    if 'rating' in kwargs.keys():
        if kwargs['rating']:
            select = f"%{kwargs['rating']}%"
            my_query = my_query.filter(Game.rating.ilike(select))

    if 'platform' in kwargs.keys():
        if kwargs['platform']:
            select = f"%{kwargs['platform']}%"
            my_query = my_query.filter(Game.platform.ilike(select))

    if 'dev' in kwargs.keys():
        if kwargs['dev']:
            select = f"%{kwargs['dev']}%"
            my_query = my_query.filter(Game.platform.ilike(select))

    if 'year' in kwargs.keys():
        my_query = my_query.filter(Game.year==kwargs['year'])

    if 'price' in kwargs.keys():
        my_query = my_query.filter(Game.price==kwargs['price'])

    
    #build html table
    my_table = GameTable(my_query)
    return my_table.__html__()

#user database functions
def query_user(name,password):
    res = session.query(User).filter(User.name==name)
    if res.all() == []:
        return False
    res = res.one()
    if (res.name == name) and (res.password == password):
        return True
    else:
        return False

def query_username(name):
    res = session.query(User).filter(User.name==name)
    if res.all() == []:
        return False
    res = res.one()
    if res.name == name:
        return True
    else:
        return False

def add_user(name,password):
    new_user = User(name=name,password=password)
    session.add(new_user)
    session.commit()