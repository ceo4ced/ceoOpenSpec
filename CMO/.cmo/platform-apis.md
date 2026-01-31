# CMO Platform API Reference

## Overview

This document specifies the social media platform API integrations available to CMO for content distribution.

> **All API calls require Human approval before posting to production accounts.**

---

## Platform Status

| Platform | API Status | Integration Level |
|----------|------------|-------------------|
| TikTok | ✅ Primary | Full |
| Instagram | 🟡 Planned | Specification ready |
| X (Twitter) | 🟡 Planned | Specification ready |
| YouTube | 🟡 Planned | Specification ready |
| LinkedIn | 🟡 Planned | Specification ready |

---

## TikTok API

### Authentication

```yaml
tiktok:
  auth_type: OAuth 2.0
  scopes:
    - user.info.basic
    - video.publish
    - video.list
  
  endpoints:
    base: https://open.tiktokapis.com/v2
    auth: https://www.tiktok.com/v2/auth/authorize/
```

### Video Upload

```python
async def publish_to_tiktok(video: dict) -> dict:
    """
    Publish video to TikTok.
    REQUIRES HUMAN APPROVAL BEFORE EXECUTION.
    """
    # Step 1: Human approval
    approval = await request_human_approval(
        type='content_publish',
        platform='tiktok',
        content=video
    )
    if not approval.approved:
        return {'status': 'rejected', 'reason': approval.reason}
    
    # Step 2: Initialize upload
    init = await tiktok_api.post('/video/init/', {
        'source_info': {
            'source': 'FILE_UPLOAD',
            'video_size': video['size_bytes']
        }
    })
    
    # Step 3: Upload video chunks
    await upload_chunks(init['upload_url'], video['file_path'])
    
    # Step 4: Publish
    result = await tiktok_api.post('/video/publish/', {
        'post_info': {
            'title': video['caption'],
            'privacy_level': 'PUBLIC_TO_EVERYONE',
            'disable_duet': False,
            'disable_stitch': False,
            'disable_comment': False
        },
        'source_info': {
            'source': 'FILE_UPLOAD',
            'video_size': video['size_bytes']
        }
    })
    
    # Log
    log_to_bigquery('content_published', {
        'platform': 'tiktok',
        'video_id': result['video_id'],
        'published_at': datetime.now(),
        'approved_by': approval.approver
    })
    
    return result
```

### Analytics

```python
async def get_tiktok_analytics(video_id: str) -> dict:
    """
    Get video analytics from TikTok.
    """
    return await tiktok_api.get(f'/video/query/', {
        'filters': {'video_ids': [video_id]},
        'fields': [
            'view_count',
            'like_count',
            'comment_count',
            'share_count',
            'create_time'
        ]
    })
```

---

## Instagram Graph API

### Authentication

```yaml
instagram:
  auth_type: OAuth 2.0
  platform: Meta Business Suite
  scopes:
    - instagram_basic
    - instagram_content_publish
    - instagram_manage_insights
    
  endpoints:
    base: https://graph.facebook.com/v18.0
```

### Content Types

| Type | Endpoint | Notes |
|------|----------|-------|
| Photo | `/{ig-user-id}/media` | Single image |
| Carousel | `/{ig-user-id}/media` | Multiple images |
| Reel | `/{ig-user-id}/media` | Short video |
| Story | Not in Graph API | Requires Instagram app |

### Publish Photo

```python
async def publish_to_instagram(content: dict) -> dict:
    """
    Publish to Instagram.
    REQUIRES HUMAN APPROVAL BEFORE EXECUTION.
    """
    # Human approval
    approval = await request_human_approval(
        type='content_publish',
        platform='instagram',
        content=content
    )
    if not approval.approved:
        return {'status': 'rejected'}
    
    # Step 1: Create media container
    creation = await ig_api.post(f'/{IG_USER_ID}/media', {
        'image_url': content['image_url'],
        'caption': content['caption'],
        'access_token': ACCESS_TOKEN
    })
    
    container_id = creation['id']
    
    # Step 2: Wait for processing
    await wait_for_processing(container_id)
    
    # Step 3: Publish container
    result = await ig_api.post(f'/{IG_USER_ID}/media_publish', {
        'creation_id': container_id,
        'access_token': ACCESS_TOKEN
    })
    
    return result
```

---

## X (Twitter) API v2

### Authentication

```yaml
twitter:
  auth_type: OAuth 2.0 + OAuth 1.0a
  scopes:
    - tweet.read
    - tweet.write
    - users.read
    
  endpoints:
    base: https://api.twitter.com/2
```

### Post Tweet

