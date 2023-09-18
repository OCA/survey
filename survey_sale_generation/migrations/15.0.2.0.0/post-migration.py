# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.m2o_to_x2m(
        env.cr,
        env["survey.question"],
        "survey_question",
        "product_ids",
        "product_id",
    )
    openupgrade.m2o_to_x2m(
        env.cr,
        env["survey.question.answer"],
        "survey_question_answer",
        "product_ids",
        "product_id",
    )
