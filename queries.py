sql_create_companies_table = """ CREATE TABLE IF NOT EXISTS companies (
                                        company_id INTEGER PRIMARY KEY,
                                        company VARCHAR(255) UNIQUE
                                        );"""

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            user_id INTEGER PRIMARY KEY,
                                            email VARCHAR(255) UNIQUE,
                                            name VARCHAR(255) NOT NULL,
                                            picture TEXT,
                                            company VARCHAR(255),
                                            phone VARCHAR(255),
                                            latitude FLOAT,
                                            longitude FLOAT,
                                            FOREIGN KEY (company) REFERENCES companies (company_id)
                                        ); """

sql_create_skills_table = """ CREATE TABLE IF NOT EXISTS skills (
                                    skill_id INTEGER PRIMARY KEY,
                                    skill_name VARCHAR(255) UNIQUE
                                    );"""

sql_create_skills_with_rating_table = """ CREATE TABLE IF NOT EXISTS skills_with_rating (
                                        skill_with_rating_id INTEGER PRIMARY KEY,
                                        skill_name VARCHAR(255) NOT NULL,
                                        rating INTEGER NOT NULL,
                                        skill_id INTEGER NOT NULL,
                                        UNIQUE(skill_name, rating),
                                        FOREIGN KEY (skill_id) REFERENCES skills (skill_id)
                                        );"""

sql_create_users_skills_table = """ CREATE TABLE IF NOT EXISTS users_skills (
                                            user_id INTEGER NOT NULL,
                                            skill_with_rating_id INTEGER NOT NULL,
                                            unique(user_id, skill_with_rating_id),
                                            FOREIGN KEY (user_id) REFERENCES users (user_id),
                                            FOREIGN KEY (skill_with_rating_id) REFERENCES skills_with_rating (skill_with_rating_id)
                                            );"""

sql_drop_users_skills_table = ''' DROP TABLE IF EXISTS users_skills'''

sql_drop_skills_table = ''' DROP TABLE IF EXISTS skills'''

sql_drop_skills_with_rating_table = ''' DROP TABLE IF EXISTS skills_with_rating'''

sql_drop_users_table = ''' DROP TABLE IF EXISTS users'''

sql_drop_companies_table = ''' DROP TABLE IF EXISTS users'''

sql_insert_user = ''' INSERT OR IGNORE INTO users(
                                email, name, picture, company, phone, latitude, Longitude)
                            VALUES (?,?,?,?,?,?,?)'''

sql_insert_company = ''' INSERT OR IGNORE INTO companies(company)
                            VALUES(?)'''

sql_insert_skill = ''' INSERT OR IGNORE INTO skills (skill_name)
                            VALUES(?)'''

sql_insert_skill_with_rating = ''' INSERT OR IGNORE INTO skills_with_rating (skill_name, rating, skill_id)
                            VALUES(?,?,?)'''
