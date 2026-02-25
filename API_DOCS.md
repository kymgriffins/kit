# Budget Ndio Story API Documentation

This document provides comprehensive API endpoint documentation for consuming the Budget Ndio Story backend from a Next.js application.

## Base URL

```
Production: https://bns.vercel.app
Development: http://localhost:8000
```

---

## ⚠️ IMPORTANT: Authentication System

The backend uses **Django REST Framework Session Authentication** (NOT JWT). The frontend API client was incorrectly configured for JWT which doesn't exist.

### Current Backend Configuration

| Setting | Value |
|---------|-------|
| Authentication | SessionAuthentication (cookie-based) |
| Permission | IsAuthenticatedOrReadOnly |
| JWT Support | ❌ Not Installed |

### Required Changes for Next.js

1. **Always include `credentials: 'include'`** in all fetch requests
2. **Use CSRF protection** - Django requires CSRF tokens for POST/PUT/DELETE
3. **No Bearer tokens** - Authentication is cookie-based

---

## Authentication Guide

### Session Authentication Flow

```typescript
// 1. Login - POST to Django admin login or custom endpoint
// 2. Browser stores session cookie automatically
// 3. All subsequent requests include the cookie
```

### Login (Using Django Admin)

```typescript
// Login via Django admin (creates session)
export async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE}/admin/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username,
      password,
      csrfmiddlewaretoken: await getCsrfToken(),
    }),
    credentials: 'include',
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  return response.json();
}

// Get CSRF token
export async function getCsrfToken(): Promise<string> {
  const response = await fetch(`${API_BASE}/api/csrf/`, {
    credentials: 'include',
  });
  const data = await response.json();
  return data.csrfToken;
}
```

### Logout

```typescript
export async function logout() {
  await fetch(`${API_BASE}/admin/logout/`, {
    method: 'POST',
    credentials: 'include',
  });
}
```

### Check Authentication Status

```typescript
export async function getCurrentUser() {
  const response = await fetch(`${API_BASE}/api/v1/accounts/users/me/`, {
    credentials: 'include',
  });
  
  if (response.status === 401) {
    return null; // Not authenticated
  }
  return response.json();
}
```

---

## Authentication API Endpoints

The following JSON API endpoints are available for authentication:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/csrf/` | Get CSRF token (required before POST) |
| POST | `/api/auth/login/` | Login with username/password |
| POST | `/api/auth/logout/` | Logout current user |
| GET | `/api/auth/user/` | Get current authenticated user |

### Example: Complete Authentication Flow

```typescript
import { login, logout, getCurrentUser, fetchCsrfToken, subscribeToNewsletter } from '@/lib/api';

// 1. Initialize - fetch CSRF token first
await fetchCsrfToken();

// 2. Login
const result = await login('myusername', 'mypassword');
if (result.success) {
  console.log('Logged in as:', result.user);
}

// 3. Check auth state
const user = await getCurrentUser();
if (user) {
  console.log('Authenticated:', user.email);
}

// 4. Make authenticated requests
await subscribeToNewsletter('user@example.com');

