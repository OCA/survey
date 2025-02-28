import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date

_logger = logging.getLogger(__name__)


type_mapping = {
    "char": [
        "char_box",
        "numerical_box",
        "date",
        "datetime",
        "simple_choice",
        "multiple_choice",
    ],
    "text": ["char_box", "date", "simple_choice"],
    "html": ["text_box", "numerical_box", "datetime", "simple_choice"],
    "integer": ["numerical_box"],
    "float": ["numerical_box"],
    "date": ["date"],
    "datetime": ["datetime"],
    "many2one": ["simple_choice"],
    "many2many": ["multiple_choice"],
    "selection": ["char_box", "simple_choice"],
}


class SurveyRecordCreationFieldValues(models.Model):
    """Configure default values of records created on survey submission"""

    _name = "survey.record.creation.field.values"

    survey_record_creation_id = fields.Many2one("survey.record.creation")
    survey_id = fields.Many2one(
        "survey.survey", related="survey_record_creation_id.survey_id"
    )
    model_id = fields.Many2one("ir.model", related="survey_record_creation_id.model_id")

    field_id = fields.Many2one(
        "ir.model.fields",
        domain="[('model_id','=',model_id),('readonly','=',False),('ttype','in',['char','selection','text','html','integer','float','date','datetime','many2one','many2many'])]",  # noqa: B950
        ondelete="cascade",
    )
    field_relation = fields.Char(related="field_id.relation")
    field_type = fields.Selection(related="field_id.ttype")
    field_help = fields.Html("Help", compute="_compute_field_help")

    value_origin = fields.Selection(
        [
            ("fixed", "Fixed"),
            ("question", "Question"),
            ("other_record", "From other created record"),
        ],
        string="Value origin",
        required=True,
        default="fixed",
        help="""* Fixed: you can set the value in value field
        * Question: Response of the question will set the value.
        If you do not see your question, maybe the type of question
        do not match the type of field
        * From other created record:
        You can set other record creation to link several created records.
        Can only be used with many2one fields.""",
    )

    fixed_value_many2one = fields.Reference(
        string="Record", selection="_selection_target_model"
    )
    fixed_value_many2many = fields.One2many(
        "survey.record.creation.field.values.x2m",
        "survey_record_creation_field_values_id",
    )
    fixed_value_char = fields.Char("Value")
    fixed_value_selection = fields.Char("Value")
    fixed_value_text = fields.Text("Value")
    fixed_value_html = fields.Html("Value")
    fixed_value_integer = fields.Integer("Value")
    fixed_value_float = fields.Float("Value")
    fixed_value_date = fields.Date("Value")
    fixed_value_datetime = fields.Datetime("Value")

    displayed_value = fields.Char("Value", compute="_compute_displayed_value")
    other_created_record_id = fields.Many2one(
        "survey.record.creation",
        string="Other record",
        domain="[('survey_id','=',survey_id),('model_id.model','=',field_relation)]",
    )

    allowed_question_ids = fields.Many2many(
        "survey.question", compute="_compute_allowed_question_ids"
    )
    question_id = fields.Many2one(
        "survey.question",
        string="Question",
        domain="[('id','in',allowed_question_ids)]",
    )

    unicity_check = fields.Boolean(
        "Unicity constraint",
        help="On record creation, if another record exists with same value, record will not be created.",  # noqa: B950
    )

    @api.depends("field_id")
    def _compute_field_help(self):
        for record in self:
            field_help = _("Field type is : <b>%s</b>", record.field_type)
            if record.field_type == "selection":
                field_help += "<br />" + _(
                    "possible values are %s",
                    ", ".join(
                        [
                            f"<b>{s.value}</b> <i>({s.name})</i>"
                            for s in record.field_id.selection_ids
                        ]
                    ),
                )
            record.field_help = field_help

    @api.depends("field_id")
    def _compute_allowed_question_ids(self):
        for record_creation_field_values in self:
            if (
                not record_creation_field_values.survey_id
                or not record_creation_field_values.field_id
            ):
                record_creation_field_values.allowed_question_ids = None
                return
            question_domain = [
                ("survey_id", "=", record_creation_field_values.survey_id.id)
            ]

            if record_creation_field_values.field_id.ttype in ["many2one", "many2many"]:
                question_domain.extend(
                    [
                        "|",
                        "&",
                        ("answer_values_type", "=", "record"),
                        (
                            "model_id",
                            "=",
                            record_creation_field_values.field_id.relation,
                        ),
                        ("answer_values_type", "=", "value"),
                    ]
                )
            if record_creation_field_values.field_id.ttype in type_mapping:
                question_domain.append(
                    (
                        "question_type",
                        "in",
                        type_mapping[record_creation_field_values.field_id.ttype],
                    )
                )

            record_creation_field_values.allowed_question_ids = self.env[
                "survey.question"
            ].search(question_domain)

    @api.model
    def _selection_target_model(self):
        return [
            (model.model, model.name)
            for model in self.env["ir.model"].sudo().search([])
        ]

    @api.onchange("field_id", "origin")
    def clean_values(self):
        # clean values
        self.fixed_value_many2many = None
        self.fixed_value_many2one = None
        self.fixed_value_char = None
        self.fixed_value_selection = None
        self.fixed_value_text = None
        self.fixed_value_html = None
        self.fixed_value_integer = None
        self.fixed_value_float = None
        self.fixed_value_date = None
        self.fixed_value_datetime = None
        self.other_created_record_id = None
        self.question_id = None

    @api.onchange("field_id")
    def _onchange_field_id(self):
        # Set reference field model and select first record
        if (
            self.field_id
            and self.field_id.ttype == "many2one"
            and self.field_id.relation
        ):
            rec = self.env[self.field_id.relation].search([], limit=1)
            if rec:
                self.fixed_value_many2one = f"{self.field_id.relation},{rec.id}"
            else:
                model_name = (
                    self.env["ir.model"]
                    .search([("model", "=", self.field_id.relation)])
                    .name
                )
                self.fixed_value_many2one = None
                raise UserError(
                    _("You should append at least one record in %s", model_name)
                )
        else:
            self.fixed_value_many2one = None

    def get_fixed_value_for_record_creation(self):
        """return val used in create() method"""
        if self.value_origin == "fixed":
            if self.field_type == "many2one":
                if self.fixed_value_many2one:
                    return self.fixed_value_many2one.id
            elif self.field_type == "many2many":
                return [
                    m2m.value_reference.id
                    for m2m in self.fixed_value_many2many
                    if m2m.value_reference
                ]
            else:
                return self["fixed_value_" + self.field_type]

    @api.onchange(
        "fixed_value_char",
        "fixed_value_selection",
        "fixed_value_text",
        "fixed_value_html",
        "fixed_value_integer",
        "fixed_value_float",
        "fixed_value_date",
        "fixed_value_datetime",
        "fixed_value_many2one",
        "fixed_value_many2many",
        "other_created_record_id",
        "question_id",
    )
    def _compute_displayed_value(self):
        for record in self:
            if record.field_id:
                if (
                    record.value_origin == "other_record"
                    and record.other_created_record_id
                ):
                    record.displayed_value = (
                        _("Other created record: ")
                        + record.other_created_record_id.name
                    )
                elif record.value_origin == "fixed":
                    if record.field_id.ttype == "many2one":
                        if record.fixed_value_many2one:
                            record.displayed_value = (
                                record.fixed_value_many2one.display_name
                            )
                        else:
                            record.displayed_value = None
                    elif record.field_id.ttype == "many2many":
                        if record.fixed_value_many2many:
                            record.displayed_value = ", ".join(
                                [
                                    r.value_reference.display_name
                                    for r in record.fixed_value_many2many
                                    if r.value_reference
                                ]
                            )
                        else:
                            record.displayed_value = None
                    elif record.field_id.ttype == "date":
                        record.displayed_value = format_date(
                            self.env, record.fixed_value_date
                        )
                    elif record.field_id.ttype == "datetime":
                        record.displayed_value = format_date(
                            self.env, record.fixed_value_datetime
                        )
                    else:
                        record.displayed_value = str(
                            record["fixed_value_" + record.field_id.ttype]
                        )
                else:  # value_origin = question
                    record.displayed_value = _(
                        "Answer to question: %s", record.question_id.title
                    )
            else:
                record.displayed_value = ""


class SurveyRecordCreationFieldValuesX2m(models.Model):
    """O2m an M2m default values"""

    _name = "survey.record.creation.field.values.x2m"

    survey_record_creation_field_values_id = fields.Many2one(
        "survey.record.creation.field.values"
    )
    value_reference = fields.Reference(
        string="Record", selection="_selection_target_model"
    )

    @api.model
    def _selection_target_model(self):
        return [
            (model.model, model.name)
            for model in self.env["ir.model"].sudo().search([])
        ]

    @api.onchange("survey_record_creation_field_values_id")
    def _onchange_model_name(self):
        # Set reference field model and select first record
        field = self.survey_record_creation_field_values_id.field_id
        if field and "2many" in field.ttype and field.relation:
            rec = self.env[field.relation].search([], limit=1)
            if rec:
                self.value_reference = f"{field.relation},{rec.id}"
            else:
                model_name = (
                    self.env["ir.model"].search([("model", "=", field.relation)]).name
                )
                raise ValueError(
                    _("You should append at least one record in %s", (model_name,))
                )
