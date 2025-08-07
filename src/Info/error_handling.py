#########################################################################################
#########################################################################################
#############                      ERROR HANDLERS                           #############
#########################################################################################
#########################################################################################


############################################
#######       Handle 404 errors      #######
############################################
@app.errorhandler(404)
def not_found(error):

    return jsonify({
        'success': False,
        'message': 'Resource not found',
        'error': 'The requested resource does not exist'
    }), 404


############################################
#######       Handle 400 errors      #######
############################################
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'message': 'Bad request',
        'error': 'The request could not be understood or was missing required parameters'
    }), 400


############################################
#######       Handle 500 errors      #######
############################################
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'message': 'Internal server error',
        'error': 'An unexpected error occurred on the server'
    }), 500