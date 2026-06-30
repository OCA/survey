Answer types that do not have a corresponding `value_<type>` field on
`survey.user_input.line` (e.g. custom types added by other modules such as
`survey_question_type_binary`) are silently skipped and will not appear in
the rendered result mail or the backend participant view.
