# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpPeriod(models.Model):
    _name = 'op.period'
    _description = 'Period'
    _order = 'sequence'

    name = fields.Char('Name', size=16, required=True)
    hour = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'),
        ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'),
        ('10', '10'), ('11', '11'), ('12', '12')
    ], 'Hours', required=True)
    minute = fields.Selection([
        ('00', '00'), ('15', '15'),
        ('30', '30'), ('45', '45'),
    ], 'Minute', required=True)
    duration = fields.Float('Duration')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True)
    sequence = fields.Integer('Sequence')


class OpTimetable(models.Model):
    _name = 'op.timetable'
    _description = 'Time Table'
    _rec_name = 'faculty_id'

    period_id = fields.Many2one('op.period', 'Period', required=True)
    start_datetime = fields.Datetime('Start', required=True)
    end_datetime = fields.Datetime('End', required=True)
    course_id = fields.Many2one('op.course', 'College', required=True)
    faculty_id = fields.Many2one('op.faculty', 'Faculty', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    division_id = fields.Many2one('op.division', 'Division')
    subject_id = fields.Many2one('op.subject', 'Subject', required=True)
    color = fields.Integer('Color Index')
    classroom_id = fields.Many2one('op.classroom', 'Classroom')
    subject_ids = fields.Many2many(string='Subjects', related='course_id.subject_ids')
    type = fields.Selection(
        [('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
         ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
         ('Friday', 'Friday'), ('Saturday', 'Saturday')], 'Days')

    @api.constrains('classroom_id', 'period_id')
    def _check_classroom_period(self):
        all_tt_ids = self.search([])
        for a in all_tt_ids:
            if a.id == self.id:
                return True
            if self.classroom_id.id == a.classroom_id.id and self.period_id.id == a.period_id.id:
                raise ValidationError(
                    _("Can't creat time table for same classroom & period."))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
