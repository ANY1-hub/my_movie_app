import random
import os


# Stats helper =========================================================================
def calculate_average(ratings):
    """
    calculates the average of the given ratings
    :param ratings: list of ratings
    :return:average
    """
    if not isinstance(ratings, (list, tuple)): return None
    if len(ratings) == 0: return None
    for number in ratings:
        if not isinstance(number, (int, float)):
            return None
    return round(sum(ratings) / len(ratings), 1)


def calculate_median(number_list):
    """
    checks the median rating of all movies
    :param number_list: ratings of the movies dependent on if elements count is even or uneven
    :return: median value
    """
    if len(number_list) == 0: return None
    elements_number = len(number_list)
    number_list = sorted(number_list)
    if elements_number % 2 == 0:
        # when elements number even, the two nearest numbers /2
        nearest_number_below = int(elements_number / 2) - 1
        nearest_number_above = int(elements_number / 2)
        return round(
            (number_list[int(nearest_number_below)] + number_list[nearest_number_above]) / 2, 1)
    return round(number_list[int(elements_number / 2)], 1)


def max_rated_movie(movies_data: dict[str, dict[str, float | int]]):
    """
    checks which is the highest rated movie
    :return: list of title and rate
    """
    best_rated = ["", 0, 0]
    for title, item in movies_data.items():
        if item["rating"] > best_rated[1]:
            best_rated[0] = title
            best_rated[1] = item["rating"]
            best_rated[2] = item["year"]
        else:
            continue
    return best_rated


def min_rated_movie(movies_data: dict[str, dict[str, float | int]]):
    """
    checks which is the lowest rated movie
    :return: list of title and rate
    """
    worst_rated = ["", 10, 0]
    for title, item in movies_data.items():
        if item["rating"] < worst_rated[1]:
            worst_rated[0] = title
            worst_rated[1] = item["rating"]
            worst_rated[2] = item["year"]
        else:
            continue
    return worst_rated


# Random choice helper ==========================================================================
def choose_movie_randomly(movies_data: dict[str, dict[str, float | int]]):
    """
    picks a title and related rating at random
    :param movie_dict: dictionary of all movies
    :return: random title and related rating
    """
    title, info = random.choice(list(movies_data.items()))
    return title, info


# display helper =======================================================================
def max_title_length(movies_data: dict[str, dict[str, float | int]]):
    """
    calculates the length of the longest title
    :param movies_data: all movies
    :return: int
    """
    if not isinstance(movies_data, dict): return None
    if movies_data == {}: return 0
    if len(movies_data) == 0: return None
    try:
        calculated_max_title_length = max(len(item) for item in movies_data.keys())
        return calculated_max_title_length
    except(TypeError, AttributeError):
        return None


# website helpers ==========================================================================

def serialize_movie(values_to_print):
    """
    writes all values from received list transformed to HTML list to output variable, if value is not None
    :param values_to_print: list of dictionaries with movie data {"title":title,"rating":rating,"year":year,"poster":p}
    :return: output string
       <li>
            <div class="movie">
                <img class="movie-poster"
                     src="https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg"/>
                <div class="movie-title">The Dark Knight</div>
                <div class="movie-year">2008</div>
            </div>
       </li>
    """
    output = ""
    if not values_to_print:
        output += '\n\t<div id="no__find"><p>Sorry, we <em>couldn\'t</em> find the movie you were looking for.</p></div>\n'
    else:
        for title, details in values_to_print.items():
            output += '\n\t<li>\n\t\t<div class="movie">\n'
            if title != '' and details != {}:
                output += f'\t\t\t<div class="movie-rating">(omdb rating: {details["rating"]})</div>\n'
                output += f'\t\t\t<img class="movie-poster" src={details["poster"]}/>\n'
                output += f'\t\t\t<div class="movie-title">{title}</div>\n'
                output += f'\t\t\t<div class="movie-year">{details["year"]}</div>\n'
            output += '\t\t\t</div>\n\t\t</li>'
    return output


def replace_html_data(template: str, new_header, new_text):
    """
    Replaces placeholder text with received text
    :param template: Original HTML string
    :param new_text: text to replace placeholder text with
    :return: string with replaced text.
    """
    with_new_header = template.replace('__TEMPLATE_TITLE__', str(new_header))
    new_movie_grid = with_new_header.replace('__TEMPLATE_MOVIE_GRID__', str(new_text))
    return new_movie_grid


# reading data ===============================================================================

def get_template_html():
    with open(os.path.join("_static", "index_template.html"), "r", encoding='utf-8', newline='') as source:
        return source.read()


# saving data ================================================================================

def save_data(file_path, text):
    """ Save data to HTML file """
    with open(os.path.join('.', '_static', file_path), 'w', encoding='utf-8', newline='') as target:
        target.write(text)
