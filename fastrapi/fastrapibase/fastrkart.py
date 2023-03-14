from django.conf import settings
from .models import ProductRate
from .serializers import ProductRateSerializer


# SAMPLE SCHEMA
# kart = {
# 	"kart": {
# 		"products": {
# 			"1": {
# 				"id": 1,
# 				"tag_id": "A7 E4 H5 3Q",
# 				"title": "Sweatshirt",
# 				"rate": 250,
#                 "quantity": 3
# 			},
# 			"2": {
# 				"id": 2,
# 				"tag_id": "A7 E4 H5 3Q",
# 				"title": "Sweatshirt",
# 				"rate": 250,
#                 "quantity": 2
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
                "tax": 0,
                "sub_total": 0,
                "total": 0
            }
        self.kart = kart

    def __iter__(self):
        product_ids = [product["id"] for product in kart["products"]]
        products = ProductRate.objects.filter(id__in=product_ids)
        kart = self.kart.copy()
        for product in products:
            kart['products'][str(product.id)] = ProductRateSerializer(product).data

    @staticmethod
    def fastkart_sub_total(products):
        sub_total = 0
        if products:
            for product_id, product in products.items():
                product_price = product["rate"] * product["quantity"]
                sub_total += product_price
            return sub_total
        return sub_total
            
    def fastrkart_add(self, product):
        product_id = str(product.id)
        if product_id not in self.kart["products"]:
            self.kart["products"][product_id] = ProductRateSerializer(product).data
            self.kart["products"][product_id]["quantity"] = 1
            # process billing
            self.kart["sub_total"] = Fastrkart.fastkart_sub_total(self.kart["products"])
            self.kart["tax"] = self.kart["sub_total"] * round((settings.KART_CHECKOUT_TAX/100),2)
            self.kart["total"] = self.kart["sub_total"] + self.kart["tax"]
        else:
            self.kart["products"][product_id]["quantity"] += 1
            # process billing
            self.kart["sub_total"] = Fastrkart.fastkart_sub_total(self.kart["products"])
            self.kart["tax"] = self.kart["sub_total"] * round((settings.KART_CHECKOUT_TAX/100),2)
            self.kart["total"] = self.kart["sub_total"] + self.kart["tax"]

    def fastrkart_remove(self, product):
        product_id = str(product.id)
        if product_id in self.kart["products"]:
            if self.kart["products"][product_id]["quantity"] > 1:
                self.kart["products"][product_id]["quantity"] -= 1
                # process billing
                self.kart["sub_total"] = Fastrkart.fastkart_sub_total(self.kart["products"])
                self.kart["tax"] = self.kart["sub_total"] * round((settings.KART_CHECKOUT_TAX/100),2)
                self.kart["total"] = self.kart["sub_total"] + self.kart["tax"]
            else:
                del self.kart["products"][product_id]
                            # process billing
                self.kart["sub_total"] = Fastrkart.fastkart_sub_total(self.kart["products"])
                self.kart["tax"] = self.kart["sub_total"] * round((settings.KART_CHECKOUT_TAX/100),2)
                self.kart["total"] = self.kart["sub_total"] + self.kart["tax"]

    # def save(self):
    #     self.session.modified = True