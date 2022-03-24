from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = "openacademy.wizard"
    _description = "Wizard : quick registration of attendees to session"

    # one session has many wizard to register
    session_id = fields.Many2one('openacademy.session', String="Session", required=True)
    # many attendee can register by many wizard
    attendee_ids = fields.Many2many('res.partner', string="Attendees")



    def add_attendee(self):
        print("any thing")
