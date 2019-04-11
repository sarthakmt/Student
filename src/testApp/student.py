"""This module will serve the api request."""

from config import client
from testApp import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import importlib.machinery as imp
import logging
from logging.handlers import RotatingFileHandler
from testApp import helpers
import pymongo as py

# Import the helpers module
helper_module = imp.SourceFileLoader('*', './testApp/helpers.py').load_module

# Select the database
db = client.studentTracker
# Select the collection
collection = db.applicants


@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Making the message looks good
    #resp = jsonify(message)
    if collection.find().count() > 0:
        # Prepare response if the docs are found
        mess = dumps(collection.find_one())
    #mess = helpers.JSONEncoder().encode(collection.find().count())
    resp = jsonify(mess)
    # Returning the object
    return resp

@app.route("/api/v1/assignmentStatus", methods=['GET'])
def fetch_status():
    """
       Function to fetch the assignment status.
       """
    try:
        # Call the function to get the query params
        query_params = helper_module.parse_query_params(request.query_string)
        # Check if dictionary is not empty
        if query_params:
            print(query_params)
            # Try to convert the value to int
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            # Fetch all the record(s)
            records_fetched = collection.find(query)

            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            #print("show me ",collection.find_one())
            if collection.find().count() > 0:
                # Prepare response if the docs are found
                return dumps(collection.find_one())
            else:
                # Return empty array if no docs are found
                return jsonify([])
    except Exception as e:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "not working", 500

@app.route("/applicant", methods=['POST'])
def fetch_applicant():
    """
       Function to fetch applicants.
       """
    app.logger.info(request.get_json())
    body = ast.literal_eval(json.dumps(request.get_json()))
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        records_fetched = collection.find(body)

        # Prepare the response
        if records_fetched.count() > 0:
            # Prepare the response
            return dumps(records_fetched)
        else:
            # No records are found
            return "", 404

    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/users", methods=['POST'])
def create_user():
    """
       Function to create new users.
       """
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = collection.insert(body)

        # Prepare the response
        if isinstance(record_created, list):
            # Return list of Id of the newly created item
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/users", methods=['GET'])
def fetch_users():
    """
       Function to fetch the users.
       """
    app.logger.info('qs :' + request.query_string.decode("utf-8") )
    try:
        # Call the function to get the query params

        query_params = helper_module.parse_query_params(request.query_string.decode("utf-8"))
        app.logger.info('qp'+query_params)
        # Check if dictionary is not empty
        if query_params:

            # Try to convert the value to int
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}
            app.logger.info('q : ' + query)
            # Fetch all the record(s)
            records_fetched = collection.find(query)
            app.logger.info('records_fetched :' + records_fetched)

            # Check if the records are found
            if records_fetched.count() > 0:
                # Prepare the response
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            # Return all the records as query string parameters are not available
            if collection.find().count > 0:
                # Prepare response if the users are found
                return dumps(collection.find())
            else:
                # Return empty array if no users are found
                return jsonify([])
    except:
        # Error while trying to fetch the resource
        # Add message for debugging purpose
        return "Can not fetch", 500


@app.route("/api/v1/users/<user_id>", methods=['POST'])
def update_user(user_id):
    """
       Function to update the user.
       """
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        # Updating the user
        records_updated = collection.update_one({"id": int(user_id)}, body)

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return "", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/users/<user_id>", methods=['DELETE'])
def remove_user(user_id):
    """
       Function to remove the user.
       """
    try:
        # Delete the user
        delete_user = collection.delete_one({"id": int(user_id)})

        if delete_user.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp

