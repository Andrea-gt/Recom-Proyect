from app.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from app.models import User
from py2neo.matching import *


graph = db_auth()
nodes_matcher = NodeMatcher(graph)

def find_user(email: str):
    user = User.match(graph, f"{email}")
    return user

def create_user(username: str, name: str, age:int, gender:str, dpto:str, prof:str, fav:str, colegio:str, email: str, password: str) -> Optional[User]:
    if find_user(email):
        return None
    user = User()
    user.username = username
    user.name = name
    user.age = age
    user.gender = gender.lower().strip().replace(" ", "")
    dpto = dpto.lower().strip().replace(" ", "")
    prof = prof.lower().strip().replace(" ", "")
    fav = fav.lower().strip().replace(" ", "")
    colegio = colegio.lower().strip().replace(" ", "")
    user.email = email
    user.hashed_password = hash_text(password)
    graph.create(user)

    # Departamento
    temp_node = graph.run(f"MATCH (x:depto) WHERE x.nombre='{dpto}' RETURN x.nombre as nombre").data()
    if not temp_node:
        graph.run(f"CREATE ({dpto}:depto {{nombre: '{dpto}'}})") # <--- ojo que esos {} andan chistosos
    graph.run(f"MATCH (a:user), (b:depto) WHERE a.email = '{email}' AND b.nombre = '{dpto}' CREATE (a)-[r:VIVE_EN]->(b)")

    # profesion
    temp_node = graph.run(f"MATCH (x:profesion) WHERE x.nombre='{prof}' RETURN x.nombre as nombre").data()
    if not temp_node:
        graph.run(f"CREATE ({prof}:profesion {{nombre: '{prof}'}})") # <--- ojo que esos {} andan chistosos
    graph.run(f"MATCH (a:user), (b:profesion) WHERE a.email = '{email}' AND b.nombre = '{prof}' CREATE (a)-[r:PROFESION]->(b)")

    # animal favorito :D !
    temp_node = graph.run(f"MATCH (x:animal) WHERE x.nombre='{fav}' RETURN x.nombre as nombre").data()
    if not temp_node:
        graph.run(f"CREATE ({fav}:animal {{nombre: '{fav}'}})") # <--- ojo que esos {} andan chistosos
    graph.run(f"MATCH (a:user), (b:animal) WHERE a.email = '{email}' AND b.nombre = '{fav}' CREATE (a)-[r:ANIMAL_FAVORITO]->(b)")

    # Casa de estudios !!! :D 
    temp_node = graph.run(f"MATCH (x:colegio) WHERE x.nombre='{colegio}' RETURN x.nombre as nombre").data()
    if not temp_node:
        graph.run(f"CREATE ({colegio}:colegio {{nombre: '{colegio}'}})") # <--- ojo que esos {} andan chistosos
    graph.run(f"MATCH (a:user), (b:colegio) WHERE a.email = '{email}' AND b.nombre = '{colegio}' CREATE (a)-[r:ESTUDIO_EN]->(b)")

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
    user_profile = graph.run(f"MATCH (x:user) WHERE x.email='{usr}' RETURN x.name as name, x.email as email").data()
    return user_profile

def similar_users(usr: str) -> Optional[User]:
   user_profile = graph.run(f"MATCH (x:user) WHERE x.email='{usr}' RETURN x.email as email").data()
   lookup_age = user_profile[0].get('email')
   query = f'''
    match (a:user)-[:VIVE_EN|ANIMAL_FAVORITO|PROFESION|ESTUDIO_EN]->()<-[:VIVE_EN|ANIMAL_FAVORITO|PROFESION|ESTUDIO_EN]-(b:user)
    where a.email = "{lookup_age}"
    return b.username as Usuario, b.email as Email, count(*) as Similaridad
    order by Similaridad desc
    limit 10
   '''
   profiles = graph.run(query).data()
   return profiles

def borrar_usuario(email: str):
    graph.run(f"MATCH (n:user) WHERE n.email = '{email}' DETACH DELETE n")