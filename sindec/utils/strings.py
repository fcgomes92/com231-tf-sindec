from django.utils.translation import ugettext as _

APP_NAME = "sindec"

# views/user
LOGIN_SUCCESS = _("Login realizado com sucesso!")
LOGIN_ERR = _("Erro de login!")
LOGIN_EMAIL_ERR = _("Login incorreto!")

PASSWORD_MISMATCH = _("Senhas não conferem!")
LBL_LOGIN = _("Login")
LBL_PASSWORD = _("Senha")
LBL_NEW_PASSWORD = _("Nova Senha")
LBL_NEW_PASSWORD_CONFIRM = _("Confirmação de nova senha")

REGISTER_MAIL_SENT = _('Por favor, verifique seu email!')
REGISTER_MAIL_ERR = _('Email inválido!')
REGISTER_MAIL_REGISTERED = _('Username registrado!')

REGISTER_CONFIRMATION = _('Muito obrigado! Agora você pode entrar no sistema!')
REGISTER_CONFIRMATION_ERR = _('Erro! Contate o administrador!')

RESET_PASSWORD_CONFIRM = _("Email enviado para {}. Verifique sua caixa de emails para continuar com o processo.")
RESET_PASSWORD_ERR_NO_EMAIL = _('Nenhum usuário encontrado com este email!')
RESET_PASSWORD_ERR_FORMAT_EMAIL = _('Entrada inválida!')
RESET_PASSWORD_ERR_SEND_EMAIL = _('Erro de envio de email! Tente novamente mais tarde!')

RECLAMACAO_ADD_SUCC = _("Reclamação adicionada com sucesso!")
RECLAMACAO_UPD_SUCC = _("Reclamação alterada com sucesso!")
RECLAMACAO_ADD_ERR = _("Reclamação não adicionada! Tente novamente!")
RECLAMACAO_UPD_ERR = _("Reclamação não alterada! Tente novamente!")

PROBLEMA_ADD_SUCC = _("Problema adicionado com sucesso!")
PROBLEMA_ADD_ERR = _("Problema não adicionado!")
PROBLEMA_UPD_SUCC = _("Problema alterado com sucesso!")
PROBLEMA_UPD_ERR = _("Problema não alterado!")

ASSUNTO_ADD_SUCC = _("Assunto adicionado com sucesso!")
ASSUNTO_ADD_ERR = _("Assunto não adicionado!")
ASSUNTO_UPD_SUCC = _("Assunto alterado com sucesso!")
ASSUNTO_UPD_ERR = _("Assunto não alterado!")

CNAE_ADD_SUCC = _("CNAE adicionado com sucesso!")
CNAE_ADD_ERR = _("CNAE não adicionado!")
CNAE_UPD_SUCC = _("CNAE alterado com sucesso!")
CNAE_UPD_ERR = _("CNAE não alterado!")

EMPRESA_ADD_SUCC = _("Empresa adicionado com sucesso!")
EMPRESA_ADD_ERR = _("Empresa não adicionado!")
EMPRESA_UPD_SUCC = _("Empresa alterado com sucesso!")
EMPRESA_UPD_ERR = _("Empresa não alterado!")
