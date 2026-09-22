#Section-1 Custom Exceptions
class InventoryError(Exception):
    """Base Exception for Apexcart inventory related errors."""
    pass
class OutOfStockError(InventoryError):
    """Raised when requested quantity is more than the available stock."""
    pass
class InvalidDiscountError(InventoryError):
    """Rasied when invalid coupon code or invalid discount is applied."""
    pass 

#Section-2 Product Management
class product:
    def __init__(self, sku, name, price, stock,*tags, **specifications):
        self.sku = sku.strip().upper()
        self.name = name.strip()

        self.price = price
        self.stock = stock
#store the all provided tags words to as a unique words
        self.tags = set(tags)
#To store all the technical specification 
        self.specifications = specifications

#Price 
    @property     #It controls on how we acess the object's attribute
    def price(self):
      return self._price

    @price.setter
    def price(self,value):

      value=float(value)
      if value<0:
        raise ValueError("{Price cannot be negative")
      self._price = value

#Stock
    @property 
    def stock(self):
      return self._stock

    @stock.setter
    def stock(self,value):

     value=int(value)
     if value<0:
        raise ValueError("Stock cannot be negative")
     self._stock = value

#Dimensions
    def get_dimensions(self):

        width =float(self.specifications.get("width",0.0))
        height =float(self.specifications.get("height",0.0))    
        depth =float(self.specifications.get("depth",0.0))
        return(width,height,depth)

#Shipping
    def shipping_cost(self):
      return 0.0

#Summary
    def summary(self):
      return f"[{self.sku}] {self.name} - ${self.price:.2f}  ({self.stock} in stock)"

    def __str__(self):
     return self.summary()

#Physical Product
class PhysicalProduct(product):
    def __init__(self, sku, name, price, stock, weight, *tags, **specifications):

        super().__init__(
            sku,
            name,
            price,
            stock,
            *tags,
            **specifications
        )

        self.weight = float(weight)
    def shipping_cost(self):
        cost = 5.00 +(2.50 * self.weight)
        return round(cost,2)

#Digital Product
class DigitalProduct(product):

    def __init__(self,
            sku,
            name, 
            price,
            stock,
            download_link,
            *tags,
            **specifications):
    
        super().__init__(
            sku,
            name,
            price,
            stock,
            *tags,
            **specifications  
        )
        self.download_link = download_link.strip()

        def shipping_cost(self):
            return 0.0

#Section-3 Customers and Orders
# Customer
class Customer:
    def __init__(self, customer_id, full_name, email, vip=False):

        self.customer_id = customer_id.strip().upper()
        self.full_name = full_name.strip()
        self.email = email.strip().lower()
        self.vip = bool(vip)

    def __str__(self):
        return f"{self.customer_id} - {self.full_name} - {self.email}"

   #Orders
class Order:
         def __init__(self, order_id, customer):

             self.order_id = order_id.strip().upper()
             self.customer = customer

             #List of tuples:
             #(product, quantity)
             self.items = []

             self.discount_percentage = 0.0

             #Add Item
         def add_item(self, product, quantity):
            if quantity <= 0:
               raise ValueError("Quantity must be greater than 0")

            if quantity > product.stock:
               raise OutOfStockError(
                f"Only {product.stock} units of {product.name} are available."
            )

            self.items.append((product, quantity))

            #Add Coupon
         def apply_coupon(self, coupon_code, discount_percentage):
             coupon_code = coupon_code.strip().upper()

             try:
                 discount_percentage = float(discount_percentage)
             except ValueError:
                 raise InvalidDiscountError("Discount must be a number.")

             if not (
                coupon_code.startswith("SAVE")
                or coupon_code.startswith("PROMO")
             ):
                 raise InvalidDiscountError("Invalid coupon code.")

             if discount_percentage < 0 or discount_percentage > 100:
                 raise InvalidDiscountError(
                   "Discount must be between 0 and 100."
                )

             self.discount_percentage = discount_percentage

    #SUBTOTAL
         def subtotal(self):
            total = 0.0
            for product, quantity in self.items:
              total += product.price*quantity
            return round(total,2)

    #Shipping
         def shipping(self):
            total = 0.0
            for product, quantity in self.items:
              total += product.shipping_cost()*quantity
            return round(total,2)

   #Discount
         def get_effective_discount(self):
             discount = self.discount_percentage

    #VIP gets a minimum 10% discount
             if self.customer.vip and discount <10:
               discount = 10.0
             return discount

   #Final Total

         def final_total(self,tax_rate=0.05):
           discount = self.get_effective_discount()
           subtotal = self.subtotal()
           discounted_subtotal = subtotal *(1-discount/100)
           tax = discounted_subtotal*tax_rate
           total=(discounted_subtotal +tax +self.shipping() )
           return round(total,2)
    
