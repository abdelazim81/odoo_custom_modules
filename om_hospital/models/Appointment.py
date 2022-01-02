from odoo import api, models, fields, _


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"

    sequence = fields.Char(string="Reference code", readonly=True, copy=False,
                             default=lambda self: _("New"))
    note = fields.Text(string="Description")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    age = fields.Integer(string="Age", readonly=True, related="patient_id.age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              help="This field will be filled automatically")
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up Time")

    # control on field using button
    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    # override create method
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "This is default description from overrided create method"

        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(HospitalAppointment, self).create(vals)

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''
