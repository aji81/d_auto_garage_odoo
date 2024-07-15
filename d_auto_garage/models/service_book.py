# -*- encoding: utf-8 -*-
##############################################################################
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError , ValidationError
import string       
from num2words import num2words
from twilio.rest import Client


class ServiceBook(models.Model):
    _name = "service.book"
    _description = "Service Book"
    _inherit = ['mail.thread','mail.activity.mixin']
    
    @api.model
    def create(self, vals):
       if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'service.book') or _('New')
       res = super(ServiceBook, self).create(vals)
       return res
        
    name = fields.Char("Name",required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'),track_visibility=True)
    customer_id = fields.Many2one('res.partner', string="Customer")
    phone_num1 = fields.Char(string='Mobile', required=True, size=10)
    phone_num2 = fields.Char(string='Phone', required=True, size=10)
    email_cust = fields.Char(string='Email', widget='email')
    cust_address = fields.Text(string='Address')
    date = fields.Date('Create Date',default=lambda self: fields.Datetime.now(),readonly=True)
    date_deadline = fields.Date(string='Deadline', track_visibility=True)
    vehicle_type = fields.Selection([('car', 'Car') ,('suv', 'SUV'), ('hatchback', 'Hatchback'),
                                     ('sedan', 'Sedan'), ('pickup_truck', 'Pickup Truck')], default='car',required=True)
    registration_no = fields.Char(string='Registration No')
    model_numb = fields.Char(string='Model')
    vehicle_colour = fields.Char(string='Colour')
    company_id = fields.Many2one('res.partner', string="Company")
    transmission_type = fields.Selection([('manual', 'Manual') ,('Auto', 'Automatic')], default='manual',required=True)
    vechile_odometer = fields.Char(string='Odometer')
    vechile_image = fields.Image(string="Image 1 ", attachment=True)
    vechile_image1 = fields.Image(string="Image 2 ", attachment=True)
    vechile_image2 = fields.Image(string="Image 3 ", attachment=True)
    vechile_image3 = fields.Image(string="Image 4 ", attachment=True)
    vechile_image4 = fields.Image(string="Image 5 ", attachment=True)
    vechile_image5 = fields.Image(string="Image 6 ", attachment=True)
    vechile_image6 = fields.Image(string="Image 7 ", attachment=True)
    vechile_image7 = fields.Image(string="Image 8 ", attachment=True)
    vechile_image8 = fields.Image(string="Image 9 ", attachment=True)
    vechile_image9 = fields.Image(string="Image 10 ", attachment=True)
    state = fields.Selection([('new', 'New'), ('confirm', 'Confirm'),
                            ('done', 'Done'), ('cancel', 'Cancel')], default='new', string="status",
                              required=True)
    line_ids =fields.One2many('service.line', 'service_id', string="Service Lines")
    parts_line_ids =fields.One2many('parts.line', 'parts_id', string="Parts Lines")
    line_total = fields.Float(string="Total", compute='_compute_line_total', store=True)
    parts_total = fields.Float(string="Total", compute='_compute_parts_total', store=True)
    grand_total = fields.Float(string="Grand Total", compute='_compute_grand_total', store=True)
    vehicle_name = fields.Char(string='Name')
    c_company = fields.Char(string="Company")

    def set_to_confirm(self):
        self.state = 'confirm'
    def set_to_done(self):
        self.state = 'done'
    def set_to_new(self):
        self.state = 'new'
    def set_to_cancel(self):
        self.state = 'cancel'

    @api.depends('line_ids.amount')
    def _compute_line_total(self):
        for record in self:
            record.line_total = sum(record.line_ids.mapped('amount'))

    @api.depends('parts_line_ids.sub_total')
    def _compute_parts_total(self):
        for record in self:
            record.parts_total = sum(record.parts_line_ids.mapped('sub_total'))

    @api.depends('line_total', 'parts_total')
    def _compute_grand_total(self):
        for record in self:
            record.grand_total = record.line_total + record.parts_total

    def amount_to_words(self):
        for rec in self:
            if rec.grand_total == 0:
                return 'Nil'
            check_amount_in_words = num2words(rec.grand_total)
            check_amount_in_words = string.capwords(check_amount_in_words).replace('And','and')
            check_amount_in_words = check_amount_in_words.replace('Point','point')
            check_amount_in_words = check_amount_in_words + " Rupees Only"
            return check_amount_in_words         
    
    def generate_invoice_report(self):
        for rec in self:
            return rec.env.ref('d_auto_garage.invoice_report_d_auto_garage').report_action(self)

    @api.model
    def send_invoice_report_whatsapp(self):
        # Get the WhatsApp number from the current record
        phone_number = self.phone_num1
        if not phone_number:
            print("phone_number==================", phone_number)
            raise exceptions.UserError("No WhatsApp number provided")

        # Find the report object by its XML ID
        report = self.env.ref('d_auto_garage.invoice_report_d_auto_garage').report_action(self)

        # Render the report
        report_rendered = report.render(self.ids)

        # Set up Twilio client with your credentials
        account_sid = 'your_account_sid'
        auth_token = 'your_auth_token'
        twilio_phone_number = 'your_twilio_phone_number'

        client = Client(account_sid, auth_token)

        # Send the invoice report via WhatsApp
        message = client.messages.create(
            from_='whatsapp:' + twilio_phone_number,
            body='Here is your invoice report:',
            media_url=[report_rendered],
            to='whatsapp:' + phone_number
        )

        return True

    # @api.model
    # def send_invoice_report_whatsapp(self):
    #     # Get the WhatsApp number from the current record
    #     phone_number = self.phone_num1
    #     if not phone_number:
    #         raise exceptions.UserError("No WhatsApp number provided")

    #     # Logic to generate the invoice report
    #     # You can use Odoo's built-in report generation functionality
    #     # to render the invoice report
    #     invoice_report = self.env['ir.actions.report'].sudo().d_auto_garage.invoice_report_d_auto_garage

    #     # Set up Twilio client with your credentials
    #     account_sid = 'your_account_sid'
    #     auth_token = 'your_auth_token'
    #     twilio_phone_number = 'your_twilio_phone_number'

    #     client = Client(account_sid, auth_token)

    #     # Send the invoice report via WhatsApp
    #     message = client.messages.create(
    #         from_='whatsapp:' + twilio_phone_number,
    #         body='Here is your invoice report:',
    #         media_url=[invoice_report],
    #         to='whatsapp:' + phone_number
    #     )

    #     return True
    

class ServiceLine(models.Model):
    _name = "service.line"
    _description = "Service Line"


    service_id = fields.Many2one('service.book', string="Service")
    job_id = fields.Many2one('job.type', string="Job")
    amount = fields.Float(string='Labour')
    carparts_id = fields.Many2one('car.parts', string="Parts") 
    quantity = fields.Float(string='Quantity', default = '1')
    price = fields.Float(string='Parts Amt')
    description = fields.Char(string='Description')
    # job_total = fields.Float(string='Total')

    @api.onchange('job_id')
    def onchange_job_id(self):
        for rec in self:
            if rec.job_id:
                rec.amount = rec.job_id.amount or 0.0

    # @api.depends('quantity','price')
    # def compute_sub_total(self):
    #     for rec in self:
    #         rec.sub_total=rec.quantity * rec.price


class PartseLine(models.Model):
    _name = "parts.line"
    _description = "Parts Line"

    parts_id = fields.Many2one('service.book', string="Services")
    carparts_id = fields.Many2one('car.parts', string="Parts") 
    quantity = fields.Float(string='Quantity', default = '1')
    price = fields.Float(string='Unit Price')
    sub_total = fields.Float(string='Total', compute='compute_sub_total')
    parts_total = fields.Float(string='Total')

    @api.onchange('carparts_id')
    def onchange_carparts_id(self):
        for rec in self:
            if rec.carparts_id:
                rec.price = rec.carparts_id.price or 0.0

    @api.depends('quantity','price')
    def compute_sub_total(self):
        for rec in self:
            rec.sub_total=rec.quantity * rec.price