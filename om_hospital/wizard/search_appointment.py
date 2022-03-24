# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SearchAppointmentWizard(models.TransientModel):
    _name = 'search.appointment.wizard'
    _description = 'Search Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)

    def action_search_appointmentM1(self):
        action = self.env.ref('om_hospital.appointment_action').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_search_appointmentM2(self):
        action = self.env['ir.actions.actions']._for_xml_id("om_hospital.appointment_action")
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_search_appointmentM3(self):
        return{
            'type': 'ir.actions.act_window',
            'name': 'Search Appointments',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form,kanban,pivot,graph,search',
            'domain': [('patient_id', '=', self.patient_id.id)]
        }
