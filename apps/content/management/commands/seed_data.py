import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Models
from apps.content.models import BlogPost, NewsItem, Category, VideoContent, Playlist
from apps.newsletter.models import Subscriber
from apps.sponsors.models import Donation, SponsorAsset
from apps.accounts.models import DonorProfile, SponsorProfile, ConsortiumPartner


class Command(BaseCommand):
    help = 'Generate comprehensive seed data from 2022-2026'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting comprehensive seed data generation...'))
        
        # Clear existing data
        self.clear_data()
        
        # Create base data
        categories = self.create_categories()
        authors = self.create_authors()
        
        # Generate data by year
        for year in [2022, 2023, 2024, 2025, 2026]:
            self.stdout.write(self.style.WARNING(f'Generating data for {year}...'))
            year_categories = random.sample(categories, k=min(3, len(categories)))
            
            # 1 blog post per week (52 per year)
            self.generate_blog_posts_for_year(year, authors, categories)
            
            # 2 news items per week (104 per year)
            self.generate_news_items_for_year(year)
            
            # Videos (approximately 2 per month = 24 per year)
            self.generate_videos_for_year(year, categories)
        
        # Generate subscribers (across all years)
        self.generate_subscribers()
        
        # Generate donors and donations
        donors = self.create_donors()
        self.generate_donations(donors)
        
        # Generate sponsors
        self.create_sponsors(authors)
        
        # Generate partners
        self.create_partners()
        
        # Print summary
        self.print_summary()

    def clear_data(self):
        """Clear all existing data"""
        self.stdout.write('Clearing existing data...')
        User.objects.filter(is_superuser=False).delete()
        BlogPost.objects.all().delete()
        NewsItem.objects.all().delete()
        VideoContent.objects.all().delete()
        Playlist.objects.all().delete()
        Subscriber.objects.all().delete()
        Donation.objects.all().delete()
        SponsorAsset.objects.all().delete()
        DonorProfile.objects.all().delete()
        SponsorProfile.objects.all().delete()

    def create_categories(self):
        """Create content categories"""
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Budget Basics', 'slug': 'budget-basics', 'description': 'Understanding government budgets'},
            {'name': 'Finance Bill', 'slug': 'finance-bill', 'description': 'Kenya Finance Bill analysis'},
            {'name': 'National Budget', 'slug': 'national-budget', 'description': 'National budget coverage'},
            {'name': 'County Budget', 'slug': 'county-budget', 'description': 'County budget analysis'},
            {'name': 'Sector Deep Dive', 'slug': 'sector-deep-dive', 'description': 'In-depth sector analysis'},
            {'name': 'Tracker Story', 'slug': 'tracker-story', 'description': 'Budget tracking stories'},
            {'name': 'Youth Voice', 'slug': 'youth-voice', 'description': 'Youth perspectives'},
            {'name': 'Economy', 'slug': 'economy', 'description': 'Economic analysis'},
            {'name': 'Politics', 'slug': 'politics', 'description': 'Political coverage'},
            {'name': 'Environment', 'slug': 'environment', 'description': 'Environmental news'},
            {'name': 'Health', 'slug': 'health', 'description': 'Health sector news'},
            {'name': 'Education', 'slug': 'education', 'description': 'Education news'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, _ = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
        
        return categories

    def create_authors(self):
        """Create author users"""
        self.stdout.write('Creating authors...')
        authors = []
        
        author_names = [
            ('Jane', 'Mwangi'),
            ('John', 'Ochieng'),
            ('Sarah', 'Nekesa'),
            ('David', 'Kimani'),
            ('Grace', 'Atieno'),
        ]
        
        for i, (first_name, last_name) in enumerate(author_names):
            unique_id = uuid.uuid4().hex[:8]
            username = f'{first_name.lower()}{last_name.lower()}_{unique_id}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{unique_id}_{username}@bns.org',
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_staff': True,
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            authors.append(user)
        
        return authors

    def generate_blog_posts_for_year(self, year, authors, categories):
        """Generate exactly 52 blog posts for a year (1 per week)"""
        # Start from January 1st of the year
        start_date = datetime(year, 1, 1)
        
        blog_templates = [
            # Budget Basics
            ('Understanding the Kenya Budget Process', 'explainer', 'budget-basics'),
            ('How Your Taxes Fund Public Services', 'explainer', 'budget-basics'),
            ('Budget Vocabulary: Terms You Need to Know', 'explainer', 'budget-basics'),
            
            # Finance Bill 2024 specific
            ('Finance Bill 2024: What It Means for You', 'investigation', 'finance-bill'),
            ('Analysis: Finance Bill 2024 Tax Proposals', 'update', 'finance-bill'),
            ('Public Response to Finance Bill 2024', 'field_report', 'finance-bill'),
            
            # National Budget
            ('National Budget 2024/25: Key Highlights', 'update', 'national-budget'),
            ('Healthcare Allocation in New Budget', 'investigation', 'national-budget'),
            ('Education Funding: What Schools Can Expect', 'explainer', 'national-budget'),
            ('Infrastructure Projects in the New Budget', 'update', 'national-budget'),
            ('Defense Spending: Breaking Down the Numbers', 'investigation', 'national-budget'),
            
            # County Budget
            ('Nairobi County Budget: Where Money Goes', 'investigation', 'county-budget'),
            ('Mombasa County Budget Analysis', 'field_report', 'county-budget'),
            ('Kisumu County: Budget Priorities', 'field_report', 'county-budget'),
            ('Nakuru County: Development Spending', 'field_report', 'county-budget'),
            
            # Sector Deep Dives
            ('Healthcare Sector: Year in Review', 'sector_deep_dive', 'health'),
            ('Education Sector: Challenges and Solutions', 'sector_deep_dive', 'education'),
            ('Agriculture: Budget Analysis', 'sector_deep_dive', 'economy'),
            ('Security Sector: Funding Breakdown', 'sector_deep_dive', 'politics'),
            
            # Tracker Stories
            ('Budget Tracker: Healthcare Promise Kept?', 'tracker_story', 'health'),
            ('Education Promise: One Year Later', 'tracker_story', 'education'),
            ('Road Infrastructure: Promise vs Reality', 'tracker_story', 'economy'),
            ('Water Projects: Tracking Progress', 'tracker_story', 'environment'),
            
            # Youth Voice
            ('Youth Perspective: Budget Priorities', 'youth_voice', 'youth-voice'),
            ('Young Kenyans and Economic Freedom', 'youth_voice', 'youth-voice'),
            ('Gen Z and Civic Engagement', 'youth_voice', 'youth-voice'),
            
            # Economy
            ('Economic Outlook: Year Ahead', 'explainer', 'economy'),
            ('Inflation Impact on Households', 'investigation', 'economy'),
            ('Jobs Report: What the Numbers Show', 'update', 'economy'),
            
            # Politics
            ('Election Year: Budget Implications', 'investigation', 'politics'),
            ('MPs and the Budget Process', 'field_report', 'politics'),
            ('County Governments: Funding Challenges', 'field_report', 'politics'),
            
            # Environment
            ('Climate Change: Budget Response', 'investigation', 'environment'),
            ('Conservation: Funding Gaps', 'field_report', 'environment'),
            ('Green Initiatives: Progress Report', 'update', 'environment'),
            
            # Sponsored
            ('Partner Spotlight: Education Initiative', 'sponsored', 'education'),
            ('Corporate Social Responsibility: Healthcare', 'sponsored', 'health'),
        ]
        
        for week in range(52):
            # Calculate the publication date (spread across the year)
            days_offset = week * 7 + random.randint(0, 3)
            pub_date = start_date + timedelta(days=days_offset)
            
            # Pick a random template
            title_base, post_type, category_slug = random.choice(blog_templates)
            title = f"{title_base} - Week {week + 1}"
            
            # Get category
            category = next((c for c in categories if c.slug == category_slug), categories[0])
            
            # Generate content
            content = self.generate_blog_content(title, category.name, year)
            
            blog_post = BlogPost.objects.create(
                title=title,
                slug=slugify(title)[:40] + f'-{year}-{week}',
                excerpt=f"Analysis and insights on {title.lower()} for {category.name}",
                content=content,
                post_type=post_type,
                author=random.choice(authors),
                published_at=pub_date,
                status='published'
            )
            blog_post.categories.add(category)
            
            # Occasionally add additional categories
            if random.random() < 0.3:
                additional_cats = random.sample([c for c in categories if c != category], k=random.randint(1, 2))
                blog_post.categories.add(*additional_cats)

    def generate_blog_content(self, title, category, year):
        """Generate realistic blog content"""
        return f"""
<h2>{title}</h2>

<p>This comprehensive analysis examines {title.lower()} and its implications for Kenyan citizens. 
Our investigation draws on official government documents, expert analysis, and on-the-ground reporting.</p>

<h3>Background</h3>

<p>The context for {category} in {year} is shaped by various economic and political factors. 
Understanding these dynamics is crucial for informed citizen engagement with government budgets.</p>

<h3>Key Findings</h3>

<p>Through our analysis of official budget documents and interviews with sector experts, 
we have identified several key findings that impact ordinary Kenyans:</p>

<ul>
<li>Funding allocation priorities and their implications</li>
<li>Implementation challenges and opportunities</li>
<li>Transparency and accountability measures</li>
<li>Citizen engagement in the budget process</li>
</ul>

<h3>Expert Analysis</h3>

<p>According to budget experts, the {year} budget cycle presents both challenges and opportunities 
for improved public resource management. The emphasis on {category.lower()} reflects 
broader policy priorities.</p>

<h3>What This Means for You</h3>

<p>For ordinary citizens, understanding these budget allocations is crucial for civic engagement. 
Whether it's healthcare, education, or infrastructure, every shilling allocated has direct 
implications for public services.</p>

<h3>Looking Ahead</h3>

<p>As we move forward, continued monitoring of budget implementation will be essential. 
Citizens can play a key role in ensuring government accountability.</p>

<p><em>Published: {year}</em></p>
"""

    def generate_news_items_for_year(self, year):
        """Generate news items throughout the year"""
        start_date = datetime(year, 1, 1)
        
        news_templates = [
            ('Breaking: Government Announces New Budget Measures', True),
            ('Parliament Approves Annual Budget', False),
            ('County Governments Receive Funding', False),
            ('Economic Update: Key Indicators Released', False),
            ('Health Sector Gets Increased Allocation', False),
            ('Education Budget: Schools to Benefit', False),
            ('Infrastructure Projects Greenlit', False),
            ('Public Consultation on Budget Begins', False),
            ('Finance Bill Debate Heats Up', True),
            ('Cabinet Approves New Spending Plan', False),
            ('Audit Report Reveals Spending Gaps', True),
            ('Citizens Demand Accountability', False),
            ('Youth Groups Engage on Budget Issues', False),
            ('Experts Warn of Economic Challenges', True),
            ('International Partners Praise Transparency', False),
            ('Local Communities Participate in Forums', False),
        ]
        
        # Generate 104 news items (2 per week)
        for i in range(104):
            template, is_breaking = random.choice(news_templates)
            
            # Calculate date - spread throughout the year
            days_offset = (i * 3) + random.randint(0, 2)
            pub_date = start_date + timedelta(days=min(days_offset, 364))
            
            title = f"{template} - {pub_date.strftime('%B %d')}"
            
            content = f"""
<h3>{title}</h3>

<p>This is a developing story. Latest updates will be provided as more information becomes available.</p>

<p>Source: Budget Ndio Story Team</p>
<p>Date: {pub_date.strftime('%B %d, %Y')}</p>
"""
            
            NewsItem.objects.create(
                title=title,
                slug=slugify(title)[:40] + f'-{year}-{i}',
                content=content,
                is_breaking=is_breaking or random.random() < 0.1,  # 10% chance of breaking
                published_at=pub_date
            )

    def generate_videos_for_year(self, year, categories):
        """Generate video content for the year"""
        video_templates = [
            ('Budget Basics: Understanding Kenya\'s Money', 'budget_basics', 300, 15000),
            ('Finance Bill Explained in 5 Minutes', 'finance_bill', 300, 25000),
            ('Where Does Your Tax Money Go?', 'budget_basics', 420, 35000),
            ('County Budget Breakdown', 'county_budget', 360, 12000),
            ('Healthcare Budget Analysis', 'national_budget', 480, 18000),
            ('Education Funding Explained', 'national_budget', 360, 22000),
            ('Track the Budget: Infrastructure', 'tracker_story', 540, 15000),
            ('Youth Voice: Our Future', 'youth_voice', 300, 28000),
            ('Deep Dive: Agriculture Sector', 'sector_deep_dive', 600, 10000),
            ('Deep Dive: Security Sector', 'sector_deep_dive', 540, 12000),
            ('Interview: Budget Expert', 'explainer', 900, 8000),
            ('Community Forum Highlights', 'field_report', 720, 6000),
        ]
        
        # Generate 24 videos per year (2 per month)
        for month in range(1, 13):
            num_videos = random.randint(1, 3)
            for _ in range(num_videos):
                template_name, content_type, duration, base_views = random.choice(video_templates)
                
                # Create date
                pub_date = datetime(year, month, random.randint(1, 28))
                
                title = f"{template_name} - {pub_date.strftime('%B %Y')}"
                
                # Platform distribution
                platform = random.choice(['youtube', 'tiktok', 'x', 'instagram'])
                
                video = VideoContent.objects.create(
                    title=title,
                    slug=slugify(title)[:30] + f'-{year}-{month}-{uuid.uuid4().hex[:8]}',
                    description=f"Video content about {content_type.replace('_', ' ')}",
                    platform=platform,
                    external_id=f'{random.randint(100000, 999999)}',
                    external_url=f'https://{platform}.com/watch?v={random.randint(100000, 999999)}',
                    thumbnail_url=f'https://example.com/thumbnails/{year}/{month}.jpg',
                    content_type=content_type,
                    duration_seconds=duration,
                    view_count=base_views + random.randint(-5000, 15000),
                    like_count=random.randint(100, 5000),
                    share_count=random.randint(50, 1000),
                    comment_count=random.randint(10, 500),
                )
                
                # Add categories
                video.categories.set(random.sample(categories, k=random.randint(1, 3)))

    def generate_subscribers(self):
        """Generate newsletter subscribers"""
        self.stdout.write('Generating subscribers...')
        
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Grace', 'James', 'Mary', 
                       'Robert', 'Patricia', 'Peter', 'Faith', 'Daniel', 'Elizabeth', 'Joseph']
        last_names = ['Ochieng', 'Mwangi', 'Nekesa', 'Kimani', 'Atieno', 'Kariuki', 'Omondi',
                      'Wambui', 'Onyango', 'Akinyi', 'Mutua', 'Njoroge', 'Kamau', 'Chebet']
        
        # Generate 500 subscribers
        for i in range(500):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            
            # Random subscription date between 2022-2026
            days_ago = random.randint(0, 1500)
            sub_date = datetime.now() - timedelta(days=days_ago)
            
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'status': random.choice(['active', 'active', 'active', 'pending', 'unsubscribed']),
                    'content_preference': random.choice(['all', 'videos_only', 'blogs_only', 'weekly_digest']),
                    'subscribed_at': sub_date,
                }
            )
            
            if created and random.random() < 0.3:
                subscriber.status = random.choice(['active', 'active', 'bounced'])
                subscriber.save()

    def create_donors(self):
        """Create donor profiles"""
        self.stdout.write('Creating donors...')
        donors = []
        
        donor_data = [
            ('Kenyan', 'Diaspora', 'diaspora@example.com'),
            ('Corporate', 'Ltd', 'corporate@example.com'),
            ('Foundation', 'Trust', 'foundation@example.com'),
            ('Individual', 'Supporter', 'supporter@example.com'),
            ('Business', 'Group', 'business@example.com'),
        ]
        
        for i, (type1, type2, email) in enumerate(donor_data):
            unique_id = uuid.uuid4().hex[:8]
            user, _ = User.objects.get_or_create(
                username=f'donor{i+1}_{unique_id}',
                defaults={
                    'email': f'{unique_id}_{email}',
                    'first_name': type1,
                    'last_name': type2,
                    'is_active': True,
                }
            )
            
            donor, created = DonorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'donor_type': random.choice(['individual', 'corporate', 'foundation']),
                    'billing_address': f'{type1} {type2}',
                }
            )
            donors.append(donor)
        
        # Create more random donors
        for i in range(20):
            first = random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Evans', 'Faith'])
            last = random.choice(['Nyong\'o', 'Kenyatta', 'Odinga', 'Ruto', 'Kenyatta', 'Mudavadi'])
            unique_id = uuid.uuid4().hex[:8]
            user, _ = User.objects.get_or_create(
                username=f'donoruser{i+6}_{unique_id}',
                defaults={
                    'email': f'{first.lower()}.{last.lower()}.{unique_id}@email.com',
                    'first_name': first,
                    'last_name': last,
                    'is_active': True,
                }
            )
            
            donor = DonorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'donor_type': 'individual',
                    'billing_address': f'{first} {last}',
                }
            )[0]
            donors.append(donor)
        
        return donors

    def generate_donations(self, donors):
        """Generate donation records"""
        self.stdout.write('Generating donations...')
        
        # Generate donations across 2022-2026
        for year in [2022, 2023, 2024, 2025, 2026]:
            # 5-15 donations per year
            num_donations = random.randint(5, 15)
            
            for _ in range(num_donations):
                donor = random.choice(donors)
                
                # Random date in the year
                days_offset = random.randint(0, 364)
                donation_date = datetime(year, 1, 1) + timedelta(days=days_offset)
                
                amount = random.choice([
                    random.randint(1000, 5000),    # Small
                    random.randint(5000, 25000),   # Medium
                    random.randint(25000, 100000), # Large
                    random.randint(100000, 500000), # Major
                ])
                
                donation = Donation.objects.create(
                    donor=donor,
                    amount=amount,
                    currency='KES',
                    payment_method=random.choice(['mpesa', 'card', 'bank', 'paypal']),
                    status='completed',
                    transaction_id=f'TXN{random.randint(100000, 999999)}',
                    receipt_number=f'RCPT-{uuid.uuid4().hex[:8].upper()}',
                    is_recurring=random.random() < 0.2,
                    created_at=donation_date,
                    completed_at=donation_date + timedelta(hours=random.randint(1, 48)),
                )
                
                # Occasionally create recurring instances
                if donation.is_recurring:
                    for month in range(1, random.randint(2, 6)):
                        recur_date = donation_date + timedelta(days=30*month)
                        if recur_date <= datetime(2026, 12, 31):
                            Donation.objects.create(
                                donor=donor,
                                amount=amount,
                                currency='KES',
                                payment_method=donation.payment_method,
                                status='completed',
                                transaction_id=f'TXN{random.randint(100000, 999999)}',
                                receipt_number=f'RCPT-{uuid.uuid4().hex[:8].upper()}',
                                is_recurring=False,
                                parent_donation=donation,
                                created_at=recur_date,
                                completed_at=recur_date + timedelta(hours=12),
                            )

    def create_sponsors(self, authors):
        """Create sponsor profiles"""
        self.stdout.write('Creating sponsors...')
        
        sponsors_data = [
            ('Safaricom Foundation', 'https://safaricom.co.ke'),
            ('Kenya Commercial Bank', 'https://kcb.co.ke'),
            ('Equity Bank', 'https://equitybank.co.ke'),
            ('Family Bank', 'https://familybank.co.ke'),
            ('Britam', 'https://britam.com'),
            ('Jubilee Insurance', 'https://jubileeinsurance.com'),
            ('APA Insurance', 'https://apainsurance.org'),
            ('Old Mutual', 'https://oldmutualkenya.com'),
        ]
        
        for i, (org_name, website) in enumerate(sponsors_data):
            unique_id = uuid.uuid4().hex[:8]
            user, _ = User.objects.get_or_create(
                username=f'sponsor{i+1}_{unique_id}',
                defaults={
                    'email': f'{unique_id}_info@{org_name.lower().replace(" ", "")}.org',
                    'first_name': org_name.split()[0],
                    'last_name': 'Sponsor',
                    'is_active': True,
                }
            )
            
            unique_id = uuid.uuid4().hex[:8]
            
            SponsorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'company_name': org_name,
                    'website': website,
                    'level': random.choice(['gold', 'silver', 'bronze']),
                    'contract_value': random.randint(5000, 50000),
                    'contract_start': datetime.now().date() - timedelta(days=random.randint(30, 365)),
                    'contract_end': datetime.now().date() + timedelta(days=random.randint(30, 365)),
                }
            )

    def create_partners(self):
        """Create consortium partners"""
        self.stdout.write('Creating partners...')
        
        partners_data = [
            ('The Continental Pot', 'Media Partner'),
            ('Colour Twist Media', 'Digital Partner'),
            ('Sen Media', 'News Partner'),
            ('African Centre for Media', 'Research Partner'),
            ('Civic Watch Kenya', 'Advocacy Partner'),
        ]
        
        for org_name, partner_type in partners_data:
            slug = org_name.lower().replace(' ', '-').replace('&', 'and')
            ConsortiumPartner.objects.get_or_create(
                name=org_name,
                defaults={
                    'slug': slug,
                    'description': f'{org_name} - {partner_type}',
                    'website': f'https://{org_name.lower().replace(" ", "").replace("&", "and")}.org',
                    'is_active': True,
                }
            )

    def print_summary(self):
        """Print data summary"""
        self.stdout.write(self.style.SUCCESS('\n=== Seed Data Summary ==='))
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Authors: {User.objects.filter(is_staff=True).count()}')
        self.stdout.write(f'Blog Posts: {BlogPost.objects.count()}')
        self.stdout.write(f'News Items: {NewsItem.objects.count()}')
        self.stdout.write(f'Videos: {VideoContent.objects.count()}')
        self.stdout.write(f'Subscribers: {Subscriber.objects.count()}')
        self.stdout.write(f'Donors: {DonorProfile.objects.count()}')
        self.stdout.write(f'Donations: {Donation.objects.count()}')
        self.stdout.write(f'Sponsors: {SponsorProfile.objects.count()}')
        self.stdout.write(f'Partners: {ConsortiumPartner.objects.count()}')
        
        # Year breakdown
        self.stdout.write(self.style.WARNING('\n=== Blog Posts by Year ==='))
        for year in [2022, 2023, 2024, 2025, 2026]:
            count = BlogPost.objects.filter(published_at__year=year).count()
            self.stdout.write(f'{year}: {count} posts')
        
        self.stdout.write(self.style.SUCCESS('\nSeed data generation complete!'))
