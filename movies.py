import movie_storage_sql as storage
from helpers import *
from movie_storage_sql import is_in_movies
import colors


# Menu Item functions ====================================================================

def print_all_movies(to_b_sorted=False):
    """
    print the complete list of movies, sorted, or unsorted
    :param movies_data: Dictionary of movies {title: {rating: float, year: int, ...}}
    :param to_b_sorted: boolean
    """

    movies_data = storage.list_movies()
    print(f"\n\nThere are {colors.CYAN}{len(movies_data)}{colors.RESET} movies in our database:\n")
    print(
        f"\t{colors.BRIGHT}{colors.YELLOW}Film Tile:{' ' * (max_title_length(movies_data) - 2)}Rating{colors.RESET_ALL}")
    if to_b_sorted:
        # the alphabetically sorted all_movies list is sorted for ranking
        all_movies = sorted([item for item in sorted(movies_data.items())],
                            key=lambda x: x[1]["rating"],
                            reverse=True)
    else:
        all_movies = movies_data.items()
    for title, item in all_movies:
        # calculates the spaces needed for the ratings to be below each other
        needed_space = max_title_length(movies_data) + 4 - len(title) - len(
            str(int(item["rating"])))
        print(f"\t{title} ({item["year"]}):{'.' * needed_space}{colors.CYAN}{item["rating"]}{colors.RESET}")
    input("\n\n(press enter to continue)")


def show_stats():
    """
    Displays some statistics about the movies
    Dictionary of movies {title: {rating: float, year: int, ...}}
    :return: None
    """
    movies_data = storage.list_movies()
    print(f"\n\n{colors.BRIGHT}Here are some fun facts about the movies we list:{colors.NORMAL}\n")
    print(
        f"The average rating of our movies is:{colors.CYAN} "
        f"{calculate_average([value["rating"] for value in movies_data.values()])}{colors.RESET}")
    print(
        f"The median of our movies is: {colors.CYAN} "
        f"{calculate_median([value["rating"] for value in movies_data.values()])}{colors.RESET}")
    print(
        f"Our best rated movie is: {colors.YELLOW}{max_rated_movie(movies_data)[0]} ({max_rated_movie(movies_data)[2]}){colors.RESET}, with a "
        f"rating of {colors.CYAN}{max_rated_movie(movies_data)[1]}{colors.RESET}")
    print(
        f"Our worst rated movie is: {colors.YELLOW}{min_rated_movie(movies_data)[0]} ({min_rated_movie(movies_data)[2]}){colors.RESET}, with a "
        f"rating of {colors.CYAN}{min_rated_movie(movies_data)[1]}{colors.RESET}")
    print("\n\n")
    input("(press enter to continue)\n\n")


def show_random_movie():
    """
    Picks and displays a random movie
    Dictionary of movies {title: {rating: float, year: int, ...}}
    :return: None
    """
    movies_data = storage.list_movies()
    title, info = choose_movie_randomly(movies_data)
    print("\n\nSo, you like it random.")
    print(
        f"Why don't you check out this random movie: {colors.YELLOW}{title} ({info["year"]}){colors.RESET} with a "
        f"rating of {colors.CYAN}{info["rating"]}{colors.RESET}")
    input("\n(press enter to continue)\n\n")


def search_movie():
    """
    takes user input and displays the search results.
    Dictionary of movies {title: {rating: float, year: int, ...}}
    :return: None
    """
    while True:
        show_header = True
        found_items = 0
        movies_data = storage.list_movies()
        search_phrase = input(
            f"\nplease enter a Title or part of it that you are looking for: ").casefold()
        for title, item in movies_data.items():
            if search_phrase in title.casefold():
                if show_header:
                    print(f"\nThe following Titles match your entry: \n")
                    show_header = False
                needed_space = max_title_length(movies_data) + 6 - len(title) - len(
                    str(item["rating"]))
                print(
                    f"\t{title} ({item["year"]}):{'.' * needed_space}rating: {colors.CYAN}{item["rating"]}{colors.RESET}")
                found_items += 1

        if found_items == 0:
            print(
                f"\n\n{colors.YELLOW}Sorry we have no movie title that matches or contains what "
                f"you entered.{colors.RESET}")
        else:
            input("\n(press enter to continue)\n\n")

        search_again = input(f"\nWant to make another search? (y/*): ").lower()
        if search_again != "y" and search_again != "yes":
            break


