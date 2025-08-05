# Blog Project: Technical Specification & Architecture

### 1. High-Level Overview

The `blog_project` is a modular and self-contained component, implemented as a Flask Blueprint, that provides a complete set of features for a multi-user blog. It is designed to be seamlessly integrated into a larger Flask application, as demonstrated by its registration within the `create_app` factory in `app.py`.

The architecture emphasizes a clear separation of concerns, with distinct modules for routes and logic (`main.py`), database models (`models.py`), and form definitions (`forms.py`). This modularity makes the project scalable, maintainable, and easy to test.

### 2. Core Architecture & Design Patterns

#### a. Flask Blueprint (`blog_bp`)
The entire functionality of the blog is encapsulated within a single Flask Blueprint named `blog_bp`.

*   **Definition**: The blueprint is defined in `blog_project/main.py`. This file serves as the central hub for the blog's routes and view functions.
blog_bp = Blueprint('blog', __name__, 
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/blog_project/static')
*   **Modularity**: It has its own dedicated `template_folder` and `static_folder`, ensuring its frontend assets are neatly organized and decoupled from the main application or other blueprints.
*   **Integration**: In `app.py`, the blueprint is registered with the main Flask application using a `url_prefix='/blog_project'`. 
from blog_project.main import blog_bp
app.register_blueprint(blog_bp, url_prefix='/blog_project')
This means all routes defined within the blueprint (e.g., `/login`, `/post/1`) are accessible under the prefixed path (e.g., `https://one-main.onrender.com/blog_project/login`).

#### b. Application Factory Pattern (`create_app`)
The main application in `app.py` utilizes the factory pattern. This is a crucial architectural choice that:
*   Avoids global application objects, which can lead to complex circular dependencies.
*   Facilitates the creation of multiple application instances with different configurations, which is essential for testing.
*   Ensures a predictable and controlled initialization sequence: extensions are initialized first, then blueprints are imported and registered.

#### c. Centralized Extension Management (`extensions.py`)
The project uses `/Users/hj/Web Development Projects/1. Main/extensions.py` to instantiate all Flask extension objects (`db`, `login_manager`, `ckeditor`, etc.). These un-configured instances are then imported and initialized within the `create_app` factory. This pattern elegantly solves the problem of circular imports that often arises when models, views, and the app factory all need to access the same extension instance.

### 3. Database and Data Layer

#### a. ORM and Models
*   **Technology**: The project uses **Flask-SQLAlchemy** as its Object-Relational Mapper (ORM) to interact with the database.
*   **Model Definitions**: The database schema is defined in `/Users/hj/Web Development Projects/1. Main/blog_project/models.py` using modern, type-annotated `Mapped` syntax. The core models are:
    *   `User`: Stores user credentials (`email`, hashed `password`, hashed `pin`), personal details (`name`, `badge`, `company`), and a `category` for role-based access control.
    *   `BlogPost`: Represents a blog article with a `title`, `subtitle`, `body`, `date`, and `img_url`.
    *   `Comment`: Represents a user's comment on a post.
*   **Relationships**: The models are linked via SQLAlchemy relationships to create a relational structure:
    *   **User to Posts**: A one-to-many relationship where one `User` can be the author of many `BlogPost`s.
    *   **User to Comments**: A one-to-many relationship where one `User` can write many `Comment`s.
    *   **Post to Comments**: A one-to-many relationship where one `BlogPost` can have many `Comment`s.
    *   **Cascading Deletes**: The relationships are configured with `cascade="all, delete-orphan"`, ensuring that when a user is deleted, all of their associated posts and comments are also automatically deleted from the database.

#### b. Database Migrations
The project is integrated with **Flask-Migrate**, which uses Alembic to handle database schema migrations. This is configured in `app.py` and `migrations/env.py`, allowing for version-controlled, programmatic updates to the database structure as the application's models evolve.

### 4. Authentication and Authorization

#### a. Authentication
*   **Session Management**: **Flask-Login** is used to manage user sessions. It handles logging users in (`login_user`), logging them out (`logout_user`), and providing access to the currently authenticated user object via `current_user`.
*   **User Loader**: The required `@login_manager.user_loader` callback is defined in `app.py`. It tells Flask-Login how to retrieve a `User` object from the database given a user ID stored in the session cookie.
*   **Password Security**: Passwords and PINs are never stored in plaintext. The `werkzeug.security` library is used to create secure hashes (`generate_password_hash`) during registration and to verify them (`check_password_hash`) during login.

#### b. Authorization (Role-Based Access Control)
Access to sensitive actions is controlled by a flexible, custom decorator.
*   **`@roles_required(*required_roles)`**: This decorator, defined in `blog_project/main.py`, provides fine-grained access control. It can be applied to any route to restrict access to users with specific roles (e.g., `@roles_required('executive', 'director')`).
*   **Logic**: The decorator first checks if a user is authenticated. If not, it redirects them to the login page. It then checks if the `current_user.category` is present in the list of `required_roles`. If the user does not have the required role, it aborts the request with a **403 Forbidden** status.

### 5. API Endpoint for External Services

The project includes a stateless API for external authentication, demonstrating a microservice-oriented approach.
*   **Route**: `/api/authenticate_badge_pin` (POST method).
*   **Purpose**: Designed to be called by an external system (e.g., an IVR or another service). It accepts a JSON payload containing a `badge` and `pin`.
*   **Functionality**: It authenticates these credentials against the `User` database by looking up the badge and verifying the hashed PIN. It returns a JSON response indicating success or failure, decoupling the core user database from other systems.

### 6. Data Flow Example: Creating a New Post

1.  **Request**: An authenticated user with an 'executive' role navigates to `/blog_project/new-post`.
2.  **Authorization**: The `@roles_required('executive', 'director')` decorator on the `add_new_post` view function executes. It confirms the user is logged in and their `category` is 'executive', granting access.
3.  **Form Handling**: The `add_new_post` function in `main.py` instantiates a `CreatePostForm` object.
4.  **Rendering**: It renders the `make-post.html` template, passing the form object to it. The template uses WTForms macros to generate the HTML form fields, including a CKEditor rich text area for the post body.
5.  **Submission**: The user fills out the form and submits it, sending a POST request.
6.  **Validation**: `form.validate_on_submit()` is called. This validates the CSRF token and checks that all required fields have been filled according to the validators defined in `forms.py`.
7.  **Database Interaction**: If validation is successful, a new `BlogPost` model object is created. Its `author` is set to `current_user`. The object is added to the database session (`db.session.add()`) and saved (`db.session.commit()`).
8.  **Response**: The user is redirected to the main blog page (`/blog_project/`) to see their newly created post.

This architecture creates a robust, maintainable, and feature-rich blog system that is well-integrated into the main portfolio application while remaining a distinct and organized module. 