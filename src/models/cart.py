from pydantic import BaseModel

from src.models.products import Product


class CartItem(BaseModel):
    product: Product
    quantity: int


class Cart(BaseModel):
    items: list[CartItem]

    def calculate_total(self) -> float:
        """Calculate the total price of all items in the cart."""
        return sum(item.product.price * item.quantity for item in self.items)

    def add_product(self, product: Product, quantity: int = 1) -> None:
        """Add product to cart or increase quantity if already exists."""
        # Check if product already exists in cart
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += quantity
                return

        # If not found, add as new item
        self.items.append(CartItem(product=product, quantity=quantity))

    def update_quantity(self, product_id: str, quantity: int) -> None:
        """Update quantity of a product in the cart."""
        for item in self.items:
            if item.product.id == product_id:
                if quantity <= 0:
                    # Remove item if quantity is zero or negative
                    self.items.remove(item)
                else:
                    item.quantity = quantity
                break

    def remove_product(self, product_id: str) -> None:
        """Remove a product from the cart."""
        self.items = [
            item for item in self.items if item.product.id != product_id
        ]
