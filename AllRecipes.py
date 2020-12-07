"""Web-scraper that utilizes the Allrecipes recipe database
Takes in ingredients as input arguments and returns X amount of recipes that include those ingredients
End goal: design a front-end website that can visualize this idea
Start date: 12/5/2020"""

from pathlib import Path
from bs4 import BeautifulSoup
from html_requests import check_isfile

# Step 1: Prompt User to enter the ingredients they would like to cook with
# Step 2: Use those ingredients to parse web data from allrecipes
# Step 3: Grab the top 5-10 recipes that contain those ingredients
# Step 4: Parse the ratings, prep and cooking time, and recipe link
# Step 5: Output the recipe name, ratings, prep and cooking time, and recipe link

class AllRecipes:
    """Contains methods to parse data from allrecipes.com

    This class contains various methods to parse data from the /search/
    section of allrecipes.com.

    Attributes
    -----------
    soup: :class:`BeautifulSoup`
        Used to parse HTML and XML code in a tree-like
        structure of the original HTML request.
    recipes: :class:`List`
        A list of dictionaries. Each dictionary contains
        recipe info that has been parsed from allrecipes.com.
    """

    def __init__(self, ingredient=''):
        self.soup = self.get_soup(ingredient=ingredient)
        self.recipes = self.get_recipes()

    def get_soup(self, ingredient=''):
        """Utilizes html_requests.py to either:
            load a pre-existing text file containing HTML code for an
            ingredient that has been searched before.

            save a new text file that contains HTML code for an ingredient
            that hasn't been searched prior.

        Passes the HTML code into the BeautifulSoup constructor for parsing
        HTML and XML code.

        :parameter
        -----------
        ingredient: :class:`str`
            The ingredient to search.

        :returns
        ---------
        soup: :class:`BeautifulSoup`
            Original HTML code passed through a BeautifulSoup constructor
            for later parsing of HTML and XML code in a tree-like structure
        """

        search_url = f'https://www.allrecipes.com/search/results/?ingIncl={ingredient}&sort=re'
        file_path = Path(
            f'C:\\{ingredient}.txt'
        )

        soup = BeautifulSoup(
            check_isfile(file_path=file_path, search_url=search_url), 'html.parser'
        )

        return soup

    def get_recipes(self):
        recipes = self.soup.select('.recipe-section .fixed-recipe-card')
        list_of_recipes = []

        for recipe in recipes:
            d = dict()

            d['name'] = self.get_recipe_name(recipe)
            d['ratings'] = self.get_ratings(recipe)
            d['description'] = self.get_description(recipe)
            d['recipe_page'] = self.get_recipe_link(recipe)

            list_of_recipes.append(d)

        return list_of_recipes

    def get_recipe_name(self, recipe):
        name = recipe.select_one('.fixed-recipe-card__title-link span').text.strip()
        return name

    def get_ratings(self, recipe):
        rating = recipe.select_one('.fixed-recipe-card__ratings span')['aria-label']
        return rating

    def get_description(self, recipe):
        description = recipe.select_one('.fixed-recipe-card__info a .fixed-recipe-card__description')
        desc_start = str(description).find('>') + 1
        desc_end = str(description).find('</div>')
        return str(description)[desc_start: desc_end]

    def get_times(self):
        pass

    def get_recipe_link(self, recipe):
        recipe_page = recipe.select_one('.fixed-recipe-card__h3 a')['href']
        return recipe_page
