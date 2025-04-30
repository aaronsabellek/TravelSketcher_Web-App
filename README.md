
# TravelSketcher - Web Application

This is a full-stack web application that allows users to create and manage travel destinations and their associated activities. Users can register, log in, and add and edit their own travel destinations and activities. Additionally, they can edit their profile and delete it if needed.

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
     python scripts/setup_db.py
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
- `/scripts` - Script to setup database with dummy data
- `/tests` - Pytest files
- `wsgi.py` - Backend entry point for production
- `run.py` - Backend entry point for development and testing

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
- **Destinations and Activities:** Create, edit, and reorder destinations and their associated activities.
- **Email Notifications:** Emails for registration, password reset, and email changes.

## Error Handling and Logging

- The backend uses Python's `logging` module for error tracking.
- Error responses are displayed on the frontend.

## Licence

```licence
Copyright (c) 2025 Aaron Sabellek

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial — You may not use the material for commercial purposes.

The full license text is available at:
https://creativecommons.org/licenses/by-nc/4.0/

If you want to use this project commercially, please contact the author for permission.
```

