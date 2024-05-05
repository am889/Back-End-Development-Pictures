from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    url={}
    for i in data:
        id = i['id']
        url[id]=i['pic_url']
        # id= i['id']
        # resp = make_response(url)
        # resp.status_code = 200

    return url

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for i in data:
        if i['id'] ==int(id):
            url = i["pic_url"]
            return i

    return ({"message":"id not found"},404)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    picture_id = picture.get('id')  # Get the picture ID from the request
    
    # Check if a picture with the given ID already exists
    for existing_picture in data:
        if existing_picture['id'] == picture_id:
            return jsonify({"Message": f"Picture with id {picture_id} already present"}), 302  
    
    # If picture with the ID doesn't exist, append it to the data list
    data.append(picture)
    
    # Increment the count
    count = len(data)
    
    # Include the 'id' field in the response JSON
    response_data = {"message": f"Picture with id {picture_id} created successfully", "id": picture_id, "count": count}
    
    return jsonify(response_data), 201
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.json  # Extract the picture data from the request body

    # Find the picture in the data list
    for picture in data:
        if picture['id'] == id:
            # Update the picture with the incoming request
            picture.update(picture_data)
            return jsonify({"message": f"Picture with id {id} updated successfully"}), 200

    # If the picture does not exist, send back a status of 404 with a message
    return jsonify({"message": "Picture not found"}), 404    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Traverse the data list to find the picture by id
    for idx, picture in enumerate(data):
        if picture['id'] == id:
            # Delete the item from the list
            del data[idx]
            return '', 204  # Return an empty body with status 204
        
    # If the picture does not exist, return status 404 with a message
    return jsonify({"message": "Picture not found"}), 404 
# @app.route("/picture", methods=["POST"])
# def create_picture(id):
#     picture = request.json
#     picture_id = id  # Get the picture ID from the URL parameter
#     picture['id'] = picture_id  # Add the picture ID to the picture data
    
#     # Check if a picture with the given ID already exists
#     for existing_picture in data:
#         if existing_picture['id'] == picture_id:
#             return jsonify({"Message": f"Picture with id {picture_id} already present"}), 302

#     # If picture with the ID doesn't exist, append it to the data list
#     data.append(picture)
    
#     return jsonify({"message": f"Picture with id {picture_id} created successfully"}), 201