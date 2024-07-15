# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CarParts(models.Model):
    _name = "car.parts"
    _description = "Car Parts"

    name = fields.Char(string='Name', required=True)
    price = fields.Float(String='Price')