// 5. Logout
await logout();
```

---

## API Endpoints Reference

### 1. Accounts API (`/api/v1/accounts/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/accounts/users/` | List all users | Yes |
| POST | `/api/v1/accounts/users/` | Create new user | No (registration) |
| GET | `/api/v1/accounts/users/me/` | Get current user | Yes |
| GET | `/api/v1/accounts/users/{id}/` | Get user details | Yes |
| PUT | `/api/v1/accounts/users/{id}/` | Update user | Yes |
| PATCH | `/api/v1/accounts/users/{id}/` | Partial update user | Yes |
| DELETE | `/api/v1/accounts/users/{id}/` | Delete user | Yes |
| GET | `/api/v1/accounts/donors/` | List all donors | No |
| POST | `/api/v1/accounts/donors/` | Create donor profile | Yes |
| GET | `/api/v1/accounts/donors/{id}/` | Get donor details | Yes |
| PUT | `/api/v1/accounts/donors/{id}/` | Update donor | Yes |
| GET | `/api/v1/accounts/sponsors/` | List all sponsors | No |
| POST | `/api/v1/accounts/sponsors/` | Create sponsor profile | Yes |
| GET | `/api/v1/accounts/sponsors/{id}/` | Get sponsor details | Yes |
| GET | `/api/v1/accounts/partners/` | List all partners | No |
| POST | `/api/v1/accounts/partners/` | Create partner | Yes |
| GET | `/api/v1/accounts/organization/` | Get organization profile | No |
| GET | `/api/v1/accounts/organization/public/` | Get public org profile | No |
| GET | `/api/v1/accounts/organization/impact/` | Get impact stats | No |
| GET | `/api/v1/accounts/organization/brand/` | Get brand identity | No |
| GET | `/api/v1/accounts/organization/contact/` | Get contact info | No |

### 2. Content API (`/api/v1/content/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/content/categories/` | List all categories | No |
| GET | `/api/v1/content/categories/{id}/` | Get category details | No |
| GET | `/api/v1/content/videos/` | List all videos | No |
| POST | `/api/v1/content/videos/` | Create video | Yes |
| GET | `/api/v1/content/videos/{id}/` | Get video details | No |
| PUT | `/api/v1/content/videos/{id}/` | Update video | Yes |
| DELETE | `/api/v1/content/videos/{id}/` | Delete video | Yes |
| GET | `/api/v1/content/videos/featured/` | Get featured videos | No |
| GET | `/api/v1/content/videos/by_platform/` | Videos grouped by platform | No |
| GET | `/api/v1/content/posts/` | List all blog posts | No |
| POST | `/api/v1/content/posts/` | Create blog post | Yes |
| GET | `/api/v1/content/posts/{slug}/` | Get post by slug | No |
| PUT | `/api/v1/content/posts/{slug}/` | Update post | Yes |
| DELETE | `/api/v1/content/posts/{slug}/` | Delete post | Yes |
| GET | `/api/v1/content/posts/featured/` | Get featured post | No |
| GET | `/api/v1/content/posts/{slug}/related/` | Get related posts | No |
| GET | `/api/v1/content/playlists/` | List all playlists | No |
| POST | `/api/v1/content/playlists/` | Create playlist | Yes |
| GET | `/api/v1/content/playlists/{slug}/` | Get playlist by slug | No |
| GET | `/api/v1/content/playlists/{slug}/videos/` | Get playlist videos | No |
| GET | `/api/v1/content/news/` | List all news items | No |
| POST | `/api/v1/content/news/` | Create news item | Yes |
| GET | `/api/v1/content/news/breaking/` | Get breaking news | No |

### 3. Newsletter API (`/api/v1/newsletter/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/newsletter/subscribers/` | List all subscribers |
| POST | `/api/v1/newsletter/subscribers/` | Create subscriber |
| GET | `/api/v1/newsletter/subscribers/{id}/` | Get subscriber details |
| PUT | `/api/v1/newsletter/subscribers/{id}/` | Update subscriber |
| DELETE | `/api/v1/newsletter/subscribers/{id}/` | Delete subscriber |
| GET | `/api/v1/newsletter/campaigns/` | List all campaigns |
| POST | `/api/v1/newsletter/campaigns/` | Create campaign |
| GET | `/api/v1/newsletter/campaigns/{id}/` | Get campaign details |
| GET | `/api/v1/newsletter/logs/` | List email logs |
| GET | `/api/v1/newsletter/logs/{id}/` | Get email log details |

### 4. Sponsors API (`/api/v1/sponsors/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/sponsors/donations/` | List all donations |
| POST | `/api/v1/sponsors/donations/` | Create donation |
| GET | `/api/v1/sponsors/donations/{id}/` | Get donation details |
| PUT | `/api/v1/sponsors/donations/{id}/` | Update donation |
| GET | `/api/v1/sponsors/deliverables/` | List deliverables |
| POST | `/api/v1/sponsors/deliverables/` | Create deliverable |
| GET | `/api/v1/sponsors/deliverables/{id}/` | Get deliverable |
| GET | `/api/v1/sponsors/assets/` | List sponsor assets |
| POST | `/api/v1/sponsors/assets/` | Create sponsor asset |
| GET | `/api/v1/sponsors/assets/{id}/` | Get asset details |

### 5. Analytics API (`/api/v1/analytics/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analytics/pageviews/` | List page views |
| POST | `/api/v1/analytics/pageviews/` | Record page view |
| GET | `/api/v1/analytics/pageviews/{id}/` | Get page view details |
| GET | `/api/v1/analytics/engagement/` | List video engagements |
| POST | `/api/v1/analytics/engagement/` | Record engagement |
| GET | `/api/v1/analytics/funnel/` | List donor funnel data |
| POST | `/api/v1/analytics/funnel/` | Record funnel event |

### 6. CMS API (`/api/v1/cms/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/cms/pages/` | List all CMS pages |
| POST | `/api/v1/cms/pages/` | Create CMS page |
| GET | `/api/v1/cms/pages/{id}/` | Get page details |
| PUT | `/api/v1/cms/pages/{id}/` | Update page |
| DELETE | `/api/v1/cms/pages/{id}/` | Delete page |
| GET | `/api/v1/cms/menus/` | List all menus |
| POST | `/api/v1/cms/menus/` | Create menu |
| GET | `/api/v1/cms/menus/{id}/` | Get menu details |
| GET | `/api/v1/cms/settings/` | List site settings |
| POST | `/api/v1/cms/settings/` | Create setting |
| GET | `/api/v1/cms/widgets/` | List all widgets |
| POST | `/api/v1/cms/widgets/` | Create widget |
| GET | `/api/v1/cms/media/` | List media library |
| POST | `/api/v1/cms/media/` | Upload media |

## Query Parameters

All list endpoints support the following query parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `page` | Page number for pagination | `?page=2` |
| `page_size` | Items per page (default: 20) | `?page_size=50` |
| `search` | Search across fields | `?search=budget` |
| `ordering` | Order by field (prefix with `-` for descending) | `?ordering=-created_at` |
| `filter[field]` | Filter by field value | `?status=published` |

## Example: Next.js API Client

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface FetchOptions extends RequestInit {
  params?: Record<string, string>;
}

export async function apiClient<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { params, ...fetchOptions } = options;
  
  let url = `${API_BASE}${endpoint}`;
  
  if (params) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams.toString()}`;
  }
  
  const response = await fetch(url, {
    ...fetchOptions,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...fetchOptions.headers,
    },
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'API request failed');
  }
  
  return response.json();
}

