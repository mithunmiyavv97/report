class MyForm(Form):
company = TextField('Company', [Required()])

def validate_company(form, field):
    if len(field.data) > 50:
        raise ValidationError('Name must be less than 50 characters')
class CompanyForm(Form):
    name = StringField('Company name', [validators.required()])
    address    = StringField('Address', [validators.required()])

class RegistrationForm(Form):
    first_name   = StringField()
    last_name    = StringField()
    company = FormField(CompanyForm, [your_custom_validation])