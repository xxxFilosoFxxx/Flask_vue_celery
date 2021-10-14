import logging
from backend import app
logging.getLogger().setLevel('DEBUG')
app.run(debug=True)  # host='0.0.0.0', port=9999
