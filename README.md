# API for YAMDB

## Project Overview

Project YAMDB collects user reviews on various types of content. The actual content is not stored in the YAMDB platform. Users can leave reviews, ratings, and comments on works such as books, movies, and music.

## Stack

- **Python**: 3.9.13
- **Django**: 3.2
- **Django Rest Framework (DRF)**
- **Authentication**: PyJWT
- **Search & Filtering**: DRF and django-filter
- **Database**: SQLite
- **Testing**: PyTest
- **Code Quality**: Ruff
- **Import Sorting**: isort

## Project Description

YaMDb collects user reviews on works like books, movies, and music. It doesn't host the actual content (you can't watch movies or listen to music here). The works are categorized (e.g., "Books," "Movies," "Music"). For instance, in the "Books" category, you might find works like *Winnie-the-Pooh* and *The Martian Chronicles*. Similarly, in the "Music" category, you might find songs like *Yesterday* by The Beatles or *Suite No. 2* by Bach. Administrators can expand categories (e.g., by adding "Fine Art" or "Jewelry").

Works can also be assigned genres from a predefined list (e.g., "Fairy Tale," "Rock," or "Art House"). Only administrators can add works, categories, and genres. Users can leave text reviews and rate the work on a scale from 1 to 10. The ratings are aggregated to form an overall score (an integer). Each user can leave only one review per work. 

Users can also leave comments on reviews. Only authenticated users can add reviews, comments, and ratings.

## Setup Instructions

### 1. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/RockurDev/api_yamdb
cd api_yamdb
```

### 2. Install and activate the virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Apply the migrations:
```bash
python api_yamdb/manage.py migrate
```

### 5. Run the development server:
```bash
python api_yamdb/manage.py runserver
```

---

### Note for macOS Users:
For full compatibility, use `python3`.

---

## User Registration Process

1. The user sends a `POST` request to `/api/v1/auth/signup/` with `email` and `username` as parameters.
2. YaMDB sends a confirmation code to the user's email.
3. The user sends a `POST` request to `/api/v1/auth/token/` with `username` and the `confirmation_code` to receive a JWT token.
4. If desired, the user can send a `PATCH` request to `/api/v1/users/me/` to update their profile.

## User Roles

- **Anonymous**: Can view descriptions of works, read reviews, and comments.
- **Authenticated User (user)**: Can do everything an Anonymous user can, plus publish reviews, rate works, and comment on reviews. This role is assigned to every new user by default.
- **Moderator**: Same rights as an Authenticated User, plus the ability to delete any review or comment.
- **Administrator (admin)**: Full control over content. Can create and delete works, categories, and genres, and assign roles to users.
- **Django Superuser**: Has administrator privileges.

## API Usage Examples

### Get the list of titles:
Endpoint: `/api/v1/titles/`
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

### Post a review:
Endpoint: `/api/v1/titles/{title_id}/reviews/`
```json
{
  "text": "Review text",
  "score": 1
}
```

### Post a comment on a review:
Endpoint: `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`
```json
{
  "text": "Comment text"
}
```

## Authors

- [RockurDev](https://github.com/RockurDev)
- [Chiken-Kitchen](https://github.com/Chiken-Kitchen)
- [Faitik](https://github.com/Faitik)

## Project Link

[API for YAMDB](https://github.com/RockurDev/api_yamdb)
```