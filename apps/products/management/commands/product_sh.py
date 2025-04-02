from django.core.management.base import BaseCommand
from apps.products.models import Product, Category  
from apps.users.models import User
from django.utils.text import slugify
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populates the products and categories in the database.'

    def handle(self, *args, **kwargs):
        # Define your mock categories
        categories_data = [
            {'name': 'Electronics'},
            {'name': 'Fashion'},
            {'name': 'Home & Garden'},
            {'name': 'Beauty & Health'},
            {'name': 'Sports & Outdoors'},
            {'name': 'Books & Media'},
        ]
        
        # Create categories if they don't exist
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=category_data['name']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' created"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' already exists"))
        
        # Define your mock products
        products = [
    {
        'id': 'prod1',
        'name': 'Smartphone X',
        'description': 'Latest flagship smartphone with high-end features and camera',
        'price': 899.99,
        'discountPrice': 799.99,
        'images': [
            'https://images.unsplash.com/photo-1598327105666-5b89351aff97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=327&q=80',
            'https://images.unsplash.com/photo-1546054454-aa26e2b734c7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=580&q=80'
        ],
        'category': 'Electronics',
        'vendorId': 'v1',
        'vendorName': 'TechGadgets Inc.',
        'rating': 4.7,
        'stock': 25,
        'createdAt': '2023-01-15T08:00:00Z',
        'updatedAt': '2023-01-15T08:00:00Z'
    },
    {
        'id': 'prod2',
        'name': 'Laptop Pro',
        'description': 'Powerful laptop for professionals with high-performance specs',
        'price': 1299.99,
        'images': [
            'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1171&q=80',
            'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=464&q=80'
        ],
        'category': 'Electronics',
        'vendorId': 'v1',
        'vendorName': 'TechGadgets Inc.',
        'rating': 4.5,
        'stock': 10,
        'createdAt': '2023-01-18T09:30:00Z',
        'updatedAt': '2023-01-18T09:30:00Z'
    },
    {
        'id': 'prod3',
        'name': 'Wireless Earbuds',
        'description': 'Premium wireless earbuds with noise cancellation',
        'price': 149.99,
        'discountPrice': 129.99,
        'images': [
            'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1078&q=80',
            'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1632&q=80'
        ],
        'category': 'Electronics',
        'vendorId': 'v2',
        'vendorName': 'AudioMasters',
        'rating': 4.3,
        'stock': 50,
        'createdAt': '2023-01-20T10:15:00Z',
        'updatedAt': '2023-01-20T10:15:00Z'
    },
    {
        'id': 'prod4',
        'name': 'Designer Dress',
        'description': 'Elegant designer dress for special occasions',
        'price': 199.99,
        'images': [
            'https://images.unsplash.com/photo-1623609163859-ca93c959b5b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=386&q=80',
            'https://images.unsplash.com/photo-1623609163903-1d3b962d2d15?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=386&q=80'
        ],
        'category': 'Fashion',
        'vendorId': 'v3',
        'vendorName': 'Fashion Couture',
        'rating': 4.8,
        'stock': 15,
        'createdAt': '2023-02-01T11:45:00Z',
        'updatedAt': '2023-02-01T11:45:00Z'
    },
    {
        'id': 'prod5',
        'name': 'Smart Watch',
        'description': 'Feature-packed smartwatch with health tracking',
        'price': 249.99,
        'discountPrice': 199.99,
        'images': [
            'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=327&q=80',
            'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1172&q=80'
        ],
        'category': 'Electronics',
        'vendorId': 'v1',
        'vendorName': 'TechGadgets Inc.',
        'rating': 4.6,
        'stock': 30,
        'createdAt': '2023-02-05T14:20:00Z',
        'updatedAt': '2023-02-05T14:20:00Z'
    },
    {
        'id': 'prod6',
        'name': 'Premium Coffee Maker',
        'description': 'Professional-grade coffee maker for home use',
        'price': 179.99,
        'images': [
            'https://images.unsplash.com/photo-1606741965429-02919c1f9f14?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1174&q=80',
            'https://images.unsplash.com/photo-1561047029-3000c68339ca?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=773&q=80'
        ],
        'category': 'Home & Garden',
        'vendorId': 'v4',
        'vendorName': 'Home Essentials',
        'rating': 4.4,
        'stock': 20,
        'createdAt': '2023-02-10T16:00:00Z',
        'updatedAt': '2023-02-10T16:00:00Z'
    },
    {
        'id': 'prod7',
        'name': 'Skincare Set',
        'description': 'Complete skincare regimen with natural ingredients',
        'price': 89.99,
        'discountPrice': 69.99,
        'images': [
            'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80',
            'https://images.unsplash.com/photo-1599305445671-ac291c95aaa9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1169&q=80'
        ],
        'category': 'Beauty & Health',
        'vendorId': 'v5',
        'vendorName': 'Natural Beauty',
        'rating': 4.9,
        'stock': 35,
        'createdAt': '2023-02-15T09:10:00Z',
        'updatedAt': '2023-02-15T09:10:00Z'
    },
    {
        'id': 'prod8',
        'name': 'Yoga Mat',
        'description': 'Professional non-slip yoga mat for all yoga styles',
        'price': 49.99,
        'images': [
            'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80',
            'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=880&q=80'
        ],
        'category': 'Sports & Outdoors',
        'vendorId': 'v6',
        'vendorName': 'FitLife',
        'rating': 4.2,
        'stock': 40,
        'createdAt': '2023-02-20T10:30:00Z',
        'updatedAt': '2023-02-20T10:30:00Z'
    },
    {
        'id': 'prod9',
        'name': 'Bestselling Novel',
        'description': 'Award-winning fiction novel by acclaimed author',
        'price': 24.99,
        'discountPrice': 19.99,
        'images': [
            'https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80',
            'https://images.unsplash.com/photo-1512820790803-83ca734da794?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1198&q=80'
        ],
        'category': 'Books & Media',
        'vendorId': 'v7',
        'vendorName': 'Book Haven',
        'rating': 4.7,
        'stock': 60,
        'createdAt': '2023-02-25T13:45:00Z',
        'updatedAt': '2023-02-25T13:45:00Z'
    },
    {
        'id': 'prod10',
        'name': 'Men\'s Leather Wallet',
        'description': 'Handcrafted genuine leather wallet with multiple compartments',
        'price': 59.99,
        'images': [
            'https://images.unsplash.com/photo-1627123424574-724758594e93?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=387&q=80',
            'https://images.unsplash.com/photo-1641431953118-cb1280080de1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=465&q=80'
        ],
        'category': 'Fashion',
        'vendorId': 'v3',
        'vendorName': 'Fashion Couture',
        'rating': 4.5,
        'stock': 45,
        'createdAt': '2023-03-01T15:20:00Z',
        'updatedAt': '2023-03-01T15:20:00Z'
    },
    {
        'id': 'prod11',
        'name': 'Wireless Keyboard and Mouse',
        'description': 'Ergonomic wireless keyboard and mouse combo for productivity',
        'price': 79.99,
        'discountPrice': 69.99,
        'images': [
            'https://images.unsplash.com/photo-1587829741301-dc798b83add3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1165&q=80',
            'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1167&q=80'
        ],
        'category': 'Electronics',
        'vendorId': 'v1',
        'vendorName': 'TechGadgets Inc.',
        'rating': 4.3,
        'stock': 25,
        'createdAt': '2023-03-05T09:00:00Z',
        'updatedAt': '2023-03-05T09:00:00Z'
    },
    {
        'id': 'prod12',
        'name': 'Indoor Plant Set',
        'description': 'Collection of 3 low-maintenance indoor plants with decorative pots',
        'price': 69.99,
        'images': [
            'https://images.unsplash.com/photo-1545165375-7c5f3a5cf057?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=474&q=80',
            'https://images.unsplash.com/photo-1509423350716-97f9360b4e09?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=449&q=80'
        ],
        'category': 'Home & Garden',
        'vendorId': 'v4',
        'vendorName': 'Home Essentials',
        'rating': 4.6,
        'stock': 30,
        'createdAt': '2023-03-10T11:30:00Z',
        'updatedAt': '2023-03-10T11:30:00Z'
    }
]

        user = User.objects.filter(user_type='Vendor').first()
        
        # Loop through the products data and create product entries
        for product_data in products:
            category = Category.objects.get(name=product_data['category'])
            
            # Create the product object
            product = Product(
                user=user,  # You may need to assign the appropriate user here
                category=category,
                title=product_data['name'],
                description=product_data['description'],
                price=int(product_data['price']),
                photo1=product_data['images'][0],
                stock_quantity=product_data['stock'],
                # is_active=product_data['is_active'],
                rating = product_data['rating'],
                discount_price=product_data.get('discountPrice',product_data['price'])
                
            )
            
            # Save the product
            product.save()
            self.stdout.write(self.style.SUCCESS(f"Product '{product.title}' created"))
