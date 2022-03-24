from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"

    name = fields.Char(string="Name", help="Patient Name", required=True, tracking=True)
    reference = fields.Char(string="Reference code", readonly=True, copy=False,
                            required=True, default=lambda self: _("New"))
    age = fields.Integer(String="Age", help="Patient Age", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], required=True, default='male', tracking=True)
    note = fields.Text(string="Description")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    appointments_count = fields.Integer(string="Appointments Count", compute="_compute_appointments_count")
    patient_image = fields.Binary(string="Image")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

    # control on field using button
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            self.state = 'cancel'

    # override create method
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "This is default description from overrided create method"

        vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals)

    # compute appointments count
    def _compute_appointments_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointments_count = appointment_count

    # override default_get method
    @api.model
    def default_get(self, fields):
        result = super(HospitalPatient, self).default_get(fields)
        print(result)
        return result

    @api.constrains('name')
    def Validate_Name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError("Record '%s' already Exists" % rec.name)

    @api.constrains('age')
    def validate_age(self):
        for rec in self:
            if rec.age <= 0:
                raise ValidationError('Age not allowed to be zero or negative number\n Please enter valid value...')

    def name_get(self):
        result = []
        for rec in self:
            name = rec.reference + '-' + rec.name
            result.append((rec.id, name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('reference', '=ilike', name.split('-')[0] + '%'), ('name', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    def action_appointment_count(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id}
        }
