# -*- coding: utf-8 -*-
from odoo import http, tools, _
from odoo.http import request

class WebsiteHelatHer(http.Controller):
    
    @http.route(['/page/symptom-tool'], type='http', auth="public", website=True)
    def screening(self, **kwargs):
        values = {}
        return request.render("healt_her_website.symptom_tool",values)
    
    @http.route(['/page/products'], type='http', auth="public", website=True)
    def donor_videos(self, **kwargs):
        values = {}
        return request.render("healt_her_website.products",values)
    
    @http.route(['/page/magazine'], type='http', auth="public", website=True)
    def prices(self, **kwargs):
        values = {}
        return request.render("healt_her_website.magazine",values)
    
    @http.route(['/page/expert-advice'], type='http', auth="public", website=True)
    def faq(self, **kwargs):
        values = {}
        return request.render("healt_her_website.expertAdvice",values)
    
    @http.route(['/page/about-us'], type='http', auth="public", website=True)
    def aboutus(self, **kwargs):
        values = {}
        return request.render("healt_her_website.aboutus",values)
    

    
    