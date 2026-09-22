# Python Skill Assessment: ApexCart System

## Overview

Build the core backend engine for **ApexCart**, an e-commerce platform that manages products, customer accounts, orders, inventory, and sales reports. 

Read the requirements below and implement the entire system in Python.

---

## 1. Custom Exceptions

Create a dedicated family of custom error classes:

- **Base Inventory Exception (`InventoryError`)**: A base exception class that inherits from Python's standard exception.
- **Out of Stock Exception (`OutOfStockError`)**: Inherits from your base inventory exception. Raise this whenever an order or checkout attempts to purchase more items than currently available in stock.
- **Invalid Discount Exception (`InvalidDiscountError`)**: Inherits from your base inventory exception. Raise this whenever an invalid coupon code or invalid discount value is applied.

---

## 2. Product Management

### Base Product (`Product`)
Create a base product class to represent general merchandise:
- **Initialization:** When creating a product, accept its SKU code, product name, base price, available stock count, any number of extra tag words (as variable positional arguments), and any number of technical specifications (as keyword arguments, such as width, height, color, etc.).
- **Data Cleanup:** Automatically clean up the product name by stripping extra leading and trailing whitespace. Clean up the SKU by stripping whitespace and converting it to uppercase.
- **Tags and Specifications:** Store all provided tag words as a set of unique words. Store all technical specifications in a dictionary.
- **Price and Stock Protection:**
  - Ensure the price cannot be set to a negative number. If a negative price is provided at creation or assigned later, raise a value error. Prices should always be stored as floating-point numbers.
  - Ensure the stock count cannot be set to a negative number. If a negative stock is provided or assigned later, raise a value error. Stock must always be stored as an integer.
- **Dimensions:** Provide a way to retrieve the product's dimensions as a 3-item tuple containing width, height, and depth extracted from its technical specifications. If any dimension was not provided in the specifications, default its value to 0.0.
- **Shipping Cost:** Base products should have a default shipping cost calculation that returns 0.0.
- **Summary:** Provide a method and a string representation that returns a clean summary showing the SKU in brackets, the product name, the price formatted to 2 decimal places, and the remaining stock count (for example: `[SKU-001] Wireless Mouse - $29.99 (15 in stock)`).

### Physical Product (`PhysicalProduct`)
Create a physical product class that inherits from the base product:
- In addition to standard product information, it should accept the product's weight in kilograms.
- **Shipping Cost Calculation:** Physical products incur shipping costs. Calculate shipping as a flat base fee of $5.00 plus $2.50 per kilogram of weight. Return the calculated shipping cost rounded to 2 decimal places.

### Digital Product (`DigitalProduct`)
Create a digital product class that inherits from the base product:
- In addition to standard product information, it should accept a digital download link string. Strip any accidental whitespace from the link.
- **Shipping Cost Calculation:** Digital products do not incur any shipping costs (shipping fee is always 0.0).

---

## 3. Customers and Orders

### Customer (`Customer`)
Create a customer class to represent shoppers:
- Accept a customer ID, full name, email address, and an optional VIP status flag (which defaults to False).
- Clean up inputs by stripping extra whitespace, converting customer ID to uppercase, and converting the email address to lowercase.

### Order (`Order`)
Create an order class to handle cart operations and billing:
- Accept an order ID and a customer object upon creation. Clean up the order ID by stripping whitespace and converting it to uppercase.
- Initialize the order with an empty list of purchased items and a starting discount percentage of 0.
- **Adding Items:**
  - Provide a way to add a product and a quantity to the order.
  - The quantity must be greater than 0; otherwise, raise a value error.
  - If the requested quantity exceeds the product's current available stock, raise your custom "out of stock" exception.
  - Store the added item as a pair (tuple) of the product object and the purchased quantity in the order's items list.
- **Applying Coupons:**
  - Provide a way to apply a coupon code and discount percentage.
  - The coupon code must start with either "SAVE" or "PROMO" (case-insensitive), and the discount percentage must be a number between 0 and 100 (inclusive). If either condition fails, raise your custom "invalid discount" exception.
