In standard Odoo, once a respondent submits a survey (`survey.user_input` reaches state `done`), the access link transitions into read-only mode. The respondent can only consult their answers or start a completely new submission from scratch without retrieving their previous answers.

However, several business scenarios require respondents to update their answers without starting over:
- Registration and enrollment forms (e.g., updating contact details, arrival dates, or uploaded documents before a deadline).
- Long multi-section questionnaires where a user realizes they made a mistake or omitted an item right after submitting.
- Periodic self-evaluations or profile forms where participants adjust their responses over time.