def handle_user_menu():
    """
    handles the main menu
    :return: None
    """
    # menu_choice = -1

    # Necessary to dynamically add the necessary Attribute to the function-call of the sorted list
    sorted_movielist_menu_item_id = None

    while True:
        print("\n")
        for i, item in enumerate(menu_items):
            # check for the "sorted list" menu item
            if "sorted" in item[0]:
                sorted_movielist_menu_item_id = i
            print(f"{colors.CYAN}{i}.{colors.RESET}\t {item[0]}")
        try:
            menu_choice = int(
                input(
                    f"\nEnter choice {colors.YELLOW}({colors.CYAN}0-{len(menu_items) - 1}{colors.YELLOW}){colors.RESET}: "))
        except ValueError:
            print(f"\n{colors.YELLOW}Ooops, This was not even a {colors.BRIGHT}number {colors.NORMAL}{colors.RESET}")
            continue
        if (len(menu_items) - 1 < menu_choice or menu_choice < 0) and isinstance(menu_choice, int):
            print(
                f"\n{colors.RED}Please enter one of the {colors.BRIGHT}menu item{colors.NORMAL}s {colors.BRIGHT}number{colors.RESET}\n")
            continue

        if menu_choice == 0:
            break
        elif menu_choice == sorted_movielist_menu_item_id:
            menu_items[menu_choice][1](True)
        else:
            menu_items[menu_choice][1]()


# Menu Item functions ====================================================================
# TODO refactoring search_handler for all functions.
# TODO refactoring confirmation_handler for all functions
# TODO refactor input validation and add to rate and year.
def add_movie():
    """
    Adds a movie to the movies' database.
    Loads the information from the database, adds the movie,
    and saves it. The function doesn't need to validate the input.
    :return: None
    """
    while True:
        movies_data = storage.list_movies()
        lookup_title = input("\n\nPlease enter the movie title you wish to add to the database: ")
        number_of_matches, title_matches = is_in_movies(movies_data, lookup_title)
        do_add_movie = False
        if number_of_matches > 0:
            print("movies_data contains similar title(s):")

            is_exact_match = ""
            for item in title_matches:
                print(f"{colors.YELLOW}\t{item}{colors.RESET}")
                if item == lookup_title:
                    is_exact_match = item
            if is_exact_match != "":
                print(f"This title already exists:{colors.RED}{is_exact_match}{colors.RESET}")
                try_again = input(f"Do you want to enter another Title? (y/*):")
                if try_again in {"y", "yes", "yeah"}:
                    continue
                else:
                    break

            if not is_exact_match:
                # print("These are similar titles:")
                try_again = input(f"{colors.GREEN}Do you want to continue? (y/*): {colors.RESET}").lower()
                if try_again in {"y", "yes", "yeah"}:
                    do_add_movie = True
                else:
                    break

        if number_of_matches == 0:
            do_add_movie = True

        if do_add_movie:
            # show movies list or not
            result = storage.add_movie(lookup_title)
            if result is None:
                answer = input(
                    "\nWe could not find the title in the OMDB database? Would you like to try again? (y/*): ").strip().lower()
                if answer in {"y", "yes", "yeah"}:
                    continue
                else:
                    break
            else:
                print(f"'{result}' added successfully!")
            answer = input("\nWould you like to see the updated list of movies? (y/*): ").strip().lower()
            if answer in {"y", "yes", "yeah"}:
                print_all_movies()
            break


# def delete_movie(movies_data: dict[str, dict[str, float | int]]):
def delete_movie():
    """
    deletes the movie entered by user from the movies_data
    :return: None
    """
    while True:
        title_to_delete = ""
        movies_data = storage.list_movies()
        lookup_title = input(
            f"Please enter the movie title you wish to {colors.RED}delete{colors.RESET} from the database "
            f"({colors.CYAN}{len(movies_data)}{colors.RESET}): ")
        number_of_matches, title_matches = is_in_movies(movies_data, lookup_title)
        # if there are no matching titles.
        if number_of_matches == 0:
            print(f"{colors.RED}Sorry, no matches found.{colors.RESET}")
            try_again = input(
                f"{colors.GREEN}Want to try another title? ({colors.BRIGHT}y/*{colors.GREEN}): {colors.RESET}").lower()
            if try_again in {"y", "yes", "yeah"}:
                continue
            else:
                break
        should_break_while = False
        # if there is more than 1 title matching, and an exact match or not.
        if number_of_matches > 1:
            print("More than one title matches your criteria:")
            is_exact_match = None
            # if there is even an exact match among the matches
            for item in title_matches:
                print(f"{colors.YELLOW}\t{item}{colors.RESET}")
                if item == lookup_title:
                    is_exact_match = item
            if is_exact_match:
                confirmation = input(
                    f"Would you like to {colors.RED}delete this{colors.RESET} (exact match) title? (y/*) "
                    f"{colors.RED}{is_exact_match}{colors.RESET}: ")
                if confirmation in {"y", "yes", "yeah"}:
                    title_to_delete = is_exact_match
                else:
                    print(f"Pleas refine your search criteria.")
                    continue

            if not is_exact_match:
                print("Please be more specific.")
                try_again = input(f"{colors.GREEN}Want to try again? (y/*): {colors.RESET}").lower()
                if try_again in {"y", "yes", "yeah"}:
                    continue
                else:
                    break
        if number_of_matches == 1 or title_to_delete != "":
            if number_of_matches == 1:
                title_to_delete = title_matches[0]
            print(f"The movie {colors.RED}to be deleted{colors.RESET} is: {colors.RED}{title_to_delete}{colors.RESET}")
            sure = input("are you sure? (y/*)").lower()
            if sure not in {"y", "yes", "yeah"}:
                break
            storage.delete_movie(title_to_delete)
            print(f"\nNow there are {colors.CYAN}{len(movies_data)}{colors.RESET} movies left in our database")
            # show movies list or not
            answer = input("\nWould you like to see them? (y/*): ").strip().lower()
            if answer in {"y", "yes", "yeah"}:
                print_all_movies()
            break


