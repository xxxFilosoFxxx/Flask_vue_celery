import logging
from backend.app import socketio
from backend import app
logging.getLogger().setLevel('DEBUG')
# app.run(debug=True)  # host='0.0.0.0', port=999
socketio.run(app, debug=True)