#Section-4 Analytical Helper functions
def get_itemized_breakdown(order):
    lines = []

    for index, (product, quantity) in enumerate(order.items, start=1):
        line_subtotal = product.price * quantity

        line = (
            f"{index}. {product.name} "
            f"(x{quantity}) "
            f"@ ${product.price:.2f} "
            f"= ${line_subtotal:.2f}"
        )

        lines.append(line)
    return lines

#Price Filter
def filter_products_by_min_price(products, minimum_price):
    result = []

    for product in products:
        if product.price >= minimum_price:
            result.append(product)
    return result

#Promotional Rate Batching
def apply_promotional_rates(products, discount_rates):
    result = []
    for product , discount_rate in zip(products, discount_rates):
        new_price = product.price* (1-discount_rate)
        result.append(round(new_price,2))
    return result

#In Stock Price lookup
def get_catalog_price_dict(catalog):
    result = {}
    for sku, product in catalog.items():
        if product.stock > 0:
            result[sku] = product.price
    return result

#Tag Cloud
def get_all_unique_tags(catalog):
    all_tags = set()
    for product in catalog.values():
        all_tags.update(product.tags)
    return all_tags

#Common Tags
def find_common_tags(product1, product2):
    return product1.tags.intersection(product2.tags)    

#Section-5 Store Enigne S persistence
#Store engine
import json

class StoreEngine:
    def __init__(self, store_name):
        self.store_name = store_name
        # SKU -> Product
        self.catalog = {}
        # Customer ID -> Customer
        self.customer_registry = {}
        # Completed orders
        self.completed_orders = []

#Register Product
    def register_product(self,product):
      self.catalog[product.sku] = product

#Register Customer
    def register_customer(self,customer):
      self.customer_registry[customer.customer_id] = customer


#Checkout
    def checkout(self, order, payment_amount, tax_rate=0.05):
        # Check every item again before checkout
        for product, quantity in order.items:
            if product.sku not in self.catalog:
                raise OutOfStockError(
                    f"{product.name} is no longer available."
                )

            catalog_product = self.catalog[product.sku]
            if quantity > catalog_product.stock:
                raise OutOfStockError(
                    f"Not enough stock for {product.name}."
                )

# Calculate final amount
        final_total = order.final_total(tax_rate)

        # Check payment
        if payment_amount < final_total:

            raise ValueError(
                f"Insufficient payment. "
                f"Amount due: ${final_total:.2f}"
            )

# Deduct stock
        for product, quantity in order.items:
            catalog_product = self.catalog[product.sku]
            catalog_product.stock -= quantity

        # Save completed order
        self.completed_orders.append(order)

        # Calculate customer's change
        change = payment_amount - final_total
        return (
            order.order_id,
            final_total,
            round(change, 2)
        )
#Receipt
    def generate_receipt(self, order, tax_rate=0.05):
        discount = order.get_effective_discount()
        subtotal = order.subtotal()
        shipping = order.shipping()
        grand_total = order.final_total(tax_rate)

        lines = []

        lines.append("=" * 45)
        lines.append(self.store_name)
        lines.append("=" * 45)

        lines.append(f"Order ID: {order.order_id}")

        lines.append(
            f"Customer ID: {order.customer.customer_id}"
        )    
        lines.append(
                    f"Customer Name: {order.customer.full_name}"
                )    
        lines.append(
                    f"Email: {order.customer.email}"
                )    
        lines.append("-"*45)

#Add Itemized products
        lines.extend(get_itemized_breakdown(order))

        lines.append("-" * 45)

        lines.append(f"Subtotal: ${subtotal:.2f}")

        lines.append(f"Shipping: ${shipping:.2f}")

        lines.append(
            f"Discount: {discount:.2f}%"
        )

        lines.append(
            f"Grand Total: ${grand_total:.2f}"
        )

        lines.append("=" * 45)
        return "\n".join(lines)

