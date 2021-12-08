from flask import render_template
from src import api, app

from src.resources.main import Main
from src.resources.register import Register


#
# Declarations of app routes in type of rest web-architecture
#

# routes
api.add_resource(Main, '/', '/main', strict_slashes=False)
api.add_resource(Register, '/register', strict_slashes=False)

# api.add_resource(Login, '/login', strict_slashes=False)
# api.add_resource(Logout, '/logout', strict_slashes=False)
# api.add_resource(Projects, '/projects', strict_slashes=False)
# api.add_resource(Project, '/project/<uuid>', strict_slashes=False)
# api.add_resource(User, '/user/<uuid>', strict_slashes=False)
# api.add_resource(UserProjectAdd, '/projectadd/<uuid>', strict_slashes=False)
# api.add_resource(Main, '/chats', strict_slashes=False)
# api.add_resource(Main, '/profile', strict_slashes=False)

# handling of 404 page error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

