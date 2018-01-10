from flask import *
from u2 import *
import json
app = Flask(__name__)
@app.route('/profile', methods=['POST', 'GET'])
def profile():
	if request.method == 'POST':
		return json.dumps(u2_profile(request.form['uid']))