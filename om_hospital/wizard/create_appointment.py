# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    date_appointment = fields.Date(string="Date")

    @api.model
    def default_get(self, fields):
        result = super(CreateAppointmentWizard, self).default_get(fields)
        if self._contex.get('active_id'):
            result['patient_id'] = self._context.get('active_id')
        return result

    # create new record from python
    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'date_appointment': self.date_appointment
        }
        # create method return the record which is created (you should access id if you need it)
        appointment_record_id = self.env['hospital.appointment'].create(vals)
        # return view after record creation
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_record_id.id,
            'target': 'new'
        }


