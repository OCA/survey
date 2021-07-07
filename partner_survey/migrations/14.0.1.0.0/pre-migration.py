# Copyright 2021 ForgeFlow S.L.  <https://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def migrate_fields_records(cr):
    cr.execute(
        """
        SELECT id, name
        FROM ir_model_fields
        WHERE model = 'survey.user_input_line'
        """
    )
    res = cr.fetchall()

    field_ids = set()
    for fid, fname in res:
        cr.execute(
            """
            SELECT 1
            FROM ir_model_fields
            WHERE model = 'survey.user_input.line' AND name = %s
            LIMIT 1
            """,
            (fname,),
        )
        if not cr.rowcount:
            field_ids.add(fid)

    cr.execute(
        """
        SELECT id
        FROM ir_model
        WHERE model = 'survey.user_input.line'
        LIMIT 1
        """
    )
    model_id = cr.fetchall()[0][0]
    openupgrade.logged_query(
        cr,
        """
        UPDATE ir_model_fields
        SET model = 'survey.user_input.line',
            model_id = %s
        WHERE id in %s
        """,
        (model_id, tuple(field_ids)),
    )
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_fields
        WHERE model = 'survey.user_input_line'
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    migrate_fields_records(env.cr)
