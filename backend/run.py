from app import create_app

# Create app instance
app = create_app()

# Enable 'debug' in development mode
if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])

