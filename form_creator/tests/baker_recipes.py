from model_bakery.recipe import Recipe
from ..models import HTMLComponent

html_component = Recipe(HTMLComponent, html="<p>HTML Component</p>")
