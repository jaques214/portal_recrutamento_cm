from odoo import fields, models, api
from odoo.http import request


class EstadoCandidatura(models.Model):
    _inherit = "hr.recruitment.stage"

    stage_name = fields.Selection([('submetida', 'Submetida'),
                                   ('analise', 'Em análise'),
                                   ('metodosSelecaoAvaliados', 'Métodos de Seleção Avaliados'),
                                   ('audienciaPrevia', 'Audiência Prévia'),
                                   ('rejeitada', 'Rejeitada'),
                                   ('cancelada', 'Cancelada'), ('selecionada', 'Selecionada')],
                                  string='Estado da Candidatura', default="submetida",
                                  required=True)

    @api.model
    def create(self, values):
        override_create = super(EstadoCandidatura, self).create(values)

        return override_create


class Candidatura(models.Model):
    _inherit = "hr.applicant"

    stage = fields.Selection([('submetida', 'Submetida'),
                              ('analise', 'Em análise'),
                              ('metodosSelecaoAvaliados', 'Métodos de Seleção Avaliados'),
                              ('audienciaPrevia', 'Audiência Prévia'),
                              ('rejeitada', 'Rejeitada'),
                              ('cancelada', 'Cancelada'), ('selecionada', 'Selecionada')],
                             string='Estado da Candidatura', default="submetida", required=True)

    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'hr.applicant')],
                                     string='Attachments')
    avaliacao_id = fields.One2many('odoo_portal_module.selection_method_evaluation', 'candidatura_id',
                                   domain=[('res_model', '=', 'hr.applicant')], string='Métodos de Avaliação',
                                   required=True)
    declaracoes_finais = fields.Char()

    def website_form_input_filter(self, request, values):
        print(values)
        applicant = request.env['hr.applicant'].sudo().search_count(
            [('job_id', '=', values['job_id'])])
        print(values)
        job = request.env['hr.job'].sudo().search([('id', '=', values['job_id'])])
        print("Count", applicant)
        application_count = 0
        if 'partner_name' in values:
            if applicant < 1:
                application_count = 1
            else:
                application_count = applicant + 1
            arg = str(application_count).rjust(4, '0') + " - " + job.name
            values.setdefault('name', arg)
        return values

    # Adicionar candidatura
    @api.model
    def create(self, values):
        values.update({"partner_id": request.env.user.partner_id.id})
        override_create = super(Candidatura, self).create(values)
        override_create['date_open'] = override_create['write_date']
        print("Values", values)
        return override_create

    def write(self, values):
        # your logic goes here
        override_write = super(Candidatura, self).write(values)

        return override_write
