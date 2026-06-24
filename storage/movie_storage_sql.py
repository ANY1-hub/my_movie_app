from sqlalchemy import create_engine, text
from fetching_movies_data import fetch_data
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_URL = f"sqlite:///{BASE_DIR / 'data' / 'movies.db'}"


# Create the engine
engine = create_engine(DB_URL, echo=False)  # echo is good when Debugging

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "title TEXT UNIQUE NOT NULL, year INTEGER NOT NULL, "
                            "rating REAL NOT NULL, "
                            "poster TEXT)"))
    connection.commit()


    # ====================================================================================================
    # existence_check helper =======================================================================
    def is_in_movies(movies_data: dict[str, dict[str, float | int]], title: str):
        """
        check if input title is equal or part of any title.
        :param title: string of movie titles
        :return: has_match, list of titles
        """
        search = title.casefold().strip()
        matches = [movie_title for movie_title in movies_data.keys()
                   if search in movie_title.casefold()]

        return len(matches), matches


    # ====================================================================================================

    def list_movies():
        """Retrieve all movies from the database."""
        with engine.connect() as connection:
            result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
            movies = result.fetchall()
        return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}


    def add_movie(title):
        """Add a new movie to the database."""
        omdb_data = fetch_data(title)
        if omdb_data is None:
            return None
        omdb_title = omdb_data['title']
        omdb_year = omdb_data['year']
        omdb_rating = omdb_data['rating']
        poster = omdb_data['poster']
        with engine.connect() as connection:
            try:
                connection.execute(text(
                    "INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                    {"title": omdb_title,
                     "year": omdb_year,
                     "rating": omdb_rating,
                     "poster": poster
                     })
                connection.commit()
            except Exception as e:
                print(f"Error: {e}")
        return omdb_title


    def delete_movie(title):
        """Delete a movie from the database."""
        with engine.connect() as connection:
            try:
                connection.execute(text("DELETE FROM movies WHERE title = :title"),
                                   {"title": title})
                connection.commit()
                print(f"Movie '{title}' deleted successfully.")
            except Exception as e:
                print(f"Error: {e}")


    def update_movie(title, rating):
        """Update a movie's rating in the database."""
        with engine.connect() as connection:
            try:
                connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                                   {"title": title, "rating": rating})
                connection.commit()
                print(f"Movie '{title}' updated successfully.")
            except Exception as e:
                print(f"Error: {e}")