- **Financial Calculations:**
  - **Subtotal:** Calculate the total price of all items in the order (unit price multiplied by quantity for each item) rounded to 2 decimal places.
  - **Shipping:** Calculate total shipping by determining the shipping cost for each item multiplied by its quantity, rounded to 2 decimal places.
  - **Final Total:**
    - Check if the customer is a VIP. If the customer is a VIP and their coupon discount is less than 10%, automatically apply a 10% VIP discount instead.
    - Calculate the discounted subtotal.
    - Calculate 5% sales tax on the discounted subtotal (allow the tax rate to be customized via an optional argument defaulting to 0.05).
    - Add the discounted subtotal, sales tax, and total shipping together to produce the final grand total, rounded to 2 decimal places.

---

## 4. Analytical Helper Functions

Implement standalone functions to perform store analytics:

1. **Itemized Receipt Breakdown (`get_itemized_breakdown`)**:
   - Takes an order and returns a list of formatted, numbered string lines for each item in the order starting from number 1.
   - Each line should show the item index, product name, quantity, unit price, and line subtotal (for example: `1. Wireless Mouse (x2) @ $29.99 = $59.98`).

2. **Price Filter (`filter_products_by_min_price`)**:
   - Takes a list of products and a minimum price threshold, and returns only those products whose base price is greater than or equal to the minimum threshold.

3. **Promotional Rate Batching (`apply_promotional_rates`)**:
   - Takes a list of products and a list of discount rates (such as 0.15 for 15% off), pairs each product with its corresponding discount rate, and returns a list of the new discounted prices rounded to 2 decimal places.

4. **In-Stock Price Lookup (`get_catalog_price_dict`)**:
   - Takes the product catalog dictionary (mapping SKUs to product objects) and returns a new dictionary mapping product SKUs to their base prices, including only products that are currently in stock (stock count greater than 0).

5. **Tag Cloud (`get_all_unique_tags`)**:
   - Takes the product catalog dictionary and returns a set containing all unique tags across all products in the catalog without duplicates.

6. **Common Tags (`find_common_tags`)**:
   - Takes two product objects and returns a set of tags that are shared by both products.

---

## 5. Store Engine & Persistence

### Store Engine (`StoreEngine`)
Create a central store engine class that ties the entire platform together:

- **Initialization:** Initialize the store with a store name, an empty catalog dictionary, an empty customer registry dictionary, and an empty list of completed orders.
- **Registration:**
  - Provide a way to register or update products in the catalog using their SKU as the key.
  - Provide a way to register or update customers in the customer registry using their customer ID as the key.
- **Order Checkout:**
  - Accept an order and a payment amount (with an optional sales tax rate defaulting to 0.05).
  - Verify that all items in the order are still available in the catalog with sufficient stock. If any item is insufficient, raise your custom "out of stock" exception.
  - Calculate the final total for the order.
  - If the payment amount provided is less than the final total, raise a value error for insufficient payment.
  - Deduct the purchased quantities directly from the catalog products' available stock.
  - Save the completed order into the store's list of completed orders.
  - Return a 3-item summary tuple containing the order ID, the final total amount, and the customer's change amount (rounded to 2 decimal places).
- **Receipt Generation:**
  - Generate and return a clean, multi-line formatted text receipt containing the store name, order ID, customer details, the numbered itemized breakdown lines, subtotal, shipping, applied discount percentage, and grand total due.
- **Saving Catalog to File:**
  - Save the entire product catalog into a JSON file. Ensure all product properties—including SKU, name, price, stock, tags, specifications, product type (physical, digital, or base), and type-specific attributes (weight or download link)—are correctly written to the file.
- **Loading Catalog from File:**
  - Read a saved JSON file from disk and restore all products into the store's catalog as their appropriate product types (`PhysicalProduct`, `DigitalProduct`, or base `Product`).
  - If the file does not exist or contains invalid JSON data, handle the error safely without crashing the program and return `False`. If loaded successfully, return `True`.
