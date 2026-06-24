import pytest
import requests
from movies import *


# ====================== calculate_average ======================
def test_calculate_average_normal_case():
    assert calculate_average([5, 10]) == 7.5


def test_calculate_average_not_list():
    assert calculate_average('String') is None
    assert calculate_average(123) is None
    assert calculate_average(None) is None


def test_calculate_average_list_with_non_numbers():
    assert calculate_average([1, 2, 'String']) is None
    assert calculate_average([1, 2, None]) is None


def test_calculate_average_empty_list():
    assert calculate_average([]) is None


def test_calculate_average_single_element():
    assert calculate_average([8]) == 8.0


def test_calculate_average_floats():
    assert calculate_average([1.5, 2.5, 3.0]) == 2.3


# ====================== calculate_median ======================
def test_calculate_median_odd_number_of_elements():
    # 3 elements → middle element (after sorting)
    assert calculate_median([1, 3, 5]) == 3.0


def test_calculate_median_even_number_of_elements():
    # 4 elements → average of the two elements in the middle
    assert calculate_median([1, 2, 3, 4]) == 2.5


def test_calculate_median_already_sorted():
    assert calculate_median([10, 20, 30, 40, 50]) == 30.0


def test_calculate_median_unsorted():
    assert calculate_median([5, 1, 9, 3]) == 4.0  # (3+5)/2 = 4


def test_calculate_median_empty_list():
    assert calculate_median([]) is None  # oder was deine Funktion wirklich macht


def test_calculate_median_single_element():
    assert calculate_median([7]) == 7.0


# ====================== max_rated_movie & min_rated_movie ======================
@pytest.fixture
def sample_movies():
    return {
        "Inception": {"rating": 8.8, "year": 2010},
        "The Matrix": {"rating": 8.7, "year": 1999},
        "Interstellar": {"rating": 8.6, "year": 2014},
        "The Room": {"rating": 3.6, "year": 2003},
    }


def test_max_rated_movie(sample_movies):
    result = max_rated_movie(sample_movies)
    assert result[0] == "Inception"
    assert result[1] == 8.8
    assert result[2] == 2010


def test_min_rated_movie(sample_movies):
    result = min_rated_movie(sample_movies)
    assert result[0] == "The Room"
    assert result[1] == 3.6
    assert result[2] == 2003


def test_max_rated_movie_single_movie():
    data = {"Solo": {"rating": 5.5, "year": 2020}}
    result = max_rated_movie(data)
    assert result == ["Solo", 5.5, 2020]


def test_min_rated_movie_single_movie():
    data = {"Solo": {"rating": 5.5, "year": 2020}}
    result = min_rated_movie(data)
    assert result == ["Solo", 5.5, 2020]


# ====================== choose_movie_randomly ======================
def test_choose_movie_randomly_returns_valid_movie(sample_movies):
    random.seed(42)  # für reproduzierbare Tests
    title, info = choose_movie_randomly(sample_movies)
    assert title in sample_movies
    assert isinstance(info, dict)
    assert "rating" in info
    assert "year" in info


def test_choose_movie_randomly_different_calls(sample_movies):
    # Nur prüfen, dass es grundsätzlich funktioniert (Randomness ist schwer 100% zu testen)
    results = set()
    for _ in range(10):
        title, _ = choose_movie_randomly(sample_movies)
        results.add(title)
    assert len(results) > 1  # mit hoher Wahrscheinlichkeit


# ====================== max_title_length ======================
def test_max_title_length_normal_case(sample_movies):
    assert max_title_length(sample_movies) == len("Interstellar")


def test_max_title_length_empty_dict():
    assert max_title_length({}) == 0


def test_max_title_length_single_movie():
    data = {"Short": {"rating": 7}}
    assert max_title_length(data) == 5
