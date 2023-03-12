from django.conf import settings
from .models import ProductPrice
from .serializers import ProductPriceSerializer


# SAMPLE SCHEMA
# kart = {
# 	"kart": {
# 		"products": {
# 			"1": {
# 				"id": 1,
# 				"tag_id": "A7 E4 H5 3Q",
# 				"title": "Sweatshirt",
# 				"price": 250
# 			},
# 			"2": {
# 				"id": 2,
# 				"tag_id": "A7 E4 H5 3Q",
# 				"title": "Sweatshirt",
# 				"price": 250
# 			}
# 		},
# 		"tax": 50,
# 		"sub_total": 500,
# 		"total": 550
# 	}
# }

class Fastrkart:
    def __init__(self, request):
        self.kart = request.session
        kart = self.kart.get(settings.KART_SESSION_ID)
        if not kart:
            kart = self.kart[settings.KART_SESSION_ID] = {
                "products": {},
                "tax": settings.KART_CHECKOUT_TAX,
                "sub_total": 0,
                "total": 0
            }
        self.kart = kart

    def __iter__(self):
        product_ids = [product["id"] for product in kart["products"]]
        products = ProductPrice.objects.filter(id__in=product_ids)
        kart = self.kart.copy()
        for product in products:
            kart['products'][str(product.id)] = ProductPriceSerializer(product).data
            
    def fastrkart_add(self, product):
        product_id = str(product.id)
        if product_id not in self.kart["products"]:
            self.kart["products"][product_id] = ProductPriceSerializer(product).data
        # self.save()

    def fastrkart_remove(self, product):
        product_id = str(product.id)
        if product_id in self.kart["products"]:
            del self.kart["products"][product_id]
            # if self.kart[product_id]['quantity'] > 0:
            #     self.kart[product_id]['quantity'] -= quantity
            #     # self.save()

    # def save(self):
    #     self.session.modified = True