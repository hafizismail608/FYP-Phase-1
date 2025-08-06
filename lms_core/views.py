from flask import render_template
from . import translearn_core_bp
 
@translearn_core_bp.route('/translearn')
def translearn_home():
    return 'TransLearn Core Home'