// Usage Examples

// Get all blog posts
export async function getBlogPosts(page = 1) {
  return apiClient<{ results: BlogPost[] }>('/api/v1/content/posts/', {
    params: { page: String(page), page_size: '20' },
  });
}

// Get single post
export async function getBlogPost(slug: string) {
  return apiClient<BlogPost>(`/api/v1/content/posts/${slug}/`);
}

// Get categories
export async function getCategories() {
  return apiClient<Category[]>('/api/v1/content/categories/');
}

// Subscribe to newsletter
export async function subscribeToNewsletter(email: string) {
  return apiClient<Subscriber>('/api/v1/newsletter/subscribers/', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
}

// Get videos
export async function getVideos(contentType?: string) {
  const params = contentType ? { content_type: contentType } : {};
  return apiClient<{ results: Video[] }>('/api/v1/content/videos/', { params });
}
```

## TypeScript Types

```typescript
// types/api.ts

export interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  content_html: string;
  post_type: 'investigation' | 'explainer' | 'update' | 'field_report' | 'opinion' | 'sponsored';
  categories: Category[];
  tags: string[];
  featured_image: string;
  author: User;
  status: 'draft' | 'review' | 'published' | 'archived';
  published_at: string;
  view_count: number;
  read_time_minutes: number;
  created_at: string;
  updated_at: string;
}

export interface VideoContent {
  id: string;
  title: string;
  slug: string;
  description: string;
  platform: 'tiktok' | 'youtube' | 'x' | 'facebook' | 'instagram';
  external_id: string;
  external_url: string;
  embed_url: string;
  thumbnail_url: string;
  content_type: string;
  duration_seconds: number;
  view_count: number;
  like_count: number;
  share_count: number;
  is_featured: boolean;
  is_published: boolean;
  published_at: string;
  categories: Category[];
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  color: string;
  icon: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Subscriber {
  id: number;
  email: string;
  subscribed_at: string;
  is_active: boolean;
}

export interface Donation {
  id: number;
  amount: number;
  currency: string;
  donor_name: string;
  donor_email: string;
  status: 'pending' | 'completed' | 'failed';
  completed_at: string;
}
```

## Error Handling

```typescript
// Error handling example
try {
  const posts = await getBlogPosts();
} catch (error) {
  if (error instanceof Error) {
    console.error('API Error:', error.message);
    // Handle specific error codes
    if (error.message.includes('401')) {
      // Redirect to login
    }
    if (error.message.includes('403')) {
      // Show permission error
    }
  }
}
```

## Pagination Response Format

```typescript
interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
```

## Webhooks (Optional)

For real-time updates, consider implementing webhooks on the Next.js side to receive notifications from the Django backend.

## Media Files

Media files are served from `/media/`. Configure your Next.js to proxy media requests:

```typescript
// next.config.js
module.exports = {
  async rewrites() {
    return [
      {
        source: '/media/:path*',
        destination: 'http://localhost:8000/media/:path*',
      },
    ];
  },
};
```

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing rate limiting on the Next.js side or using Django's cache-based rate limiting.

---

For additional details, visit the API documentation at `/api/docs/` when the server is running.
