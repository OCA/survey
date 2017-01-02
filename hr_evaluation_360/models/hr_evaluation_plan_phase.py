# -*- coding: utf-8 -*-
# Copyright 2016 Luis Felipe Mileo - <mileo@kmee.com.br> - KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
import time

from openerp import api, fields, models

evaluation_360_list = []


def evaluation_360(evaluation_func):
    evaluation_360_list.append(evaluation_func)
    return evaluation_360


class HrEvaluationPlanPhase(models.Model):

    _inherit = 'hr_evaluation.plan.phase'

    action = fields.Selection(
        selection_add=[
            ('360', u'360-degree feedback'),
            ('360-anonymous', u'360-degree anonymous feedback'),
        ]
    )


class HrEvaluationEvaluation(models.Model):

    _inherit = 'hr_evaluation.evaluation'

    @evaluation_360
    def _get_360_evaluation_child(self, evaluation):
        return evaluation.employee_id.child_ids

    @evaluation_360
    def _get_360_evaluation_parent(self, evaluation):
        return evaluation.employee_id.parent_id

    @evaluation_360
    def _get_360_evaluation_myself(self, evaluation):
        return evaluation.employee_id

    @evaluation_360
    def _get_360_evaluation_department(self, evaluation):
        return self.env['hr.employee'].search(
            [('department_id', '=',
              evaluation.employee_id.department_id.id)]
        )

    @api.multi
    def button_plan_in_progress(self):
        hr_eval_inter_obj = self.env['hr.evaluation.interview']
        for evaluation in self:
            wait = False
            for phase in evaluation.plan_id.phase_ids:
                if phase.action not in ('360', '360-anonymous'):
                    return super(HrEvaluationEvaluation,
                                 self).button_plan_in_progress()

                children = self.env['hr.employee']
                for item in evaluation_360_list:
                    children |= item(self, evaluation)

                for child in children:
                    int_id = hr_eval_inter_obj.create({
                        'evaluation_id': evaluation.id,
                        'phase_id': phase.id,
                        'deadline': (
                            parser.parse(
                                datetime.now().strftime('%Y-%m-%d')
                            ) + relativedelta(months=+1)).strftime(
                            '%Y-%m-%d'),
                        'user_id': child.user_id.id,
                    })
                    if phase.wait:
                        wait = True
                    if not wait:
                        int_id.survey_req_waiting_answer()

                    if (not wait) and phase.mail_feature:
                        body = phase.mail_body % {
                            'employee_name': child.name,
                            'user_signature': child.user_id.signature,
                            'eval_name': phase.survey_id.title,
                            'date': time.strftime('%Y-%m-%d'),
                            'time': time,
                        }
                        sub = phase.email_subject
                        if child.work_email:
                            vals = {
                                'state': 'outgoing',
                                'subject': sub,
                                'body_html': '<pre>%s</pre>' % body,
                                'email_to': child.work_email,
                                'email_from': evaluation.employee_id.work_email
                            }
                            self.env['mail.mail'].create(vals)
        self.write({'state': 'wait'})


class HrEvaluationInterview(models.Model):

    _inherit = 'hr.evaluation.interview'

    @api.constrains('state')
    def _check_state_done(self):
        for item in self.sudo():
            if (item.state == 'done' and
                    item.phase_id.action == '360-anonymous'):
                item.user_id = False
                item.request_id.partner_id = False
                item.request_id.email = False
