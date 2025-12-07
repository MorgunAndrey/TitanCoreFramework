TitanCoreFramework: A FastAPI-based Python backend with layered architecture (Controllers/Views/Models). Features auth, CLI, DB abstraction, queues. Supports Node.js/React frontend. Perfect for robust REST APIs and web apps.

Warning: Before using in production, you must fix security and architecture problems. I don't have time for that yet.

Key Features
CLI Commands

Database Migrations

Authentication

Middleware

React Frontend

Template Engine

Service Layer

titanCoreFramework/
 alembic.ini                    # Database migration configuration (Alembic)

 craft.py                       # CLI utility for project management

 package.json                   # npm/Node.js dependencies configuration

 requirements.txt               # Python project dependencies

 run.py                         # Application entry point

 webpack.config.js              # Frontend build configuration (Webpack)


app/
 main.py                        # Main application initialization file

 Console/
  Kernel.py                  # Console commands kernel

  Commands/
   Command.py             # Base class for all commands

   MakeControllerCommand.py    # Controller generator

   MakeMigrationCommand.py     # Migration generator

   MakeModelCommand.py         # Model generator

   MigrateCommand.py           # Migration executor

   SeedCommand.py              # Database seeder

 Controllers/
  Auth/
   LoginController.py          # User login handler

   RegisterController.py       # User registration handler

   ForgotPasswordController.py # Password recovery handler

   ResetPasswordController.py  # Password reset handler

  Home/
   HomeController.py           # Home page controller

  Main/
   MainController.py           # Main controller

  Test/
   TestController.py           # Testing controller

 Middleware/
  auth.py                  # Authentication middleware

  not_auth.py              # Guest user middleware

 Models/
  User.py                  # User model

  UsersPasswordHistory.py  # User password history model

  UsersPasswordResetToken.py # Password reset tokens model

  Test.py                  # Test model

 Services/
  RequestParser.py         # HTTP request parser

  CsrfService.py           # CSRF protection service

  EmailService.py          # Email sending service

 Views/
  layouts/
   head.html            # Page header layout

   headauth.html        # Auth pages header layout

  auth/
   auth.html            # Base authentication template

  home/
   index.html           # Home page template

  main/
   index.html           # Main template

  test/
   index.html           # Testing template


config/
 app.py                       # Main application settings

 auth.py                      # Authentication configuration

 database.py                  # Database configuration

 mail.py                      # Email service configuration

 route.py                     # Application routing

 security.py                  # Security settings

 services.py                  # Services configuration

 templates.py                 # Template engine settings


database/
 migrations/
  versions/
   20250725_001554_create_users_table.py              # Users table creation

   20250725_003757_users_create_password_reset_tokens_table.py  # Password reset tokens

   20250823_135521_create_users_password_history_table.py       # Password history

   20250826_160506_create_test_table.py              # Test table creation

 seeders/
  database_seeder.py       # Main database seeder


components/
 auth/
  Login.js                 # Login component

  Register.js              # Registration component

  ForgotPassword.js        # Password recovery component

  ResetPassword.js         # Password reset component

  RoutesReact.js           # React routes for auth

  app.js                   # Auth React app initialization

 test/
  Test.js                  # Test component

  RoutesReact.js           # Test routes

  app.js                   # Test app initialization


static/
 css/
  styles.css              # Main styles

  styleauth.css           # Authentication styles

 dist/
  auth.js                 # Compiled auth bundle

  test.js                 # Compiled test bundle

 fonts/
  Manrope/                # Manrope font family

  Roboto/                 # Roboto font family

 img/
  gallery/                # Image gallery

  title-icon.png          # Site favicon

 libs/
  bootstrap/              # Bootstrap CSS framework


storage/
 framework/                  # Framework storage files

 logs/
  app.log                # Application log file


tests/
 utils/
  test_db_connect.py     # Database connection tests

  test_mail.py           # Email service tests
