# Reciprocity

A recipe sharing and collaboration website, made in Django as a final project for a Code Fellows 401 Python course.

## Features

Users may add, view, and edit recipes. Go to the homepage to see a list of the most recent recipes and their variations; view a single recipe to see a complete list of related recipes.

Recipes can be set as public or private; private recipes will not display to a general audience.

Users may also offer variations for existing recipes.

## Sweet Relations
- recipe to ingredient: many to many (using 'through'!)
- recipe to original recipe: many to one
- recipe to total variations: many to many

## Installation
- Clone the repository (git clone https://github.com/TeamReciprocity/reciprocity.git)
- Create a virtual environment; Reciprocity is 2.7 and 3.5 compatible
- Install requirements (pip install -r requirements.txt)
- Run locally with python manage.py runserver

## How to contribute
Fork the repository and make a pull request!

## Contact
Contact the authors via their github accounts or this repository.

## License
Reciprocity is MIT. See LICENSE.

## Authors
- AJ Wohlfert
- Hannah Krager
- Michael Stokley
