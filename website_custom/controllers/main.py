from odoo import http
from odoo.http import request

class WebsiteCustom(http.Controller):
    @http.route('/', auth='public', website=True)
    def index(self):
        return request.render('website_custom.website_custom_homepage')
