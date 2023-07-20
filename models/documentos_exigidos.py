from odoo import fields, models


class RequiredDocuments(models.Model):
    _name = 'odoo_portal_module.required_documents'
    _description = 'Documentos Exigidos'

    nome_anexo = fields.Char(string="Nome do Documento", required=True)
    descricao = fields.Text(string="Descrição", required=True)
    job_id = fields.Many2one("hr.job", string="Job ID")
