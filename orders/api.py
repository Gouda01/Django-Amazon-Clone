from rest_framework import generics , status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
import datetime

from .serializer import OrderSerializer , OrderDetailSerializer , CartSerializer , CartDetailSerializer
from .models import Order , OrderDetail , Cart , CartDetail , Coupon , Address
from products.models import Product
from settings.models import DeliveryFee


class OrderListAPI (generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListAPI, self).get_queryset()
        user = User.objects.get(username = self.kwargs['username'])
        queryset = queryset.filter(user=user)
        return queryset
    

    #The Same Resault of  get_queryset :

    # def list(self,request,*args,**kwargs):
    #     queryset = super(OrderListAPI, self).get_queryset()
    #     user = User.objects.get(username = self.kwargs['username'])
    #     queryset = queryset.filter(user=user)
    #     data = OrderSerializer(queryset,many=True).data
    #     return Response({'orders' : data})

class OrderDetailAPI (generics.RetrieveAPIView) :
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ApplyCouponAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        coupon = get_object_or_404 (Coupon , code=request.data['coupon_code'])
        delivery_fee = DeliveryFee.objects.last().fee
        cart= Cart.objects.get(user=request.user,status='Inprogress')

        if coupon and coupon.quantity > 0 :
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.end_date :
                coupon_value = round(cart.cart_total / 100 * coupon.discount,2)
                sub_total = round(cart.cart_total - coupon_value,2)
                total = round(sub_total + delivery_fee,2)

                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()

                coupon.quantity -= 1
                coupon.save()

                return Response({'message':'Coupon was applied successfuly'},status=status.HTTP_200_OK)
            else :
                return Response({'message':'Coupon is invalid or expired'})
            
        return Response({'message':'Coupon not found'})


class CreateOrderAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username = self.kwargs['username'])
        code = request.data['payment_code']
        address = request.data['address_id']

        cart = Cart.objects.get(user = user , status = 'Inprogress')
        cart_detail = CartDetail.objects.filter(cart=cart)
        user_address = Address.objects.get(id=address)

        
        # Cart : Order | Cart_detail : Order_detail
        new_order = Order.objects.create(
            user = user,
            status = 'Recieved',
            code = code,
            address = user_address,
            coupon = cart.coupon,
            total_with_coupon = cart.total_with_coupon,
            total = cart.cart_total,
        )

        # Order Detail
        for item in cart_detail :
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create (
                order = new_order,
                product = product,
                quantity = item.quantity,
                price = product.price,
                total = round(item.quantity * product.price , 2)
            )
            

            # Decrease Product quantity
            product.quantity -= 1
            product.save()
        
        # Close Cart
        cart.status = 'Completed'
        cart.save()

        return Response({'message' : 'Order was created successfuly'},status=status.HTTP_201_CREATED)

class CartCreateUpdateDelete(generics.GenericAPIView):
    pass