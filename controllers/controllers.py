# -*- coding: utf-8 -*-
import base64
import json
import xmlrpc.client
from datetime import date
import datetime
import requests
from odoo.addons.http_routing.models.ir_http import slugify
import werkzeug
from werkzeug.exceptions import NotFound, BadRequest
from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.addons.odoo_portal_module.models.selection_method import Juri, SelectionMethod, SelectionMethodEvaluation
from odoo.addons.website.controllers.main import Website
from odoo.exceptions import ValidationError, UserError, _logger
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment
from odoo.http import request, route
from odoo.addons.hr.models.hr_job import Job
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website_form.controllers.main import WebsiteForm

creatio = "https://148.69.67.24:8001"


class PortalRh(http.Controller):
    srv = "http://localhost:8069"
    dbname = request.env.cr.dbname
    username = "jaquesafr@gmail.com"
    password = "postgres"

    @http.route('/anuncio/publicarAnuncio/', auth='api_key', methods=['POST'], type='json')
    def publicarAnuncio(self, **kw):
        data = http.request.jsonrequest

        temp = data
        state = temp['state']

        data.update({
            'job_state': state
        })

        data.pop('state')

        common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % self.srv)
        api = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % self.srv)

        uid = common.login(self.dbname, self.username, self.password)

        anuncio_juri = api.execute_kw(self.dbname, uid, self.password, Juri._name, 'create',
                                      [data["juri_id"]])

        anuncio_metodo_selecao = api.execute_kw(self.dbname, uid, self.password, SelectionMethod._name, 'create',
                                                [data["metodo_selecao_id"]])

        anuncio_documentos = api.execute_kw(self.dbname, uid, self.password, "odoo_portal_module.required_documents",
                                            'create', [data["documentos_exigidos_id"]])

        data["juri_id"] = anuncio_juri
        data["metodo_selecao_id"] = anuncio_metodo_selecao
        data["documentos_exigidos_id"] = anuncio_documentos

        id_anuncio_record = api.execute_kw(self.dbname, uid, self.password, Job._name, 'create',
                                           [data])

        return id_anuncio_record

    @http.route('/anuncio/updateAnuncio', auth='api_key', methods=['PUT'], type='json')
    def updateAnuncio(self, **kw):
        data = http.request.jsonrequest

        temp = data
        state = temp['state']

        temp.update({
            'job_state': state
        })

        temp.pop('state')

        common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % self.srv)
        api = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % self.srv)

        domain = [("cod_oferta", "=", data["cod_oferta"])]

        uid = common.login(self.dbname, self.username, self.password)

        id = api.execute_kw(self.dbname, uid, self.password, Job._name, "search", [domain])

        api.execute_kw(self.dbname, uid, self.password, Job._name, "write", [id,
                                                                       temp])
        job = request.env['hr.job'].sudo().browse(id)

        if job.job_state == "finalizado":
            job.state = "open"

        # get record name after having changed it
        new_record = api.execute_kw(self.dbname, uid, self.password, Job._name, 'name_get', [id])
        return new_record

    @http.route('/candidatura/avaliacaoCandidato/', auth='api_key', methods=['POST'], type='json')
    def avaliacaoCandidato(self, **kw):
        data = http.request.jsonrequest

        common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % self.srv)
        api = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % self.srv)

        uid = common.login(self.dbname, self.username, self.password)

        job_id = api.execute_kw(self.dbname, uid, self.password, 'hr.job', "search",
                                [[("cod_oferta", "=", data["cod_oferta"])]], {'limit': 1})

        partner_id = api.execute_kw(self.dbname, uid, self.password, 'res.partner', "search",
                                    [[("cc", "=", data["cc"])]], {'limit': 1})

        id = api.execute_kw(self.dbname, uid, self.password, 'hr.applicant', 'search_read',
                            [[('job_id', '=', job_id[0]), ('partner_id', '=', partner_id[0])]])

        final_id = id[0]['id']

        body = data
        body.pop('cod_oferta')
        body.pop('cc')

        new_record = []
        for evaluation in body['avaliacao_id']:
            evaluation.update({"candidatura_id": final_id, "res_model": "hr.applicant"})
            date_time = datetime.datetime.strptime(evaluation["date_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
            evaluation["date_time"] = date_time
            evaluation_ids = api.execute_kw(self.dbname, uid, self.password, SelectionMethodEvaluation._name, "create",
                                            [evaluation])
            new_record.append(evaluation_ids)

        # get record
        return new_record

    @http.route('/candidatura/updateCandidatura', auth='api_key', methods=['PUT'], type='json')
    def updateCandidatura(self, **kw):
        data = http.request.jsonrequest

        common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % self.srv)
        api = xmlrpc.client.ServerProxy('%s/xmlrpc/2/object' % self.srv)

        uid = common.login(self.dbname, self.username, self.password)

        job_id = api.execute_kw(self.dbname, uid, self.password, 'hr.job', "search",
                                [[("cod_oferta", "=", data["cod_oferta"])]], {'limit': 1})

        partner_id = api.execute_kw(self.dbname, uid, self.password, 'res.partner', "search",
                                    [[("cc", "=", data["cc"])]], {'limit': 1})

        id = api.execute_kw(self.dbname, uid, self.password, 'hr.applicant', 'search_read',
                            [[('job_id', '=', job_id[0]), ('partner_id', '=', partner_id[0])]])

        final_id = id[0]['id']

        domain = [("candidatura_id", "=", final_id)]

        avaliacao_candidatura = api.execute_kw(self.dbname, uid, self.password, SelectionMethodEvaluation._name,
                                               "search_read", [domain],
                                               {'fields': ['nome_metodo'], "order": "nome_metodo asc"})

        if 'stage' in data.keys() and 'avaliacao_id' not in data.keys():
            body_state = {
                "stage": data.get('stage')
            }
            api.execute_kw(self.dbname, uid, self.password, 'hr.applicant', "write",
                           [[final_id], body_state])
        elif 'avaliacao_id' in data.keys() and 'stage' not in data.keys():
            body = data
            body.pop('cod_oferta')
            body.pop('cc')

            sorted_avaliacao = sorted(body['avaliacao_id'], key=lambda avaliacao: avaliacao["nome_metodo"])

            for i in range(len(avaliacao_candidatura)):
                evaluation_id = avaliacao_candidatura[i]['id']
                api.execute_kw(self.dbname, uid, self.password, SelectionMethodEvaluation._name, "write",
                               [[evaluation_id], sorted_avaliacao[i]])

        elif 'stage' in data.keys() and 'avaliacao_id' in data.keys():
            body_state = {
                "stage": data.get('stage')
            }
            api.execute_kw(self.dbname, uid, self.password, 'hr.applicant', "write",
                           [[final_id], body_state])

            body = data
            body.pop('cod_oferta')
            body.pop('cc')

            sorted_avaliacao = sorted(body['avaliacao_id'], key=lambda avaliacao: avaliacao["nome_metodo"])

            for i in range(len(avaliacao_candidatura)):
                evaluation_id = avaliacao_candidatura[i]['id']
                api.execute_kw(self.dbname, uid, self.password, SelectionMethodEvaluation._name, "write",
                               [[evaluation_id], sorted_avaliacao[i]])

        # get record name after having changed it
        new_record = api.execute_kw(self.dbname, uid, self.password, 'hr.applicant', 'name_get', [final_id])
        print("New Record", new_record)
        return new_record

    @http.route('/applications', auth='user', website=True, type="http")
    def show_applications(self, **kw):
        candidaturas = request.env['hr.applicant'].sudo().search([('partner_id', '=', request.env.user.partner_id.id)])
        print(candidaturas)
        stages = request.env['hr.applicant']._fields['stage'].selection
        candidatura_stage = ""
        for candidatura in candidaturas:
            for stage in stages:
                if stage[0] == candidatura.stage:
                    candidatura_stage = stage[1]
        return http.request.render('odoo_portal_module.page', {
            'candidaturas': candidaturas,
            'candidatura_stage': candidatura_stage
        })

    @http.route('/jobs/history', auth='user', website=True, type="http")
    def show_history(self, **kw):
        today = date.today()
        print(today)
        jobs = request.env['hr.job'].sudo().search([('is_published', '=', True),
                                                    '|', ('job_state', '=', 'cancelado'), ('job_state', '=', 'finalizado')])
        print(jobs)
        return http.request.render('odoo_portal_module.history', {
            'old_jobs': jobs
        })

    @http.route("/application/detail/<int:candidatura_id>", auth='user', website=True, type="http")
    def show_application_detail(self, candidatura_id, **kw):
        candidatura = request.env['hr.applicant'].sudo().search([('id', '=', candidatura_id)])
        num_attachments = request.env['ir.attachment'].sudo().search_count([('res_id', '=', candidatura_id)])
        print(candidatura.job_id.id)
        documents = request.env['odoo_portal_module.required_documents'].sudo().search_count([('job_id', '=',
                                                                                               candidatura.job_id.id)])
        stages = request.env['hr.applicant']._fields['stage'].selection
        candidatura_stage = ""
        for stage in stages:
            if stage[0] == candidatura.stage:
                candidatura_stage = stage[1]

        print("Num documents", documents)
        print(num_attachments)
        date_open = candidatura.date_open.strftime("%d/%m/%Y %H:%M")
        # date = datetime.date(candidatura.date_open.year, 5, 12)
        avaliacao = request.env['odoo_portal_module.selection_method_evaluation'].sudo().search(
            [('candidatura_id', '=', int(candidatura.id))])
        num_avaliacao = request.env['odoo_portal_module.selection_method_evaluation'].sudo().search_count(
            [('candidatura_id', '=', int(candidatura.id))])

        print("Job State", candidatura.job_id.job_state)

        anexos_principais = []
        if documents > 0:
            for doc in range(documents):
                for x in candidatura.attachment_ids:
                    if x.name[:3] == str(doc + 1).rjust(3, '0'):
                        anexos_principais.append(x)
            print("anexos_principais", anexos_principais)

        outros_anexos = [x for x in candidatura.attachment_ids if
                         x.name[:3] == str(documents + 1).rjust(3, '0')]

        print("outros_anexos", outros_anexos)

        nivel_habitacional = candidatura.partner_id._fields['nivel_habitacional'].selection
        print(list(dict(nivel_habitacional).values()))
        print(list(dict(nivel_habitacional).keys()))

        for key, value in dict(nivel_habitacional).items():
            if key == candidatura.partner_id.nivel_habitacional:
                nivel_habitacional = value

        #link = unidecode.unidecode(candidatura.job_id.name.lower().replace(' ', '-'))
        link = slugify(candidatura.job_id.name)

        return http.request.render('odoo_portal_module.detail_page', {
            'candidatura': candidatura,
            'nivel_habitacional': nivel_habitacional,
            'date_open': date_open,
            'candidatura_stage': candidatura_stage,
            'anexos_principais': anexos_principais,
            'outros_anexos': outros_anexos,
            'avaliacao': avaliacao,
            'link': link,
            'num_avaliacao': num_avaliacao,
            'documents': documents,
            'num_attachments': num_attachments
        })

    @http.route('''/attachments/form/update/''', type='http', auth="public",
                website=True, csrf=False)
    def attachments_form_update(self, **post):
        documents = request.httprequest.files

        res = request.httprequest.referrer.split("/")
        candidatura_id = res[len(res) - 1]
        candidatura = request.env['hr.applicant'].sudo().search([("id", "=", candidatura_id)])
        num_documents_exigidos = request.env['odoo_portal_module.required_documents'].sudo().search_count(
            [('job_id', '=', candidatura.job_id.id)])
        # docs = []

        for doc in documents:
            post[doc].filename = str(num_documents_exigidos + 1).rjust(3, '0') + "_" + post[doc].filename

            fileStorage = post[doc]
            file_name = fileStorage.filename
            file_content = base64.b64encode(fileStorage.read())
            file_length = len(file_content)

            # New Doc
            new_doc = {
                'name': file_name,
                'res_model': 'hr.applicant',
                'type': 'binary',
                'datas': str(file_content.decode()),
                'res_id': candidatura_id,
                'file_size': file_length
            }

            attachment = request.env['ir.attachment'].sudo().create(new_doc)

        request.env['hr.applicant'].sudo().write({
            "attachment_ids": attachment
        })

        return request.render('odoo_portal_module.tmp_customer_form_success', {
            "attachment_ids": attachment
        })


class Website(Website):
    @http.route(auth='public')
    def index(self, **kw):
        super(Website, self).index()
        return http.redirect_with_hash('/jobs')


class PortalAuthSignup(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                elif request.env["res.partner"].sudo().search([("cc", "=", qcontext.get("cc"))]):
                    print(request.env["res.partner"].sudo().search([("cc", "=", qcontext.get("cc"))]))
                    qcontext["error"] = "Another user is already registered using this cc."
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

                for context in qcontext.items():
                    if not context:
                        qcontext['error'] = "Field " + context + "is null"

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def get_auth_signup_qcontext(self):
        qcontext = super(PortalAuthSignup, self).get_auth_signup_qcontext()
        # Get cc from request.params
        partner = request.env['res.partner']
        qcontext['partner'] = partner._fields['nivel_habitacional'].selection
        qcontext['cc'] = request.params.get('cc') or ''
        qcontext['bday'] = request.params.get('bday') or ''
        qcontext['genero'] = request.params.get('genero') or ''
        qcontext['vat'] = request.params.get('vat') or ''
        qcontext['nivel_habitacional'] = request.params.get('nivel_habitacional') or ''
        qcontext['mobile'] = request.params.get('mobile') or ''
        qcontext['street'] = request.params.get('street') or ''
        qcontext['zip'] = request.params.get('zip') or ''
        qcontext['city'] = request.params.get('city') or ''
        qcontext['addressType'] = request.params.get('addressType') or ''
        qcontext['area_formacao'] = request.params.get('area_formacao') or ''

        return qcontext

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'cc', 'bday', 'genero', 'vat',
                                                     'nivel_habitacional', 'mobile', 'street', 'zip', 'city',
                                                     'addressType', 'area_formacao')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()


class WebsiteFormCandidatura(WebsiteForm):
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True,
                csrf=False)
    def website_form(self, model_name, **kwargs):
        anuncio = request.env['hr.job'].sudo().search([('id', '=', kwargs['job_id'])])
        contact = request.env['res.partner'].sudo().search([('id', '=', request.env.user.partner_id.id)])
        job_id = kwargs['job_id']
        name = request.env.user.partner_id.name
        applicant = request.env['hr.applicant'].sudo().search_count(
            [('job_id', '=', job_id), ('partner_name', '=', name)])
        dados = {
            "partner_name": name,
            "email_from": request.env.user.partner_id.email,
            "partner_id": contact
        }
        kwargs.update(dados)

        applicant_count = applicant
        if model_name == 'hr.applicant' and applicant < 1:
            json_login = json.dumps({'Username': 'Supervisor', 'UserPassword': 'Supervisor'})
            url_login = creatio + "/ServiceModel/AuthService.svc/Login"
            login_headers = {"Content-Type": 'application/json', "ForceUseSession": 'true'}
            login_response = requests.post(url_login, data=json_login, headers=login_headers, verify=False)

            # Cookies
            login_cookies = login_response.cookies.get_dict()

            # Login Request Data
            print("***** LOGIN REQUEST DATA *****")
            print("Login Body:", json_login)
            print("Login Request Cookies:")
            print(".ASPXAUTH:\n", login_cookies.get('.ASPXAUTH'))
            print("BPMCSRF:\n", login_cookies.get('BPMCSRF'))
            print("CsrfToken:\n", login_cookies.get('CsrfToken'))
            print("Login Status Code:", login_response.status_code)

            # aspxauth_token = login_cookies.get('.ASPXAUTH')
            bpmcsrf = login_cookies.get('BPMCSRF')
            # csrf_token = login_cookies.get('CsrfToken')

            # Documents Files
            documents = request.httprequest.files
            docs = []

            j = 1
            for doc in documents:
                if "Resume" in doc:
                    kwargs[doc].filename = str(len(anuncio.documentos_exigidos_id) + 1).rjust(3, '0') + "_" + kwargs[
                        doc].filename
                else:
                    kwargs[doc].filename = str(j).rjust(3, '0') + "_" + kwargs[doc].filename

                j = j + 1
                fileStorage = kwargs[doc]
                file_name = fileStorage.filename
                file_content = base64.b64encode(fileStorage.read())
                file_length = len(file_content)

                # New Doc
                new_doc = {
                    "Name": str(file_name),
                    "Data": str(file_content.decode()),
                    "Size": file_length
                }

                partner_attachments = {
                    'name': new_doc.get("Name"),
                    'res_model': 'res.partner',
                    'datas': new_doc.get("Data"),
                    'res_id': contact.id,
                    'file_size': new_doc.get("Size")
                }

                request.env['ir.attachment'].sudo().create(partner_attachments)

                # Add to new_doc to docs
                docs.append(new_doc)

            # Create Candidatura
            url_method = creatio + "/0/rest/ImdCustomServiceGestaoCandidaturas/submeterCandidatura"
            method_headers = {'Content-Type': 'application/json', "BPMCSRF": f'{bpmcsrf}'}
            method_body = json.dumps({
                "candidatura": {
                    "ImdCodOfertaAnuncio": anuncio.cod_oferta,
                    "ImdCandidatoNumCC": request.env.user.partner_id.cc,
                    "Documentos": docs
                }
            })

            # Send Candidatura
            method_response = requests.post(url_method, data=method_body, headers=method_headers,
                                            cookies=login_response.cookies, verify=False)
            msg = method_response.json()['submeterCandidaturaResult']

            # Check if the response was successfull
            if method_response.status_code != 200 or msg == "CC do Contacto não Existe!" or msg == "Código de Oferta do Anúncio não Existe!":
                raise BadRequest('Failed to communicate with Creatio (Error: ' + str(
                    method_response.status_code) + ', Message: ' + msg + ')')

            # Body Request Data
            print("***** METHOD REQUEST DATA *****")
            print("Method Body:", method_body)
            print("Method Headers:", method_headers)
            print("Method Request Cookies:", method_response.cookies.get_dict())
            print("Method Status Code:", method_response.status_code)
        else:
            print("Não pode inserir mais candidaturas")

        return super(WebsiteFormCandidatura, self).website_form(model_name, **kwargs)


