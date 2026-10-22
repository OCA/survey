**Public User Session Retention**

- **Anonymous submissions without a tokenized URL**:
  If a public user completes an open public survey directly via the generic link `/survey/start/<survey_token>`, their session identity is stored only in the browser cookie `survey_<survey_token>`.
  - If the user clears their browser cache/cookies, switches browsers, or opens the generic survey link on another device, Odoo cannot technically identify them (to prevent anonymous users from accessing other respondents' data). In this situation, visiting the generic link starts a new blank survey.
  - However, if the survey was distributed via email invitations (which include the unique `answer_token` in the URL), public users can return and edit their answers from any device at any time using that link.
  - A possible roadmap improvement could be an option to email a resumption link with the answer token upon first submission for anonymous respondents.

**Scoring and Certification**

- For surveys with scoring and certification, retaking or editing answers currently retains the standard certification behavior (e.g., if certification is already issued).

