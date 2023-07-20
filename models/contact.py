import json
import re

from odoo import fields, models, api, http
import requests
from odoo.addons.odoo_portal_module.static.src.utils import creatio_authenticate, host
from odoo.exceptions import AccessDenied, ValidationError


class Nacionality(models.Model):
    _inherit = "res.country"

    nacionality = fields.Selection([('andorran', 'AD'),
                                    ('emirati', 'AE'),
                                    ('afghan', 'AF'),
                                    ('antiguan and barbudan', 'AG'),
                                    ('Anguillan', 'AI'),
                                    ('albanian', 'AL'),
                                    ('armenian', 'AM'),
                                    ('algolano', 'AO'),
                                    ('', 'AQ'),
                                    ('argentine', 'AR'),
                                    ('american samoan', 'AS'),
                                    ('austrian', 'AT'),
                                    ('australian', 'AU'),
                                    ('', 'AW'),
                                    ('', 'AX'),
                                    ('', 'AZ'),
                                    ('', 'BA'),
                                    ('', 'BB'),
                                    ('', 'BD'),
                                    ('', 'BE'),
                                    ('', 'BF'),
                                    ('', 'BG'),
                                    ('', 'BH'),
                                    ('', 'BI'),
                                    ('', 'BJ'),
                                    ('', 'BL'),
                                    ('', 'BM'),
                                    ('', 'BN'),
                                    ('', 'BO'),
                                    ('', 'BQ'),
                                    ('', 'BR'),
                                    ('', 'BS'),
                                    ('', 'BT'),
                                    ('', 'BV'),
                                    ('', 'BW'),
                                    ('', 'BY'),
                                    ('', 'BZ'),
                                    ('', 'CA'),
                                    ('', 'CC'),
                                    ('', 'CF'),
                                    ('', 'CD'),
                                    ('', 'CG'),
                                    ('', 'CH'),
                                    ('', 'CI'),
                                    ('', 'CK'),
                                    ('', 'CL'),
                                    ('', 'CM'),
                                    ('', 'CN'),
                                    ('', 'CO'),
                                    ('', 'CR'),
                                    ('', 'CU'),
                                    ('', 'CV'),
                                    ('', 'CW'),
                                    ('', 'CX'),
                                    ('', 'CY'),
                                    ('', 'CZ'),
                                    ('', 'DE'),
                                    ('', 'DJ'),
                                    ('', 'DK'),
                                    ('', 'DM'),
                                    ('', 'DO'),
                                    ('', 'DZ'),
                                    ('', 'EC'),
                                    ('', 'EE'),
                                    ('', 'EG'),
                                    ('', 'EH'),
                                    ('', 'ER'),
                                    ('', 'ES'),
                                    ('', 'ET'),
                                    ('', 'FI'),
                                    ('', 'FJ'),
                                    ('', 'FK'),
                                    ('', 'FM'),
                                    ('', 'FO'),
                                    ('', 'FR'),
                                    ('', 'GA'),
                                    ('', 'GD'),
                                    ('', 'GE'),
                                    ('', 'GF'),
                                    ('', 'GH'),
                                    ('', 'GI'),
                                    ('', 'GG'),
                                    ('', 'GL'),
                                    ('', 'GM'),
                                    ('', 'GN'),
                                    ('', 'GP'),
                                    ('', 'GQ'),
                                    ('', 'GR'),
                                    ('', 'GS'),
                                    ('', 'GT'),
                                    ('', 'GU'),
                                    ('', 'GW'),
                                    ('', 'GY'),
                                    ('', 'HK'),
                                    ('', 'HM'),
                                    ('', 'HN'),
                                    ('', 'HR'),
                                    ('', 'HT'),
                                    ('', 'HU'),
                                    ('', 'ID'),
                                    ('', 'IE'),
                                    ('', 'IL'),
                                    ('', 'IM'),
                                    ('', 'IN'),
                                    ('', 'IO'),
                                    ('', 'IQ'),
                                    ('', 'IR'),
                                    ('', 'IS'),
                                    ('', 'IT'),
                                    ('', 'JE'),
                                    ('', 'JM'),
                                    ('', 'JO'),
                                    ('', 'JP'),
                                    ('', 'KE'),
                                    ('', 'KG'),
                                    ('', 'KH'),
                                    ('', 'KI'),
                                    ('', 'KM'),
                                    ('', 'KN'),
                                    ('', 'KP'),
                                    ('', 'KR'),
                                    ('', 'KW'),
                                    ('', 'KY'),
                                    ('', 'KZ'),
                                    ('', 'LA'),
                                    ('', 'LB'),
                                    ('', 'LC'),
                                    ('', 'LI'),
                                    ('', 'LK'),
                                    ('', 'LR'),
                                    ('', 'LS'),
                                    ('', 'LT'),
                                    ('', 'LU'),
                                    ('', 'LV'),
                                    ('', 'LY'),
                                    ('', 'MA'),
                                    ('', 'MC'),
                                    ('', 'MD'),
                                    ('', 'ME'),
                                    ('', 'MF'),
                                    ('', 'MG'),
                                    ('', 'MH'),
                                    ('', 'MK'),
                                    ('', 'ML'),
                                    ('', 'MM'),
                                    ('', 'MN'),
                                    ('', 'MO'),
                                    ('', 'MP'),
                                    ('', 'MQ'),
                                    ('', 'MR'),
                                    ('', 'MS'),
                                    ('', 'MT'),
                                    ('', 'MU'),
                                    ('', 'MV'),
                                    ('', 'MW'),
                                    ('', 'MX'),
                                    ('', 'MY'),
                                    ('', 'MZ'),
                                    ('', 'NA'),
                                    ('', 'NC'),
                                    ('', 'NE'),
                                    ('', 'NF'),
                                    ('', 'NG'),
                                    ('', 'NI'),
                                    ('', 'NL'),
                                    ('', 'NO'),
                                    ('', 'NP'),
                                    ('', 'NR'),
                                    ('', 'NU'),
                                    ('', 'NZ'),
                                    ('', 'OM'),
                                    ('', 'PA'),
                                    ('', 'PE'),
                                    ('', 'PF'),
                                    ('', 'PG'),
                                    ('', 'PH'),
                                    ('', 'PK'),
                                    ('', 'PL'),
                                    ('', 'PM'),
                                    ('', 'PN'),
                                    ('', 'PR'),
                                    ('', 'PS'),
                                    ('', 'PT'),
                                    ('', 'PW'),
                                    ('', 'PY'),
                                    ('', 'QA'),
                                    ('', 'RE'),
                                    ('', 'RO'),
                                    ('', 'RS'),
                                    ('', 'RU'),
                                    ('', 'RW'),
                                    ('', 'SA'),
                                    ('', 'SB'),
                                    ('', 'SC'),
                                    ('', 'SD'),
                                    ('', 'SE'),
                                    ('', 'SG'),
                                    ('', 'SH'),
                                    ('', 'SI'),
                                    ('', 'SJ'),
                                    ('', 'SK'),
                                    ('', 'SL'),
                                    ('', 'SM'),
                                    ('', 'SN'),
                                    ('', 'SO'),
                                    ('', 'SR'),
                                    ('', 'SS'),
                                    ('', 'ST'),
                                    ('', 'SV'),
                                    ('', 'SX'),
                                    ('', 'SY'),
                                    ('', 'SZ'),
                                    ('', 'TC'),
                                    ('', 'TD'),
                                    ('', 'TF'),
                                    ('', 'TG'),
                                    ('', 'TH'),
                                    ('', 'TJ'),
                                    ('', 'TK'),
                                    ('', 'TM'),
                                    ('', 'TN'),
                                    ('', 'TO'),
                                    ('', 'TL'),
                                    ('', 'TR'),
                                    ('', 'TT'),
                                    ('', 'TV'),
                                    ('', 'TW'),
                                    ('', 'TZ'),
                                    ('', 'UA'),
                                    ('', 'UG'),
                                    ('', 'GB'),
                                    ('', 'UM'),
                                    ('', 'US'),
                                    ('', 'UY'),
                                    ('', 'UZ'),
                                    ('', 'VA'),
                                    ('', 'VC'),
                                    ('', 'VE'),
                                    ('', 'VG'),
                                    ('', 'VI'),
                                    ('', 'VN'),
                                    ('', 'VU'),
                                    ('', 'WF'),
                                    ('', 'WS'),
                                    ('', 'YE'),
                                    ('', 'YT'),
                                    ('', 'ZA'),
                                    ('', 'ZM'),
                                    ('', 'ZW'),
                                    ('', 'XK'),
                                    ], string='Nacionality',
                                   required=True)

    @api.model
    def create(self, values):
        override_create = super(Nacionality, self).create(values)

        return override_create

    def write(self, values):
        override_write = super(Nacionality, self).write(values)

        return override_write


