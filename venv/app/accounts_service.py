from app.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from app.models import User
from py2neo import Graph, Node, Relationship
from py2neo.matching import *


graph = db_auth()
nodes_matcher = NodeMatcher(graph)

def find_user(email: str):
    user = User.match(graph, f"{email}")
    return user

def create_user(username: str, name: str, age:int, email: str, password: str) -> Optional[User]:
    if find_user(email):
        return None
    user = User()
    user.username = username
    user.name = name
    user.age = age
    user.email = email
    user.hashed_password = hash_text(password)
    graph.create(user)
    return user

def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text

def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)

def login_User(email: str, password: str) -> Optional[User]:
    user = User.match(graph, f"{email}").first()
    if not user:
        print(f"Invalid User - {email}")
        return None
    if not verify_hash(user.hashed_password, password):
        print(f"Invalid Password for {email}")
        return None
    print(f"User {email} passed authentication")
    return user

def get_profile(usr: str) -> Optional[User]:
    # user = User.match(graph, f"{usr}").first()
    user_profile = graph.run(f"MATCH (x:user) WHERE x.email='{usr}' RETURN x.name as name, x.company as company, x.email as email").data()
    return user_profile

def similar_users(usr: str) -> Optional[User]:
   user_profile = graph.run(f"MATCH (x:user) WHERE x.email='{usr}' RETURN x.age as age").data()
   lookup_age = user_profile[0].get('age')
   query = f'''
    MATCH (x:user) 
    WHERE x.age={lookup_age} AND x.email <> '{usr}' 
    RETURN x.username 
   '''
   user_profile = graph.run(query).data()
   similar_name = user_profile[0].get('x.username')
   return similar_name