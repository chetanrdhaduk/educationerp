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

from openerp import models, fields,api,_
from openerp.exceptions import ValidationError

class OpBook(models.Model):
    _name = 'op.book'

    name = fields.Char('Title', size=128, required=True)
    number_book = fields.Integer('No. Of Books', required=True)
    id_book = fields.Char('ISBN Code', size=64)
    tag = fields.Many2many('op.tag', string='Tag')
    author_ids = fields.Many2many('op.author', string='Author', required=True)
    state = fields.Selection(
        [('a', 'Available'), ('i', 'Issued'), ('r', 'Reserved'),
         ('l', 'Lost')], 'State', default='a')
    edition = fields.Text('Edition')
    publisher_ids = fields.Many2many(
        'op.publisher', string='Publisher', required=True)
    course_ids = fields.Many2many('op.course', string='College', required=True)
    movement_line = fields.One2many('op.book.movement', 'book_id', 'Movement')
    subject_ids = fields.Many2many(
        'op.subject', string='Subjects', required=True)
    internal_code = fields.Char('Internal ID', size=128)
    queue_ids = fields.Many2many('op.book.queue', string='Book Queue')
    #availability_book = fields.Integer(compute = '_get_available_book',string ="Availability")

#     @api.constrains('number_book')
#     def _check_number_book(self):
#         for rec in movement_line:
#             print rec.id,"dddd"
#             self.number_book -= rec.movement_line.quantity
#             if self.number_book > rec.movement_line.quantity:
#                  return True
#             if self.number_book < rec.movement_line.quantity:
#                  raise ValidationError(
#                      _("Book not available"))
                
    @api.model
    def create(self, vals):
        res = super(OpBook, self).create(vals)
        for move_id in res.movement_line:
            move_id.student_id.write({'book_ids':[(4,move_id.id)]})
        for move_id in res.movement_line:
            move_id.faculty_id.write({'book_ids':[(4,move_id.id)]})
        return res
        
    @api.multi
    def write(self, vals):
        res = super(OpBook, self).write(vals)
        for move_id in self.movement_line:
            move_id.student_id.write({'book_ids':[(4,move_id.id)]})
        for move_id in self.movement_line:
            move_id.faculty_id.write({'book_ids':[(4,move_id.id)]})
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
