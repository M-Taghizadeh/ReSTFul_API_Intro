from flask import Flask, request, jsonify # for working with json files in flask we can use jsonify 
import requests
from flask import url_for

app = Flask(__name__)

products = ["Phone", "Mobile", "Computer", "Laptop"] # Suppose our MODEL is a list

# -------------------------------------------------------------------
# CRUD in ReST : each one of our view do one of this operation:
# Create:POST, Read:GET, Update:PUT/PATCH, Delete:Delete

# -------------------------------------------------------------------
# 1:[GET] 
# 1.1: Get all model data
@app.route("/", methods=["GET"])
def get_products():
    # return jsonify(products) # jsonify for return your response as json file
    return {"products" : products}, 200 # {} is new feature in flask version 1.1.1 for return json object as return value :)

# 1.2: GET some of model data
@app.route("/<int:index>", methods=["GET"])
def get_product(index):
    try:
        return products[index], 200
    except IndexError:
        return {}, 404

# -------------------------------------------------------------------
# 2:[POST] 
@app.route('/', methods=['POST'])
def create_product():
    arg = request.get_json() # get json data that post to route
    if arg.get('name'):
        products.append(arg['name'])
        return {}, 201
    return {}

# -------------------------------------------------------------------
# 3:[PUST/PATCH] 
# patch : Part of the data changes
# put   : All data changes
@app.route("/<int:index>", methods=["PUT"])
def modify_product(index):
    arg = request.get_json() # get json data that post to route
    if arg.get('name'):
        try:
            products[index] = arg["name"]
            return {}, 204
        except IndexError:
            return {}, 404
    return {}, 400

# 4:[DELETE] -------------------------------------------------------------------
@app.route("/<int:index>", methods=["DELETE"])
def delete_product(index):
    try:
        del products[index]
        return {}, 204
    except IndexError:
        return {}, 404
            
# -------------------------------------------------------------------
# [Send with Requests]
# we can use 'curl' in linux but in python we can use requests library (>>> pip install requests)
# -------------------------------------------------------------------
# 1 : requests.post()
@app.route("/post-request/", methods=["GET"])
def post_request():
    product = request.args.get("product")
    requests.post(url_for('create_product', _external=True), json={"name" : product})
    return f'request sent successfuly and "{product}" added.'
# request exmp : http://127.0.0.1:5000/post-request/?product=Computer

# -------------------------------------------------------------------
# 2 : requests.put()
@app.route("/put-request/", methods=["GET"])
def put_request():
    index = request.args.get("index")
    product = request.args.get("product")
    requests.put(url_for('modify_product', index=index, _external=True), json={"name" : product})
    return f'request sent successfuly and "{product}" can be updated with any index that you want.'
# request exmp: http://127.0.0.1:5000/put-request/?index=3&product=Computer

# -------------------------------------------------------------------
# 3 : requests.delete()
@app.route("/delete-request/", methods=["GET"])
def delete_request():
    index = int(request.args.get("index"))
    requests.delete(url_for('delete_product', index=index, _external=True))
    return f'delete index of "{index}" from list was successfuly.'
# request exmp: http://127.0.0.1:5000/delete-request/?index=2

# -------------------------------------------------------------------
# [RESPONSE STATUS CODE]:
# 201 : new data added
# 200 : response ok
# 404 : page not found
# 204 : when we use modify mode(delete put patch) thats mean that changes have been applied
# 400 : bad request
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# [Read this]
# ReST API: Representational state transfer that use json
# Backend <= Frontend <= User
# -------------------------------------------------------------------

# Representational state transfer (REST) is a software architectural
# style that defines a set of constraints to be used for creating Web
# services. Web services that conform to the REST architectural style,
# called RESTful Web services, provide interoperability between computer
# systems on the Internet. RESTful Web services allow the requesting systems
# to access and manipulate textual representations of Web resources by using
# a uniform and predefined set of stateless operations. Other kinds of Web
# services, such as SOAP Web services, expose their own arbitrary sets of operations.[1]

# "Web resources" were first defined on the World Wide Web as documents or
# files identified by their URLs. However, today they have a much more
# generic and abstract definition that encompasses every thing or entity
# that can be identified, named, addressed, or handled, in any way whatsoever,
# on the Web. In a RESTful Web service, requests made to a resource's URI
# will elicit a response with a payload formatted in HTML, XML, JSON, or
# some other format. The response can confirm that some alteration has been
# made to the stored resource, and the response can provide hypertext links
# to other related resources or collections of resources. When HTTP is used,
# as is most common, the operations (HTTP methods) available are GET, HEAD,
# POST, PUT, PATCH, DELETE, CONNECT, OPTIONS and TRACE.[2]

# By using a stateless protocol and standard operations, RESTful systems
# aim for fast performance, reliability, and the ability to grow by reusing
# components that can be managed and updated without affecting the system
# as a whole, even while it is running.

# The term representational state transfer was introduced and defined in 2000
# by Roy Fielding in his doctoral dissertation.[3][4] Fielding's dissertation
# explained the REST principles that were known as the "HTTP object model"
# beginning in 1994, and were used in designing the HTTP 1.1 and Uniform Resource
# Identifiers (URI) standards.[5][6] The term is intended to evoke an image of how 
# a well-designed Web application behaves: it is a network of Web resources
# (a virtual state-machine) where the user progresses through the application by
# selecting resource identifiers such as http://www.example.com/articles/21
# and resource operations such as GET or POST (application state transitions),
# resulting in the next resource's representation (the next application state)
# being transferred to the end user for their use.

# https://en.wikipedia.org/wiki/Representational_state_transfer


