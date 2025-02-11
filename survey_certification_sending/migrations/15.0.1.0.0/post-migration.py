from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    surveys = env["survey.survey"].search(
        [
            ("certification", "=", True),
            ("certification_mail_template_id", "!=", False),
        ]
    )
    for survey in surveys:
        template = survey.certification_mail_template_id
        user_inputs = env["survey.user_input"].search(
            [
                ("survey_id", "=", survey.id),
                ("scoring_success", "=", True),
                ("certification_sent", "=", False),
            ]
        )
        for user_input in user_inputs:
            user_lang = user_input.partner_id.lang or env.user.lang
            email_values = template.with_context(lang=user_lang).generate_email(
                user_input.id, ["subject"]
            )
            subject_rendered = email_values.get("subject", "")
            mail_exists = (
                env["mail.message"].search_count(
                    [
                        ("model", "=", "survey.user_input"),
                        ("res_id", "=", user_input.id),
                        ("subject", "ilike", subject_rendered),
                    ]
                )
                > 0
            )
            if mail_exists:
                user_input.write({"certification_sent": True})
