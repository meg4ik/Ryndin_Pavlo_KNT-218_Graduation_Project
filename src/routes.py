from flask import render_template
from src import api, app

from src.resources.main import Main
from src.resources.register import Register
from src.resources.login import Login, Logout
from src.resources.addgame import AddGame
from src.resources.game import Game
from src.resources.buygame import BuyGame
from src.resources.carts import Carts


#
# Declarations of app routes in type of rest web-architecture
#

# routes
api.add_resource(Main, '/', '/main', strict_slashes=False)
api.add_resource(Register, '/register', strict_slashes=False)
api.add_resource(Login, '/login', strict_slashes=False)
api.add_resource(Logout, '/logout', strict_slashes=False)
api.add_resource(AddGame, '/addgame', strict_slashes=False)
api.add_resource(Game, '/game/<uuid>', strict_slashes=False)
api.add_resource(BuyGame, '/buygame', strict_slashes=False)
api.add_resource(Carts, '/carts', strict_slashes=False)

# handling of 404 page error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

