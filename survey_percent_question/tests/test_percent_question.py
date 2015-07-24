# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from __future__ import unicode_literals

from openerp.tests.common import TransactionCase


class TestPercentQuestion(TransactionCase):
    def setUp(self):
        super(TestPercentQuestion, self).setUp()
        self.survey = self.env["survey.survey"].create({
            "title": "Percent Question Test",
        })

        self.page = self.env["survey.page"].create({
            "title": "Page1",
            "survey_id": self.survey.id,
        })

        self.q_percent = self.env["survey.question"].create({
            "page_id": self.page.id,
            "question": "Coverage status of your lines",
            "type": "percent_split",
            "labels_ids": [
                (0, 0, {'sequence': 1, 'value': 'Covered'}),
                (0, 0, {'sequence': 2, 'value': 'Not Covered'}),
            ],
        })

        self.l_covered = self.q_percent.labels_ids[0]
        self.l_uncover = self.q_percent.labels_ids[1]

        self.tag = "{0}_{1}_{2}".format(
            self.survey.id,
            self.page.id,
            self.q_percent.id,
        )

    def test_validate(self):
        qobj = self.env["survey.question"]
        err = qobj.validate_percent_split(
            self.q_percent,
            {"{0}_{1}".format(self.tag, self.l_covered.id): "50",
             "{0}_{1}".format(self.tag, self.l_uncover.id): "45"},
            self.tag,
        )
        self.assertIn(self.tag, err,
                      "Validation should fail for a total of 95%")

        err = qobj.validate_percent_split(
            self.q_percent,
            {},
            self.tag,
        )
        self.assertIn(self.tag, err,
                      "Validation should fail for no answer")

        err = qobj.validate_percent_split(
            self.q_percent,
            {"{0}_{1}".format(self.tag, self.l_covered.id): "all"},
            self.tag,
        )
        self.assertIn(self.tag, err,
                      "Validation should fail with bad float format")

    def test_validate_comment(self):
        qobj = self.env["survey.question"]
        self.q_percent.comments_allowed = True

        err = qobj.validate_percent_split(
            self.q_percent,
            {"{0}_comment_value".format(self.tag): "100"},
            self.tag,
        )
        self.assertIn(self.tag, err,
                      "Validation should fail if no comment label")

        err = qobj.validate_percent_split(
            self.q_percent,
            {"{0}_comment_value".format(self.tag): "50",
             "{0}_comment_label".format(self.tag): "Just Imported",
             "{0}_{1}".format(self.tag, self.l_covered.id): "45",
             "{0}_{1}".format(self.tag, self.l_uncover.id): "55"},
            self.tag,
        )
        self.assertIn(self.tag, err,
                      "Validation should take comment value into account")

        err = qobj.validate_percent_split(
            self.q_percent,
            {"{0}_comment_value".format(self.tag): "50",
             "{0}_comment_label".format(self.tag): "Just Imported",
             "{0}_{1}".format(self.tag, self.l_covered.id): "0.01",
             "{0}_{1}".format(self.tag, self.l_uncover.id): "49.99"},
            self.tag,
        )
        self.assertFalse(err, "Validation should pass, counting comment")

    def test_save_line_w_comments(self):
        input_id = self.env["survey.user_input"].create({
            "token": "test",
            "survey_id": self.survey.id,
        }).id
        self.q_percent.comments_allowed = True
        line_obj = self.env["survey.user_input_line"]
        line_obj.save_line_percent_split(
            input_id,
            self.q_percent,
            {"{0}_comment_value".format(self.tag): "50",
             "{0}_comment_label".format(self.tag): "Just Imported",
             "{0}_{1}".format(self.tag, self.l_covered.id): "0.01",
             "{0}_{1}".format(self.tag, self.l_uncover.id): "49.99"},
            self.tag,
        )

        for line in line_obj.get_old_lines(input_id, self.q_percent):
            if line.value_suggested_row:
                if line.value_suggested_row.id == self.l_covered.id:
                    self.assertEquals(line.value_number, 0.01,
                                      "Covered value should be 0.01%")
                elif line.value_suggested_row.id == self.l_uncover.id:
                    self.assertEquals(line.value_number, 49.99,
                                      "Uncovered value should be 49.99%")
                else:
                    raise AssertionError("Unexpected result line")
            else:
                self.assertEquals(line.value_text, "Just Imported")
                self.assertEquals(line.value_number, 50,
                                  "Just Imported value should be 50%")

        # Test that saving again overwrites the data
        line_obj.save_line_percent_split(
            input_id,
            self.q_percent,
            {"{0}_comment_value".format(self.tag): "30",
             "{0}_comment_label".format(self.tag): "Data",
             "{0}_{1}".format(self.tag, self.l_covered.id): "60",
             "{0}_{1}".format(self.tag, self.l_uncover.id): "10"},
            self.tag,
        )
        for line in line_obj.get_old_lines(input_id, self.q_percent):
            if line.value_suggested_row:
                if line.value_suggested_row.id == self.l_covered.id:
                    self.assertEquals(line.value_number, 60,
                                      "Covered value should be 60%")
                elif line.value_suggested_row.id == self.l_uncover.id:
                    self.assertEquals(line.value_number, 10,
                                      "Uncovered value should be 10%")
                else:
                    raise AssertionError("Unexpected result line")
            else:
                self.assertEquals(line.value_text, "Data")
                self.assertEquals(line.value_number, 30,
                                  "Data value should be 30%")
