from odoo import models, fields, api
from datetime import datetime



_STATES = [
    ('draft', 'Draft'),
    ('to_approve', 'To be checked'),
    ('approved', 'Checked'),
    ('rejected', 'Rejected'),
    ('done', 'Done'),
    ('unfulfilled','unFulfilled'),
('fulfilled','Fulfilled')
]


class purchase_request_extend(models.Model):
    _inherit="purchase.request"


    send_to = fields.Selection([(
		'procurement','Procurement'),('batching','Batching Plant')],default="procurement")
    state2 = fields.Selection([('unfulfilled','unFulfilled'),('fulfilled','Fulfilled')],default="unfulfilled")
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             index=True,
                             track_visibility='onchange',
                             required=True,
                             copy=False,
                             default='draft')



class SalesOrderExtend(models.Model):
    _inherit = "sale.order"

    name = fields.Text(string='Description')
    purchase_request_id = fields.Many2one('purchase.request',string="Purchase Request")

    @api.onchange('purchase_request_id')
    def _compute_sale_line_new(self):
        for rec in self:
            lines = []
            for request in rec.purchase_request_id.line_ids:
                lines.append((0, 0, {
                    'product_id':request.product_id.id,
                    'product_uom_qty': request.product_qty,
                     'product_uom':request.product_id.uom_id.id,
		     'name':request.product_id.name,
              })
	      )
            rec.order_line = lines



class BatchingPlantClass(models.Model):
    _name = "bp.production"


    name = fields.Char()
    production_date = fields.Date(string="Date of Production")
    created_by = fields.Many2one('res.users',string="Created By")
    purchase_request_id = fields.Many2one('purchase.request',string="Purchase Request Reference")
    production_line = fields.One2many('bp.production.line','id',string="Production line",store=True)
    state = fields.Selection([('draft','Draft'),('posted','Posted')],default='draft')
    #stock_location_id = fields.Many2one('stock.location',string="Stock Location")


    @api.multi
    def update_inventory_action(self):
        #update stock
        for a in self.production_line:
            move = self.env['stock.move'].create({
               'name': 'Batching Plant',
               'location_id': a.stock_location_id.id,
               'location_dest_id':a.stock_location_id.id,
               'product_id': a.product_id.id,
               'product_uom': a.product_id.uom_id.id,
               'product_uom_qty': a.qty_produced,
                })
            move.action_confirm()
            move.action_assign()
            #move.move_line_ids.write({'qty_done': a.qty_produced}) # This creates a stock.move.line record. You could also do it manually
            #move.action_done()

        self.purchase_request_id.write({'state':'fulfilled'})
        self.write({'state':'posted'})

class BatchingPlantLineClass(models.TransientModel):
    _name= "bp.production.line"


    product_id = fields.Many2one('product.product',string="Product")
    qty_produced = fields.Float(string="Quantity Produced")
    stock_location_id = fields.Many2one('stock.location',string="Stock Location")