class WebsiteApply(WebsiteHrRecruitment):

    @http.route('''/jobs/apply/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="user", website=True)
    def jobs_apply(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()

        applicant = request.env['hr.applicant'].sudo().search_count(
            [('job_id', '=', job.id), ('partner_name', '=', request.env.user.partner_id.name)])

        num_documents = request.env['odoo_portal_module.required_documents'].sudo().search_count(
            [('job_id', '=', job.id)])

        if applicant >= 1:
            return http.redirect_with_hash('/jobs')

        error = {}
        default = {}

        partner = request.env.user.partner_id

        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')

        return request.render("odoo_portal_module.apply_form", {
            'job': job,
            'error': error,
            'default': default,
            'num_documents': num_documents,
            'partner': partner,
        })


class PortalExtend(CustomerPortal):
    MANDATORY_BILLING_FIELDS = ["name", "phone", "email", "vat", "street", "city", "country_id", "cc", "zipcode"]
    OPTIONAL_BILLING_FIELDS = ["state_id", "company_name", 'nivel_habitacional']

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        values.update({
            'error': {},
            'error_message': [],
        })

        countries = request.env['res.country'].sudo().search([])
        niveis = partner._fields['nivel_habitacional'].selection

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)

                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'niveis': niveis,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")),
                                                                                   data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            else:
                error_message.append(
                    _('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message


class JobDetail(WebsiteHrRecruitment):
    @http.route('''/jobs/detail/<model("hr.job", "[('website_id', 'in', (False, current_website_id))]"):job>''',
                type='http', auth="public", website=True)
    def jobs_detail(self, job, **kwargs):
        if not job.can_access_from_current_website():
            raise NotFound()

        partner_id = request.env.user.partner_id.id
        applicant = request.env['hr.applicant'].sudo().search_count(
            [('job_id', '=', int(job.id)), ('partner_id', '=', partner_id)])
        applicantObj = request.env['hr.applicant'].sudo().search(
            [('job_id', '=', int(job.id)), ('partner_id', '=', partner_id)])
        juris = request.env['odoo_portal_module.juri'].sudo().search(
            [('job_id', '=', int(job.id))])
        metodos = request.env['odoo_portal_module.selection_method'].sudo().search(
            [('job_id', '=', int(job.id))])
        num_selection_methods = request.env['odoo_portal_module.selection_method'].sudo().search_count(
            [('job_id', '=', int(job.id))])

        estados = job._fields['job_state'].selection

        stages = list(dict(estados).values())

        classes = []
        for k in list(dict(estados).keys()):
            if k == job.job_state:
                classes.append('active_flag')
            else:
                classes.append('estado')

        final = []
        for i in range(len(stages)):
            obj = {
                "class": classes[i],
                "value": stages[i]
            }
            final.append(obj)

        return request.render("website_hr_recruitment.detail", {
            'job': job,
            "juris": juris,
            "metodos": metodos,
            "num_selection_methods": num_selection_methods,
            'size': applicant,
            'applicantObj': applicantObj,
            'estados': final,
            'main_object': job,
        })
