import stripe
from http import HTTPStatus

from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from common.views import TitleMixin
from orders.forms import OrderForm
from products.models import Basket
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY

# Заказ оплачен
class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


# Открытие заказов, которые были все
class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created',)
    
    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


# Открытие конкретного заказа
class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ # {self.object.id}'
        return context


# Создание заказа
class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    # success_url - Когда пользователь отправляет форму создания, и данные сохраняются успешно, Django автоматически перенаправляет пользователя на указанный URL.
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    # Видоизменяем метод post, который и так отрабатываем при отправки заказа, но добавляем,
    # Что бы срабатывал метод для stripe: checkout_session = stripe...
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        # Берем конкретно тот товар, который выбрал пользвоатель
        baskets = Basket.objects.filter(user=self.request.user)
        # line_items = []
        # for basket in baskets:
        #     item = {
        #         'price': basket.product.stripe_product_price_id,
        #         'quantity': basket.quantity,
        #     }
        #     line_items.append(item)

        checkout_session = stripe.checkout.Session.create(
            # line_items - формируется из нашего заказа
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    # Добавляем поле initiator - тот кто делает заказ
    def form_valid(self, form):
        # instance - берем сам обьект, который получается
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


# Передача вебхука, что делаем после оплаты
def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
