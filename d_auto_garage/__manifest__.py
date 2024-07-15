# -*- encoding: utf-8 -*-
##############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Malabar Auto Garage',
    'version': '16.0.0.0.1',
    'category': 'Accounting',
    'summary': 'Malabar Auto Garage',
    'description': """
                    This Module contains customisations done for Malabar Auto Garage.
                    """,
    'author': 'Destiny  ',
    'license': "LGPL-3",
    'website': '',
    'depends': ['base','sale','purchase'],
    'data': [
            'security/ir.model.access.csv',
            'reports/reports.xml',
            'reports/service_book_template.xml',
            'reports/invoice_report.xml',
            'views/service_book_view.xml',
            'views/job_type_view.xml',
            'views/carparts_views.xml',
        ],
    'test':  [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