```python
async def post_tweet(tweet: dict) -> dict:
    """
    Post to X/Twitter.
    REQUIRES HUMAN APPROVAL BEFORE EXECUTION.
    """
    # Human approval
    approval = await request_human_approval(
        type='content_publish',
        platform='twitter',
        content=tweet
    )
    if not approval.approved:
        return {'status': 'rejected'}
    
    # Post tweet
    result = await twitter_api.post('/tweets', {
        'text': tweet['text'],
        'media': tweet.get('media'),  # Optional
        'reply_settings': 'everyone'
    })
    
    return result
```

### Media Upload

```python
async def upload_twitter_media(media: dict) -> str:
    """
    Upload media to Twitter.
    """
    # Initialize upload
    init = await twitter_api.post('/media/upload', {
        'command': 'INIT',
        'media_type': media['mime_type'],
        'total_bytes': media['size_bytes']
    })
    
    media_id = init['media_id_string']
    
    # Upload chunks
    await upload_chunks_twitter(media_id, media['file_path'])
    
    # Finalize
    await twitter_api.post('/media/upload', {
        'command': 'FINALIZE',
        'media_id': media_id
    })
    
    return media_id
```

---

## YouTube Data API v3

### Authentication

```yaml
youtube:
  auth_type: OAuth 2.0
  scopes:
    - https://www.googleapis.com/auth/youtube.upload
    - https://www.googleapis.com/auth/youtube.readonly
    
  endpoints:
    base: https://www.googleapis.com/youtube/v3
    upload: https://www.googleapis.com/upload/youtube/v3
```

### Video Upload

```python
async def upload_to_youtube(video: dict) -> dict:
    """
    Upload video to YouTube.
    REQUIRES HUMAN APPROVAL BEFORE EXECUTION.
    """
    # Human approval
    approval = await request_human_approval(
        type='content_publish',
        platform='youtube',
        content=video
    )
    if not approval.approved:
        return {'status': 'rejected'}
    
    # Prepare metadata
    body = {
        'snippet': {
            'title': video['title'],
            'description': video['description'],
            'tags': video.get('tags', []),
            'categoryId': video.get('category_id', '22')  # People & Blogs
        },
        'status': {
            'privacyStatus': 'private',  # Always start private
            'selfDeclaredMadeForKids': video.get('made_for_kids', False)
        }
    }
    
    # Upload video
    result = await youtube_api.upload(
        '/videos?part=snippet,status',
        body=body,
        media=video['file_path']
    )
    
    return result
```

---

## LinkedIn API

### Authentication

```yaml
linkedin:
  auth_type: OAuth 2.0
  scopes:
    - w_member_social
    - r_organization_social
    
  endpoints:
    base: https://api.linkedin.com/v2
```

### Share Post

```python
async def post_to_linkedin(post: dict) -> dict:
    """
    Post to LinkedIn.
    REQUIRES HUMAN APPROVAL BEFORE EXECUTION.
    """
    # Human approval
    approval = await request_human_approval(
        type='content_publish',
        platform='linkedin',
        content=post
    )
    if not approval.approved:
        return {'status': 'rejected'}
    
    # Create share
    result = await linkedin_api.post('/shares', {
        'owner': f'urn:li:organization:{ORG_ID}',
        'text': {'text': post['text']},
        'distribution': {
            'linkedInDistributionTarget': {}
        }
    })
    
    return result
```

---

## Nano Banana API

### Configuration

```yaml
nano_banana:
  purpose: AI content generation
  
  endpoints:
    base: https://api.nanobanana.com/v1  # Placeholder
    
  capabilities:
    - text_generation
    - image_generation
    - video_concepts
    - trend_analysis
```

### Content Generation

```python
async def generate_content(brief: dict) -> dict:
    """
    Generate content using Nano Banana.
    """
    result = await nano_api.post('/generate', {
        'type': brief['content_type'],
        'platform': brief['target_platform'],
        'guidelines': brief['brand_guidelines'],
        'prompt': brief['creative_prompt'],
        'audience': brief['target_audience']
    })
    
    # ADD TO APPROVAL QUEUE (not auto-publish)
    await add_to_approval_queue(result)
    
    return result
```

---

## API Credential Management

All API credentials stored in GCP Secret Manager:

```yaml
secrets:
  tiktok_access_token: projects/{p}/secrets/tiktok-token
  instagram_access_token: projects/{p}/secrets/instagram-token
  twitter_bearer_token: projects/{p}/secrets/twitter-token
  youtube_credentials: projects/{p}/secrets/youtube-creds
  linkedin_access_token: projects/{p}/secrets/linkedin-token
  nano_banana_api_key: projects/{p}/secrets/nano-banana-key
```

---

## Rate Limits

| Platform | Rate Limit | Window |
|----------|------------|--------|
| TikTok | 100/day | 24 hours |
| Instagram | 25 posts/day | 24 hours |
| Twitter | 300 tweets/day | 24 hours |
| YouTube | 10,000 units/day | 24 hours |
| LinkedIn | 100 shares/day | 24 hours |

---

*All platforms ready. All posts require Human approval.*
