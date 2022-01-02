# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'
#     _description = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
import random
from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class Course(models.Model):
    _name = "openacademy.course"
    _description = "OpenAcademy Courses"
    name = fields.Char(string="title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', String="Responsible", index=True)
    session_ids = fields.One2many('openacademy.session',"course_id", string="Sessions")
    _sql_constraints = [
        ('check_course_title_is_not_description', 'CHECK(name != description)', "Course title can\'t be description "),
        ('check_if_name_is_unique', 'UNIQUE(name)', "Course name should be unique")
    ]

class Sessions(models.Model):
    _name = "openacademy.session"
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration In Days")
    seats = fields.Integer(string="Number Of Seats")
    instructor_id = fields.Many2one('res.partner', String="Instructor")
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade', String="Course",  required=True)
    attendee_ids = fields.Many2many('res.partner', String="Atendees")
    taken_seats = fields.Float(String="Taken Seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    active = fields.Boolean(default=True)
    attendees_count = fields.Integer(string="Attendees Count", compute='_get_attendees_count', store=True)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = (len(record.attendee_ids) / record.seats) * 100.0
    @api.depends('start_date','duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            else:
                duration = timedelta(days=r.duration, seconds=-1)
                r.end_date = r.start_date + duration
    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            else:
                r.duration = (r.end_date - r.start_date).days + 1

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return{
                'warning':{
                    'title':_("Invalid 'seats' value"),
                    'message':_("The number of seats must be greater than zero")
                },
            }
        if self.seats < len(self.attendee_ids ):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees")
                },
            }

    @api.constrains('seats')
    def _Validate_Seats(self):
        for record in self:
            if record.seats  < 0:
                raise ValidationError("Seats cannot be negative number %s" %record.seats)
    @api.constrains('instructor_id','attendee_ids')
    def validate_instructor_not_in_atendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise ValidationError("Session's instructor cannot be one of attendees")



