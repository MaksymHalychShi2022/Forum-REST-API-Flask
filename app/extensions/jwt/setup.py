from flask import jsonify


def set_jwt_callbacks(jwt):
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        response = jsonify({"message": "The token has expired"})
        response.status_code = 401
        return response

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        response = jsonify({"message": "Signature verification failed"})
        response.status_code = 401
        return response

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        response = jsonify({"message": "Request does not contain an access token"})
        response.status_code = 401
        return response
