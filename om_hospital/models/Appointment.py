from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"

    name = fields.Char(string="Reference code", readonly=True, copy=False,
                       default=lambda self: _("New"))
    note = fields.Text(string="Description")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string="Status", tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    age = fields.Integer(string="Age", readonly=True, related="patient_id.age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              help="This field will be filled automatically")
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check Up Time")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id', string="Medicine")

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
            rec.state = 'cancel'

    # override create method
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "This is default description from overrided create method"

        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
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

    # @api.model
    # def default_get(self, fields):
    #     res = super(HospitalAppointment, self).default_get(fields)
    #     print(res)

    # override unlink method
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("You cannot delete %s because it is in a Done state", self.name))
        return super(HospitalAppointment, self).unlink()

    def url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.google.com.eg/'
        }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(String="Medicine")
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")


