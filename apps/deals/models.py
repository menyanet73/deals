from django.db import models
from django.utils import timezone


class Customer(models.Model):
    username = models.CharField(
        verbose_name='Логин', max_length=255,
        unique=True, null=False, blank=False)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    @staticmethod
    def get_top_customers(limit: int = 5) -> models.QuerySet['Customer']:
        return Customer.objects.annotate(
            spent_money=models.Sum('deals__total')
        ).order_by('-spent_money').values('id', 'username', 'spent_money')[:limit]

    def __str__(self) -> str:
        return self.username


class Gem(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=255,
        unique=True, null=False, blank=False
    )

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'

    @staticmethod
    def get_gems_buyed_by_customers(
        customers: models.QuerySet[Customer],
        count_buyed_gems: int = 2) -> models.QuerySet['Gem']:

        return Gem.objects.filter(
            deals__customer__id__in=customers.values_list('id', flat=True)
        ).annotate(
            num_gems_buyed_by_customers=models.Count(
                'deals__customer', distinct=True)
        ).filter(
            num_gems_buyed_by_customers__gte=count_buyed_gems)

    def __str__(self) -> str:
        return self.name


class Deal(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, 
        related_name='deals',verbose_name='Клиент')
    item = models.ForeignKey(
        Gem, on_delete=models.PROTECT,
        related_name='deals', verbose_name='Камень')
    total = models.FloatField(verbose_name='Всего')
    quantity = models.IntegerField(verbose_name='Количество')
    date = models.DateTimeField(verbose_name='Дата', default=timezone.now)

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self) -> str:
        return f'{self.customer} {self.item} {self.date.date()}'
