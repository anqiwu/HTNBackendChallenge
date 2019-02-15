# Hack The North Backend Challenge
A RESTful API server implemented using Flask and SQLite database to store and work with the hackathon participants' data

# Table of Contents

- [Start the Server Locally](#startserverlocally)
	- [Populate database](#populatedb)
	- [Start Server](#startserver)
- [Database Design](#databasedesign)
	- [Tables and Models](#tablesandmodels)
	- [Overview](#overview)
	- [Company](#company)
	- [User](#user)
	- [Skill](#skill)
	- [SkillWithRating](#skillwithrating)
	- [users_skills](#users_skills)
- [API](#api)
    - [Endpoints](#endpoints)
    - [/users](#users)
    - [/users/id](#users/id)
    - [/skills](#skills)

# Start the Server Locally

## Populate database

Run the script `populate_db.py` to populate the SQLite database with data from: https://htn-interviews.firebaseio.com/users.json
The database can be found under `HTN_BackendChallenge/db/data.db`

## Start Server

- start the venv, `source venv/Scripts/activate` from `HTN_Backend_Challenge` directory
- In `HTN_BackendChallenge`, do `export FLASK_APP=app.py`
- `python -m flask run` to start the server locally

# Database Design

## Tables and Models

### Tables

- `companies`
- `users`
- `skills`
- `skills_with_rating`
- `users_skills`, junction table for `users` and `skills_with_rating`

### Models

- `Company` for the `companies` table
- `User` for the `users` table
- `SkillWithRating` for the `skills_with_rating` table
- `Skill` for the `skills` table

## Overview

It is also possible to get rid of `skills_with_rating` table altogether and link the `User` entity with `Skill` entity directly using and associative entity with an extra column for each association between the `user_id` and the `skill_id`...

The relationships between the models are:
- In a `Company`, there can be multiple `User` (1:m)
- A `User` can have multiple `SkillWithRating` and a `SkillWithRating` can have multiple `User` because many users can give the same rating to the same skill. (m:m) This many-to-many relationship is linked by the association entity `users_skills`
- A `Skill` can have multiple `SkillWithRating` (1:m)

## Company

```
class Company(db.Model):  
    __tablename__ = 'companies'  

    company_id = db.Column(db.Integer, primary_key=True)  
    company = db.Column(db.String(255), unique=True)  
    users = db.relationship('User', backref='user', lazy=True)  
```

## User

```
class User(db.Model):  
    __tablename__ = 'users'  

    user_id = db.Column(db.Integer, primary_key=True)  
    email = db.Column(db.String(255), nullable=False, unique=True)  
    name = db.Column(db.String(255), nullable=False)  
    picture = db.Column(db.Text)  
    company = db.Column(db.Integer, db.ForeignKey('companies.company_id'))  
    phone = db.Column(db.String(255))  
    latitude = db.Column(db.Float)  
    longitude = db.Column(db.Float)  

    skills_with_rating = db.relationship("SkillWithRating", secondary=users_skills,  
  lazy="dynamic", backref=db.backref("users", lazy="dynamic"))
```

## Skill

```
class Skill(db.Model):  
    __tablename__ = 'skills'  

    skill_id = db.Column(db.Integer, primary_key=True)  
    skill_name = db.Column(db.String(255), nullable=False, unique=True)  
    skill_with_ratings = db.relationship('SkillWithRating')
```
## SkillWithRating

```
class SkillWithRating(db.Model):  
    __tablename__ = 'skills_with_rating'  

	skill_with_rating_id = db.Column(db.Integer, primary_key=True)  
    skill_name = db.Column(db.String(255), nullable=False)  
    rating = db.Column(db.Integer, nullable=False)  
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'))  

    db.UniqueConstraint('skill_name', 'rating')
```

## users_skills

Association entity betwen `User` and `SkillWithRating`
maps a `user_id` to a `skill_with_rating_id`.

```
users_skills = db.Table('users_skills',  
  db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),  
  db.Column('skill_with_rating_id', db.Integer, db.ForeignKey('skills_with_rating.skill_with_rating_id'), primary_key=True)  
)
```

# API

## Endpoints
- /users
- /users/id
- /skills

## /users

### GET request

Returns a list of all user data from the database in a JSON format.
```JSON
{
  "name": <string>,
  "picture": <string>,
  "company": <string>,
  "email": <string>,
  "phone": <string>,
  "latitude": <float>,
  "longitude": <float>,
  "skills": [
    {
      "name": <string>,
      "rating": <int>
    }
  ]
}
```
EXAMPLE:
```
[
    {
        "company": "Slambda",
        "email": "elizawright@slambda.com",
        "latitude": 48.4862,
        "longitude": -34.7754,
        "name": "Jenna Luna",
        "phone": "+1 (913) 504-2495",
        "picture": "http://lorempixel.com/200/200/sports/8",
        "skills": [
            {
                "name": "JS",
                "rating": 5
            },
            {
                "name": "Go",
                "rating": 5
            }
        ]
    },
    {
        "company": "Veraq",
        "email": "jennaluna@veraq.com",
        "latitude": 48.9743,
        "longitude": -34.1247,
        "name": "Dora Schultz",
        "phone": "+1 (949) 580-2608",
        "picture": "http://lorempixel.com/200/200/sports/0",
        "skills": [
            {
                "name": "C",
                "rating": 7
            },
            {
                "name": "Android",
                "rating": 9
            },
            {
                "name": "Android",
                "rating": 2
            }
        ]
    },
    ...
]
```

## /users/id

### GET request

Return the user data for a specific user, in a json format, same as above

EXAMPLE: `http://localhost:5000/users/23` Returns

```
{
    "company": "Parcoe",
    "email": "montoyagill@parcoe.com",
    "latitude": 49.2812,
    "longitude": -33.8064,
    "name": "Hester Castillo",
    "phone": "+1 (873) 589-2507",
    "picture": "http://lorempixel.com/200/200/sports/8",
    "skills": [
        {
            "name": "iOS",
            "rating": 7
        },
        {
            "name": "NodeJS",
            "rating": 3
        }
    ]
}
```

### PUT request

updates a given user's data by accepting data in a JSON format and returns the updated user data as the response.
- supports partial updating and type checks the values
- if a user has new skills, these skills should be added to the database. Any existing skills should have their ratings updated.

EXAMPLE:
a PUT request with the JSON body below at `http://localhost:5000/users/23`
```
{
    "phone": "123456789",
    "name": "An Qi",
    "skills": [
      {
      	"name": "Awesome new skill",
      	"rating": 4
      }
    ]
}
```
will update user with user_id 23:
```
{
    "company": "Parcoe",
    "email": "montoyagill@parcoe.com",
    "latitude": 49.2812,
    "longitude": -33.8064,
    "name": "Hester Castillo",
    "phone": "+1 (873) 589-2507",
    "picture": "http://lorempixel.com/200/200/sports/8",
    "skills": [
        {
            "name": "iOS",
            "rating": 7
        },
        {
            "name": "NodeJS",
            "rating": 3
        }
    ]
}
```
to
```{
    "company": "Parcoe",
    "email": "montoyagill@parcoe.com",
    "latitude": 49.2812,
    "longitude": -33.8064,
    "name": "An Qi",
    "phone": "123456789",
    "picture": "http://lorempixel.com/200/200/sports/8",
    "skills": [
        {
            "name": "iOS",
            "rating": 7
        },
        {
            "name": "NodeJS",
            "rating": 3
        },
        {
            "name": "Awesome new skill",
            "rating": 4
        }
    ]
}
```

## /skills

### GET request

returns a skill data in JSON format, that can filtered by parameters.
supported params are:
- min_frequency
- min_rating
If no request parameters are specified, default to zero.

EXAMPLE:
`http://localhost:5000/skills` returns
```
[
    {
        "average_rating": 5.76,
        "frequency": 191,
        "name": "JS"
    },
    {
        "average_rating": 5.47,
        "frequency": 179,
        "name": "Go"
    },
    {
        "average_rating": 5.3,
        "frequency": 190,
        "name": "C"
    },
    {
        "average_rating": 5.33,
        "frequency": 192,
        "name": "Android"
    },
    {
        "average_rating": 5.32,
        "frequency": 197,
        "name": "Public Speaking"
    },
    {
        "average_rating": 5.42,
        "frequency": 221,
        "name": "iOS"
    },
    {
        "average_rating": 5.08,
        "frequency": 191,
        "name": "Angular"
    },
    {
        "average_rating": 5.5,
        "frequency": 189,
        "name": "C++"
    },
    {
        "average_rating": 5.35,
        "frequency": 187,
        "name": "HTML/CSS"
    },
    {
        "average_rating": 5.34,
        "frequency": 196,
        "name": "NodeJS"
    },
    {
        "average_rating": 5.43,
        "frequency": 205,
        "name": "Java"
    },
    {
        "average_rating": 5.49,
        "frequency": 185,
        "name": "Product Design"
    },
    {
        "average_rating": 4,
        "frequency": 1,
        "name": "Awesome new skill"
    }
]
```
`http://localhost:5000/skills?min_frequency=200` returns
```
[
    {
        "average_rating": 5.42,
        "frequency": 221,
        "name": "iOS"
    },
    {
        "average_rating": 5.43,
        "frequency": 205,
        "name": "Java"
    }
]
```
`http://localhost:5000/skills?min_frequency=200&min_rating=6` returns
```
[]
```
