from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from config import ACCESS_EXPIRES
from ..extensions import jwt_redis_blocklist, jwt_manager
from ..auth.models import User
from . import auth_api_bp


basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return email
    
@basic_auth.error_handler
def auth_error(status):
    return jsonify(message = "Wrong data! Access denied!") , status


@auth_api_bp.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    access_token = create_access_token(identity=basic_auth.current_user())
    refresh_token = create_refresh_token(identity=basic_auth.current_user())
    return jsonify(access_token=access_token, refresh_token=refresh_token)

@auth_api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@jwt_manager.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@auth_api_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES[ttype])

    return jsonify(msg=f"{ttype.capitalize()} token successfully revorked")