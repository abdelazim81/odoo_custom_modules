from odoo import models, fields, api
class Wizard(models.TransientModel):
    _name = "openacademy.wizard"
    _description = "Wizard : quick registeration of attendees to session"
    #  get current id of session
    def _default_session(self):
        return self.env['openacademy.session'].browse(self._context.get('id'))
    # one session has many wizard to register
    session_id = fields.Many2one('openacademy.session', String="Session", required=True, default=_default_session)
    # many attendee can register by many wizard
    attendee_ids = fields.Many2many('res.partener', string="Attendees")