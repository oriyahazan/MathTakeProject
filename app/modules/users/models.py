from flask import Flask, jsonify 

class User:
    def signup(self, data) :
        user = {
            "name": data["name"],
            "email": data["email"],
            "id": data["id"],
            "role": data["role"],
            "password": data["password"]
        }
        return user

 