#Save Catalog
    def save_catalog(self, filename):

        data = []
        for product in self.catalog.values():

            product_data = {
                "sku": product.sku,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "tags": list(product.tags),
                "specifications": product.specifications
            }

            #Save Product type
            if isinstance(product, PhysicalProduct):

                product_data["product_type"] = "physical"
                product_data["weight"] = product.weight

            elif isinstance(product, DigitalProduct):

                product_data["product_type"] = "digital"
                product_data["download_link"] = product.download_link

            else:

                product_data["product_type"] = "base"

            data.append(product_data)

        with open(filename, "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )

#Load Catalog
def load_catalog(self, filename):
    try:
        with open(filename, "r") as file:
                data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return False
    try:
        self.catalog = {}

        for item in data:

           product_type = item.get("product_type","base") 
           sku = item["sku"]
           name = item["name"]
           price = item["price"]
           stock = item["stock"]

           tags = item.get("tags", [])

           specifications = item.get(
               "specifications",
                {}
            )  

 #Physical 
        if product_type == "physical":

                    product = PhysicalProduct(
                        sku,
                        name,
                        price,
                        stock,
                        item["weight"],
                        *tags,
                        **specifications
                    ) 
#Digital
        elif product_type == "digital":

                    product = DigitalProduct(
                        sku,
                        name,
                        price,
                        stock,
                        item["download_link"],
                        *tags,
                        **specifications
                    )                     
#Base
        else:

                    product = product(
                        sku,
                        name,
                        price,
                        stock,
                        *tags,
                        **specifications
                    )

        self.catalog[product.sku] = product
    except (KeyError, TypeError, ValueError):
        return False
    return True

print("Apexcart program is running successfully.") #To check program successfully run or not.

# TESTING APEXCART/Print the apexcart
print("\nSECTION 1: CUSTOM EXCEPTIONS")

try:
    raise OutOfStockError("Test: Product is out of stock.")
except OutOfStockError as e:
    print(e)

try:
    raise InvalidDiscountError("Test: Invalid discount.")
except InvalidDiscountError as e:
    print(e)

print("\nSECTION 2: PRODUCT MANAGEMENT")
# Create a normal product
product1 = product(
    "p001",
    "Laptop",
    50000,
    10,
    "electronics",
    "computer",
    brand="HP",
    width=30,
    height=2,
    depth=20
)

print("Product:", product1)
print("SKU:", product1.sku)
print("Name:", product1.name)
print("Price:", product1.price)
print("Stock:", product1.stock)
print("Tags:", product1.tags)
print("Specifications:", product1.specifications)
print("Dimensions:", product1.get_dimensions())
print("Shipping Cost:", product1.shipping_cost())

# Create a physical product
physical1 = PhysicalProduct(
    "p002",
    "Keyboard",
    2000,
    20,
    1.5,
    "electronics",
    "computer"
)

print("\nPhysical Product:", physical1)
print("Weight:", physical1.weight)
print("Shipping Cost:", physical1.shipping_cost())

# Create a digital product
digital1 = DigitalProduct(
    "p003",
    "Python Course",
    1000,
    100,
    "https://example.com/python",
    "education",
    "python"
)

print("\nDigital Product:", digital1)
print("Download Link:", digital1.download_link)
print("Shipping Cost:", digital1.shipping_cost())


print("\nSECTION 3: CUSTOMER AND ORDER")
# Create customer
customer1 = Customer(
    "c001",
    "Sana",
    "sana@example.com",
    vip=True
)
print("Customer:", customer1)


# Create order
order1 = Order("o001", customer1)
print("Order ID:", order1.order_id)

# Add products
order1.add_item(product1, 2)
order1.add_item(physical1, 1)

print("Order Items:", len(order1.items))

# Apply coupon
order1.apply_coupon("SAVE10", 10)

print("Discount:", order1.discount_percentage, "%")
print("Effective Discount:", order1.get_effective_discount(), "%")
print("Subtotal:", order1.subtotal())
print("Shipping:", order1.shipping())
print("Final Total:", order1.final_total())


print("\nSECTION 4: ANALYTICAL FUNCTIONS")

# Itemized breakdown
print("\nItemized Breakdown:")
for line in get_itemized_breakdown(order1):
    print(line)

# Price filter
products = [product1, physical1, digital1]
expensive_products = filter_products_by_min_price(
    products,
    1500
)

print("\nProducts with price >= 1500:")

for product in expensive_products:
    print(product)


# Promotional rates
discount_rates = [0.10, 0.20, 0.15]

promotional_prices = apply_promotional_rates(
    products,
    discount_rates
)

print("\nPromotional Prices:")
print(promotional_prices)


# Catalog
catalog = {
    product1.sku: product1,
    physical1.sku: physical1,
    digital1.sku: digital1
}

# In-stock price dictionary
price_dict = get_catalog_price_dict(catalog)

print("\nIn-stock Price Dictionary:")
print(price_dict)


# Unique tags
unique_tags = get_all_unique_tags(catalog)

print("\nAll Unique Tags:")
print(unique_tags)


# Common tags
common_tags = find_common_tags(
    product1,
    physical1
)

print("\nCommon Tags:")
print(common_tags)


print("\nSECTION 5: STORE ENGINE")

# Create store
store = StoreEngine("ApexCart Store")

print("Store Name:", store.store_name)


# Register products
store.register_product(product1)
store.register_product(physical1)
store.register_product(digital1)

print("Products in Catalog:", len(store.catalog))


# Register customer
store.register_customer(customer1)

print("Customers Registered:", len(store.customer_registry))


# Checkout
payment = order1.final_total() + 1000

result = store.checkout(
    order1,
    payment
)

print("\nCheckout Result:")
print("Order ID:", result[0])
print("Final Total:", result[1])
print("Change:", result[2])

# Receipt
print("\n===== RECEIPT =====")
receipt = store.generate_receipt(order1)
print(receipt)

print("\n===== TEST COMPLETED =====")