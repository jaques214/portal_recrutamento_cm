from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Juri(models.Model):
    _name = 'odoo_portal_module.juri'
    _description = 'Juri'

    name = fields.Char()
    funcao = fields.Char()
    res_model = fields.Char('Resource Model', readonly=True,
                            help="The database object this attachment will be attached to.")
    job_id = fields.Many2oneReference('Job ID', model_field='res_model',
                                      readonly=True, help="The record id this is attached to.")


class SelectionMethod(models.Model):
    _name = 'odoo_portal_module.selection_method'
    _description = 'Selection Method'

    descricao = fields.Char()
    sigla = fields.Char()
    nome_metodo = fields.Char()
    ponderacao = fields.Integer()
    valoracao_minima = fields.Float()
    valor_avaliacao = fields.Integer()
    res_model = fields.Char('Resource Model', readonly=True,
                            help="The database object this attachment will be attached to.")
    job_id = fields.Many2oneReference('Job ID', model_field='res_model',
                                      readonly=True, help="The record id this is attached to.")

    @api.constrains('valor_avaliacao')
    def _check_value(self):
        if self.field_name >= 0 or self.field_name <= 20:
            raise ValidationError('Enter Value Between 0-20.')


class SelectionMethodEvaluation(models.Model):
    _name = 'odoo_portal_module.selection_method_evaluation'
    _description = 'Selection Method Evaluation'

    nome_metodo = fields.Char(string="Método de Seleção")
    titulo_candidatura = fields.Char(string="Candidatura")
    date_time = fields.Datetime(string="Data e Hora")
    valor_avaliacao = fields.Integer(string="Valor Avaliação")
    ponderacao = fields.Integer(string="Ponderação")
    valor_ponderado_avaliacao = fields.Float(string="Valor Ponderado da Avaliação")
    res_model = fields.Char('Resource Model', readonly=True,
                            help="The database object this attachment will be attached to.")
    candidatura_id = fields.Many2oneReference('ID da Candidatura', model_field='res_model',
                                              readonly=True, help="The record id this is attached to.")
