**Architecture & Token Lifecycle**

Odoo surveys rely on a dual-token mechanism:
1. **Survey Access Token (`survey.access_token`)**: Unique hash identifying the survey definition (e.g., `/survey/start/<survey_token>`).
2. **Answer Access Token (`survey.user_input.access_token`)**: Unique hash identifying a specific participant's submission session (e.g., `/survey/<survey_token>/<answer_token>`).

When a respondent initiates a survey via `/survey/start/<survey_token>`, Odoo sets an HTTP cookie in the browser:
```text
survey_<survey_token>=<answer_token>
```
with a default validity of 24 hours. Subsequent visits to `/survey/<survey_token>` read this cookie to match the current respondent session.

**Navigation and Editing Workflow**

1. **Initial Submission**:
   - The respondent completes the questions and clicks **Submit**.
   - The submission is marked as done (`state = 'done'`), and the completion `end_datetime` is recorded.
   - The respondent lands on the native completion screen.

2. **Consultation and Edit Option**:
   - On the completion screen, the respondent can:
     - Click **Review your answers** (`/survey/print/<survey_token>?answer_token=<answer_token>&review=True`) to view their submitted responses in read-only mode.
     - Click **Edit your answers** (`/survey/start/<survey_token>?answer_token=<answer_token>&edit=1`) to enter modification mode.
   - Direct visits or page refreshes on `/survey/<survey_token>/<answer_token>` remain on the completion screen; the survey is not prematurely restarted unless the user explicitly clicks the edit button.

3. **Editing Mode**:
   - When **Edit your answers** is clicked, the system executes:
     - The response transitions from `done` to `in_progress` (logged in chatter).
     - The pagination pointer is reset, placing the respondent at the first question.
     - All previous responses remain pre-filled in the form.
     - Backward navigation is enabled across all pages.

4. **Resubmission**:
   - The respondent edits their answers and clicks **Submit**.
   - Answer lines are updated in-place, ensuring no duplicate line entries are created.
   - The submission returns to `done`, updating `end_datetime` and logging the completion state change in chatter.

**Respondent Lifecycles: Public vs Logged-In Users**

- **Registered / Logged-in Users**:
  - The submission is permanently associated with the user's partner record (`partner_id`).
  - Even if the browser cookie is deleted or the user accesses the survey from a different device, visiting `/survey/start/<survey_token>` automatically retrieves their existing submission.
  - If the survey was previously completed, the user is presented with the completion screen with the options to review or edit.

- **Public / Anonymous Users**:
  - The submission is not tied to a registered partner account.
  - Identification relies on:
    1. The active browser cookie (`survey_<survey_token>`), or
    2. The tokenized URL (`/survey/<survey_token>/<answer_token>`), such as those sent via email invitation links.
  - As long as the cookie remains active in their browser, a public user can complete the survey, consult their answers, and click **Edit your answers** to modify their submission.
