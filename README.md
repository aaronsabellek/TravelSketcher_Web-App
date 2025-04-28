# **TravelSketcher - Web Application**

This is a web application that allows users to create, save, and manage travel destinations and their associated activities. Users can register, log in, and add and edit their own travel destinations and activities. Additionally, they can edit their profile and delete it if needed.

## **Technologies**
- **Backend:** Python, Flask, SQLite (for development), PostgreSQL (for production)
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Testing:** Pytest (Backend), Parametrized tests for the frontend are still to be implemented

## **Installation**

### **Backend Setup**

1. **Install Backend Dependencies:**
   - Ensure you have Python and `pip` installed on your system.
   - Install the dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Environment Variables:**
   - Set up environment variables in a `.env` file. Example:
     ```env
     FLASK_ENV=development
     SECRET_KEY=your_secret_key
     DATABASE_URI_DEV=sqlite:///database.db
     DATABASE_URI_Prod=postgresql://your_db_user:your_db_password@localhost/your_db_name
     MAINTENANCE_MODE=False
     MAINTENANCE_MESSAGE="This Website is currently in Maintenance mode. Please try again later."
     MAIL_SERVER=localhost
     MAIL_PORT=1025
     MAIL_USE_TLS=False
     MAIL_USE_SSL=False
     MAIL_USERNAME=None
     MAIL_PASSWORD=None
     MAIL_DEFAULT_SENDER=you_mail_adress
     UNSPLASH_ACCESS_KEY=your_unsplash_api_key
     ```

3. **Setup Database (for Development):**
   - The database is set to SQLite by default for development. For production, you can switch to PostgreSQL.
   - To load dummy data (only for development):
     ```bash
     python scripts/setup_dev_db.py
     ```

4. **Run the Backend Server:**
   - To start the Flask server:
     ```bash
     python run.py
     ```

5. **Run Tests:**
   - All backend tests are written using Pytest. To run the tests, use:
     ```bash
     pytest
     ```

   - You can also run specific test files, e.g.:
     ```bash
     pytest tests/test_routes/test_destination_routes.py
     ```

### **Frontend Setup**

1. **Install Frontend Dependencies:**
   - Make sure you have Node.js and npm/yarn installed on your system.
   - Install the dependencies:
     ```bash
     npm install
     ```

2. **Set Environment Variables:**
   - Create a `.env.local` file in the root directory and set the following variables:
     ```env
     NEXT_PUBLIC_API_BASE_URL=https://your_backend_url
     NEXT_PUBLIC_UNSPLASH_API_KEY=your_unsplash_api_key
     ```

3. **Start the Frontend Server:**
   - To run the frontend in development mode:
     ```bash
     npm run dev
     ```

4. **Run Tests:**
   - Parametrized tests for the frontend are yet to be implemented. Currently, it's recommended to manually test the application to ensure everything works as expected. Once the tests are added, this README will be updated.

## **Folder Structure**

### **Backend (Flask)**
- `/app` - Contains the core application code
  - `/helpers` - Helper functions
  - `/routes` - All Flask API routes
  - `config.py` - Configuration files
  - `errors.py` - Error handling
  - `models.py` - Database models
- `/scripts` - Helper script `setup_dev_db.py` for loading dummy data
- `/tests` - Pytest files and helpers for the backend
- `run.py` - Entry point to run the Flask server

### **Frontend (Next.js)**
- `/src` - Source code for the frontend
  - `/components` - Reusable components
  - `/contexts` - State and context management
  - `/hooks` - Custom hooks
  - `/pages` - Page components
  - `/services` - Services for API interaction
  - `/styles` - Tailwind CSS styles
  - `/types` - TypeScript type definitions
  - `/utils` - Utility functions
- `/public` - Static files (images, etc.)

## **Usage**

### **Main Features of the Application:**
- **User Registration and Login:** Users can register, confirm their email, and log in.
- **Destinations and Activities:** Users can create and manage travel destinations. Activities can be can also be added to each destination and can be edited.
- **Profile Management:** Users can edit their profile data and delete their account (password confirmation required).

## **Error Handling and Logging**
- The backend uses `logging` for error tracking.
- Error codes and messages are properly handled in the frontend and shown to the user.

## **License**

The code in this project is licensed under the MIT License.

```text
MIT License

Copyright (c) 2025 Aaron Sabellek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```