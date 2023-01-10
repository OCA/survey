This module adds compatibility bewtween `form.io <https://formio.github.io/formio.js/app/builder>` and Survey. It adds a function on survey.survey that generates
a form.io compatible JSON that represents that survey. It also adds a function to generate a survey.user_input
from a JSON returned by form.io.
Use `survey.survey::generate_formio_json()` to get the json representing a survey that can be rendered using the form.io widget.
Use `survey.survey::user_input_from_formio()` to create a user_input with the answer from form.io.

It does not work with question of type 'matrix' because there's no corresponding compoment in form.io.
