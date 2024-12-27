Installation:
====================================
1>First create virtual env
: python -m venv env
====================================

2>install django
: pip install django
====================================
pip install django
3>database required is:
:pip install psycopg2
====================================
postgressql for this db configuration we need to install adapter to install it user below command:
pip install psycopg2


**Features**
====================================
**Implemented full-text search with PostgreSQL by which users can search recipes based on individual ingredients(main feature).**
**Integrated the shortcut buttons to search recipes based on category.**


**User Authentication**
====================================

Users can register and log in to the portal.

**Create and Manage Blogs**
====================================

Post new Recipe blogs.
Edit and delete Recipe blogs from "Your Recipe" section.

**Dashboard**
====================================
View the total number of Recipe posted by the user.
View the combined total number of Recipe and likes.


**Home Page**
====================================

Browse and read all Recipe.
Filter Recipes by category.
Like and comment on Recipe blog.
users can like Recipe only once.


**Recipe Blog Approval System**
====================================

Overview

This project features a Recipe blog system where users can write and submit blogs. By default, the submitted Recipe blogs are not visible on the website until they are reviewed and approved by an admin. This ensures that only appropriate content is published.

How It Works

User Submission: Users submit Recipe blogs through a user interface.

Flagging: The is_active flag for each new Recipe blog is automatically set to 0.

Admin Review: Admin users access the Django admin interface to review submitted blogs.

Approval: Admin users can approve blogs by setting the is_active flag to 1.

Visibility: Approved Recipe blogs become visible on the website.


[15f0f242-3552-4f43-b049-5c9cda8439ea.webm](https://github.com/user-attachments/assets/57bd1870-cf02-4e7d-8e54-ab8d79445d48)













.
