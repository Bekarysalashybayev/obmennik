from django.db import models


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


class Valuta(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Client(models.Model):
    code = models.IntegerField(primary_key=True)
    fio = models.CharField(max_length=500, default='')
    passport = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return self.fio


class ClientValutaAccount(models.Model):
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    code_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bik = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, default='')


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


class OrganizationValutaAccount(models.Model):
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    code_organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, default='')


class Contract(models.Model):
    date = models.DateField()
    code_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    code_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)


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
        return str(self.category)


class Sotrudnik(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CursValuta(models.Model):
    date = models.DateField()
    code_valuta = models.ForeignKey(Valuta, on_delete=models.CASCADE)
    curs = models.FloatField()
    cursProd = models.FloatField()
    cursPokup = models.FloatField()


class Session(models.Model):
    date = models.DateField()
    sotrudnik = models.ForeignKey(Sotrudnik, on_delete=models.CASCADE)
    cursValuta = models.ForeignKey(CursValuta, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.sotrudnik)
