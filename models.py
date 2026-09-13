from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    CATEGORY_TYPES = [
        ('story', 'Story Book'),
        ('research', 'Research Book'),
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-Fiction'),
        ('education', 'Education'),
        ('tech', 'Technology'),
        ('science', 'Science'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('children', 'Children\'s Book'),
        ('comics', 'Comics & Graphic Novels'),
        ('poetry', 'Poetry'),
        ('selfhelp', 'Self-Help'),
        ('business', 'Business'),
        ('health', 'Health & Wellness'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='story')
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Book(models.Model):
    BOOK_TYPES = [
        ('story', 'Story Book'),
        ('research', 'Research Book'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    cover_image_url = models.URLField(blank=True, null=True)  # External image URL
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES, default='general')

    # Book details
    publisher = models.CharField(max_length=100, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    pages = models.IntegerField(default=0)
    language = models.CharField(max_length=50, default='English')
    isbn = models.CharField(max_length=20, blank=True)

    # Featured flags
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_audiobook = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    # Rating
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.0)
    total_reviews = models.IntegerField(default=0)

    # Stock
    stock_quantity = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_cover_url(self):
        """Get cover image URL - priority: uploaded image > external URL > default"""
        if self.cover_image and hasattr(self.cover_image, 'url') and self.cover_image.url:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        return '/static/images/default-book.jpg'
