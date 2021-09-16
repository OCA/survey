import logging


def migrate(cr, version):
    logger = logging.getLogger("survey_conditional_questions.migrations.11.0.1.3.0")

    def rename(old, new):
        """ Rename column if the old column exists and the new one does not """
        cr.execute(
            """ SELECT EXISTS(
            SELECT *
            FROM information_schema.columns
            WHERE table_name='survey_question'
            AND column_name=%s) """,
            (new,),
        )
        if cr.fetchone()[0]:
            logger.info("Column %s already exists", new)
            return
        cr.execute(
            """ SELECT EXISTS(
            SELECT *
            FROM information_schema.columns
            WHERE table_name='survey_question'
            AND column_name=%s) """,
            (old,),
        )
        if not cr.fetchone()[0]:
            logger.info("Column %s does not exist", old)
            return
        logger.info("Renaming column %s to %s", new, old)
        cr.execute(
            """ ALTER TABLE survey_question
            RENAME COLUMN %s to %s """
            % (old, new)
        )

    for old, new in [
        ("conditional", "is_conditional"),
        ("question_conditional_id", "triggering_question_id"),
        ("answer_id", "triggering_answer_id"),
    ]:
        rename(old, new)
