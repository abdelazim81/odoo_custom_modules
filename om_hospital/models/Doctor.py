from odoo import models, fields, api, _


class hospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Model for representing doctors at hospital"
    # specify the name of record
    _rec_name = "doctor_name"
    # specify field to order according {fields separated with comma then space order type asc or desc }
    _order = "reference,doctor_name desc"

    doctor_name = fields.Char(string="Name", required=True, tracking=True)
    reference = fields.Char(string="Sequence", default=lambda self: _("New"))
    age = fields.Integer(string="Age", copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male', tracking=True, required=True)
    note = fields.Text(string="Description")
    doctor_image = fields.Binary(string="Profile Image")
    appointments_count = fields.Integer(string="Appointments Count", compute="_compute_appointments_count")
    active = fields.Boolean(string="Active", default=True)

    #     override create method
    @api.model
    def create(self, vals):
        if not vals['note']:
            vals['note'] = "this is default description"
        vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
        return super(hospitalDoctor, self).create(vals)

    #     override duplicate / copy method
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('doctor_name'):
            default['doctor_name'] = _("%s (COPY)", self.doctor_name)
        return super(hospitalDoctor, self).copy(default)

    # compute appointments count
    def _compute_appointments_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointments_count = appointment_count
