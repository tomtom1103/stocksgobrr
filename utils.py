import pickle

colnames =['comment_limit', 'comment_sort', '_reddit', 'approved_at_utc',
           'subreddit', 'selftext', 'author_fullname', 'saved', 'mod_reason_title', 'gilded', 'clicked',
           'title', 'link_flair_richtext', 'subreddit_name_prefixed', 'hidden', 'pwls', 'link_flair_css_class',
           'downs', 'top_awarded_type', 'hide_score', 'name', 'quarantine', 'link_flair_text_color', 'upvote_ratio',
           'author_flair_background_color', 'subreddit_type', 'ups', 'total_awards_received', 'media_embed',
           'author_flair_template_id', 'is_original_content', 'user_reports', 'secure_media', 'is_reddit_media_domain',
           'is_meta', 'category', 'secure_media_embed', 'link_flair_text', 'can_mod_post', 'score', 'approved_by',
           'is_created_from_ads_ui', 'author_premium', 'thumbnail', 'edited', 'author_flair_css_class',
           'author_flair_richtext', 'gildings', 'content_categories', 'is_self', 'mod_note', 'created',
           'link_flair_type', 'wls', 'removed_by_category', 'banned_by', 'author_flair_type', 'domain',
           'allow_live_comments', 'selftext_html', 'likes', 'suggested_sort', 'banned_at_utc', 'view_count',
           'archived', 'no_follow', 'is_crosspostable', 'pinned', 'over_18', 'all_awardings', 'awarders', 'media_only',
           'link_flair_template_id', 'can_gild', 'spoiler', 'locked', 'author_flair_text', 'treatment_tags', 'visited',
           'removed_by', 'num_reports', 'distinguished', 'subreddit_id', 'author_is_blocked', 'mod_reason_by',
           'removal_reason', 'link_flair_background_color', 'id', 'is_robot_indexable', 'report_reasons', 'author',
           'discussion_type', 'num_comments', 'send_replies', 'whitelist_status', 'contest_mode', 'mod_reports',
           'author_patreon_flair', 'author_flair_text_color', 'permalink', 'parent_whitelist_status', 'stickied',
           'url', 'subreddit_subscribers', 'created_utc', 'num_crossposts', 'media', 'is_video', '_fetched',
           '_comments_by_id', 'thumbnail_height', 'thumbnail_width', 'num_duplicates', '_comments', 'flair', 'mod']

indexes = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']

def maybelater(z):
    l = []
    for key in z:
        l.append(key)
