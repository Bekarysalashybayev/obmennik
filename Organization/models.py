from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class Bank(models.Model):
    bik = models.IntegerField(primary_key=True, verbose_name='БИК')
    name = models.CharField(max_length=255, default='', verbose_name='Атауы')
    city = models.CharField(max_length=255, default='', verbose_name='Қала')
    correspondent_account = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банктар"


class Valuta(models.Model):
    code = models.IntegerField(primary_key=True, verbose_name='Код')
    name = models.CharField(max_length=255, default='', verbose_name='Атауы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валютлар"


class Client(AbstractUser):
    code = models.IntegerField(primary_key=True, verbose_name='Код')
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        null=True, verbose_name='клиенттің логині'
    )
    password = models.CharField(max_length=128, default='', verbose_name='пароль')
    # fio = models.CharField(max_length=500, default='')
    passport = models.CharField(max_length=50, default='', unique=True, verbose_name='паспорт')

    def __str__(self):
        return "".join([self.first_name, " ", self.last_name])

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенттер"


class ClientValutaAccount(models.Model):
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name='валютаның коды')
    code_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиентің коды')
    bik = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='')
    account_number = models.CharField(max_length=50, default='', verbose_name='аккаунт номері')

    def __str__(self):
        return "".join([self.code_valuta.name, " ", self.code_client.first_name])

    class Meta:
        verbose_name = "Клиенттің валютадағы шоттары"
        verbose_name_plural = "Клиенттердің валютадағы шоттары"


class Organization(models.Model):
    code = models.IntegerField(primary_key=True, verbose_name='Код')
    name = models.CharField(max_length=500, default='', verbose_name='Атауы')
    inn = models.CharField(max_length=50, default='', verbose_name='ИНН')
    kpp = models.CharField(max_length=50, default='', verbose_name='КПП')
    address = models.CharField(max_length=50, default='', verbose_name='Мекен-жайы')
    phone = models.CharField(max_length=11, default='', verbose_name='Телефон номері')
    facs = models.CharField(max_length=50, default='', verbose_name='Факс')
    director = models.CharField(max_length=50, default='', verbose_name='Директор')
    buhgalter = models.CharField(max_length=50, default='', verbose_name='Бугалтер')
    okpo = models.CharField(max_length=50, default='', verbose_name='ОКПО')
    pc = models.CharField(max_length=50, default='', verbose_name='ПК')
    bik = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='БИК')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Ұйым"
        verbose_name_plural = "Ұйымдар"


class OrganizationValutaAccount(models.Model):
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name='Валюта коды')
    code_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Ұйым коды')
    account_number = models.CharField(max_length=50, default='', verbose_name='акканут номері')

    def __str__(self):
        return "".join([self.code_valuta.name, " ", self.code_organization.name])

    class Meta:
        verbose_name = "Ұйымның валюталық шоттары"
        verbose_name_plural = "Ұйымның валюталық шоттары"


class Contract(models.Model):
    date = models.DateField( verbose_name='Дата')
    code_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, verbose_name='Ұйым коды')
    code_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, verbose_name='Клиент коды')

    def __str__(self):
        return "".join(["Организация: ", self.code_organization.name, ", Клиент: ", self.code_client.first_name, " ",
                        self.code_client.last_name])

    class Meta:
        verbose_name = "Келісім шарт"
        verbose_name_plural = "Келісім шарттар"


class OperationCategory(models.Model):
    name = models.CharField(max_length=50, default='', verbose_name='Атауы')

    def __str__(self):
        return self.name


class Operation(models.Model):
    code = models.IntegerField(primary_key=True, verbose_name='Коды')
    category = models.ForeignKey(OperationCategory, on_delete=models.CASCADE, verbose_name='Категориясы')
    date = models.DateField(verbose_name='Дата')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Контракт')
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name='Валюта коды')
    sum = models.IntegerField(verbose_name='Соммасы')

    def __str__(self):
        return "".join([self.category.name, "-> Организация: ", self.contract.code_organization.name, ", Клиент: ",
                        self.contract.code_client.first_name, " ",
                        self.contract.code_client.last_name, " "])

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операциялар"


class Sotrudnik(models.Model):
    code = models.IntegerField(primary_key=True, verbose_name='Код')
    name = models.CharField(max_length=50, verbose_name='Атауы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Қызметкер"
        verbose_name_plural = "Қызметкерлер"


class CursValuta(models.Model):
    date = models.DateField(verbose_name='Дата')
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE, verbose_name='Валюта коды')
    curs = models.FloatField(verbose_name='Курс')
    cursProd = models.FloatField(verbose_name='Сатылым Курсы')
    cursPokup = models.FloatField(verbose_name='Сатып алу курсы')

    def __str__(self):
        return "".join([self.code_valuta.name, " -> ", self.date.__str__()])

    class Meta:
        verbose_name = "Валюта бағамы"
        verbose_name_plural = "Валюта бағамдары"


class Session(models.Model):
    date = models.DateField(verbose_name='Дата')
    sotrudnik = models.ForeignKey(Sotrudnik, on_delete=models.CASCADE, verbose_name='Қызметкер')
    cursValuta = models.ForeignKey(CursValuta, on_delete=models.CASCADE, verbose_name='Валюта курсы')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Операция')

    def __str__(self):
        return "".join(["Сотрудник: ", self.sotrudnik.name, ", ", self.operation.__str__()])

    class Meta:
        verbose_name = "Сессия"
        verbose_name_plural = "Сессиялар"