class Contact(models.Model):
    _inherit = "res.partner"

    #   variableName = fields.<Type>(RepresentationName, parameters)
    cc = fields.Char(string='cc', store=True, required=True)
    genero = fields.Selection([('M', 'Male'), ('F', 'Female')], string='Genero', default="M",
                              required=True)
    bday = fields.Date()
    country_id = fields.Many2one('res.country', string='Country', delegate=True, ondelete='restrict', required=True)
    area_formacao = fields.Char(string="Área de Formação", required=True)
    nivel_habitacional = fields.Selection([('1', 'Nível A - Menos de 4 Anos de Escolaridade'),
                                           ('2', 'Nível B - 4º Ano'),
                                           ('3', 'Nível I - 6º Ano'),
                                           ('4', 'Nível II - 9º Ano'),
                                           ('5', 'Nível III - 12º Ano'),
                                           ('6', 'Nível IV - Curso Profissional'),
                                           ('7', 'Nível V - CTESP'),
                                           ('8', 'Nível VI - Licenciatura'),
                                           ('9', 'Nível VII - Mestrado'),
                                           ('10', 'Nível VIII - Doutoramento'),
                                           ], string='Nivel habitacional', default="1",
                                          required=True)

    addressType = fields.Char(string='Address Type', default="Home")

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$', self.email)
            if match is None:
                raise ValidationError('Not a valid E-mail ID')

    # Override Create Function
    @api.model
    def create(self, values):
        print("Create Method")
        values["is_published"] = True
        values.update({"country_id": 183})
        override_create = super(Contact, self).create(values)
        print("Params", values)
        login_cookies, login_response = creatio_authenticate()

        # Cookies
        bpmcsrf = login_cookies.get('BPMCSRF')

        bday = values['bday'].split('-')

        val = bday[1] + "/" + bday[2] + "/" + bday[0]

        print(val)
        print(login_response.status_code)
        # Method Request
        if login_response.status_code == 200:
            url_method = "https://" + host + "/0/rest/ImdCustomServiceGestaoContactos/registarContacto"
            print(url_method)
            method_headers = {'Content-Type': 'application/json', "BPMCSRF": f'{bpmcsrf}'}
            address = values['street'] + ", " + values['zip'] + ", " + values['city']

            if values['nivel_habitacional']:
                nivel = values['nivel_habitacional']
            else:
                nivel = str(1)

            method_body = json.dumps({
                "contact": {
                    "Name": values['name'],
                    "Email": values['email'],
                    "MobilePhone": values['mobile'],
                    "Gender": values['genero'],
                    "ImdContactNationality": "português(esa)",
                    "ImdContactNumCC": values['cc'],
                    "ImdContactNif": values['vat'],
                    "ImdContactAreaFormacao": values['area_formacao'],
                    "ImdContactNivelHabilitacional": nivel,
                    "Address": address,
                    "AddressType": "Home",
                    "BirthDate": val
                }
            })

            method_response = requests.post(url_method, data=method_body, headers=method_headers,
                                            cookies=login_response.cookies, verify=False)

            print("Method Body:", method_body)
            print(method_response)
            method_response_text = json.loads(method_response.text)
            print(method_response_text)

            if method_response.status_code != 200 or method_response_text['registarContactoResult'] != '200':
                raise ValidationError(method_response.reason + " - " + method_response.text)

            print("***** METHOD REQUEST DATA *****")
            print("Method Body:", method_body)
            print("Method Headers:", method_headers)
            print("Method Request Cookies:", method_response.cookies.get_dict())
            print("Method Status Code:", method_response.status_code)
        else:
            raise AccessDenied(str(login_response))

        return override_create

    # Override Write Function
    def write(self, values):
        # your logic goes here
        print("**** Write function ****")
        url = self.env['ir.config_parameter'].get_param('web.base.url')
        path = http.request.httprequest.full_path
        print(url)
        print(path)
        full_path = str(url) + str(path)
        # address1 = self.street + ", " + self.zip + ", " + self.city + ", "
        if full_path.find('web/signup') >= 0:
            values.update({
                "name": self.name,
                "email": self.email,
                "mobile": self.mobile,
                "genero": self.genero,
                "phone": self.mobile,
                "cc": self.cc,
                "vat": self.vat,
                "area_formacao": self.area_formacao,
                "nivel_habitacional": self.nivel_habitacional,
                "street": self.street,
                "zip": self.zip,
                "city": self.city,
                "addressType": "Home",
                'bday': self.bday,
            })
        # else:
        #     values.update({
        #         'bday': self.bday,
        #         "genero": self.genero,
        #         "area_formacao": self.area_formacao,
        #         "mobile": self.phone
        #     })

        print("Values", values)
        override_write = super(Contact, self).write(values)
        for record in self:
            values.update({
                "name": record.name,
                "email": record.email,
                "mobile": record.mobile,
                "genero": record.genero,
                "phone": record.mobile,
                "cc": record.cc,
                "vat": record.vat,
                "area_formacao": record.area_formacao,
                "nivel_habitacional": record.nivel_habitacional,
                "street": record.street,
                "zip": record.zip,
                "city": record.city,
                "addressType": "Home",
                'bday': record.bday,
            })

        if self.exists():
            print("Self: ", self)
            # Login Request
            login_cookies, login_response = creatio_authenticate()
            print(login_response)
            # Cookies
            aspxauth_token = login_cookies.get('.ASPXAUTH')
            bpmcsrf = login_cookies.get('BPMCSRF')
            csrf_token = login_cookies.get('CsrfToken')

            address = values['street'] + ", " + values['zip'] + ", " + values['city']

            # Method Request
            if login_response.status_code == 200:
                url_method = "https://" + host + "/0/rest/ImdCustomServiceGestaoContactos/updateContacto"
                print(url_method)
                method_headers = {'Content-Type': 'application/json', "BPMCSRF": f'{bpmcsrf}',
                                  ".ASPXAUTH": f'{aspxauth_token}',
                                  "CsrfToken": f'{csrf_token}'}

                temp = values['bday']
                bday = str(temp).split('-')

                val = bday[1] + "/" + bday[2] + "/" + bday[0]

                method_body = json.dumps({
                    "contact": {
                        "Name": values["name"],
                        "Email": values["email"],
                        "MobilePhone": values['mobile'],
                        "Gender": values['genero'],
                        "ImdContactNationality": "português(esa)",
                        "ImdContactNumCC": values["cc"],
                        "ImdContactNif": values["vat"],
                        "ImdContactAreaFormacao": values['area_formacao'],
                        "ImdContactNivelHabilitacional": values["nivel_habitacional"],
                        "Address": address,
                        "AddressType": "Home",
                        "BirthDate": val
                    }
                })
                # method_body = json.dumps(values)
                method_response = requests.put(url_method, data=method_body, headers=method_headers,
                                               cookies=login_response.cookies, verify=False)

                method_response_text = json.loads(method_response.text)

                if method_response.status_code != 200 or method_response_text['updateContactoResult'] != '200':
                    raise ValidationError(method_response.reason + " - " + method_response.text)

                print("Method Body:", method_body)
                print("Method Headers:", method_headers)
                print("Method Request Cookies:", method_response.cookies.get_dict())
                print("Method Status Code:", method_response.status_code)
            else:
                raise AccessDenied(str(login_response))
        else:
            print("Record does not exist")

        return override_write
