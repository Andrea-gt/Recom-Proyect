from py2neo import Graph
def db_auth():
    graph = Graph('http://localhost:7474/', auth=('neo4j', 'admin'))
    return graph