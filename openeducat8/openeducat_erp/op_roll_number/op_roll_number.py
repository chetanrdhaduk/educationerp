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

from openerp import models, fields


class OpRollNumber(models.Model):
    _name = 'op.roll.number'
    _rec_name = 'roll_number'

    roll_number = fields.Char('Roll Number', size=8, required=True)
    course_id = fields.Many2one('op.course', 'College', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True)
    standard_id = fields.Many2one('op.standard', 'Standard', required=True)
    division_id = fields.Many2one('op.division', 'Division')
    student_id = fields.Many2one('op.student', 'Student', required=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
