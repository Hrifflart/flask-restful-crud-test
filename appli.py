from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


#--------------------------------------------------------------------------


app = Flask(__name__)
api = Api(app)


#--------------------------------------------------------------------------


#Initialisation d'une liste
list = {
}


#--------------------------------------------------------------------------


def abort_if_p_doesnt_exist(n): #Si p n'existe pas dans la liste alors on affiche le msg d'erreur
    if n not in list:
        abort(404, message="p n'existe pas".format(n))

def abort_if_p_exist(n): #Si p existe dans la liste alors on affiche le msg d'erreur
    if n in list:
        abort(404, message="p existe deja".format(n))

#---------------------------------------------

parser = reqparse.RequestParser()
parser.add_argument('task')

#---------------------------------------------

class P(Resource):
    def get(self, n): #prendre la valeur, vérifier si elle existe bien, si elle existe on l'affiche
        abort_if_p_doesnt_exist(n)
        return list[n]

    def delete(self, n): #prendre la valeur, vérifier si elle existe bien, si elle existe on l'a supprime
        abort_if_p_doesnt_exist(n)
        del list[n]
        return '', 204

    def put(self, n): #prendre la valeur, vérifier si elle existe bien, si elle existe on l'a met à jour
        if n not in list:
            abort_if_p_doesnt_exist(n)
        else:
            args = parser.parse_args()
            task = {'task': args['task']}
            list[n] = task
            return task, 201

    def post(self, n): #prendre la valeur, vérifier si elle n'existe pas, si elle n'existe pas on l'a crée
        if n in list:
            abort_if_p_exist(n)
        else:
            args = parser.parse_args()
            task = {'task': args['task']}
            list[n] = task
            return task, 201

#---------------------------------------------

class nl(Resource):
    def get(self): #prendre la valeur et l'afficher
        return list

#--------------------------------------------------------------------------


api.add_resource(nl, '/list') #Permet l'envoie à la class nl
api.add_resource(P, '/list/<n>') #Permet l'envoie à la class p


#--------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)