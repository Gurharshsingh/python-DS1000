"""
Integrated Python Assessment Test Suite
Project: ApexCart Engine
Covers: All 19 Python Core Modules

Run with:
    python test_python_assessment.py
or (if pytest is installed):
    pytest test_python_assessment.py
"""

import os
import sys
import unittest

# Try importing the student's solution
try:
    from student_code import (
        InventoryError,
        OutOfStockError,
        InvalidDiscountError,
        Product,
        PhysicalProduct,
        DigitalProduct,
        Customer,
        Order,
        StoreEngine,
        get_itemized_breakdown,
        filter_products_by_min_price,
        apply_promotional_rates,
        get_catalog_price_dict,
        get_all_unique_tags,
        find_common_tags,
    )
except ImportError as e:
    # If run in an environment where student_code is not yet created
    print(f"\n[!] WARNING: Could not import from 'student_code.py': {e}")
    print("Please create 'student_code.py' and implement the required classes/functions.\n")


class TestApexCartSystem(unittest.TestCase):
    """Integrated test suite verifying all 19 Python concepts in ApexCart."""

    # -------------------------------------------------------------
    # 1. Tests for Product Hierarchy & OOP Encapsulation
    # Covers: Basics, Operators, Strings, Sets, Tuples, Dictionaries,
    #         *args, **kwargs, OOP Basics, OOP Concepts
    # -------------------------------------------------------------
    def test_product_basics_and_encapsulation(self):
        p = Product(
            "  sku-001  ",
            " Gaming Mouse ",
            59.99,
            10,
            "electronics",
            "rgb",
            width=12.5,
            height=4.0,
            depth=6.5,
        )
        # Strings: Cleaned SKU and Name
        self.assertEqual(p.sku, "SKU-001")
        self.assertEqual(p.name, "Gaming Mouse")

        # Basics & Encapsulation: Valid Price & Stock
        self.assertEqual(p.base_price, 59.99)
        self.assertEqual(p.stock, 10)

        # Sets: *args converted to a set of tags
        self.assertIsInstance(p.tags, set)
        self.assertIn("electronics", p.tags)
        self.assertIn("rgb", p.tags)

        # Tuples & Dictionaries: Dimensions extracted from **specs
        self.assertEqual(p.get_dimensions_tuple(), (12.5, 4.0, 6.5))

        # f-strings: Summary representation
        self.assertIn("[SKU-001]", p.get_summary())
        self.assertIn("59.99", p.get_summary())

        # Encapsulation validation: Negative values must raise ValueError
        with self.assertRaises(ValueError):
            p.base_price = -10.0
        with self.assertRaises(ValueError):
            p.stock = -5

    # -------------------------------------------------------------
    # 2. Tests for Inheritance and Polymorphism
    # Covers: OOP Concepts (Inheritance, super(), Polymorphic dispatch)
    # -------------------------------------------------------------
    def test_oops_inheritance_and_polymorphism(self):
        p_item = PhysicalProduct("p-100", "Monitor", 200.0, 5, 4.0, "electronics", "screen")
        d_item = DigitalProduct("d-200", "E-Book", 15.0, 100, "https://apex.cart/dl/ebook", "education", "book")

        # Inheritance check
        self.assertIsInstance(p_item, Product)
        self.assertIsInstance(d_item, Product)

        # Polymorphic shipping cost calculation
        # Physical: $5.0 base + ($2.5 * 4.0 kg) = $15.0
        self.assertEqual(p_item.calculate_shipping_cost(), 15.0)
        # Digital: $0.0 shipping
        self.assertEqual(d_item.calculate_shipping_cost(), 0.0)

    # -------------------------------------------------------------
    # 3. Tests for Customer, Order, Control Flow & Custom Exceptions
    # Covers: Control Flow, Nested Control Flow, Functions, Custom Exceptions
    # -------------------------------------------------------------
    def test_order_and_discount_rules(self):
        cust_regular = Customer("C01", "Alice", "alice@example.com", is_vip=False)
        cust_vip = Customer("C02", "Bob", "bob@example.com", is_vip=True)

        mouse = PhysicalProduct("SKU-M", "Mouse", 50.0, 10, 1.0)
        keyboard = PhysicalProduct("SKU-K", "Keyboard", 100.0, 5, 2.0)

        order_reg = Order("ORD-001", cust_regular)
        order_reg.add_item(mouse, 2)
        order_reg.add_item(keyboard, 1)

        # Subtotal: (50*2) + (100*1) = 200.0
        self.assertEqual(order_reg.calculate_subtotal(), 200.0)
        # Shipping: (5 + 1*2.5)*2 + (5 + 2*2.5)*1 = (7.5 * 2) + 10.0 = 25.0
        self.assertEqual(order_reg.calculate_shipping(), 25.0)

        # Coupon validation
        order_reg.apply_coupon("SAVE20", 20.0)
        self.assertEqual(order_reg.discount_percent, 20.0)

        # Subtotal after 20% discount = 160.0; Tax (5%) = 8.0; Shipping = 25.0; Total = 193.0
        self.assertEqual(order_reg.calculate_final_total(tax_rate=0.05), 193.0)

        # Invalid coupons must raise InvalidDiscountError
        with self.assertRaises(InvalidDiscountError):
            order_reg.apply_coupon("BAD_CODE", 15.0)
        with self.assertRaises(InvalidDiscountError):
            order_reg.apply_coupon("PROMO10", 150.0)

        # VIP automatic discount of at least 10%
        order_vip = Order("ORD-002", cust_vip)
        order_vip.add_item(mouse, 1)
        # Subtotal = 50.0, VIP 10% discount => 45.0, Tax (5%) = 2.25, Shipping = 7.50 => Total = 54.75
        self.assertEqual(order_vip.calculate_final_total(tax_rate=0.05), 54.75)

        # Stock check exception
        with self.assertRaises(OutOfStockError):
            order_reg.add_item(keyboard, 50)  # Only 5 available

    # -------------------------------------------------------------
    # 4. Tests for Special Functions, Comprehensions & Sets
    # Covers: lambda, filter, zip, enumerate, list/dict comprehensions, sets
    # -------------------------------------------------------------
    def test_special_functions_and_comprehensions(self):
        p1 = Product("P1", "Alpha", 10.0, 5, "tagA", "tagB")
        p2 = Product("P2", "Beta", 50.0, 0, "tagB", "tagC")
        p3 = Product("P3", "Gamma", 100.0, 3, "tagC", "tagD")

        # filter + lambda
        expensive = filter_products_by_min_price([p1, p2, p3], 40.0)
        self.assertEqual(len(expensive), 2)
        self.assertEqual(expensive[0].name, "Beta")
        self.assertEqual(expensive[1].name, "Gamma")

        # zip
        discounted = apply_promotional_rates([p1, p3], [0.10, 0.20])
        self.assertEqual(discounted, [9.0, 80.0])

        # dict comprehension (only in-stock items)
        catalog = {"P1": p1, "P2": p2, "P3": p3}
        price_dict = get_catalog_price_dict(catalog)
        self.assertEqual(price_dict, {"P1": 10.0, "P3": 100.0})

        # Set operations
        all_tags = get_all_unique_tags(catalog)
        self.assertEqual(all_tags, {"tagA", "tagB", "tagC", "tagD"})
        common = find_common_tags(p1, p2)
        self.assertEqual(common, {"tagB"})

        # enumerate breakdown
        cust = Customer("C01", "Test", "test@test.com")
        ord_sample = Order("O1", cust)
        ord_sample.add_item(p1, 2)
        breakdown = get_itemized_breakdown(ord_sample)
        self.assertTrue(len(breakdown) > 0)
        self.assertTrue(breakdown[0].startswith("1."))

    # -------------------------------------------------------------
    # 5. Tests for StoreEngine, File I/O, Exceptions, JSON & Receipts
    # Covers: Modules (json), File Handling (with), Exceptions (try/except), f-strings
    # -------------------------------------------------------------
    def test_store_engine_integrated_workflow(self):
        store = StoreEngine("Apex Electronics")
        laptop = PhysicalProduct("LAP-01", "Pro Laptop", 1200.0, 3, 2.0, "tech", "work")
        software = DigitalProduct("SW-01", "Antivirus Suite", 50.0, 20, "https://apex.cart/av", "tech", "security")

        store.register_product(laptop)
        store.register_product(software)

        cust = Customer("CUST-99", "Diana Prince", "diana@themyscira.gov", is_vip=False)
        store.register_customer(cust)

        order = Order("ORD-999", cust)
        order.add_item(laptop, 1)
        order.add_item(software, 1)

        # Underpayment error
        with self.assertRaises(ValueError):
            store.checkout_order(order, payment_amount=1000.0)

        # Successful checkout
        order_id, total, change = store.checkout_order(order, payment_amount=1400.0)
        self.assertEqual(order_id, "ORD-999")
        self.assertEqual(total, 1322.50)
        self.assertEqual(change, 77.50)
        self.assertEqual(laptop.stock, 2)  # Stock decremented

        # Receipt text validation
        receipt = store.generate_receipt_text(order)
        self.assertIn("Apex Electronics", receipt)
        self.assertIn("ORD-999", receipt)
        self.assertIn("1322.50", receipt)

        # File Handling: Save and load catalog
        test_cat_path = "test_apex_catalog.json"
        store.save_catalog_to_file(test_cat_path)
        self.assertTrue(os.path.exists(test_cat_path))

        new_store = StoreEngine("Restored Store")
        loaded = new_store.load_catalog_from_file(test_cat_path)
        self.assertTrue(loaded)
        self.assertIn("LAP-01", new_store.catalog)
        self.assertEqual(new_store.catalog["LAP-01"].stock, 2)
        self.assertIsInstance(new_store.catalog["LAP-01"], PhysicalProduct)
        self.assertIsInstance(new_store.catalog["SW-01"], DigitalProduct)

        # Clean up temporary test file
        if os.path.exists(test_cat_path):
            os.remove(test_cat_path)

        # Graceful handling of missing files
        self.assertFalse(new_store.load_catalog_from_file("non_existent_file_xyz.json"))


if __name__ == "__main__":
    unittest.main()
