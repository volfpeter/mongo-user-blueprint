"""
Application start-up script.
"""

if __name__ == "__main__":
    from mongo_user_blueprint.app import app
    app.run(debug=True)
