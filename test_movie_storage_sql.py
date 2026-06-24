import pytest
from movie_storage_sql import *


# ====================== calculate_average ======================
def test_add_movie_normal_case():
    add_movie("Inception")
    print(list_movies())


def test_list_movies():
    # Test listing movies
    movies = list_movies()
    print(movies)


def test_update_movie_normal_case():
    update_movie("Inception", 9.0)
    print(list_movies())


def test_delete_movie_normal_case():
    delete_movie("Inception")
    print(list_movies())
