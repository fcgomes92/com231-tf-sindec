from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from sindec.util import strings as sindec_strings


class User(AbstractUser):
    endereco = models.OneToOneField("Endereco", null=True, blank=True)
    timestamp = models.DateTimeField(blank=False, null=False)
    last_update = models.DateTimeField(blank=False, null=False)

    def save(self, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        self.last_update = timezone.now()
        super(User, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME


class Procom(User):
    CHOICES_REGIAO = (
        (1, "Norte"),
        (2, "Nordeste"),
        (3, "Sudeste"),
        (4, "Sul"),
        (5, "Centro-Oeste"),
    )
    regiao = models.PositiveIntegerField(choices=CHOICES_REGIAO, null=False, blank=False)
    uf = models.CharField(max_length=2, null=False, blank=False)

    class Meta:
        app_label = sindec_strings.APP_NAME
        unique_together = (("regiao", "uf",),)


class Consumidor(models.Model):
    CHOICES_GENDER = (
        ('M', "Masculino"),
        ('F', "Feminino"),
        ('N', "Não se aplica"),
    )

    CHOICES_FE = (
        (1, "até 20 anos"),
        (2, "entre 21 e 30 anos"),
        (3, "entre 31 e 40 anos"),
        (4, "entre 41 e 50 anos"),
        (5, "entre 51 e 60 anos"),
        (6, "entre 61 e 70 anos"),
        (7, "mais de 70 anos"),
        (8, "Nao Informada"),
        (0, "Não se aplica"),
    )

    sexo = models.CharField(max_length=1, null=False, blank=False, choices=CHOICES_GENDER)
    data_nascimento = models.DateField(null=True, blank=True)
    faixa_etaria = models.IntegerField(null=True, blank=True, choices=CHOICES_FE)
    cep_consumidor = models.PositiveIntegerField(null=True, blank=True)
    endereco = models.OneToOneField("Endereco", null=True, blank=True)

    class Meta:
        app_label = sindec_strings.APP_NAME


class Reclamacao(models.Model):
    reclamador = models.ForeignKey("Consumidor", null=False)
    registrador = models.ForeignKey("Procom", null=False)
    empresa = models.ForeignKey("Empresa", null=False)

    ano = models.PositiveIntegerField(null=False, blank=False)

    assunto = models.ForeignKey("Assunto", null=False, blank=False)
    problema = models.ForeignKey("Problema", null=False, blank=False)

    data_abertura = models.DateTimeField(blank=False, null=False)
    data_fechamento = models.DateTimeField(blank=True, null=True)

    atendida = models.BooleanField(blank=False, null=False)

    last_update = models.DateTimeField()

    def save(self, **kwargs):
        self.last_update = timezone.now()
        super(Reclamacao, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME
        unique_together = (('reclamador', 'registrador', 'empresa',),)


class Assunto(models.Model):
    codigo_assunto = models.PositiveIntegerField(null=False, blank=False, primary_key=True)
    descricao_assunto = models.CharField(max_length=128, null=False, blank=False)

    last_update = models.DateTimeField()

    def save(self, **kwargs):
        self.last_update = timezone.now()
        super(Assunto, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME


class Problema(models.Model):
    codigo_problema = models.PositiveIntegerField(null=False, blank=False, primary_key=True)
    descricao_problema = models.CharField(max_length=128, null=False, blank=False)

    last_update = models.DateTimeField()

    def save(self, **kwargs):
        self.last_update = timezone.now()
        super(Problema, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME


class Empresa(models.Model):
    razao_social_sindec = models.CharField(max_length=64, null=False, blank=False)
    nome_fantasia_sindec = models.CharField(max_length=64, null=False, blank=True)

    pessoa_juridica = models.BooleanField(null=False, blank=False)

    cnpj = models.PositiveIntegerField(null=False, blank=False, primary_key=True)
    cnpj_radical = models.PositiveIntegerField(null=True, blank=True)

    razao_social_rfb = models.CharField(max_length=64, null=True, blank=True)
    nome_fantasia_rfb = models.CharField(max_length=64, null=True, blank=True)

    cnae = models.ForeignKey("CNAE", null=True, blank=True)

    last_update = models.DateTimeField()

    def save(self, **kwargs):
        self.last_update = timezone.now()
        super(Empresa, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME


class CNAE(models.Model):
    codigo_cnae = models.PositiveIntegerField(null=False, blank=False, primary_key=True)
    descricao_cnae = models.CharField(max_length=128, null=False, blank=False)

    last_update = models.DateTimeField()

    def save(self, **kwargs):
        self.last_update = timezone.now()
        super(CNAE, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME


class Endereco(models.Model):
    logradouro = models.CharField(max_length=128, null=False, blank=False)
    bairro = models.CharField(max_length=128, null=False, blank=False)
    cep = models.CharField(max_length=12, null=False, blank=False)
    cidade = models.CharField(max_length=128, null=False, blank=False)
    estado = models.CharField(max_length=2, null=False, blank=False)
    pais = models.CharField(max_length=64, default='Brasil', null=False, blank=False)

    timestamp = models.DateTimeField(blank=False, null=False)
    last_update = models.DateTimeField()

    def save(self, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        self.last_update = timezone.now()
        super(Endereco, self).save(**kwargs)

    class Meta:
        app_label = sindec_strings.APP_NAME
