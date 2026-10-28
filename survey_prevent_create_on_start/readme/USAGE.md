In standard Odoo, accessing the survey start URL (`/survey/start/<survey_token>`) without
an `answer_token` automatically creates a new blank response (`survey.user_input`).

When **Prevent creating answers on start** is enabled:

* Accessing `/survey/start/<survey_token>` without an `answer_token` parameter
  (and without an existing valid answer token stored in session cookies)
  displays an error page informing the user that direct access is not allowed.
* To participate in the survey, respondents must use a personalized invitation
  link containing their unique `answer_token`
  (e.g., `/survey/start/<survey_token>?answer_token=<answer_token>`).
* This module is particularly useful when answers are generated upstream
  by custom business logic, automated workflows, or modules such as
  [survey_user_input_edit](https://github.com/OCA/survey/tree/19.0/survey_user_input_edit),
  ensuring that respondents cannot create new awnser (`survey.user_input`).
