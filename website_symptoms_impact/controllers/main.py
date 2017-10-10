import json
import logging
from werkzeug.exceptions import Forbidden
 
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.base.ir.ir_qweb.fields import nl2br
from odoo.addons.website.models.website import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import ValidationError
from odoo.addons.website_form.controllers.main import WebsiteForm
 
_logger = logging.getLogger(__name__)
 
CPG = 20  # Category Per Page
CPR = 4   # Category Per Row

SPG = 20  # Symptoms Per Page
SPR = 4   # Symptoms Per Row

class CategoryTableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= CPR:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(CPR):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, categories, cpg=CPG):
        # Compute category positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        for p in categories:
            x = min(max(p.website_size_x, 1), CPR)
            y = min(max(p.website_size_y, 1), CPR)
            if index >= cpg:
                x = y = 1
            pos = minpos
            while not self._check_place(pos % CPR, pos / CPR, x, y):
                pos += 1
            # if 21st cateogry  (index 20) and the last line is full (CPR cateogry in it), break
            # (pos + 1.0) / CPR is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= cpg and ((pos + 1.0) / CPR) > maxy:
                break
            if x == 1 and y == 1:   # simple heuristic for CPU optimization
                minpos = pos / CPR
            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos / CPR) + y2][(pos % CPR) + x2] = False
            self.table[pos / CPR][pos % CPR] = {
                'category': p, 'x': x, 'y': y,
            }
            if index <= cpg:
                maxy = max(maxy, y + (pos / CPR))
            index += 1

        # Format table according to HTML needs
        rows = self.table.items()
        rows.sort()
        rows = map(lambda x: x[1], rows)
        for col in range(len(rows)):
            cols = rows[col].items()
            cols.sort()
            x += len(cols)
            rows[col] = [c for c in map(lambda x: x[1], cols) if c]
        return rows

class SymptomsTableCompute(object):
 
    def __init__(self):
        self.table = {}
 
    def _check_place(self, posx, posy, sizex, sizey):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= SPR:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(SPR):
                self.table[posy + y].setdefault(x, None)
        return res
 
    def process(self, symptoms, spg=SPG):
        # Compute category positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        for p in symptoms:
            x = min(max(p.website_size_x, 1), CPR)
            y = min(max(p.website_size_y, 1), CPR)
            if index >= spg:
                x = y = 1
            pos = minpos
            while not self._check_place(pos % CPR, pos / CPR, x, y):
                pos += 1
            # if 21st cateogry  (index 20) and the last line is full (CPR cateogry in it), break
            # (pos + 1.0) / CPR is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= spg and ((pos + 1.0) / SPR) > maxy:
                break
            if x == 1 and y == 1:   # simple heuristic for CPU optimization
                minpos = pos / SPR
            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos / SPR) + y2][(pos % SPR) + x2] = False
            self.table[pos / SPR][pos % SPR] = {
                'symptom': p, 'x': x, 'y': y,
            }
            if index <= spg:
                maxy = max(maxy, y + (pos / SPR))
            index += 1
 
        # Format table according to HTML needs
        rows = self.table.items()
        rows.sort()
        rows = map(lambda x: x[1], rows)
        for col in range(len(rows)):
            cols = rows[col].items()
            cols.sort()
            x += len(cols)
            rows[col] = [c for c in map(lambda x: x[1], cols) if c]
        return rows   
 
class WebsiteSymptoms(http.Controller):
 
    @http.route(['/page/symptoms_category','/page/symptoms/<model("symptoms.category"):categories>'], type='http', auth="public", website=True)
    def symptoms_category(self, page=0, category=None, search='', cpg=False, **post):
        if cpg:
            try:
                cpg = int(cpg)
            except ValueError:
                cpg = CPG
            post["cpg"] = cpg
        else:
            cpg = CPG
        Categories = request.env['symptoms.category']
        categories = Categories.search([],limit=cpg)
        values = {
            'categories': categories,
            'bins': CategoryTableCompute().process(categories, cpg),
            'rows': CPR,
        }
        return request.render("website.symptoms_category", values)
    
    @http.route(['/page/symptoms/<model("symptoms.category"):categories>'], type='http', auth="public", website=True)
    def symptoms(self, categories, category='', search='', spg=False,  **kwargs):
        if spg:
            try:
                spg = int(spg)
            except ValueError:
                spg = SPG
            post["spg"] = spg
        else:
            spg = SPG
        count = len(categories)
        Symptoms = request.env['symptoms.symptoms']
        symptoms = Symptoms.search([('category_ids','in',categories.id)],limit=spg)
        print symptoms
        values = {
            'symptoms': symptoms,
            'bins': SymptomsTableCompute().process(symptoms, spg),
            'rows': SPR,
            'categories': categories
        }
        return request.render("website.symptoms", values)
