from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class Bank(models.Model):
    bik = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    correspondent_account = models.IntegerField()

    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банк"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"


class Valuta(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class Client(AbstractUser):
    code = models.IntegerField(primary_key=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        null=True
    )
    password = models.CharField(max_length=128, default='')
    # fio = models.CharField(max_length=500, default='')
    passport = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return "".join([self.first_name, " ", self.last_name])

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class ClientValutaAccount(models.Model):
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    code_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bik = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, default='')

    def __str__(self):
        return "".join([self.code_valuta.name, " ", self.code_client.first_name])

    class Meta:
        verbose_name = "Валютные счета Клиента"
        verbose_name_plural = "Валютные счета Клиента"


class Organization(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, default='')
    inn = models.CharField(max_length=50, default='')
    kpp = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=11, default='')
    facs = models.CharField(max_length=50, default='')
    director = models.CharField(max_length=50, default='')
    buhgalter = models.CharField(max_length=50, default='')
    okpo = models.CharField(max_length=50, default='')
    pc = models.CharField(max_length=50, default='')
    bik = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организация"


class OrganizationValutaAccount(models.Model):
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    code_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, default='')

    def __str__(self):
        return "".join([self.code_valuta.name, " ", self.code_organization.name])

    class Meta:
        verbose_name = "Валютные счета организации"
        verbose_name_plural = "Валютные счета организации"


class Contract(models.Model):
    date = models.DateField()
    code_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    code_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "".join(["Организация: ", self.code_organization.name, ", Клиент: ", self.code_client.first_name, " ",
                        self.code_client.last_name])

    class Meta:
        verbose_name = "Договоры"
        verbose_name_plural = "Договоры"


class OperationCategory(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Operation(models.Model):
    code = models.IntegerField(primary_key=True)
    category = models.ForeignKey(OperationCategory, on_delete=models.CASCADE)
    date = models.DateField()
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    sum = models.IntegerField()

    def __str__(self):
        return "".join([self.category.name, "-> Организация: ", self.contract.code_organization.name, ", Клиент: ",
                        self.contract.code_client.first_name, " ",
                        self.contract.code_client.last_name, " "])

    class Meta:
        verbose_name = "Операции"
        verbose_name_plural = "Операции"


class Sotrudnik(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"


class CursValuta(models.Model):
    date = models.DateField()
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    curs = models.FloatField()
    cursProd = models.FloatField()
    cursPokup = models.FloatField()

    def __str__(self):
        return "".join([self.code_valuta.name, " -> ", self.date.__str__()])

    class Meta:
        verbose_name = "Курсы валют"
        verbose_name_plural = "Курсы валют"


class Session(models.Model):
    date = models.DateField()
    sotrudnik = models.ForeignKey(Sotrudnik, on_delete=models.CASCADE)
    cursValuta = models.ForeignKey(CursValuta, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "".join(["Сотрудник: ", self.sotrudnik.name, ", ", self.operation.__str__()])

    class Meta:
        verbose_name = "Сессии"
        verbose_name_plural = "Сессии"
