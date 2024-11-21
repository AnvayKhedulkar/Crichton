from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Flask app
app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate("crichton-bafe6-firebase-adminsdk-uvjmf-f7cc364f54.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/signup", methods=["POST"])
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400
        email = data["email"]
        password = data["password"]

        # Proceed with Firebase signup
        user = auth.create_user(email=email, password=password)
        user_data = {"email": email, "uid": user.uid}
        db.collection("users").document(user.uid).set(user_data)

        return jsonify({"message": "User created successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/login", methods=["POST"])
def login():
    try:
        # Get user details from request
        data = request.json
        email = data["email"]
        password = data["password"]

        # Authenticate the user using Firebase Auth (no need for manual password check)
        try:
            # Attempt to sign in the user with email and password
            user = auth.get_user_by_email(email)
            # If the user is found, we can verify password using Firebase Admin SDK
            auth.verify_id_token(user.uid)
        except firebase_admin.auth.UserNotFoundError:
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": "Authentication failed: " + str(e)}), 401
        
        # If successful, return the message
        return jsonify({"message": "Login successful!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