# Update a movies rating in the list of movies
def update_movie_rating():
    """
    Updates a movie from the movies' database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    :return:
    """
    # get user input for title and check if in list of movies
    while True:
        lookup_title = input(
            f"Which movie's rating do you wish to change?: ")
        title_to_modify = ""
        movies_data = storage.list_movies()
        number_of_matches, title_matches = is_in_movies(movies_data, lookup_title)
        should_break_while = False

        if number_of_matches == 0:
            try_again = input(f"Want to try another title? (y/*): ").lower()
            if try_again in {"y", "yes", "yeah"}:
                continue
            else:
                return
        if number_of_matches > 1:
            print("More than one title matches your criteria:")
            is_exact_match = False
            for item in title_matches:
                print(f"{colors.YELLOW}\t{item}{colors.RESET}")
                if item == lookup_title:
                    is_exact_match = True
                    title_to_modify = item

            if is_exact_match:
                confirmation = input(
                    f"Wold you like to {colors.RED}modify this{colors.RESET} title? (y/*) {colors.RED}{title_to_modify}{colors.RESET}: ")
                if confirmation not in {"y", "yes", "yeah"}:
                    should_break_while = True

            if not is_exact_match:
                print("Please be more specific:")
                try_again = input(f"{colors.GREEN}Want to try another title? (y/*): {colors.RESET}").lower()
                if try_again in {"y", "yes", "yeah"}:
                    continue
                else:
                    break
        if should_break_while:
            break
        if number_of_matches == 1 or title_to_modify != "":
            if number_of_matches == 1: title_to_modify = title_matches[0]
            # get rating from user and check if valid entry
            rating = -1
            while not 0 <= rating <= 10:
                try:
                    print(
                        f"The title that matches your search is: {colors.YELLOW}{title_to_modify}{colors.RESET}")
                    rating = round(float(input("Please enter your rating (0.0 - 10.0): ")), 1)
                except ValueError:
                    print(
                        f"\n{colors.RED}Please enter a valid number {colors.BRIGHT, colors.YELLOW}(0.0 - 10.0){colors.RESET_ALL}")
                    continue
                if rating < 0 or rating > 10:
                    print(
                        f"\n{colors.RED}Please enter a valid number {colors.BRIGHT, colors.YELLOW}(0.0 - 10.0){colors.RESET_ALL}")
                    continue

            storage.update_movie(title_to_modify, rating)
            # show movies list or not
            answer = input("\nWould you like to see the updated movie list? (y/*): ").strip().lower()
            if answer in {"y", "yes", "yeah"}:
                print_all_movies()
            break


def generate_website():
    """
    collects template HTML and data to display, has data serialized, and placed in template HTML
    :return:
    """

    movies_data = storage.list_movies()
    template_html = get_template_html()
    header_text = "My Movie App"
    html_movie_details = serialize_movie(movies_data)
    new_html = replace_html_data(template_html, header_text, html_movie_details)
    save_data("index.html", new_html)
    print(f"{colors.GREEN}Created index.html {colors.ITALIC}successfully{colors.RESET_ITALIC} !{colors.RESET}")


menu_items = [("Exit", None), ("List movies", print_all_movies), ("Add movie", add_movie),
              ("Delete movie", delete_movie),
              ("Update movie rating", update_movie_rating), ("Stats", show_stats),
              ("Random movie", show_random_movie),
              ("Search movie", search_movie), ("Movies sorted by rating", print_all_movies),
              ("Generate Website", generate_website)]


def main():
    print(
        f"\n\n{colors.GREEN_B}**********{colors.RESET_B} {colors.YELLOW}My Movies Database{colors.RESET} "
        f"{colors.GREEN_B}**********{colors.RESET_B}")
    handle_user_menu()


if __name__ == "__main__":
    main()
