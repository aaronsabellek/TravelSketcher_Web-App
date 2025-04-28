
# TravelSketcher - Web Application

This is a web application that allows users to create, save, and manage travel destinations and their associated activities. Users can register, log in, and add and edit their own travel destinations and activities. Additionally, they can edit their profile and delete it if needed.

## Technologies

- **Backend:** Python, Flask, SQLite (development), PostgreSQL (production)
- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Testing:** Pytest (backend), MailHog, frontend tests (to be implemented)

## Installation

### Backend Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Create a `.env` file with the following content:
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
   MAIL_DEFAULT_SENDER=your_email_address
   UNSPLASH_ACCESS_KEY=your_unsplash_api_key
   ```

3. **Third-Party Services:**
   - **Mail Server (for Email Functionality):**
     - User registration, password reset, and email change require a running mail server.
     - During development, you can use [MailHog](https://github.com/mailhog/MailHog).
     - Example using Docker:
       ```bash
       docker run -p 1025:1025 -p 8025:8025 mailhog/mailhog
       ```
     - Access the MailHog web interface at `http://localhost:8025`.
     - Make sure MailHog is running before running backend tests.

   - **Unsplash API (for Image Search):**
     - An Unsplash API key is required to retrieve images for travel destinations and activities.
     - Create an account at [Unsplash Developers](https://unsplash.com/developers).
     - Register an application to obtain an **Access Key**.
     - Add this key to your `.env` file as `UNSPLASH_ACCESS_KEY`.

4. **Database Setup:**
   - The default development database uses SQLite. For production, you can switch to PostgreSQL.
   - To populate dummy data for testing:
     ```bash
     python scripts/setup_dev_db.py
     ```

5. **Run the Backend Server:**
   ```bash
   python run.py
   ```

6. **Run Backend Tests:**
   ```bash
   pytest
   ```
   To run a specific test file:
   ```bash
   pytest tests/test_routes/test_destination_routes.py
   ```

### Frontend Setup

1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Environment Variables:**
   Create a `.env.local` file with:
   ```env
   NEXT_PUBLIC_API_BASE_URL=https://your_backend_url
   ```

3. **Run the Frontend Server:**
   ```bash
   npm run dev
   ```

4. **Frontend Testing:**
   - Automated tests for the frontend are not yet implemented.
   - Manual testing is currently recommended.

## Folder Structure

### Backend (Flask)

- `/app` - Core application
  - `/helpers` - Helper functions
  - `/routes` - API routes
  - `config.py` - Configuration
  - `errors.py` - Error handling
  - `models.py` - Database models
- `/scripts` - Script to setup database with dummy data (`setup_dev_db.py`)
- `/tests` - Pytest files
- `run.py` - Backend entry point

### Frontend (Next.js)

- `/src` - Frontend source
  - `/components` - Reusable components
  - `/contexts` - Context and state management
  - `/hooks` - Custom hooks
  - `/pages` - Page components
  - `/services` - API services
  - `/styles` - Styling (Tailwind CSS)
  - `/types` - TypeScript types
  - `/utils` - Utility functions
- `/public` - Static assets

## Features

- **User Management:** Registration, email confirmation, login, profile editing, and account deletion.
- **Destinations and Activities:** Create, update, and manage destinations with associated activities.
- **Email Notifications:** Emails for registration, password reset, and email changes.

## Error Handling and Logging

- The backend uses Python's `logging` module for error tracking.
- Error responses are displayed on the frontend.

## License

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
