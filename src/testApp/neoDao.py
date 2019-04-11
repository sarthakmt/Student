from py2neo import Graph, Node, Relationship


uri = "bolt://localhost:11001"
user = "user"
password = "password"
graph = Graph(uri, auth=(user, password))