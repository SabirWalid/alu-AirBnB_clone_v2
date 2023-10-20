#!/usr/bin/python3
"""Starts a flask app
    listens to 0.0.0.0, port 5000

"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def display_states_list():
    """Displays an HTML page with a list of all State objects in DBStorage.
    States are sorted by name.
    """
    states = storage.all("State")
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template("7-states_list.html", states=states)


@app.route('/states/<id>', strict_slashes=False)
def display_cities(id):
    """Displays an HTML page with a list of all City objects in DBStorage.
    Routes to /states/<id>
    """
    state = storage.get("State", id)
    if state:
        cities = state.cities if storage.__class__.__name__ == 'DBStorage' else state.cities()
        sorted_cities = sorted(cities, key=lambda city: city.name)
        return render_template('cities.html', state=state, cities=sorted_cities)
    else:
        return render_template('not_found.html')


@app.teardown_appcontext
def teardown_db(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
