from model_bakery.recipe import Recipe, foreign_key, seq
from .. import models as fc_models

html_component = Recipe(fc_models.HTMLComponent, html="<p>HTML Component</p>")
form_element_order = Recipe(
    fc_models.FormElementOrder,
    form=foreign_key(Recipe(fc_models.Form)),
    seq_no=seq(1),
)
