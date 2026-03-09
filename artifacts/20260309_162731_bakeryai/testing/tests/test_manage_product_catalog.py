import pytest
from generated_app.manage_product_catalog import build_manage_product_catalog

def test_build_manage_product_catalog():
    """
    Test if build_manage_product_catalog function is correctly built
    """
    assert build_manage_product_catalog is not None

@pytest.fixture
def manage_product_catalog():
    """
    Fixture to provide manage_product_catalog instance for tests
    """
    return build_manage_product_catalog()

class TestManageProductCatalog:

    @pytest.mark.usefixtures("manage_product_catalog")
    def test_add_product(self, manage_product_catalog):
        """
        Test adding a new product to the catalog
        """
        product = manage_product_catalog.add_product(
            "Bread",
            "Freshly baked artisan bread",
            price=1.5,
            stock=10,
            image="bread.jpg"
        )
        assert product is not None
        assert product.name == "Bread"
        assert product.description == "Freshly baked artisan bread"
        assert product.price == 1.5
        assert product.stock == 10

    @pytest.mark.usefixtures("manage_product_catalog")
    def test_edit_product(self, manage_product_catalog):
        """
        Test editing an existing product's details
        """
        product = manage_product_catalog.add_product(
            "Cake",
            "Delicious chocolate cake",
            price=3.5,
            stock=5,
            image="cake.jpg"
        )
        manage_product_catalog.edit_product(product.id, name="Cake Red Velvet", description="Red Velvet cake")
        edited_product = manage_product_catalog.get_product_by_id(product.id)
        assert edited_product.name == "Cake Red Velvet"
        assert edited_product.description == "Red Velvet cake"

    @pytest.mark.usefixtures("manage_product_catalog")
    def test_delete_product(self, manage_product_catalog):
        """
        Test deleting a product from the catalog
        """
        product = manage_product_catalog.add_product(
            "Pastry",
            "Buttery croissant",
            price=2.5,
            stock=7,
            image="pastry.jpg"
        )
        manage_product_catalog.delete_product(product.id)
        with pytest.raises(KeyError):
            manage_product_catalog.get_product_by_id(product.id)
