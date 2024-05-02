from decimal import Decimal,ROUND_HALF_UP
from django.conf import settings
from apps.Global.models import Product, Pack

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID) 
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        

    def add(self, item, tipo, cantidad=1, anular_cantidad=False):
        item_id = str(item.id)
        if tipo == 'Pack':
            packs_a_eliminar = []
            for key, value in self.cart.items():
                if value['tipo'] == 'Pack':
                    packs_a_eliminar.append(key)
            for pack_key in packs_a_eliminar:
                del self.cart[pack_key]

        if item_id not in self.cart:
            self.cart[item_id] = {'cantidad': 0, 'precio': str(item.precio), 'tipo': tipo, 'item-id': str(item.id)}
        if anular_cantidad:
            self.cart[item_id]['cantidad'] = cantidad
        else:
            self.cart[item_id]['cantidad'] += cantidad

        
        self.save()
    
    def save(self):
        self.session.modified = True

    def remove(self, item):
        item_id  = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()
    
    def __iter__(self):
        product_ids = [key for key, value in self.cart.items() if value['tipo'] == 'Product']
        products = Product.objects.filter(id__in=product_ids)
        pack_ids = [key for key, value in self.cart.items() if value['tipo'] == 'Pack']
        packs = Pack.objects.filter(id__in=pack_ids)
        
        for item_id, item_data in self.cart.items():
            if item_data['tipo'] == 'Product':
                item = products.get(id=int(item_id))
            elif item_data['tipo'] == 'Pack':
                item = packs.get(id=int(item_id))

            item_data['producto'] = item
            item_data['precio'] = Decimal(item_data['precio'])
            item_data['total_precio'] = item_data['precio'] * item_data['cantidad']
            yield item_data

    def __len__(self):
        return sum(item['cantidad'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_pack(self):
        for item_id, item_data in self.cart.items():
            if item_data['tipo'] == 'Pack':
                pack_id = item_data['item-id']
                pack = Pack.objects.get(id=pack_id)
                return pack
            
    def get_total_price_with_tax(self):
        subtotal = self.get_total_price()
        tax = Decimal('0.05') + subtotal
        tax = tax * Decimal('0.239')  # Calcula el 21% del subtotal como impuesto
        total_price_with_tax = subtotal + tax
        total_price_with_tax = total_price_with_tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Redondea a dos decimales
        total_price_with_tax_str = str(total_price_with_tax).replace(',', '.')  # Reemplaza la coma por un punto
        return total_price_with_tax_str
    
    def get_products(self):
        product_ids = [key for key, value in self.cart.items() if value['tipo'] == 'Product']
        products = Product.objects.filter(id__in=product_ids)
        return products