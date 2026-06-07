import os
import urllib.request
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds database with categories, developer products in INR, and downloads premium photos.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with Indian market prices and premium setup images...')

        # 1. Create Default Admin Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: username="admin", password="adminpassword"'))
        else:
            self.stdout.write('Superuser "admin" already exists.')

        # 2. Categories definition
        categories_data = [
            {
                'name': 'Keyboards',
                'description': 'Mechanical, split, ergonomic, and wireless keyboards for peak typing efficiency.'
            },
            {
                'name': 'Monitors',
                'description': 'Ultra-wide, curved, and vertical monitors for massive screen real estate.'
            },
            {
                'name': 'Mice',
                'description': 'Ergonomic vertical mice and ultra-lightweight gaming mice.'
            },
            {
                'name': 'Audio',
                'description': 'Active noise-canceling headphones and studio-quality condenser microphones.'
            },
            {
                'name': 'Ergonomic Chairs',
                'description': 'Premium mesh task chairs engineered for lumbar comfort during long coding sessions.'
            }
        ]

        categories = {}
        for cat_info in categories_data:
            cat, created = Category.objects.get_or_create(
                name=cat_info['name'],
                defaults={'description': cat_info['description']}
            )
            categories[cat_info['name']] = cat
            if created:
                self.stdout.write(f'Created Category: {cat.name}')

        # Create media directory for saving images
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)

        # 3. Products definition with INR pricing and Unsplash source URLs
        products_data = [
            # Keyboards
            {
                'category': 'Keyboards',
                'name': 'Keychron K2 Wireless Keyboard',
                'description': 'A 75% layout wireless mechanical keyboard with Gateron switches and RGB backlighting. Features hot-swappable keys and compatibility with macOS and Windows.',
                'price': 7999.00,
                'stock': 25,
                'img_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80'
            },
            {
                'category': 'Keyboards',
                'name': 'ErgoDox EZ Split Keyboard',
                'description': 'An ergonomic split mechanical keyboard with custom firmware. Highly customizable layout, column-linear keys, and dual wrist rests.',
                'price': 24999.00,
                'stock': 8,
                'img_url': 'https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=600&auto=format&fit=crop&q=80'
            },
            {
                'category': 'Keyboards',
                'name': 'HHKB Professional Hybrid Type-S',
                'description': 'Happy Hacking Keyboard featuring Topre electrostatic capacitive silent switches. Compact 60% layout designed for programmers.',
                'price': 21999.00,
                'stock': 12,
                'img_url': 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&auto=format&fit=crop&q=80'
            },
            # Monitors
            {
                'category': 'Monitors',
                'name': 'Dell UltraSharp 38 Curved Monitor',
                'description': 'A 38-inch curved ultrawide WQHD+ monitor. USB-C hub connectivity provides up to 90W of power delivery to charge your laptop.',
                'price': 79999.00,
                'stock': 5,
                'img_url': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&auto=format&fit=crop&q=80'
            },
            {
                'category': 'Monitors',
                'name': 'LG DualUp 28-Inch Monitor',
                'description': 'A unique 16:18 aspect ratio screen, equivalent to two 21-inch monitors stacked. Fits vertical code listings and documents perfectly.',
                'price': 49999.00,
                'stock': 15,
                'img_url': 'https://images.unsplash.com/photo-1547082299-de196ea013d6?w=600&auto=format&fit=crop&q=80'
            },
            # Mice
            {
                'category': 'Mice',
                'name': 'Logitech MX Master 3S',
                'description': 'The ultimate ergonomic productivity mouse. Features a MagSpeed electromagnetic scroll wheel, 8K DPI sensor, and silent clicks.',
                'price': 8999.00,
                'stock': 35,
                'img_url': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=600&auto=format&fit=crop&q=80'
            },
            {
                'category': 'Mice',
                'name': 'Anker Ergonomic Vertical Mouse',
                'description': 'A vertical mouse designed to reduce wrist strain. Encourages a healthy neutral "handshake" wrist alignment.',
                'price': 2499.00,
                'stock': 50,
                'img_url': 'https://images.unsplash.com/photo-1629429408209-1f912961dbd8?w=600&auto=format&fit=crop&q=80'
            },
            # Audio
            {
                'category': 'Audio',
                'name': 'Sony WH-1000XM5 Headphones',
                'description': 'Industry-leading active noise-canceling wireless headphones. Equipped with 8 microphones and a dual-processor noise cancellation system.',
                'price': 29999.00,
                'stock': 20,
                'img_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80'
            },
            {
                'category': 'Audio',
                'name': 'Shure SM7B Vocal Microphone',
                'description': 'A legendary dynamic cardioid microphone used for recording podcasts, music, and streaming. Yields warm, smooth vocals.',
                'price': 34999.00,
                'stock': 10,
                'img_url': 'https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=600&auto=format&fit=crop&q=80'
            },
            # Ergonomic Chairs
            {
                'category': 'Ergonomic Chairs',
                'name': 'Herman Miller Aeron Chair',
                'description': 'The gold standard of ergonomic office seating. Features Pellicle mesh backing for temperature control, PostureFit SL lumbar support, and fully adjustable armrests.',
                'price': 119999.00,
                'stock': 4,
                'img_url': 'https://images.unsplash.com/photo-1580481072645-022f9a6dbf27?w=600&auto=format&fit=crop&q=80'
            },
            {
                'category': 'Ergonomic Chairs',
                'name': 'Steelcase Gesture Office Chair',
                'description': 'Designed for multi-device support. The Gesture adapts to a wide range of natural postures, encouraging healthy sitting behaviors.',
                'price': 99999.00,
                'stock': 6,
                'img_url': 'https://images.unsplash.com/photo-1505797149-43b0069ec26b?w=600&auto=format&fit=crop&q=80'
            }
        ]

        for prod_info in products_data:
            cat = categories[prod_info['category']]
            prod, created = Product.objects.get_or_create(
                name=prod_info['name'],
                defaults={
                    'category': cat,
                    'description': prod_info['description'],
                    'price': prod_info['price'],
                    'stock': prod_info['stock']
                }
            )
            
            # If product is newly created or has no image file set, download it
            if created or not prod.image:
                filename = prod_info['name'].lower().replace(' ', '_').replace('-', '_') + '.jpg'
                filepath = os.path.join(media_products_dir, filename)
                
                # Check if file exists first to avoid repeating downloads
                if not os.path.exists(filepath):
                    self.stdout.write(f'Downloading image for "{prod.name}"...')
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    req = urllib.request.Request(prod_info['img_url'], headers=headers)
                    try:
                        with urllib.request.urlopen(req, timeout=15) as response:
                            with open(filepath, 'wb') as out_file:
                                out_file.write(response.read())
                        prod.image = f'products/{filename}'
                        prod.save()
                        self.stdout.write(self.style.SUCCESS(f'Linked downloaded photo to "{prod.name}"'))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'Could not download photo for {prod.name}: {e}'))
                else:
                    prod.image = f'products/{filename}'
                    prod.save()
                    self.stdout.write(f'Linked existing photo to "{prod.name}"')

            elif not created and prod.price != prod_info['price']:
                prod.price = prod_info['price']
                prod.save()
                self.stdout.write(f'Updated price to INR for "{prod.name}"')

        self.stdout.write(self.style.SUCCESS('Database seeding and image synchronization completed!'))
