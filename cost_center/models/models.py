# -*- coding: utf-8 -*-

from odoo import models, fields, api


class journal_entry_inherit(models.Model):
      _inherit="account.move.line"


      @api.model
      def _query_get(self, domain=None):
          context = dict(self._context or {})
          domain = domain or []
          if not isinstance(domain, (list, tuple)):
              domain = safe_eval(domain)

          date_field = 'date'
          if context.get('aged_balance'):
              date_field = 'date_maturity'
          if context.get('date_to'):
              domain += [(date_field, '<=', context['date_to'])]
          if context.get('date_from'):
              if not context.get('strict_range'):
                  domain += ['|', (date_field, '>=', context['date_from']), ('account_id.user_type_id.include_initial_balance', '=', True)]
              elif context.get('initial_bal'):
                  domain += [(date_field, '<', context['date_from'])]
              else:
                  domain += [(date_field, '>=', context['date_from'])]

          if context.get('journal_ids'):
              domain += [('journal_id', 'in', context['journal_ids'])]

          state = context.get('state')
          if state and state.lower() != 'all':
              domain += [('move_id.state', '=', state)]

          if context.get('company_id'):
              domain += [('company_id', '=', context['company_id'])]

          if 'company_ids' in context:
              domain += [('company_id', 'in', context['company_ids'])]
  
          if context.get('reconcile_date'):
              domain += ['|', ('reconciled', '=', False), '|', ('matched_debit_ids.create_date', '>', context['reconcile_date']), ('matched_credit_ids.create_date', '>', context['reconcile_date'])]

          if context.get('account_tag_ids'):
              domain += [('account_id.tag_ids', 'in', context['account_tag_ids'].ids)]

          if context.get('analytic_tag_ids'):
              domain += ['|', ('analytic_account_id.tag_ids', 'in', context['analytic_tag_ids'][0]), ('analytic_tag_ids', 'in', context['analytic_tag_ids'][0])]

          if context.get('analytic_label_id'):
              domain += ['|', ('analytic_account_id.label_id', 'in', context['analytic_label_id'][0]), ('analytic_label_id', 'in', context['analytic_label_id'][0])]

          if context.get('analytic_account_id'):
              domain += [('analytic_account_id', 'in', context['analytic_account_id'])]

          where_clause = ""
          where_clause_params = []
          tables = ''
          if domain:
              query = self._where_calc(domain)
              tables, where_clause, where_clause_params = query.get_sql()
          return tables, where_clause, where_clause_params     


class balance_inherit(models.TransientModel):
      _inherit="account.balance.report"


      analytic_tag_ids = fields.Many2many('account.analytic.tag', 'account_balance_report_analytic_tag_ids_rel', 'account_id','analytic_tag_ids', string='Analytic tags')
      analytic_account_id = fields.Many2many('account.analytic.account','account_balance_report_analytic_account_id_rel', 'account_id','analytic_account_id', string='Analytic Account')
      analytic_label_id = fields.Many2many('material.label','account_balance_report_analytic_label_id_rel', 'account_id', 'analytic_label_id', string="Analytic Label")


class accountcommon_report_inherit(models.TransientModel):
      _inherit="account.common.report"


      def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        result['analytic_tag_ids'] = 'analytic_tag_ids' in data['form'] and data['form']['analytic_tag_ids'] or False
	result['analytic_account_id'] = 'analytic_account_id' in data['form'] and data['form']['analytic_account_id'] or False
        result['analytic_label_id'] = 'analytic_label_id' in data['form'] and data['form']['analytic_label_id'] or False

        return result

      @api.multi
      def check_report(self):
          self.ensure_one()
          data = {}
          data['ids'] = self.env.context.get('active_ids', [])
          data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
          data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move','analytic_tag_ids','analytic_account_id','analytic_label_id'])[0]
          print(data)
          used_context = self._build_contexts(data)
          data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
          return self._print_report(data)


class financial_account_report_inherit(models.TransientModel):
    _inherit="accounting.report"

    analytic_tag_ids = fields.Many2many('account.analytic.tag', 'accounting_report_analytic_tag_ids_rel', 'account_id','analytic_tag_ids', string='Analytic tags')
    analytic_account_id = fields.Many2many('account.analytic.account','accounting_report_analytic_account_id_rel', 'account_id','analytic_account_id', string='Analytic Account')
    analytic_label_id = fields.Many2many('material.label','accounting_report_analytic_label_id_rel', 'account_id', 'analytic_label_id', string='Analytic Label')



    def _build_comparison_context(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['analytic_tag_ids'] = 'analytic_tag_ids' in data['form'] and data['form']['analytic_tag_ids'] or False
        result['analytic_account_id'] = 'analytic_account_id' in data['form'] and data['form']['analytic_account_id'] or False
	result['analytic_label_id'] = 'analytic_label_id' in data['form'] and data['form']['analytic_label_id'] or False


	if data['form']['filter_cmp'] == 'filter_date':
            result['date_from'] = data['form']['date_from_cmp']
            result['date_to'] = data['form']['date_to_cmp']
            result['strict_range'] = True
        return result
    
    @api.multi
    def check_report(self):
        res = super(financial_account_report_inherit, self).check_report()
        data = {}
        data['form'] = self.read(['account_report_id', 'date_from_cmp', 'date_to_cmp', 'journal_ids', 'filter_cmp', 'target_move','analytic_tag_ids','analytic_account_id', 'analytic_label_id'])[0]
        for field in ['account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(data)
        res['data']['form']['comparison_context'] = comparison_context
        return res

    def _print_report(self, data):
        data['form'].update(self.read(['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter', 'target_move','analytic_tag_ids','analytic_account_id','analytic_label_id'])[0])
        return self.env['report'].get_action(self, 'account.report_financial', data=data)




        
