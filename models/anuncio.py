# -*- coding: utf-8 -*-
from odoo import models, fields


class Entidade(models.Model):
    _inherit = "hr.department"


class Anuncio(models.Model):
    _inherit = "hr.job"

    # Atributos
    cod_oferta = fields.Char(string="Código de Oferta", required=True)
    tipoOferta = fields.Selection([('ProcedimentoConcursalIngresso', 'Procedimento Concursal de Ingresso'),
                                   ('ProcedimentoConcursalAcesso', 'Procedimento Concursal de Acesso'),
                                   ('ProcedimentoConcursalEspecial', 'Procedimento Concursal Especial'),
                                   ('ProcedimentoConcursalInternoGeral', 'Procedimento Concursal Interno Geral'),
                                   ('ProcedimentoConcursalComum', 'Procedimento Concursal Comum'),
                                   ('ProcedimentoConcursalInternoCondicionado',
                                    'Procedimento Concursal Interno Condicionado'),
                                   ('ProcedimentoConcursalConstituicaoReservaOrgao',
                                    'Procedimento Concursal para Constituição de Reserva de Órgão/Serviço')],
                                  string='Tipo de Oferta', default="ProcedimentoConcursalComum", required=True)
    job_state = fields.Selection([('aberto', 'Aberto'), ('preselecao', 'Pré - Seleção dos candidatos'),
                              ('avaliacaoCandidato', 'Avaliação dos Candidatos'),
                              ('selecaoCandidatos', 'Seleção dos Candidatos'), ('finalizado', 'Finalizado'),
                              ('cancelado', 'Cancelado')], string='Job Status', readonly=True,
                             required=True, default='aberto')
    orgao = fields.Char(string="Orgão/Serviço", required=False)
    modalidade_vinculo = fields.Char(string="Modalidade de Vínculo", required=False)
    regime = fields.Char(string="Regime", required=False)
    grau_complexidade = fields.Integer(string="Grau de Complexidade", required=False)
    remuneracao = fields.Text(string="Remuneração", required=False)
    suplemento_mensal = fields.Float(string="Suplemento Mensal", required=False)
    relacao_juridica = fields.Text(string="Relação Jurídica", required=False)
    requisitos_constituicao_juridica = fields.Text(string="Requisitos para a Constituição de Relação Jurídica",
                                                   required=False)
    autorizacao_artigo = fields.Text(string="Autorização dos membros do Governo Artigo 30º LTFP", required=False)
    requisitos_nacionalidade = fields.Boolean(string="Requisitos de Nacionalidade", required=False)
    nivel_organico = fields.Char(string="Nível Orgânico", required=False)
    entity = fields.Char(string="Entidade", required=True)
    apply_start_date = fields.Date(string="Data Início das Candidaturas", required=True)
    apply_end_date = fields.Date(string="Prazo para Candidaturas", required=True)
    nivel_habitacional_exigido = fields.Text("Nível Habilitacional Exigido", required=True)
    metodo_selecao_id = fields.One2many('odoo_portal_module.selection_method', 'job_id',
                                        domain=[('res_model', '=', 'hr.job')], string='Métodos de Seleção',
                                        required=True)
    juri_id = fields.One2many('odoo_portal_module.juri', 'job_id', domain=[('res_model', '=', 'hr.job')],
                              string='Júri', required=True)
    address = fields.Text("Address", required=True)
    workplace_address = fields.Text("Workplace_address", required=True)
    local_candidatura = fields.Char("Local para a Candidatura", required=True)
    forma_candidatura = fields.Char("Forma da Candidatura", required=False)
    ato_autorizacao = fields.Char(string='Ato de Autorização', required=False)
    restricao_procedimento_concursal = fields.Text(string="Restrição Procedimento Concursal", required=False)
    substituto_nivel_habilitacional = fields.Char(string="Substituição do Nível habilitacional", required=False)
    candidatos_sem_admissao = fields.Char(string="Candidatos que não podem ser admitidos", required=False)
    formula_classificacao_final = fields.Text(string="Fórmula da Classificação Final", required=False)
    forma_publicitacao = fields.Char(string="Forma Publicitação da Lista Unitária Final", required=False)
    quota_deficiencia = fields.Integer(string="Quota para Portadores de Deficiência", required=False)
    documentos_exigidos_id = fields.One2many('odoo_portal_module.required_documents', 'job_id',
                                             string='Documentos Exigidos', onDelete="cascade", required=True)
