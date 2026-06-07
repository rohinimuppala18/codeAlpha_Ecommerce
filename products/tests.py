from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Review

class ProductModelTest(TestCase):
    def setUp(self):
        # Create a category
        self.category = Category.objects.create(
            name="Developer Tools",
            description="Software and developer licenses"
        )
        # Create a product
        self.product = Product.objects.create(
            category=self.category,
            name="IDE License Ultimate",
            description="All products pack for development.",
            price=199.99,
            stock=10
        )
        # Create a test user
        self.user = User.objects.create_user(
            username='testcoder',
            email='coder@test.com',
            password='testpassword'
        )

    def test_automatic_slug_generation(self):
        """Verifies that category and product slugs are automatically populated on save."""
        self.assertEqual(self.category.slug, "developer-tools")
        self.assertEqual(self.product.slug, "ide-license-ultimate")

    def test_average_rating_calculation(self):
        """Verifies that average rating calculation is accurate for multiple reviews."""
        # Initial rating should be 0.0
        self.assertEqual(self.product.average_rating, 0.0)

        # Submit first review
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Awesome IDE! Saved me hours of work."
        )
        self.assertEqual(self.product.average_rating, 5.0)

        # Submit second review from another user
        user2 = User.objects.create_user(username='tester2', password='pass2')
        Review.objects.create(
            product=self.product,
            user=user2,
            rating=3,
            comment="It's good but uses too much memory."
        )
        # Average of 5 and 3 should be 4.0
        self.assertEqual(self.product.average_rating, 4.0)


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Displays")
        self.product = Product.objects.create(
            category=self.category,
            name="4K Coding Monitor",
            description="Chrystalline text clarity.",
            price=399.00,
            stock=5
        )

    def test_homepage_view(self):
        """Verifies that the homepage resolves and renders correctly."""
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AlphaCart")
        self.assertContains(response, "4K Coding Monitor")

    def test_shop_view(self):
        """Verifies that the catalog view displays all products and categories."""
        response = self.client.get(reverse('products:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "4K Coding Monitor")

    def test_product_detail_view(self):
        """Verifies that product details load correctly with details and actions."""
        response = self.client.get(reverse('products:product_detail', args=[self.product.id, self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "4K Coding Monitor")
        self.assertContains(response, "Displays")
        self.assertContains(response, "₹399.00")
