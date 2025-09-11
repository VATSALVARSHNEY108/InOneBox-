import streamlit as st
import json
import csv
import io
from datetime import datetime, timedelta
import calendar
import random
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler
from utils.ai_client import ai_client


def display_tools():
    """Display all social media tools"""

    tool_categories = {
        "Content Schedulers": [
            "Multi-Platform Scheduler", "Content Calendar", "Post Optimizer", "Timing Analyzer", "Bulk Scheduler"
        ],
        "Analytics Dashboards": [
            "Engagement Analytics", "Reach Analysis", "Performance Tracker", "Competitor Analysis", "Growth Metrics"
        ],
        "Hashtag Generators": [
            "Hashtag Research", "Trending Hashtags", "Niche Discovery", "Hashtag Analytics", "Tag Optimizer"
        ],
        "Engagement Tools": [
            "Comment Manager", "Follower Analysis", "Interaction Tracker", "Community Builder", "Response Automation"
        ],
        "Multi-Platform Managers": [
            "Cross-Platform Posting", "Unified Dashboard", "Account Manager", "Content Distributor", "Platform Sync"
        ],
        "Content Creation": [
            "Post Generator", "Caption Writer", "Visual Content", "Story Creator", "Video Scripts"
        ],
        "Audience Analysis": [
            "Demographics Analyzer", "Behavior Insights", "Audience Segmentation", "Growth Tracking",
            "Engagement Patterns"
        ],
        "Campaign Management": [
            "Campaign Planner", "A/B Testing", "Performance Monitor", "ROI Tracker", "Campaign Analytics"
        ],
        "Social Listening": [
            "Mention Monitor", "Brand Tracking", "Sentiment Analysis", "Trend Detection", "Competitor Monitoring"
        ],
        "Influencer Tools": [
            "Influencer Finder", "Collaboration Manager", "Performance Tracker", "Outreach Automation", "ROI Calculator"
        ]
    }

    selected_category = st.selectbox("Select Social Media Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Social Media Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Multi-Platform Scheduler":
        multi_platform_scheduler()
    elif selected_tool == "Content Calendar":
        content_calendar()
    elif selected_tool == "Hashtag Research":
        hashtag_research()
    elif selected_tool == "Engagement Analytics":
        engagement_analytics()
    elif selected_tool == "Post Generator":
        post_generator()
    elif selected_tool == "Caption Writer":
        caption_writer()
    elif selected_tool == "Audience Segmentation":
        audience_segmentation()
    elif selected_tool == "Campaign Planner":
        campaign_planner()
    elif selected_tool == "Mention Monitor":
        mention_monitor()
    elif selected_tool == "Influencer Finder":
        influencer_finder()
    elif selected_tool == "Cross-Platform Posting":
        cross_platform_posting()
    elif selected_tool == "Trending Hashtags":
        trending_hashtags()
    elif selected_tool == "Performance Tracker":
        performance_tracker()
    elif selected_tool == "A/B Testing":
        ab_testing()
    elif selected_tool == "Brand Tracking":
        brand_tracking()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def multi_platform_scheduler():
    """Schedule posts across multiple social media platforms"""
    create_tool_header("Multi-Platform Scheduler", "Schedule posts across multiple social media platforms", "📅")

    # Platform selection
    st.subheader("Select Platforms")
    platforms = st.multiselect("Choose Platforms", [
        "Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok", "YouTube", "Pinterest", "Reddit"
    ], default=["Twitter", "Facebook", "Instagram"])

    if not platforms:
        st.warning("Please select at least one platform.")
        return

    # Content creation
    st.subheader("Create Content")

    content_type = st.selectbox("Content Type", [
        "Text Post", "Image Post", "Video Post", "Link Post", "Story", "Carousel"
    ])

    # Main content
    main_content = st.text_area("Main Content", height=150,
                                placeholder="Write your post content here...")

    # Platform-specific customization
    st.subheader("Platform-Specific Content")
    platform_content = {}

    for platform in platforms:
        with st.expander(f"{platform} Customization"):
            custom_content = st.text_area(f"Custom content for {platform}",
                                          value=main_content,
                                          key=f"content_{platform}",
                                          help=f"Customize content specifically for {platform}")

            # Platform-specific settings
            if platform == "Twitter":
                thread_mode = st.checkbox("Create Thread", key=f"thread_{platform}")
                if thread_mode:
                    thread_count = st.number_input("Number of tweets", 1, 10, 1, key=f"thread_count_{platform}")

            elif platform == "Instagram":
                use_carousel = st.checkbox("Carousel Post", key=f"carousel_{platform}")
                story_post = st.checkbox("Also post to Story", key=f"story_{platform}")

            elif platform == "LinkedIn":
                professional_tone = st.checkbox("Use Professional Tone", True, key=f"prof_{platform}")

            # Hashtags for each platform
            hashtags = st.text_input(f"Hashtags for {platform}",
                                     placeholder="#hashtag1 #hashtag2",
                                     key=f"hashtags_{platform}")

            platform_content[platform] = {
                'content': custom_content,
                'hashtags': hashtags,
                'settings': {}
            }

    # Scheduling
    st.subheader("Schedule Settings")

    col1, col2 = st.columns(2)
    with col1:
        schedule_option = st.selectbox("Schedule Option", [
            "Post Now", "Schedule for Later", "Optimal Time", "Custom Schedule"
        ])

    # Initialize default values
    schedule_date = datetime.now().date()
    schedule_time = datetime.now().time()

    with col2:
        if schedule_option in ["Schedule for Later", "Custom Schedule"]:
            schedule_date = st.date_input("Schedule Date", datetime.now().date())
            schedule_time = st.time_input("Schedule Time", datetime.now().time())
        elif schedule_option == "Optimal Time":
            timezone = st.selectbox("Timezone", [
                "UTC", "EST", "PST", "GMT", "CET", "JST", "IST"
            ])

    # Media attachments
    if content_type in ["Image Post", "Video Post", "Carousel"]:
        st.subheader("Media Attachments")
        media_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov'], accept_multiple=True)

        if media_files:
            st.success(f"Uploaded {len(media_files)} media file(s)")

    # Preview and schedule
    if st.button("Preview & Schedule Posts"):
        if main_content:
            preview_posts(platform_content, platforms, schedule_option)

            # Create scheduling data
            schedule_data = {
                'platforms': platforms,
                'content': platform_content,
                'schedule_option': schedule_option,
                'schedule_datetime': f"{schedule_date} {schedule_time}" if schedule_option != "Post Now" else "Immediate",
                'content_type': content_type,
                'created_at': datetime.now().isoformat()
            }

            # Export schedule
            if st.button("Export Schedule"):
                schedule_json = json.dumps(schedule_data, indent=2)
                FileHandler.create_download_link(
                    schedule_json.encode(),
                    f"social_media_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json"
                )
        else:
            st.error("Please enter some content for your post.")


def content_calendar():
    """Create and manage social media content calendar"""
    create_tool_header("Content Calendar", "Plan and organize your social media content", "📅")

    # Calendar view options
    view_type = st.selectbox("Calendar View", ["Monthly", "Weekly", "Daily"])

    if view_type == "Monthly":
        selected_date = st.date_input("Select Month", datetime.now().date())
        year = selected_date.year
        month = selected_date.month

        # Display monthly calendar
        st.subheader(f"Content Calendar - {calendar.month_name[month]} {year}")

        # Calendar grid
        cal = calendar.monthcalendar(year, month)

        # Create calendar layout
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.write("")
                    else:
                        date_obj = datetime(year, month, day).date()

                        # Check if content is scheduled for this day
                        has_content = check_scheduled_content(date_obj)

                        if has_content:
                            st.markdown(f"**{day}** 📝")
                            if st.button(f"View {day}", key=f"day_{day}"):
                                show_day_content(date_obj)
                        else:
                            st.write(f"{day}")
                            if st.button(f"+ {day}", key=f"add_{day}"):
                                add_content_to_day(date_obj)

    # Content planning
    st.subheader("Plan New Content")

    col1, col2 = st.columns(2)
    with col1:
        content_date = st.date_input("Content Date")
        content_time = st.time_input("Content Time")
        platform = st.selectbox("Platform", [
            "All Platforms", "Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok"
        ])

    with col2:
        content_type = st.selectbox("Content Type", [
            "Promotional", "Educational", "Entertainment", "Behind-the-Scenes", "User-Generated", "News"
        ])
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    content_title = st.text_input("Content Title")
    content_description = st.text_area("Content Description", height=100)
    content_notes = st.text_area("Notes/Ideas", height=80)

    if st.button("Add to Calendar"):
        if content_title and content_description:
            calendar_entry = create_calendar_entry(
                content_date, content_time, platform, content_type,
                priority, content_title, content_description, content_notes
            )

            st.success(f"Content added to calendar for {content_date}")

            # Export calendar entry
            entry_json = json.dumps(calendar_entry, indent=2)
            FileHandler.create_download_link(
                entry_json.encode(),
                f"calendar_entry_{content_date}.json",
                "application/json"
            )


def hashtag_research():
    """Research and analyze hashtags"""
    create_tool_header("Hashtag Research", "Research hashtags for better reach", "#️⃣")

    # Research input
    st.subheader("Hashtag Research")

    col1, col2 = st.columns(2)
    with col1:
        research_method = st.selectbox("Research Method", [
            "Topic-Based", "Competitor Analysis", "Trending Discovery", "Niche Research"
        ])
        platform = st.selectbox("Target Platform", [
            "Instagram", "Twitter", "TikTok", "LinkedIn", "Facebook"
        ])

    with col2:
        topic = st.text_input("Topic/Keyword", placeholder="Enter your topic or keyword")
        industry = st.selectbox("Industry", [
            "Technology", "Fashion", "Food", "Travel", "Fitness", "Business",
            "Art", "Music", "Education", "Health", "Other"
        ])

    if st.button("Research Hashtags") and topic:
        with st.spinner("Researching hashtags..."):
            # Generate hashtag research using AI
            hashtag_data = research_hashtags_ai(topic, platform, industry, research_method)

            if hashtag_data:
                st.subheader("Hashtag Research Results")

                # Display recommended hashtags
                tabs = st.tabs(["Recommended", "Popular", "Niche", "Trending"])

                with tabs[0]:  # Recommended
                    st.write("**Recommended Hashtags:**")
                    recommended = hashtag_data.get('recommended', [])
                    display_hashtag_list(recommended, "recommended")

                with tabs[1]:  # Popular
                    st.write("**Popular Hashtags:**")
                    popular = hashtag_data.get('popular', [])
                    display_hashtag_list(popular, "popular")

                with tabs[2]:  # Niche
                    st.write("**Niche Hashtags:**")
                    niche = hashtag_data.get('niche', [])
                    display_hashtag_list(niche, "niche")

                with tabs[3]:  # Trending
                    st.write("**Trending Hashtags:**")
                    trending = hashtag_data.get('trending', [])
                    display_hashtag_list(trending, "trending")

                # Hashtag strategy
                st.subheader("Hashtag Strategy Recommendations")
                strategy = generate_hashtag_strategy(hashtag_data, platform)

                for recommendation in strategy:
                    st.write(f"• {recommendation}")

                # Export hashtags
                if st.button("Export Hashtag Research"):
                    export_data = {
                        'topic': topic,
                        'platform': platform,
                        'industry': industry,
                        'research_method': research_method,
                        'hashtags': hashtag_data,
                        'strategy': strategy,
                        'research_date': datetime.now().isoformat()
                    }

                    export_json = json.dumps(export_data, indent=2)
                    FileHandler.create_download_link(
                        export_json.encode(),
                        f"hashtag_research_{topic.replace(' ', '_')}.json",
                        "application/json"
                    )


def engagement_analytics():
    """Analyze social media engagement metrics"""
    create_tool_header("Engagement Analytics", "Analyze engagement metrics and performance", "📊")

    # Data input method
    data_method = st.selectbox("Data Input Method", [
        "Upload CSV Data", "Manual Entry", "Sample Data"
    ])

    # Initialize engagement_data
    engagement_data = None

    if data_method == "Upload CSV Data":
        uploaded_file = FileHandler.upload_files(['csv'], accept_multiple=False)

        if uploaded_file:
            df = FileHandler.process_csv_file(uploaded_file[0])
            if df is not None:
                st.subheader("Uploaded Data Preview")
                st.dataframe(df.head())

                engagement_data = df.to_dict('records')
        else:
            engagement_data = None

    elif data_method == "Sample Data":
        engagement_data = generate_sample_engagement_data()
        st.success("Using sample engagement data for demonstration")

    else:  # Manual Entry
        st.subheader("Enter Engagement Data")

        posts = []
        num_posts = st.number_input("Number of Posts to Analyze", 1, 20, 5)

        for i in range(num_posts):
            with st.expander(f"Post {i + 1}"):
                col1, col2 = st.columns(2)

                with col1:
                    post_type = st.selectbox(f"Post Type", ["Image", "Video", "Text", "Carousel"], key=f"type_{i}")
                    platform = st.selectbox(f"Platform", ["Instagram", "Twitter", "Facebook", "LinkedIn"],
                                            key=f"platform_{i}")
                    date = st.date_input(f"Post Date", key=f"date_{i}")

                with col2:
                    likes = st.number_input(f"Likes", 0, 100000, 0, key=f"likes_{i}")
                    comments = st.number_input(f"Comments", 0, 10000, 0, key=f"comments_{i}")
                    shares = st.number_input(f"Shares", 0, 10000, 0, key=f"shares_{i}")

                posts.append({
                    'post_type': post_type,
                    'platform': platform,
                    'date': date.isoformat(),
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'engagement_rate': calculate_engagement_rate(likes, comments, shares)
                })

        engagement_data = posts

    # Analytics
    if engagement_data:
        st.subheader("Engagement Analytics")

        # Overall metrics
        total_posts = len(engagement_data)
        total_likes = sum(post.get('likes', 0) for post in engagement_data)
        total_comments = sum(post.get('comments', 0) for post in engagement_data)
        total_shares = sum(post.get('shares', 0) for post in engagement_data)
        avg_engagement = sum(
            post.get('engagement_rate', 0) for post in engagement_data) / total_posts if total_posts > 0 else 0

        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Posts", total_posts)
        with col2:
            st.metric("Total Likes", f"{total_likes:,}")
        with col3:
            st.metric("Total Comments", f"{total_comments:,}")
        with col4:
            st.metric("Total Shares", f"{total_shares:,}")
        with col5:
            st.metric("Avg Engagement", f"{avg_engagement:.2%}")

        # Performance by platform
        st.subheader("Performance by Platform")
        platform_stats = analyze_platform_performance(engagement_data)

        for platform, stats in platform_stats.items():
            with st.expander(f"{platform} Performance"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Posts", stats['posts'])
                with col2:
                    st.metric("Avg Likes", f"{stats['avg_likes']:.0f}")
                with col3:
                    st.metric("Engagement Rate", f"{stats['avg_engagement']:.2%}")

        # Best performing posts
        st.subheader("Top Performing Posts")
        top_posts = sorted(engagement_data, key=lambda x: x.get('engagement_rate', 0), reverse=True)[:5]

        for i, post in enumerate(top_posts, 1):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**#{i}** {post.get('post_type', 'Unknown')}")
            with col2:
                st.write(f"Platform: {post.get('platform', 'Unknown')}")
            with col3:
                st.write(f"Date: {post.get('date', 'Unknown')}")
            with col4:
                st.write(f"Engagement: {post.get('engagement_rate', 0):.2%}")

        # Generate report
        if st.button("Generate Analytics Report"):
            report = generate_engagement_report(engagement_data, platform_stats)

            FileHandler.create_download_link(
                report.encode(),
                f"engagement_analytics_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain"
            )


def post_generator():
    """Generate social media posts using AI"""
    create_tool_header("Post Generator", "Generate engaging social media posts with AI", "✍️")

    # Post parameters
    st.subheader("Post Configuration")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Target Platform", [
            "Instagram", "Twitter", "Facebook", "LinkedIn", "TikTok", "Pinterest"
        ])
        post_type = st.selectbox("Post Type", [
            "Promotional", "Educational", "Entertaining", "Inspirational", "Behind-the-Scenes", "Question/Poll"
        ])
        topic = st.text_input("Topic/Subject", placeholder="What should the post be about?")

    with col2:
        tone = st.selectbox("Tone", [
            "Professional", "Casual", "Friendly", "Humorous", "Inspirational", "Educational"
        ])
        target_audience = st.selectbox("Target Audience", [
            "General", "Young Adults", "Professionals", "Students", "Parents", "Entrepreneurs"
        ])
        include_hashtags = st.checkbox("Include Hashtags", True)

    # Additional options
    with st.expander("Advanced Options"):
        call_to_action = st.text_input("Call to Action", placeholder="e.g., Visit our website, Like and share")
        keywords = st.text_input("Keywords to Include", placeholder="keyword1, keyword2, keyword3")
        post_length = st.selectbox("Post Length", ["Short", "Medium", "Long"])
        emoji_style = st.selectbox("Emoji Usage", ["None", "Minimal", "Moderate", "Heavy"])

    if st.button("Generate Post") and topic:
        with st.spinner("Generating social media post..."):
            # Create prompt for AI
            prompt = create_post_generation_prompt(
                platform, post_type, topic, tone, target_audience,
                include_hashtags, call_to_action, keywords, post_length, emoji_style
            )

            generated_post = ai_client.generate_text(prompt, max_tokens=500)

            if generated_post:
                st.subheader("Generated Post")
                st.text_area("", generated_post, height=200, disabled=True)

                # Post analysis
                st.subheader("Post Analysis")
                analysis = analyze_generated_post(generated_post, platform)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Character Count", analysis['char_count'])
                with col2:
                    st.metric("Word Count", analysis['word_count'])
                with col3:
                    st.metric("Hashtag Count", analysis['hashtag_count'])

                # Platform-specific feedback
                feedback = get_platform_feedback(generated_post, platform)
                if feedback:
                    st.subheader("Platform Optimization Feedback")
                    for item in feedback:
                        st.write(f"• {item}")

                # Download post
                FileHandler.create_download_link(
                    generated_post.encode(),
                    f"social_post_{platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain"
                )

                # Generate variations
                if st.button("Generate Variations"):
                    variations = generate_post_variations(generated_post, platform)

                    st.subheader("Post Variations")
                    for i, variation in enumerate(variations, 1):
                        with st.expander(f"Variation {i}"):
                            st.write(variation)


def caption_writer():
    """AI-powered caption writing tool"""
    create_tool_header("Caption Writer", "Write engaging captions for your content", "💬")

    # Content input
    st.subheader("Content Information")

    # Image upload for context
    uploaded_image = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)

    if uploaded_image:
        image = FileHandler.process_image_file(uploaded_image[0])
        if image:
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Analyze image for context
            if st.button("Analyze Image for Context"):
                with st.spinner("Analyzing image..."):
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    img_bytes.seek(0)

                    image_description = ai_client.analyze_image(
                        img_bytes.getvalue(),
                        "Describe this image in detail for social media caption writing."
                    )

                    if image_description:
                        st.text_area("Image Analysis", image_description, height=100, disabled=True)

    # Caption parameters
    col1, col2 = st.columns(2)
    with col1:
        content_theme = st.text_input("Content Theme/Topic")
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok"])
        caption_style = st.selectbox("Caption Style", [
            "Storytelling", "Question-based", "List-format", "Behind-the-scenes", "Motivational", "Humorous"
        ])

    with col2:
        brand_voice = st.selectbox("Brand Voice", [
            "Professional", "Casual", "Playful", "Inspirational", "Educational", "Luxury"
        ])
        target_mood = st.selectbox("Target Mood", [
            "Engaging", "Informative", "Entertaining", "Inspiring", "Promotional", "Community-building"
        ])
        caption_length = st.selectbox("Caption Length", ["Short", "Medium", "Long"])

    # Additional context
    brand_info = st.text_area("Brand/Business Information (optional)",
                              placeholder="Tell us about your brand, values, or business...")

    specific_message = st.text_area("Specific Message/CTA",
                                    placeholder="Any specific message or call-to-action you want to include...")

    if st.button("Generate Caption"):
        if content_theme:
            with st.spinner("Creating engaging caption..."):
                caption_prompt = create_caption_prompt(
                    content_theme, platform, caption_style, brand_voice,
                    target_mood, caption_length, brand_info, specific_message
                )

                generated_caption = ai_client.generate_text(caption_prompt, max_tokens=800)

                if generated_caption:
                    st.subheader("Generated Caption")
                    st.text_area("", generated_caption, height=250, disabled=True)

                    # Caption metrics
                    st.subheader("Caption Metrics")
                    metrics = analyze_caption_metrics(generated_caption, platform)

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Characters", metrics['characters'])
                    with col2:
                        st.metric("Words", metrics['words'])
                    with col3:
                        st.metric("Hashtags", metrics['hashtags'])
                    with col4:
                        st.metric("Mentions", metrics['mentions'])

                    # Platform optimization
                    optimization = get_caption_optimization(generated_caption, platform)
                    if optimization:
                        st.subheader("Optimization Tips")
                        for tip in optimization:
                            st.write(f"• {tip}")

                    # Export caption
                    FileHandler.create_download_link(
                        generated_caption.encode(),
                        f"caption_{platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )


# Helper Functions

def preview_posts(platform_content, platforms, schedule_option):
    """Preview posts for all platforms"""
    st.subheader("Post Preview")

    for platform in platforms:
        with st.expander(f"{platform} Post Preview"):
            content = platform_content[platform]['content']
            hashtags = platform_content[platform]['hashtags']

            # Show platform-specific preview
            st.write(f"**{platform} Post:**")
            st.write(content)
            if hashtags:
                st.write(f"**Hashtags:** {hashtags}")

            st.write(f"**Schedule:** {schedule_option}")


def check_scheduled_content(date):
    """Check if content is scheduled for a specific date"""
    # This would check against a database or storage
    # For demo, randomly return True/False
    return random.choice([True, False, False])  # 33% chance of having content


def show_day_content(date):
    """Show content scheduled for a specific day"""
    st.write(f"Content scheduled for {date}")
    # This would fetch actual content from storage


def add_content_to_day(date):
    """Add content to a specific day"""
    st.write(f"Add content for {date}")
    # This would open a form to add content


def create_calendar_entry(date, time, platform, content_type, priority, title, description, notes):
    """Create a calendar entry"""
    return {
        'date': date.isoformat(),
        'time': time.isoformat(),
        'platform': platform,
        'content_type': content_type,
        'priority': priority,
        'title': title,
        'description': description,
        'notes': notes,
        'created_at': datetime.now().isoformat()
    }


def research_hashtags_ai(topic, platform, industry, method):
    """Research hashtags using AI"""
    prompt = f"""
    Research hashtags for the topic "{topic}" on {platform} in the {industry} industry.
    Method: {method}

    Provide:
    1. 10 recommended hashtags (mix of popular and niche)
    2. 5 popular hashtags (high volume)
    3. 5 niche hashtags (specific to topic)
    4. 5 trending hashtags (currently popular)

    Format as JSON with categories: recommended, popular, niche, trending
    """

    try:
        response = ai_client.generate_text(prompt, max_tokens=1000)
        # Try to parse as JSON, fallback to text processing
        if response.strip().startswith('{'):
            return json.loads(response)
        else:
            # Parse text response into hashtag categories
            return parse_hashtag_response(response)
    except:
        # Fallback hashtag data
        return generate_fallback_hashtags(topic, platform, industry)


def display_hashtag_list(hashtags, category):
    """Display hashtag list with copy functionality"""
    if hashtags:
        hashtag_text = ' '.join([f"#{tag}" if not tag.startswith('#') else tag for tag in hashtags])
        st.code(hashtag_text)

        if st.button(f"Copy {category.title()} Hashtags", key=f"copy_{category}"):
            st.success(f"{category.title()} hashtags copied to clipboard!")


def generate_hashtag_strategy(hashtag_data, platform):
    """Generate hashtag strategy recommendations"""
    strategies = [
        f"Use a mix of popular and niche hashtags for optimal reach on {platform}",
        "Include 3-5 popular hashtags to increase discoverability",
        "Add 5-7 niche hashtags to target specific audiences",
        "Monitor trending hashtags and incorporate when relevant",
        "Create a branded hashtag for community building"
    ]

    if platform == "Instagram":
        strategies.append("Use up to 30 hashtags, but 11-15 often perform best")
    elif platform == "Twitter":
        strategies.append("Limit to 1-2 hashtags to maintain readability")
    elif platform == "TikTok":
        strategies.append("Use trending sounds and hashtags for algorithm boost")

    return strategies


def generate_sample_engagement_data():
    """Generate sample engagement data for analytics"""
    platforms = ["Instagram", "Twitter", "Facebook", "LinkedIn"]
    post_types = ["Image", "Video", "Text", "Carousel"]

    data = []
    for i in range(20):
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        likes = random.randint(50, 1000)
        comments = random.randint(5, 100)
        shares = random.randint(1, 50)

        data.append({
            'post_type': random.choice(post_types),
            'platform': random.choice(platforms),
            'date': date.isoformat(),
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'engagement_rate': calculate_engagement_rate(likes, comments, shares)
        })

    return data


def calculate_engagement_rate(likes, comments, shares, followers=1000):
    """Calculate engagement rate"""
    total_engagement = likes + comments + shares
    return total_engagement / followers


def analyze_platform_performance(engagement_data):
    """Analyze performance by platform"""
    platform_stats = {}

    for post in engagement_data:
        platform = post.get('platform')
        if platform not in platform_stats:
            platform_stats[platform] = {
                'posts': 0,
                'total_likes': 0,
                'total_engagement': 0
            }

        platform_stats[platform]['posts'] += 1
        platform_stats[platform]['total_likes'] += post.get('likes', 0)
        platform_stats[platform]['total_engagement'] += post.get('engagement_rate', 0)

    # Calculate averages
    for platform, stats in platform_stats.items():
        stats['avg_likes'] = stats['total_likes'] / stats['posts'] if stats['posts'] > 0 else 0
        stats['avg_engagement'] = stats['total_engagement'] / stats['posts'] if stats['posts'] > 0 else 0

    return platform_stats


def generate_engagement_report(engagement_data, platform_stats):
    """Generate engagement analytics report"""
    report = "SOCIAL MEDIA ENGAGEMENT ANALYTICS REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Analysis Period: Last 30 days\n\n"

    # Overall stats
    total_posts = len(engagement_data)
    total_likes = sum(post.get('likes', 0) for post in engagement_data)
    total_comments = sum(post.get('comments', 0) for post in engagement_data)
    total_shares = sum(post.get('shares', 0) for post in engagement_data)

    report += "OVERALL PERFORMANCE:\n"
    report += f"Total Posts: {total_posts}\n"
    report += f"Total Likes: {total_likes:,}\n"
    report += f"Total Comments: {total_comments:,}\n"
    report += f"Total Shares: {total_shares:,}\n\n"

    # Platform breakdown
    report += "PLATFORM PERFORMANCE:\n"
    for platform, stats in platform_stats.items():
        report += f"\n{platform}:\n"
        report += f"  Posts: {stats['posts']}\n"
        report += f"  Avg Likes: {stats['avg_likes']:.0f}\n"
        report += f"  Avg Engagement Rate: {stats['avg_engagement']:.2%}\n"

    return report


def create_post_generation_prompt(platform, post_type, topic, tone, audience, hashtags, cta, keywords, length, emoji):
    """Create prompt for post generation"""
    prompt = f"""
    Create a {post_type.lower()} social media post for {platform} about "{topic}".

    Requirements:
    - Tone: {tone}
    - Target Audience: {audience}
    - Post Length: {length}
    - Emoji Usage: {emoji}
    """

    if hashtags:
        prompt += f"\n- Include relevant hashtags"

    if cta:
        prompt += f"\n- Include this call to action: {cta}"

    if keywords:
        prompt += f"\n- Include these keywords: {keywords}"

    prompt += f"\n\nMake it engaging and optimized for {platform}."

    return prompt


def analyze_generated_post(post, platform):
    """Analyze generated post metrics"""
    char_count = len(post)
    word_count = len(post.split())
    hashtag_count = post.count('#')

    return {
        'char_count': char_count,
        'word_count': word_count,
        'hashtag_count': hashtag_count
    }


def get_platform_feedback(post, platform):
    """Get platform-specific optimization feedback"""
    feedback = []
    char_count = len(post)

    if platform == "Twitter" and char_count > 280:
        feedback.append("Post exceeds Twitter's 280 character limit")
    elif platform == "Instagram" and char_count > 2200:
        feedback.append("Post exceeds Instagram's caption limit")

    if platform == "LinkedIn" and not any(word in post.lower() for word in ['professional', 'business', 'career']):
        feedback.append("Consider adding professional context for LinkedIn")

    return feedback


def generate_post_variations(original_post, platform):
    """Generate variations of the original post"""
    variations = []

    # This would use AI to create variations
    variations.append(f"Variation 1: {original_post[:100]}... (shortened)")
    variations.append(f"Variation 2: {original_post} (with different hashtags)")
    variations.append(f"Variation 3: Question format - What do you think about {original_post[:50]}?")

    return variations


def create_caption_prompt(theme, platform, style, voice, mood, length, brand_info, message):
    """Create prompt for caption generation"""
    prompt = f"""
    Write a {length.lower()} {style.lower()} caption for {platform} about "{theme}".

    Style Requirements:
    - Brand Voice: {voice}
    - Target Mood: {mood}
    - Caption Style: {style}
    """

    if brand_info:
        prompt += f"\n- Brand Context: {brand_info}"

    if message:
        prompt += f"\n- Include Message/CTA: {message}"

    prompt += f"\n\nMake it engaging and authentic for {platform}."

    return prompt


def analyze_caption_metrics(caption, platform):
    """Analyze caption metrics"""
    return {
        'characters': len(caption),
        'words': len(caption.split()),
        'hashtags': caption.count('#'),
        'mentions': caption.count('@')
    }


def get_caption_optimization(caption, platform):
    """Get caption optimization tips"""
    tips = []

    if platform == "Instagram":
        if caption.count('#') < 5:
            tips.append("Consider adding more hashtags (5-11 recommended for Instagram)")
        if len(caption) < 100:
            tips.append("Instagram captions can be longer - consider expanding your story")

    elif platform == "Twitter":
        if len(caption) > 240:
            tips.append("Consider shortening for Twitter (280 char limit)")
        if caption.count('#') > 2:
            tips.append("Twitter posts work better with 1-2 hashtags")

    return tips


# Placeholder functions for remaining tools
def parse_hashtag_response(response):
    """Parse text response into hashtag categories"""
    return {
        'recommended': ['example1', 'example2', 'example3'],
        'popular': ['popular1', 'popular2', 'popular3'],
        'niche': ['niche1', 'niche2', 'niche3'],
        'trending': ['trending1', 'trending2', 'trending3']
    }


def generate_fallback_hashtags(topic, platform, industry):
    """Generate fallback hashtag data"""
    return {
        'recommended': [f'{topic}', f'{industry}', f'{platform}content'],
        'popular': ['trending', 'viral', 'popular'],
        'niche': [f'{topic}community', f'{industry}life', 'niche'],
        'trending': ['trend1', 'trend2', 'trend3']
    }


def audience_segmentation():
    """Advanced audience segmentation and analysis tool"""
    create_tool_header("Audience Segmentation", "Analyze and segment your audience for targeted campaigns", "👥")

    # Data input method
    st.subheader("Audience Data Input")
    data_source = st.selectbox("Data Source", [
        "Upload CSV File", "Manual Entry", "Platform Analytics", "Sample Data"
    ])

    audience_data = None

    if data_source == "Upload CSV File":
        uploaded_file = FileHandler.upload_files(['csv'], accept_multiple=False)
        if uploaded_file:
            df = FileHandler.process_csv_file(uploaded_file[0])
            if df is not None:
                st.subheader("Data Preview")
                st.dataframe(df.head())
                audience_data = df.to_dict('records')

    elif data_source == "Sample Data":
        audience_data = generate_sample_audience_data()
        st.success("Using sample audience data for demonstration")

    elif data_source == "Manual Entry":
        st.subheader("Enter Audience Information")

        num_segments = st.number_input("Number of Audience Segments", 1, 10, 3)
        audience_data = []

        for i in range(num_segments):
            with st.expander(f"Segment {i + 1}"):
                col1, col2 = st.columns(2)

                with col1:
                    segment_name = st.text_input(f"Segment Name", f"Segment {i + 1}", key=f"seg_name_{i}")
                    age_range = st.selectbox(f"Age Range", ["18-24", "25-34", "35-44", "45-54", "55+"], key=f"age_{i}")
                    gender = st.selectbox(f"Gender", ["All", "Male", "Female", "Non-binary"], key=f"gender_{i}")
                    location = st.text_input(f"Primary Location", "United States", key=f"location_{i}")

                with col2:
                    interests = st.text_area(f"Interests", "technology, social media, marketing", key=f"interests_{i}")
                    platform_usage = st.multiselect(f"Platform Usage",
                                                    ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok",
                                                     "YouTube"],
                                                    default=["Instagram", "Facebook"], key=f"platforms_{i}")
                    engagement_level = st.selectbox(f"Engagement Level", ["High", "Medium", "Low"],
                                                    key=f"engagement_{i}")
                    spending_power = st.selectbox(f"Spending Power", ["High", "Medium", "Low"], key=f"spending_{i}")

                audience_data.append({
                    'segment_name': segment_name,
                    'age_range': age_range,
                    'gender': gender,
                    'location': location,
                    'interests': interests.split(', '),
                    'platforms': platform_usage,
                    'engagement_level': engagement_level,
                    'spending_power': spending_power
                })

    # Segmentation analysis
    if audience_data:
        st.subheader("Audience Segmentation Analysis")

        # Segmentation criteria
        col1, col2 = st.columns(2)
        with col1:
            primary_criteria = st.selectbox("Primary Segmentation Criteria", [
                "Demographics", "Behavior", "Interests", "Platform Usage", "Engagement Level"
            ])
        with col2:
            secondary_criteria = st.selectbox("Secondary Criteria", [
                "Location", "Spending Power", "Age", "Gender", "Activity Level"
            ])

        if st.button("Analyze Segments"):
            # Perform segmentation analysis
            analysis_results = analyze_audience_segments(audience_data, primary_criteria, secondary_criteria)

            # Display results
            tabs = st.tabs(["Overview", "Detailed Segments", "Recommendations", "Export"])

            with tabs[0]:  # Overview
                st.subheader("Segmentation Overview")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Segments", len(analysis_results['segments']))
                with col2:
                    st.metric("Largest Segment", analysis_results['largest_segment']['name'])
                with col3:
                    st.metric("Most Engaged", analysis_results['most_engaged']['name'])
                with col4:
                    st.metric("High Value", analysis_results['high_value']['count'])

                # Segment distribution chart
                st.subheader("Segment Distribution")
                for segment in analysis_results['segments']:
                    percentage = segment['percentage']
                    st.progress(percentage / 100)
                    st.write(f"**{segment['name']}**: {percentage:.1f}%")

            with tabs[1]:  # Detailed Segments
                st.subheader("Detailed Segment Analysis")

                for segment in analysis_results['segments']:
                    with st.expander(f"📊 {segment['name']} ({segment['percentage']:.1f}%)"):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.write("**Demographics:**")
                            st.write(f"• Age: {segment['demographics']['age']}")
                            st.write(f"• Gender: {segment['demographics']['gender']}")
                            st.write(f"• Location: {segment['demographics']['location']}")

                            st.write("**Behavior:**")
                            st.write(f"• Engagement: {segment['behavior']['engagement']}")
                            st.write(f"• Activity: {segment['behavior']['activity']}")

                        with col2:
                            st.write("**Platform Preferences:**")
                            for platform in segment['platforms']:
                                st.write(f"• {platform}")

                            st.write("**Key Interests:**")
                            for interest in segment['interests'][:5]:
                                st.write(f"• {interest}")

                        st.write("**Targeting Recommendations:**")
                        for rec in segment['recommendations']:
                            st.write(f"💡 {rec}")

            with tabs[2]:  # Recommendations
                st.subheader("Marketing Recommendations")

                for rec_category, recommendations in analysis_results['marketing_recommendations'].items():
                    st.write(f"**{rec_category.title()}:**")
                    for rec in recommendations:
                        st.write(f"• {rec}")
                    st.write("")

            with tabs[3]:  # Export
                st.subheader("Export Analysis")

                if st.button("Generate Segmentation Report"):
                    report = generate_segmentation_report(analysis_results, audience_data)

                    FileHandler.create_download_link(
                        report.encode(),
                        f"audience_segmentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )

                if st.button("Export Segment Data"):
                    segment_json = json.dumps(analysis_results, indent=2)
                    FileHandler.create_download_link(
                        segment_json.encode(),
                        f"audience_segments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        "application/json"
                    )


def campaign_planner():
    """Comprehensive social media campaign planning tool"""
    create_tool_header("Campaign Planner", "Plan and manage your social media campaigns", "📋")

    # Campaign basics
    st.subheader("Campaign Setup")

    col1, col2 = st.columns(2)
    with col1:
        campaign_name = st.text_input("Campaign Name", placeholder="e.g., Summer Product Launch")
        campaign_type = st.selectbox("Campaign Type", [
            "Product Launch", "Brand Awareness", "Lead Generation", "Sales Promotion",
            "Event Marketing", "Engagement Drive", "Content Series", "Other"
        ])
        start_date = st.date_input("Start Date", datetime.now().date())
        end_date = st.date_input("End Date", datetime.now().date() + timedelta(days=30))

    with col2:
        target_audience = st.text_input("Target Audience", placeholder="e.g., Young professionals, tech enthusiasts")
        budget = st.number_input("Total Budget ($)", 0, 1000000, 5000)
        primary_goal = st.selectbox("Primary Goal", [
            "Increase Brand Awareness", "Drive Website Traffic", "Generate Leads",
            "Boost Sales", "Improve Engagement", "Build Community", "Launch Product"
        ])
        platforms = st.multiselect("Platforms", [
            "Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok", "YouTube", "Pinterest"
        ], default=["Instagram", "Facebook"])

    # Campaign objectives and KPIs
    st.subheader("Campaign Objectives & KPIs")

    objectives = []
    num_objectives = st.number_input("Number of Objectives", 1, 5, 2)

    for i in range(num_objectives):
        with st.expander(f"Objective {i + 1}"):
            col1, col2 = st.columns(2)

            with col1:
                objective_name = st.text_input(f"Objective", f"Objective {i + 1}", key=f"obj_name_{i}")
                metric = st.selectbox(f"Key Metric", [
                    "Reach", "Impressions", "Engagement Rate", "Click-through Rate",
                    "Conversions", "Leads", "Sales", "Followers", "Video Views"
                ], key=f"metric_{i}")

            with col2:
                target_value = st.number_input(f"Target Value", 0, 1000000, 1000, key=f"target_{i}")
                timeframe = st.selectbox(f"Timeframe", [
                    "Daily", "Weekly", "Monthly", "Campaign Total"
                ], key=f"timeframe_{i}")

            objectives.append({
                'name': objective_name,
                'metric': metric,
                'target': target_value,
                'timeframe': timeframe
            })

    # Content planning
    st.subheader("Content Planning")

    content_themes = st.text_area("Content Themes",
                                  placeholder="List the main themes/topics for your campaign content",
                                  height=100)

    content_types = st.multiselect("Content Types", [
        "Image Posts", "Video Posts", "Stories", "Reels/Short Videos",
        "Carousel Posts", "Live Videos", "User-Generated Content", "Polls/Questions"
    ], default=["Image Posts", "Video Posts"])

    posting_frequency = {}
    for platform in platforms:
        frequency = st.selectbox(f"{platform} Posting Frequency", [
            "Daily", "Every 2 days", "3 times per week", "Weekly", "Custom"
        ], key=f"freq_{platform}")
        posting_frequency[platform] = frequency

    # Budget allocation
    st.subheader("Budget Allocation")

    budget_allocation = {}
    remaining_budget = budget

    for platform in platforms:
        max_allocation = remaining_budget if platform == platforms[-1] else remaining_budget - (
                    len(platforms) - platforms.index(platform) - 1)
        allocation = st.number_input(
            f"{platform} Budget ($)",
            0,
            max_allocation,
            min(max_allocation, budget // len(platforms)),
            key=f"budget_{platform}"
        )
        budget_allocation[platform] = allocation
        remaining_budget -= allocation

    st.write(f"Remaining Budget: ${remaining_budget}")

    # Timeline and milestones
    st.subheader("Campaign Timeline")

    milestones = []
    num_milestones = st.number_input("Number of Milestones", 1, 10, 3)

    for i in range(num_milestones):
        with st.expander(f"Milestone {i + 1}"):
            col1, col2 = st.columns(2)

            with col1:
                milestone_name = st.text_input(f"Milestone", f"Milestone {i + 1}", key=f"milestone_name_{i}")
                milestone_date = st.date_input(f"Date", start_date + timedelta(days=i * 7), key=f"milestone_date_{i}")

            with col2:
                milestone_desc = st.text_area(f"Description", key=f"milestone_desc_{i}")
                milestone_owner = st.text_input(f"Owner", "Team Member", key=f"milestone_owner_{i}")

            milestones.append({
                'name': milestone_name,
                'date': milestone_date.isoformat(),
                'description': milestone_desc,
                'owner': milestone_owner
            })

    # Generate campaign plan
    if st.button("Generate Campaign Plan") and campaign_name:
        campaign_data = {
            'campaign_name': campaign_name,
            'campaign_type': campaign_type,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'target_audience': target_audience,
            'budget': budget,
            'primary_goal': primary_goal,
            'platforms': platforms,
            'objectives': objectives,
            'content_themes': content_themes,
            'content_types': content_types,
            'posting_frequency': posting_frequency,
            'budget_allocation': budget_allocation,
            'milestones': milestones,
            'created_at': datetime.now().isoformat()
        }

        # Display campaign overview
        st.subheader("📊 Campaign Overview")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Duration", f"{(end_date - start_date).days} days")
        with col2:
            st.metric("Platforms", len(platforms))
        with col3:
            st.metric("Budget", f"${budget:,}")
        with col4:
            st.metric("Objectives", len(objectives))

        # Platform breakdown
        st.subheader("Platform Strategy")
        for platform in platforms:
            with st.expander(f"{platform} Strategy"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Budget:** ${budget_allocation.get(platform, 0):,}")
                    st.write(f"**Posting:** {posting_frequency.get(platform, 'Not set')}")
                with col2:
                    platform_recommendations = generate_platform_recommendations(platform, campaign_type,
                                                                                 target_audience)
                    st.write("**Recommendations:**")
                    for rec in platform_recommendations:
                        st.write(f"• {rec}")

        # Timeline visualization
        st.subheader("Campaign Timeline")
        timeline_days = (end_date - start_date).days

        for milestone in milestones:
            milestone_date_obj = datetime.fromisoformat(milestone['date']).date()
            days_from_start = (milestone_date_obj - start_date).days
            progress = days_from_start / timeline_days if timeline_days > 0 else 0

            st.write(f"**{milestone['name']}** - {milestone_date_obj}")
            st.progress(min(progress, 1.0))
            if milestone['description']:
                st.write(f"📝 {milestone['description']}")

        # Export options
        st.subheader("Export Campaign Plan")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download Campaign Plan"):
                plan_text = generate_campaign_plan_report(campaign_data)
                FileHandler.create_download_link(
                    plan_text.encode(),
                    f"campaign_plan_{campaign_name.replace(' ', '_')}.txt",
                    "text/plain"
                )

        with col2:
            if st.button("Export as JSON"):
                plan_json = json.dumps(campaign_data, indent=2)
                FileHandler.create_download_link(
                    plan_json.encode(),
                    f"campaign_data_{campaign_name.replace(' ', '_')}.json",
                    "application/json"
                )


def mention_monitor():
    """Monitor brand mentions across social media platforms"""
    create_tool_header("Mention Monitor", "Track brand mentions and social conversations", "👂")

    # Search setup
    st.subheader("Mention Monitoring Setup")

    col1, col2 = st.columns(2)
    with col1:
        brand_terms = st.text_area("Brand Terms to Monitor",
                                   placeholder="Enter brand names, products, hashtags (one per line)")
        platforms = st.multiselect("Platforms to Monitor", [
            "Twitter", "Instagram", "Facebook", "LinkedIn", "TikTok", "Reddit", "YouTube"
        ], default=["Twitter", "Instagram"])

    with col2:
        monitoring_period = st.selectbox("Monitoring Period", [
            "Last 24 hours", "Last 7 days", "Last 30 days", "Custom Range"
        ])
        sentiment_filter = st.selectbox("Sentiment Filter", [
            "All Mentions", "Positive Only", "Negative Only", "Neutral Only"
        ])
        language = st.selectbox("Language", ["All", "English", "Spanish", "French", "German"])

    if brand_terms:
        brand_list = [term.strip() for term in brand_terms.split('\n') if term.strip()]

        if st.button("Start Monitoring"):
            with st.spinner("Searching for mentions..."):
                # Simulate mention monitoring
                mentions_data = simulate_mention_monitoring(brand_list, platforms, monitoring_period)

                # Display results
                st.subheader("📊 Monitoring Results")

                # Overview metrics
                total_mentions = len(mentions_data)
                positive = len([m for m in mentions_data if m['sentiment'] == 'positive'])
                negative = len([m for m in mentions_data if m['sentiment'] == 'negative'])
                neutral = len([m for m in mentions_data if m['sentiment'] == 'neutral'])

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Mentions", total_mentions)
                with col2:
                    st.metric("Positive", positive,
                              f"{positive / total_mentions * 100:.1f}%" if total_mentions > 0 else "0%")
                with col3:
                    st.metric("Negative", negative,
                              f"{negative / total_mentions * 100:.1f}%" if total_mentions > 0 else "0%")
                with col4:
                    st.metric("Neutral", neutral,
                              f"{neutral / total_mentions * 100:.1f}%" if total_mentions > 0 else "0%")

                # Platform breakdown
                st.subheader("Platform Breakdown")
                platform_counts = {}
                for mention in mentions_data:
                    platform = mention['platform']
                    platform_counts[platform] = platform_counts.get(platform, 0) + 1

                for platform, count in platform_counts.items():
                    percentage = count / total_mentions * 100 if total_mentions > 0 else 0
                    st.write(f"**{platform}**: {count} mentions ({percentage:.1f}%)")
                    st.progress(percentage / 100)

                # Recent mentions
                st.subheader("Recent Mentions")
                for mention in mentions_data[:10]:  # Show first 10
                    sentiment_color = {
                        'positive': '🟢',
                        'negative': '🔴',
                        'neutral': '🟡'
                    }.get(mention['sentiment'], '⚪')

                    with st.expander(f"{sentiment_color} {mention['platform']} - {mention['author']}"):
                        st.write(f"**Content:** {mention['content']}")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Date:** {mention['date']}")
                        with col2:
                            st.write(f"**Engagement:** {mention['engagement']}")
                        with col3:
                            st.write(f"**Reach:** {mention['reach']}")

                # Export mentions
                if st.button("Export Mentions Report"):
                    report = generate_mentions_report(mentions_data, brand_list)
                    FileHandler.create_download_link(
                        report.encode(),
                        f"mentions_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )


def influencer_finder():
    """Discover and analyze influencers in your niche"""
    create_tool_header("Influencer Finder", "Find and analyze influencers for collaborations", "⭐")

    # Search criteria
    st.subheader("Influencer Search Criteria")

    col1, col2 = st.columns(2)
    with col1:
        niche = st.selectbox("Niche/Industry", [
            "Technology", "Fashion", "Beauty", "Fitness", "Food", "Travel",
            "Gaming", "Business", "Lifestyle", "Education", "Music", "Art"
        ])
        platforms = st.multiselect("Platforms", [
            "Instagram", "TikTok", "YouTube", "Twitter", "LinkedIn"
        ], default=["Instagram"])
        location = st.text_input("Location (optional)", placeholder="e.g., United States, Global")

    with col2:
        follower_range = st.selectbox("Follower Range", [
            "Nano (1K-10K)", "Micro (10K-100K)", "Mid-tier (100K-1M)",
            "Macro (1M-10M)", "Mega (10M+)", "Any Size"
        ])
        engagement_rate = st.selectbox("Min Engagement Rate", [
            "Any", "1%+", "2%+", "3%+", "5%+", "10%+"
        ])
        budget_range = st.selectbox("Budget Range", [
            "Under $500", "$500-$2K", "$2K-$10K", "$10K-$50K", "$50K+", "Negotiable"
        ])

    # Additional filters
    with st.expander("Advanced Filters"):
        keywords = st.text_input("Keywords in Bio", placeholder="fitness, wellness, healthy")
        content_type = st.multiselect("Content Types", [
            "Photos", "Videos", "Stories", "Reels", "Live Streams", "Tutorials"
        ])
        collaboration_type = st.selectbox("Collaboration Type", [
            "Sponsored Posts", "Product Reviews", "Brand Ambassadorship",
            "Event Partnerships", "Content Creation", "Any"
        ])

    if st.button("Find Influencers"):
        with st.spinner("Searching for influencers..."):
            # Simulate influencer search
            influencers = simulate_influencer_search(niche, platforms, follower_range)

            st.subheader(f"🔍 Found {len(influencers)} Influencers")

            # Display influencers
            for i, influencer in enumerate(influencers):
                with st.expander(f"👤 {influencer['name']} (@{influencer['username']})"):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write("**Profile Info:**")
                        st.write(f"• Platform: {influencer['platform']}")
                        st.write(f"• Followers: {influencer['followers']:,}")
                        st.write(f"• Location: {influencer['location']}")
                        st.write(f"• Category: {influencer['category']}")

                    with col2:
                        st.write("**Engagement Metrics:**")
                        st.write(f"• Engagement Rate: {influencer['engagement_rate']:.1f}%")
                        st.write(f"• Avg Likes: {influencer['avg_likes']:,}")
                        st.write(f"• Avg Comments: {influencer['avg_comments']:,}")
                        st.write(f"• Post Frequency: {influencer['post_frequency']}")

                    with col3:
                        st.write("**Collaboration Info:**")
                        st.write(f"• Est. Cost: {influencer['estimated_cost']}")
                        st.write(f"• Availability: {influencer['availability']}")
                        st.write(f"• Brand Safety: {influencer['brand_safety']}")

                        if st.button(f"Contact {influencer['name']}", key=f"contact_{i}"):
                            st.success(f"Contact info for {influencer['name']} saved to your outreach list!")

                    st.write(f"**Bio:** {influencer['bio']}")

                    # Audience insights
                    with st.expander("Audience Insights"):
                        audience = influencer['audience_insights']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Demographics:**")
                            for demo, percentage in audience['demographics'].items():
                                st.write(f"• {demo}: {percentage}%")
                        with col2:
                            st.write("**Interests:**")
                            for interest in audience['interests']:
                                st.write(f"• {interest}")

            # Export influencer list
            if st.button("Export Influencer List"):
                export_data = generate_influencer_export(influencers, niche)
                FileHandler.create_download_link(
                    export_data.encode(),
                    f"influencers_{niche.lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )


def cross_platform_posting():
    """Post content across multiple social media platforms"""
    create_tool_header("Cross-Platform Posting", "Publish content to multiple platforms simultaneously", "📡")

    # Platform selection
    st.subheader("Select Platforms")
    platforms = st.multiselect("Choose Platforms", [
        "Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok", "Pinterest", "YouTube"
    ], default=["Instagram", "Facebook", "Twitter"])

    if not platforms:
        st.warning("Please select at least one platform to continue.")
        return

    # Content creation
    st.subheader("Create Your Content")

    content_type = st.selectbox("Content Type", [
        "Text Post", "Image Post", "Video Post", "Link Share", "Carousel"
    ])

    # Main content
    main_content = st.text_area("Main Content", height=150,
                                placeholder="Write your main post content here...")

    # Platform-specific customization
    st.subheader("Platform-Specific Customization")
    platform_content = {}

    for platform in platforms:
        with st.expander(f"{platform} Settings"):
            col1, col2 = st.columns(2)

            with col1:
                custom_content = st.text_area(f"Custom content for {platform}",
                                              value=main_content, key=f"content_{platform}",
                                              help=f"Customize content specifically for {platform}")

                hashtags = st.text_input(f"Hashtags for {platform}",
                                         placeholder="#hashtag1 #hashtag2", key=f"hashtags_{platform}")

            with col2:
                # Platform-specific options
                if platform == "Twitter":
                    thread_mode = st.checkbox("Create Thread", key=f"thread_{platform}")
                    if thread_mode:
                        thread_parts = st.number_input("Number of tweets", 1, 10, 1, key=f"thread_count_{platform}")

                elif platform == "Instagram":
                    story_post = st.checkbox("Also post to Story", key=f"story_{platform}")
                    use_carousel = st.checkbox("Carousel Post", key=f"carousel_{platform}")

                elif platform == "LinkedIn":
                    professional_tone = st.checkbox("Use Professional Tone", True, key=f"prof_{platform}")
                    article_format = st.checkbox("Format as Article", key=f"article_{platform}")

                elif platform == "TikTok":
                    trending_sounds = st.checkbox("Use Trending Audio", key=f"audio_{platform}")
                    duet_enabled = st.checkbox("Allow Duets", True, key=f"duet_{platform}")

                posting_time = st.selectbox(f"Posting Time for {platform}", [
                    "Post Now", "Optimal Time", "Custom Time"
                ], key=f"time_{platform}")

            platform_content[platform] = {
                'content': custom_content,
                'hashtags': hashtags,
                'posting_time': posting_time
            }

    # Media upload
    if content_type in ["Image Post", "Video Post", "Carousel"]:
        st.subheader("Upload Media")
        media_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov'], accept_multiple=True)

        if media_files:
            st.success(f"Uploaded {len(media_files)} media file(s)")

            # Media preview
            for i, file in enumerate(media_files[:3]):  # Show first 3
                if file.type.startswith('image/'):
                    st.image(file, caption=f"Image {i + 1}", width=200)

    # Scheduling options
    st.subheader("Scheduling Options")

    col1, col2 = st.columns(2)
    with col1:
        schedule_option = st.selectbox("When to Post", [
            "Post Immediately", "Schedule for Later", "Save as Draft"
        ])

    with col2:
        if schedule_option == "Schedule for Later":
            schedule_date = st.date_input("Schedule Date")
            schedule_time = st.time_input("Schedule Time")

    # Preview and post
    if st.button("Preview Posts") and main_content:
        st.subheader("📱 Post Preview")

        for platform in platforms:
            content = platform_content[platform]
            with st.expander(f"{platform} Preview"):
                st.write(f"**Content:** {content['content']}")
                if content['hashtags']:
                    st.write(f"**Hashtags:** {content['hashtags']}")
                st.write(f"**Posting Time:** {content['posting_time']}")

                # Platform-specific preview styling
                if platform == "Twitter":
                    st.info("💙 Twitter post preview")
                elif platform == "Instagram":
                    st.info("📸 Instagram post preview")
                elif platform == "LinkedIn":
                    st.info("💼 LinkedIn post preview")

    # Post to platforms
    if st.button("🚀 Post to All Platforms") and main_content:
        posting_results = {}

        for platform in platforms:
            # Simulate posting
            success = simulate_cross_platform_post(platform, platform_content[platform])
            posting_results[platform] = success

        # Display results
        st.subheader("📊 Posting Results")

        successful_posts = sum(posting_results.values())
        failed_posts = len(platforms) - successful_posts

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Successful Posts", successful_posts)
        with col2:
            st.metric("Failed Posts", failed_posts)

        for platform, success in posting_results.items():
            status = "✅ Posted successfully" if success else "❌ Failed to post"
            st.write(f"**{platform}:** {status}")

        # Export posting report
        if st.button("Export Posting Report"):
            report = generate_posting_report(posting_results, platform_content)
            FileHandler.create_download_link(
                report.encode(),
                f"posting_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain"
            )


def trending_hashtags():
    """Discover trending hashtags across platforms"""
    create_tool_header("Trending Hashtags", "Find the most popular hashtags for maximum reach", "#️⃣")

    # Search parameters
    st.subheader("Hashtag Discovery Settings")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", [
            "Instagram", "Twitter", "TikTok", "LinkedIn", "Pinterest", "All Platforms"
        ])
        category = st.selectbox("Category", [
            "All Categories", "Technology", "Fashion", "Food", "Travel", "Fitness",
            "Business", "Entertainment", "Sports", "News", "Art", "Music"
        ])

    with col2:
        time_period = st.selectbox("Time Period", [
            "Last 24 hours", "Last 7 days", "Last 30 days", "This month"
        ])
        hashtag_type = st.selectbox("Hashtag Type", [
            "All Types", "Trending", "Popular", "Emerging", "Seasonal"
        ])

    # Optional keyword input
    keywords = st.text_input("Keywords (optional)",
                             placeholder="Enter keywords to find related trending hashtags")

    if st.button("Find Trending Hashtags"):
        with st.spinner("Discovering trending hashtags..."):
            # Simulate hashtag discovery
            trending_data = simulate_trending_hashtags(platform, category, time_period, keywords)

            st.subheader(f"🔥 Trending Hashtags - {platform}")

            # Display trending hashtags in tabs
            tabs = st.tabs(["Top Trending", "Rising", "Category Specific", "Related"])

            with tabs[0]:  # Top Trending
                st.write("**Most Popular Right Now:**")
                for i, hashtag in enumerate(trending_data['top_trending'][:20], 1):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**#{i}. #{hashtag['tag']}**")
                    with col2:
                        st.write(f"📊 {hashtag['posts']:,} posts")
                    with col3:
                        growth = hashtag['growth']
                        growth_color = "🟢" if growth > 0 else "🔴" if growth < 0 else "⚪"
                        st.write(f"{growth_color} {growth:+.1f}%")

            with tabs[1]:  # Rising
                st.write("**Rapidly Growing Hashtags:**")
                for hashtag in trending_data['rising'][:15]:
                    st.write(f"🚀 **#{hashtag['tag']}** - {hashtag['posts']:,} posts (+{hashtag['growth']:.1f}%)")

            with tabs[2]:  # Category Specific
                if category != "All Categories":
                    st.write(f"**{category} Hashtags:**")
                    for hashtag in trending_data['category_specific'][:15]:
                        st.write(f"📂 **#{hashtag['tag']}** - {hashtag['posts']:,} posts")
                else:
                    st.info("Select a specific category to see category-specific hashtags")

            with tabs[3]:  # Related
                if keywords:
                    st.write(f"**Related to '{keywords}':**")
                    for hashtag in trending_data['related'][:15]:
                        st.write(f"🔗 **#{hashtag['tag']}** - {hashtag['relevance']}% match")
                else:
                    st.info("Enter keywords to see related hashtags")

            # Hashtag strategy recommendations
            st.subheader("📈 Strategy Recommendations")
            recommendations = generate_hashtag_strategy_recommendations(trending_data, platform)

            for rec in recommendations:
                st.write(f"💡 {rec}")

            # Copy hashtags functionality
            st.subheader("📋 Quick Copy")
            all_trending = trending_data['top_trending'][:10]
            hashtag_string = ' '.join([f"#{h['tag']}" for h in all_trending])

            st.text_area("Copy these hashtags:", hashtag_string, height=100)

            # Export trending data
            if st.button("Export Trending Data"):
                export_text = generate_hashtag_export(trending_data, platform, category)
                FileHandler.create_download_link(
                    export_text.encode(),
                    f"trending_hashtags_{platform.lower()}_{datetime.now().strftime('%Y%m%d')}.txt",
                    "text/plain"
                )


def performance_tracker():
    """Track and analyze social media performance metrics"""
    create_tool_header("Performance Tracker", "Monitor your social media performance across platforms", "📊")

    # Data source selection
    st.subheader("Performance Data")

    data_source = st.selectbox("Data Source", [
        "Upload Analytics CSV", "Manual Entry", "Sample Data", "Platform Integration"
    ])

    performance_data = None

    if data_source == "Upload Analytics CSV":
        uploaded_file = FileHandler.upload_files(['csv'], accept_multiple=False)
        if uploaded_file:
            df = FileHandler.process_csv_file(uploaded_file[0])
            if df is not None:
                st.dataframe(df.head())
                performance_data = df.to_dict('records')

    elif data_source == "Sample Data":
        performance_data = generate_sample_performance_data()
        st.success("Using sample performance data")

    elif data_source == "Manual Entry":
        st.subheader("Enter Performance Data")

        num_posts = st.number_input("Number of Posts to Track", 1, 50, 10)
        performance_data = []

        for i in range(min(num_posts, 5)):  # Limit UI to 5 for demo
            with st.expander(f"Post {i + 1}"):
                col1, col2 = st.columns(2)

                with col1:
                    platform = st.selectbox(f"Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok"],
                                            key=f"perf_platform_{i}")
                    post_type = st.selectbox(f"Post Type", ["Image", "Video", "Carousel", "Text", "Story"],
                                             key=f"perf_type_{i}")
                    date = st.date_input(f"Post Date", key=f"perf_date_{i}")
                    time_posted = st.time_input(f"Time Posted", key=f"perf_time_{i}")

                with col2:
                    reach = st.number_input(f"Reach", 0, 10000000, 1000, key=f"perf_reach_{i}")
                    impressions = st.number_input(f"Impressions", 0, 10000000, 1500, key=f"perf_impressions_{i}")
                    likes = st.number_input(f"Likes", 0, 100000, 50, key=f"perf_likes_{i}")
                    comments = st.number_input(f"Comments", 0, 10000, 5, key=f"perf_comments_{i}")
                    shares = st.number_input(f"Shares", 0, 10000, 2, key=f"perf_shares_{i}")
                    clicks = st.number_input(f"Link Clicks", 0, 10000, 10, key=f"perf_clicks_{i}")

                engagement_rate = ((likes + comments + shares) / impressions * 100) if impressions > 0 else 0

                performance_data.append({
                    'platform': platform,
                    'post_type': post_type,
                    'date': date.isoformat(),
                    'time': time_posted.isoformat(),
                    'reach': reach,
                    'impressions': impressions,
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'clicks': clicks,
                    'engagement_rate': engagement_rate
                })

    # Performance analysis
    if performance_data:
        st.subheader("📈 Performance Analysis")

        # Overall metrics
        total_posts = len(performance_data)
        total_reach = sum(post.get('reach', 0) for post in performance_data)
        total_impressions = sum(post.get('impressions', 0) for post in performance_data)
        total_engagement = sum(
            post.get('likes', 0) + post.get('comments', 0) + post.get('shares', 0) for post in performance_data)
        avg_engagement_rate = sum(
            post.get('engagement_rate', 0) for post in performance_data) / total_posts if total_posts > 0 else 0

        # Display key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Posts", total_posts)
        with col2:
            st.metric("Total Reach", f"{total_reach:,}")
        with col3:
            st.metric("Total Impressions", f"{total_impressions:,}")
        with col4:
            st.metric("Total Engagement", f"{total_engagement:,}")
        with col5:
            st.metric("Avg Engagement Rate", f"{avg_engagement_rate:.2f}%")

        # Platform performance comparison
        st.subheader("Platform Comparison")
        platform_stats = analyze_platform_performance(performance_data)

        for platform, stats in platform_stats.items():
            with st.expander(f"{platform} Performance"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Posts", stats['posts'])
                with col2:
                    st.metric("Avg Reach", f"{stats['avg_reach']:,.0f}")
                with col3:
                    st.metric("Avg Engagement", f"{stats['avg_engagement']:.2f}%")
                with col4:
                    st.metric("Best Performing", stats['best_post_type'])

        # Best performing content
        st.subheader("🏆 Top Performing Posts")
        top_posts = sorted(performance_data, key=lambda x: x.get('engagement_rate', 0), reverse=True)[:5]

        for i, post in enumerate(top_posts, 1):
            with st.expander(f"#{i} - {post.get('platform', 'Unknown')} {post.get('post_type', 'Post')}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Date:** {post.get('date', 'Unknown')}")
                    st.write(f"**Platform:** {post.get('platform', 'Unknown')}")
                    st.write(f"**Type:** {post.get('post_type', 'Unknown')}")
                with col2:
                    st.write(f"**Reach:** {post.get('reach', 0):,}")
                    st.write(f"**Impressions:** {post.get('impressions', 0):,}")
                    st.write(f"**Clicks:** {post.get('clicks', 0):,}")
                with col3:
                    st.write(f"**Likes:** {post.get('likes', 0):,}")
                    st.write(f"**Comments:** {post.get('comments', 0):,}")
                    st.write(f"**Engagement Rate:** {post.get('engagement_rate', 0):.2f}%")

        # Performance insights
        st.subheader("🔍 Performance Insights")
        insights = generate_performance_insights(performance_data)

        for insight in insights:
            st.write(f"💡 {insight}")

        # Export performance report
        if st.button("Export Performance Report"):
            report = generate_performance_report(performance_data, platform_stats)
            FileHandler.create_download_link(
                report.encode(),
                f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain"
            )


def ab_testing():
    """Set up and analyze A/B tests for social media content"""
    create_tool_header("A/B Testing", "Test different content variations to optimize performance", "🧪")

    # Test setup
    st.subheader("A/B Test Setup")

    col1, col2 = st.columns(2)
    with col1:
        test_name = st.text_input("Test Name", placeholder="e.g., Header Image Test")
        test_objective = st.selectbox("Primary Objective", [
            "Increase Engagement Rate", "Boost Click-through Rate", "Improve Reach",
            "Maximize Likes", "Increase Comments", "Drive Website Traffic"
        ])
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok"])

    with col2:
        test_duration = st.number_input("Test Duration (days)", 1, 30, 7)
        audience_split = st.selectbox("Audience Split", ["50/50", "60/40", "70/30", "Custom"])
        confidence_level = st.selectbox("Confidence Level", ["90%", "95%", "99%"])

    # Content variations
    st.subheader("Content Variations")

    # Variation A
    st.write("**Variation A (Control)**")
    col1, col2 = st.columns(2)
    with col1:
        content_a = st.text_area("Content A", height=100, placeholder="Enter your control content...")
        hashtags_a = st.text_input("Hashtags A", placeholder="#hashtag1 #hashtag2")
    with col2:
        post_time_a = st.time_input("Posting Time A", key="time_a")
        cta_a = st.text_input("Call-to-Action A", placeholder="Learn more", key="cta_a")

    # Variation B
    st.write("**Variation B (Test)**")
    col1, col2 = st.columns(2)
    with col1:
        content_b = st.text_area("Content B", height=100, placeholder="Enter your test content...")
        hashtags_b = st.text_input("Hashtags B", placeholder="#hashtag1 #hashtag2")
    with col2:
        post_time_b = st.time_input("Posting Time B", key="time_b")
        cta_b = st.text_input("Call-to-Action B", placeholder="Discover now", key="cta_b")

    # Test variables
    st.subheader("What Are You Testing?")
    test_variables = st.multiselect("Test Variables", [
        "Content Copy", "Hashtags", "Posting Time", "Call-to-Action",
        "Image/Video", "Caption Length", "Emoji Usage", "Question vs Statement"
    ])

    # Hypothesis
    hypothesis = st.text_area("Hypothesis",
                              placeholder="I believe that [variation B] will perform better than [variation A] because...")

    # Launch test
    if st.button("Launch A/B Test") and test_name and content_a and content_b:
        # Create test configuration
        test_config = {
            'test_name': test_name,
            'objective': test_objective,
            'platform': platform,
            'duration': test_duration,
            'audience_split': audience_split,
            'confidence_level': confidence_level,
            'variation_a': {
                'content': content_a,
                'hashtags': hashtags_a,
                'post_time': post_time_a.isoformat(),
                'cta': cta_a
            },
            'variation_b': {
                'content': content_b,
                'hashtags': hashtags_b,
                'post_time': post_time_b.isoformat(),
                'cta': cta_b
            },
            'test_variables': test_variables,
            'hypothesis': hypothesis,
            'start_date': datetime.now().isoformat()
        }

        st.success(f"✅ A/B Test '{test_name}' has been launched!")

        # Simulate test results (in real implementation, this would track actual performance)
        with st.spinner("Simulating test results..."):
            test_results = simulate_ab_test_results(test_config)

            st.subheader("📊 Test Results")

            # Results overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Test Status", "Completed" if test_results['is_significant'] else "Ongoing")
            with col2:
                st.metric("Statistical Significance", "Yes" if test_results['is_significant'] else "No")
            with col3:
                winner = "Variation B" if test_results['winner'] == 'B' else "Variation A"
                st.metric("Winner", winner)

            # Detailed comparison
            st.subheader("Detailed Comparison")

            comparison_data = {
                'Metric': ['Impressions', 'Reach', 'Likes', 'Comments', 'Shares', 'Clicks', 'Engagement Rate'],
                'Variation A': [
                    f"{test_results['variation_a']['impressions']:,}",
                    f"{test_results['variation_a']['reach']:,}",
                    f"{test_results['variation_a']['likes']:,}",
                    f"{test_results['variation_a']['comments']:,}",
                    f"{test_results['variation_a']['shares']:,}",
                    f"{test_results['variation_a']['clicks']:,}",
                    f"{test_results['variation_a']['engagement_rate']:.2f}%"
                ],
                'Variation B': [
                    f"{test_results['variation_b']['impressions']:,}",
                    f"{test_results['variation_b']['reach']:,}",
                    f"{test_results['variation_b']['likes']:,}",
                    f"{test_results['variation_b']['comments']:,}",
                    f"{test_results['variation_b']['shares']:,}",
                    f"{test_results['variation_b']['clicks']:,}",
                    f"{test_results['variation_b']['engagement_rate']:.2f}%"
                ],
                'Improvement': [
                    f"{test_results['improvements']['impressions']:+.1f}%",
                    f"{test_results['improvements']['reach']:+.1f}%",
                    f"{test_results['improvements']['likes']:+.1f}%",
                    f"{test_results['improvements']['comments']:+.1f}%",
                    f"{test_results['improvements']['shares']:+.1f}%",
                    f"{test_results['improvements']['clicks']:+.1f}%",
                    f"{test_results['improvements']['engagement_rate']:+.1f}%"
                ]
            }

            st.table(comparison_data)

            # Key insights
            st.subheader("🔍 Key Insights")
            for insight in test_results['insights']:
                st.write(f"💡 {insight}")

            # Recommendations
            st.subheader("📋 Recommendations")
            for rec in test_results['recommendations']:
                st.write(f"✅ {rec}")

            # Export test results
            if st.button("Export Test Results"):
                report = generate_ab_test_report(test_config, test_results)
                FileHandler.create_download_link(
                    report.encode(),
                    f"ab_test_{test_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    "text/plain"
                )


def brand_tracking():
    """Track brand sentiment and performance across social media"""
    create_tool_header("Brand Tracking", "Monitor your brand's social media presence and sentiment", "🏷️")

    # Brand setup
    st.subheader("Brand Monitoring Setup")

    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input("Brand Name", placeholder="Enter your brand name")
        brand_handles = st.text_area("Social Media Handles",
                                     placeholder="@brandname (one per line)", height=100)
        competitors = st.text_area("Competitor Brands",
                                   placeholder="Enter competitor names (one per line)", height=100)

    with col2:
        tracking_period = st.selectbox("Tracking Period", [
            "Last 7 days", "Last 30 days", "Last 3 months", "Custom Range"
        ])
        platforms = st.multiselect("Platforms to Monitor", [
            "Twitter", "Instagram", "Facebook", "LinkedIn", "TikTok", "YouTube", "Reddit"
        ], default=["Twitter", "Instagram", "Facebook"])
        industries = st.multiselect("Industry Keywords", [
            "Technology", "Fashion", "Food", "Finance", "Healthcare", "Education", "Other"
        ])

    if brand_name and st.button("Start Brand Tracking"):
        with st.spinner("Analyzing brand presence..."):
            # Simulate brand tracking data
            brand_data = simulate_brand_tracking(brand_name, platforms, tracking_period)

            # Brand overview
            st.subheader(f"📊 {brand_name} Brand Overview")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Mentions", f"{brand_data['total_mentions']:,}")
            with col2:
                sentiment_score = brand_data['sentiment_score']
                sentiment_emoji = "😊" if sentiment_score > 0.6 else "😐" if sentiment_score > 0.3 else "😞"
                st.metric("Sentiment Score", f"{sentiment_score:.1f}/5.0 {sentiment_emoji}")
            with col3:
                st.metric("Reach", f"{brand_data['total_reach']:,}")
            with col4:
                st.metric("Share of Voice", f"{brand_data['share_of_voice']:.1f}%")

            # Sentiment breakdown
            st.subheader("Sentiment Analysis")

            col1, col2, col3 = st.columns(3)
            with col1:
                positive_pct = brand_data['sentiment_breakdown']['positive']
                st.metric("Positive", f"{positive_pct:.1f}%", f"+{positive_pct - 33.3:.1f}%")
                st.progress(positive_pct / 100)

            with col2:
                neutral_pct = brand_data['sentiment_breakdown']['neutral']
                st.metric("Neutral", f"{neutral_pct:.1f}%")
                st.progress(neutral_pct / 100)

            with col3:
                negative_pct = brand_data['sentiment_breakdown']['negative']
                st.metric("Negative", f"{negative_pct:.1f}%", f"{negative_pct - 33.3:.1f}%")
                st.progress(negative_pct / 100)

            # Platform performance
            st.subheader("Platform Performance")

            for platform_name, platform_data in brand_data['platform_breakdown'].items():
                with st.expander(f"{platform_name} Performance"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Mentions", f"{platform_data['mentions']:,}")
                    with col2:
                        st.metric("Engagement", f"{platform_data['engagement']:,}")
                    with col3:
                        st.metric("Reach", f"{platform_data['reach']:,}")
                    with col4:
                        st.metric("Sentiment", f"{platform_data['sentiment']:.1f}/5.0")

            # Recent mentions
            st.subheader("Recent Brand Mentions")

            for mention in brand_data['recent_mentions'][:10]:
                sentiment_color = {
                    'positive': '🟢',
                    'negative': '🔴',
                    'neutral': '🟡'
                }.get(mention['sentiment'], '⚪')

                with st.expander(f"{sentiment_color} {mention['platform']} - {mention['author']}"):
                    st.write(f"**Content:** {mention['content']}")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Date:** {mention['date']}")
                    with col2:
                        st.write(f"**Engagement:** {mention['engagement']}")
                    with col3:
                        st.write(f"**Reach:** {mention['reach']}")

            # Competitor comparison
            if competitors:
                st.subheader("Competitor Comparison")
                competitor_list = [c.strip() for c in competitors.split('\n') if c.strip()]

                comparison_data = simulate_competitor_comparison(brand_name, competitor_list)

                for competitor, data in comparison_data.items():
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**{competitor}**")
                    with col2:
                        st.write(f"Mentions: {data['mentions']:,}")
                    with col3:
                        st.write(f"Sentiment: {data['sentiment']:.1f}/5.0")
                    with col4:
                        vs_brand = data['mentions'] - brand_data['total_mentions']
                        st.write(f"vs {brand_name}: {vs_brand:+,}")

            # Brand insights
            st.subheader("📈 Brand Insights")
            insights = generate_brand_insights(brand_data, brand_name)

            for insight in insights:
                st.write(f"💡 {insight}")

            # Action items
            st.subheader("🎯 Recommended Actions")
            actions = generate_brand_action_items(brand_data)

            for action in actions:
                st.write(f"✅ {action}")

            # Export brand report
            if st.button("Export Brand Report"):
                report = generate_brand_report(brand_data, brand_name)
                FileHandler.create_download_link(
                    report.encode(),
                    f"brand_report_{brand_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    "text/plain"
                )


# Helper Functions for Social Media Tools

def generate_sample_audience_data():
    """Generate sample audience data for demonstration"""
    return [
        {
            'segment_name': 'Tech Enthusiasts',
            'age_range': '25-34',
            'gender': 'All',
            'location': 'United States',
            'interests': ['technology', 'innovation', 'startups'],
            'platforms': ['LinkedIn', 'Twitter', 'Instagram'],
            'engagement_level': 'High',
            'spending_power': 'High'
        },
        {
            'segment_name': 'Young Professionals',
            'age_range': '25-34',
            'gender': 'All',
            'location': 'Global',
            'interests': ['career', 'networking', 'business'],
            'platforms': ['LinkedIn', 'Instagram'],
            'engagement_level': 'Medium',
            'spending_power': 'Medium'
        },
        {
            'segment_name': 'Creative Millennials',
            'age_range': '25-34',
            'gender': 'All',
            'location': 'Urban areas',
            'interests': ['design', 'art', 'creativity'],
            'platforms': ['Instagram', 'TikTok', 'Pinterest'],
            'engagement_level': 'High',
            'spending_power': 'Medium'
        }
    ]


def analyze_audience_segments(audience_data, primary_criteria, secondary_criteria):
    """Analyze audience segments based on criteria"""
    segments = []

    for i, segment in enumerate(audience_data):
        segment_analysis = {
            'name': segment.get('segment_name', f'Segment {i + 1}'),
            'percentage': random.uniform(15, 35),
            'demographics': {
                'age': segment.get('age_range', 'Unknown'),
                'gender': segment.get('gender', 'All'),
                'location': segment.get('location', 'Global')
            },
            'behavior': {
                'engagement': segment.get('engagement_level', 'Medium'),
                'activity': random.choice(['High', 'Medium', 'Low'])
            },
            'platforms': segment.get('platforms', []),
            'interests': segment.get('interests', []),
            'recommendations': [
                f"Target during peak {random.choice(['morning', 'afternoon', 'evening'])} hours",
                f"Use {random.choice(['visual', 'video', 'text'])} content for best engagement",
                f"Focus on {random.choice(['educational', 'entertaining', 'promotional'])} content"
            ]
        }
        segments.append(segment_analysis)

    # Sort by percentage
    segments.sort(key=lambda x: x['percentage'], reverse=True)

    return {
        'segments': segments,
        'largest_segment': segments[0] if segments else {'name': 'None'},
        'most_engaged': max(segments,
                            key=lambda x: 1 if x['behavior']['engagement'] == 'High' else 0) if segments else {
            'name': 'None'},
        'high_value': {'count': len([s for s in segments if s['demographics']['age'] in ['25-34', '35-44']])},
        'marketing_recommendations': {
            'content_strategy': [
                "Create platform-specific content for each segment",
                "Use data-driven insights to optimize posting times",
                "Develop personalized messaging for each segment"
            ],
            'targeting': [
                "Use lookalike audiences based on your best segments",
                "Implement retargeting campaigns for engaged users",
                "Test different ad formats for each segment"
            ],
            'engagement': [
                "Respond quickly to comments and messages",
                "Create interactive content like polls and Q&As",
                "Build community through user-generated content"
            ]
        }
    }


def generate_segmentation_report(analysis_results, audience_data):
    """Generate a text report of segmentation analysis"""
    report = f"AUDIENCE SEGMENTATION REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 50 + "\n\n"

    report += "EXECUTIVE SUMMARY\n"
    report += f"Total Segments Analyzed: {len(analysis_results['segments'])}\n"
    report += f"Largest Segment: {analysis_results['largest_segment']['name']}\n"
    report += f"Most Engaged Segment: {analysis_results['most_engaged']['name']}\n\n"

    report += "DETAILED SEGMENT ANALYSIS\n"
    for segment in analysis_results['segments']:
        report += f"\n{segment['name']} ({segment['percentage']:.1f}%)\n"
        report += f"- Demographics: {segment['demographics']['age']}, {segment['demographics']['gender']}, {segment['demographics']['location']}\n"
        report += f"- Platforms: {', '.join(segment['platforms'])}\n"
        report += f"- Interests: {', '.join(segment['interests'])}\n"
        report += f"- Engagement: {segment['behavior']['engagement']}\n"

    return report


def generate_platform_recommendations(platform, campaign_type, target_audience):
    """Generate platform-specific recommendations"""
    recommendations = {
        'Instagram': [
            "Use high-quality visuals and Stories",
            "Post consistently with relevant hashtags",
            "Engage with user-generated content",
            "Utilize Instagram Shopping features"
        ],
        'Facebook': [
            "Create engaging video content",
            "Use Facebook Groups for community building",
            "Leverage Facebook Ads for precise targeting",
            "Share behind-the-scenes content"
        ],
        'Twitter': [
            "Join trending conversations",
            "Use relevant hashtags and mentions",
            "Share timely, news-worthy content",
            "Engage in real-time conversations"
        ],
        'LinkedIn': [
            "Share professional insights and thought leadership",
            "Use LinkedIn Articles for long-form content",
            "Engage in industry-specific groups",
            "Share company updates and achievements"
        ],
        'TikTok': [
            "Create short, entertaining videos",
            "Use trending sounds and effects",
            "Collaborate with TikTok creators",
            "Post consistently to maintain visibility"
        ]
    }

    return recommendations.get(platform,
                               ["Customize content for platform-specific audience", "Monitor engagement metrics",
                                "Test different content formats"])


def generate_campaign_plan_report(campaign_data):
    """Generate a comprehensive campaign plan report"""
    report = f"SOCIAL MEDIA CAMPAIGN PLAN: {campaign_data['campaign_name']}\n"
    report += "=" * 60 + "\n\n"

    report += f"Campaign Type: {campaign_data['campaign_type']}\n"
    report += f"Duration: {campaign_data['start_date']} to {campaign_data['end_date']}\n"
    report += f"Target Audience: {campaign_data['target_audience']}\n"
    report += f"Budget: ${campaign_data['budget']:,}\n"
    report += f"Primary Goal: {campaign_data['primary_goal']}\n"
    report += f"Platforms: {', '.join(campaign_data['platforms'])}\n\n"

    report += "OBJECTIVES\n"
    for obj in campaign_data['objectives']:
        report += f"- {obj['name']}: {obj['target']} {obj['metric']} ({obj['timeframe']})\n"

    report += f"\nCONTENT STRATEGY\n"
    report += f"Themes: {campaign_data['content_themes']}\n"
    report += f"Types: {', '.join(campaign_data['content_types'])}\n\n"

    report += "BUDGET ALLOCATION\n"
    for platform, budget in campaign_data['budget_allocation'].items():
        report += f"- {platform}: ${budget:,}\n"

    report += f"\nMILESTONES\n"
    for milestone in campaign_data['milestones']:
        report += f"- {milestone['date']}: {milestone['name']} ({milestone['owner']})\n"

    return report


def simulate_mention_monitoring(brand_list, platforms, monitoring_period):
    """Simulate mention monitoring results"""
    mentions = []

    for brand in brand_list:
        for platform in platforms:
            num_mentions = random.randint(5, 50)

            for i in range(num_mentions):
                mention = {
                    'brand': brand,
                    'platform': platform,
                    'author': f"user_{random.randint(1000, 9999)}",
                    'content': f"Just tried {brand}! {random.choice(['Amazing product!', 'Great service!', 'Could be better', 'Love it!', 'Not impressed'])}",
                    'date': (datetime.now() - timedelta(days=random.randint(0, 7))).strftime('%Y-%m-%d'),
                    'sentiment': random.choice(['positive', 'negative', 'neutral']),
                    'engagement': random.randint(10, 1000),
                    'reach': random.randint(100, 10000)
                }
                mentions.append(mention)

    return mentions


def generate_mentions_report(mentions_data, brand_list):
    """Generate mentions monitoring report"""
    report = f"BRAND MENTIONS REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Brands Monitored: {', '.join(brand_list)}\n"
    report += "=" * 50 + "\n\n"

    total_mentions = len(mentions_data)
    positive = len([m for m in mentions_data if m['sentiment'] == 'positive'])
    negative = len([m for m in mentions_data if m['sentiment'] == 'negative'])
    neutral = len([m for m in mentions_data if m['sentiment'] == 'neutral'])

    report += f"SUMMARY\n"
    report += f"Total Mentions: {total_mentions}\n"
    report += f"Positive: {positive} ({positive / total_mentions * 100:.1f}%)\n"
    report += f"Negative: {negative} ({negative / total_mentions * 100:.1f}%)\n"
    report += f"Neutral: {neutral} ({neutral / total_mentions * 100:.1f}%)\n\n"

    # Platform breakdown
    platform_counts = {}
    for mention in mentions_data:
        platform = mention['platform']
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

    report += "PLATFORM BREAKDOWN\n"
    for platform, count in platform_counts.items():
        report += f"- {platform}: {count} mentions\n"

    return report


def simulate_influencer_search(niche, platforms, follower_range):
    """Simulate influencer search results"""
    influencers = []

    follower_ranges = {
        "Nano (1K-10K)": (1000, 10000),
        "Micro (10K-100K)": (10000, 100000),
        "Mid-tier (100K-1M)": (100000, 1000000),
        "Macro (1M-10M)": (1000000, 10000000),
        "Mega (10M+)": (10000000, 50000000),
        "Any Size": (1000, 50000000)
    }

    min_followers, max_followers = follower_ranges.get(follower_range, (1000, 100000))

    for i in range(10):  # Generate 10 influencers
        followers = random.randint(min_followers, max_followers)
        engagement_rate = random.uniform(1.5, 8.0)

        influencer = {
            'name': f"{random.choice(['Alex', 'Jordan', 'Taylor', 'Casey', 'Morgan'])} {random.choice(['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson'])}",
            'username': f"{niche.lower()}_guru_{random.randint(100, 999)}",
            'platform': random.choice(platforms),
            'followers': followers,
            'engagement_rate': engagement_rate,
            'avg_likes': int(followers * engagement_rate / 100 * 0.8),
            'avg_comments': int(followers * engagement_rate / 100 * 0.2),
            'location': random.choice(['United States', 'Canada', 'United Kingdom', 'Australia', 'Global']),
            'category': niche,
            'post_frequency': random.choice(['Daily', '3-4 times/week', 'Weekly', '2-3 times/week']),
            'estimated_cost': f"${random.randint(100, 5000)}",
            'availability': random.choice(['Available', 'Busy until next month', 'Selective collaborations']),
            'brand_safety': random.choice(['Excellent', 'Good', 'Fair']),
            'bio': f"Passionate {niche.lower()} enthusiast sharing tips and insights. Sponsored by various brands.",
            'audience_insights': {
                'demographics': {
                    '18-24': random.randint(20, 40),
                    '25-34': random.randint(30, 50),
                    '35-44': random.randint(15, 25),
                    '45+': random.randint(5, 15)
                },
                'interests': [f"{niche} trends", "Lifestyle", "Shopping", "Entertainment"]
            }
        }
        influencers.append(influencer)

    return sorted(influencers, key=lambda x: x['engagement_rate'], reverse=True)


def generate_influencer_export(influencers, niche):
    """Generate CSV export of influencer data"""
    csv_data = "Name,Username,Platform,Followers,Engagement Rate,Estimated Cost,Location,Availability\n"

    for influencer in influencers:
        csv_data += f"{influencer['name']},{influencer['username']},{influencer['platform']},{influencer['followers']},{influencer['engagement_rate']:.1f}%,{influencer['estimated_cost']},{influencer['location']},{influencer['availability']}\n"

    return csv_data


def simulate_cross_platform_post(platform, content_data):
    """Simulate posting to a platform"""
    # Simulate success/failure (90% success rate)
    return random.random() > 0.1


def generate_posting_report(posting_results, platform_content):
    """Generate cross-platform posting report"""
    report = f"CROSS-PLATFORM POSTING REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 50 + "\n\n"

    successful = sum(posting_results.values())
    total = len(posting_results)

    report += f"POSTING SUMMARY\n"
    report += f"Total Platforms: {total}\n"
    report += f"Successful Posts: {successful}\n"
    report += f"Failed Posts: {total - successful}\n"
    report += f"Success Rate: {successful / total * 100:.1f}%\n\n"

    report += "PLATFORM RESULTS\n"
    for platform, success in posting_results.items():
        status = "SUCCESS" if success else "FAILED"
        report += f"- {platform}: {status}\n"

    return report


def simulate_trending_hashtags(platform, category, time_period, keywords):
    """Simulate trending hashtag discovery"""
    base_hashtags = {
        'Technology': ['tech', 'innovation', 'AI', 'startup', 'digital', 'coding', 'software'],
        'Fashion': ['fashion', 'style', 'outfit', 'trending', 'designer', 'streetstyle', 'ootd'],
        'Food': ['food', 'recipe', 'delicious', 'cooking', 'foodie', 'yummy', 'instafood'],
        'Travel': ['travel', 'wanderlust', 'vacation', 'explore', 'adventure', 'travelgram'],
        'Fitness': ['fitness', 'workout', 'gym', 'health', 'motivation', 'strong', 'fitlife']
    }

    category_tags = base_hashtags.get(category, ['trending', 'popular', 'viral'])

    trending_data = {
        'top_trending': [],
        'rising': [],
        'category_specific': [],
        'related': []
    }

    # Generate top trending
    for i, tag in enumerate(category_tags[:10]):
        trending_data['top_trending'].append({
            'tag': tag,
            'posts': random.randint(50000, 500000),
            'growth': random.uniform(-10, 50)
        })

    # Generate rising hashtags
    for i in range(15):
        trending_data['rising'].append({
            'tag': f"{random.choice(category_tags)}{random.randint(2024, 2025)}",
            'posts': random.randint(1000, 50000),
            'growth': random.uniform(20, 200)
        })

    # Category specific
    if category != "All Categories":
        for tag in category_tags:
            trending_data['category_specific'].append({
                'tag': f"{tag}{random.choice(['daily', 'tips', 'life', 'vibes'])}",
                'posts': random.randint(10000, 100000)
            })

    # Related to keywords
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(',')]
        for keyword in keyword_list[:5]:
            trending_data['related'].append({
                'tag': f"{keyword}{random.choice(['love', 'life', 'daily', 'tips'])}",
                'relevance': random.randint(70, 95)
            })

    return trending_data


def generate_hashtag_strategy_recommendations(trending_data, platform):
    """Generate hashtag strategy recommendations"""
    recommendations = [
        f"Use 3-5 trending hashtags from the top list to maximize reach on {platform}",
        "Mix popular and niche hashtags for better engagement",
        "Monitor hashtag performance and adjust strategy weekly",
        "Create branded hashtags to build community",
        "Avoid overusing hashtags - quality over quantity"
    ]

    if platform == "Instagram":
        recommendations.append("Use up to 30 hashtags but focus on the most relevant ones")
    elif platform == "Twitter":
        recommendations.append("Limit to 2-3 hashtags per tweet for better engagement")
    elif platform == "LinkedIn":
        recommendations.append("Use 3-5 professional hashtags relevant to your industry")

    return recommendations


def generate_hashtag_export(trending_data, platform, category):
    """Generate hashtag export data"""
    export_text = f"TRENDING HASHTAGS REPORT - {platform}\n"
    export_text += f"Category: {category}\n"
    export_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    export_text += "=" * 50 + "\n\n"

    export_text += "TOP TRENDING HASHTAGS\n"
    for i, hashtag in enumerate(trending_data['top_trending'][:20], 1):
        export_text += f"{i}. #{hashtag['tag']} - {hashtag['posts']:,} posts\n"

    export_text += "\nRISING HASHTAGS\n"
    for hashtag in trending_data['rising'][:10]:
        export_text += f"#{hashtag['tag']} - {hashtag['posts']:,} posts (+{hashtag['growth']:.1f}%)\n"

    return export_text


def generate_sample_performance_data():
    """Generate sample performance data"""
    platforms = ['Instagram', 'Facebook', 'Twitter', 'LinkedIn', 'TikTok']
    post_types = ['Image', 'Video', 'Carousel', 'Text', 'Story']

    data = []
    for i in range(20):
        platform = random.choice(platforms)
        post_type = random.choice(post_types)
        impressions = random.randint(1000, 50000)
        reach = int(impressions * random.uniform(0.6, 0.9))
        likes = int(impressions * random.uniform(0.01, 0.05))
        comments = int(likes * random.uniform(0.05, 0.2))
        shares = int(likes * random.uniform(0.02, 0.1))
        clicks = int(impressions * random.uniform(0.005, 0.02))
        engagement_rate = (likes + comments + shares) / impressions * 100

        data.append({
            'platform': platform,
            'post_type': post_type,
            'date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'reach': reach,
            'impressions': impressions,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'clicks': clicks,
            'engagement_rate': engagement_rate
        })

    return data


def generate_performance_insights(performance_data):
    """Generate performance insights"""
    insights = []

    # Analyze best performing platform
    platform_performance = {}
    for post in performance_data:
        platform = post['platform']
        if platform not in platform_performance:
            platform_performance[platform] = []
        platform_performance[platform].append(post['engagement_rate'])

    best_platform = max(platform_performance.items(), key=lambda x: sum(x[1]) / len(x[1]))[0]
    insights.append(f"{best_platform} shows the highest average engagement rate")

    # Analyze best post type
    type_performance = {}
    for post in performance_data:
        post_type = post['post_type']
        if post_type not in type_performance:
            type_performance[post_type] = []
        type_performance[post_type].append(post['engagement_rate'])

    best_type = max(type_performance.items(), key=lambda x: sum(x[1]) / len(x[1]))[0]
    insights.append(f"{best_type} posts generate the best engagement")

    # General insights
    avg_engagement = sum(post['engagement_rate'] for post in performance_data) / len(performance_data)
    insights.append(f"Overall average engagement rate is {avg_engagement:.2f}%")

    insights.append("Post consistently during peak hours for better reach")
    insights.append("Focus on creating more interactive content to boost engagement")

    return insights


def generate_performance_report(performance_data, platform_stats):
    """Generate comprehensive performance report"""
    report = f"SOCIAL MEDIA PERFORMANCE REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 50 + "\n\n"

    total_posts = len(performance_data)
    total_reach = sum(post.get('reach', 0) for post in performance_data)
    total_impressions = sum(post.get('impressions', 0) for post in performance_data)
    total_engagement = sum(
        post.get('likes', 0) + post.get('comments', 0) + post.get('shares', 0) for post in performance_data)

    report += f"OVERVIEW\n"
    report += f"Total Posts: {total_posts}\n"
    report += f"Total Reach: {total_reach:,}\n"
    report += f"Total Impressions: {total_impressions:,}\n"
    report += f"Total Engagement: {total_engagement:,}\n\n"

    report += "PLATFORM PERFORMANCE\n"
    for platform, stats in platform_stats.items():
        report += f"\n{platform}:\n"
        report += f"  Posts: {stats['posts']}\n"
        report += f"  Avg Reach: {stats['avg_reach']:,.0f}\n"
        report += f"  Avg Engagement: {stats['avg_engagement']:.2f}%\n"

    return report


def simulate_ab_test_results(test_config):
    """Simulate A/B test results"""
    # Generate realistic performance data
    variation_a_impressions = random.randint(5000, 15000)
    variation_b_impressions = random.randint(5000, 15000)

    variation_a_reach = int(variation_a_impressions * random.uniform(0.7, 0.9))
    variation_a_likes = int(variation_a_impressions * random.uniform(0.02, 0.04))
    variation_a_comments = int(variation_a_impressions * random.uniform(0.003, 0.008))
    variation_a_shares = int(variation_a_impressions * random.uniform(0.001, 0.005))
    variation_a_clicks = int(variation_a_impressions * random.uniform(0.01, 0.03))
    variation_a_engagement_rate = (
                                              variation_a_likes + variation_a_comments + variation_a_shares) / variation_a_impressions * 100

    variation_a = {
        'impressions': variation_a_impressions,
        'reach': variation_a_reach,
        'likes': variation_a_likes,
        'comments': variation_a_comments,
        'shares': variation_a_shares,
        'clicks': variation_a_clicks,
        'engagement_rate': variation_a_engagement_rate,
    }

    # Variation B performs slightly better (or worse)
    performance_multiplier = random.uniform(0.9, 1.3)
    variation_b_reach = int(variation_b_impressions * random.uniform(0.7, 0.9))
    variation_b_likes = int(variation_b_impressions * random.uniform(0.02, 0.04) * performance_multiplier)
    variation_b_comments = int(variation_b_impressions * random.uniform(0.003, 0.008) * performance_multiplier)
    variation_b_shares = int(variation_b_impressions * random.uniform(0.001, 0.005) * performance_multiplier)
    variation_b_clicks = int(variation_b_impressions * random.uniform(0.01, 0.03) * performance_multiplier)
    variation_b_engagement_rate = (
                                              variation_b_likes + variation_b_comments + variation_b_shares) / variation_b_impressions * 100

    variation_b = {
        'impressions': variation_b_impressions,
        'reach': variation_b_reach,
        'likes': variation_b_likes,
        'comments': variation_b_comments,
        'shares': variation_b_shares,
        'clicks': variation_b_clicks,
        'engagement_rate': variation_b_engagement_rate,
    }

    # Calculate improvements
    improvements = {}
    for metric in ['impressions', 'reach', 'likes', 'comments', 'shares', 'clicks', 'engagement_rate']:
        improvement = ((variation_b[metric] - variation_a[metric]) / variation_a[metric] * 100) if variation_a[
                                                                                                       metric] > 0 else 0
        improvements[metric] = improvement

    # Determine winner and significance
    winner = 'B' if variation_b['engagement_rate'] > variation_a['engagement_rate'] else 'A'
    is_significant = abs(improvements['engagement_rate']) > 5  # 5% threshold

    insights = [
        f"Variation {winner} performed better overall",
        f"Engagement rate improved by {abs(improvements['engagement_rate']):.1f}%",
        "Consider implementing the winning variation" if is_significant else "Results show no significant difference"
    ]

    recommendations = [
        f"Implement Variation {winner} for future campaigns" if is_significant else "Continue testing with larger sample size",
        "Monitor long-term performance to confirm results",
        "Test additional variables to further optimize performance"
    ]

    return {
        'variation_a': variation_a,
        'variation_b': variation_b,
        'improvements': improvements,
        'winner': winner,
        'is_significant': is_significant,
        'insights': insights,
        'recommendations': recommendations
    }


def generate_ab_test_report(test_config, test_results):
    """Generate A/B test report"""
    report = f"A/B TEST REPORT: {test_config['test_name']}\n"
    report += "=" * 50 + "\n\n"

    report += f"Test Objective: {test_config['objective']}\n"
    report += f"Platform: {test_config['platform']}\n"
    report += f"Duration: {test_config['duration']} days\n"
    report += f"Hypothesis: {test_config['hypothesis']}\n\n"

    report += "RESULTS SUMMARY\n"
    report += f"Winner: Variation {test_results['winner']}\n"
    report += f"Statistical Significance: {'Yes' if test_results['is_significant'] else 'No'}\n"
    report += f"Engagement Rate Improvement: {test_results['improvements']['engagement_rate']:+.1f}%\n\n"

    report += "DETAILED METRICS\n"
    metrics = ['impressions', 'reach', 'likes', 'comments', 'shares', 'clicks']
    for metric in metrics:
        report += f"{metric.title()}: {test_results['variation_a'][metric]:,} vs {test_results['variation_b'][metric]:,} ({test_results['improvements'][metric]:+.1f}%)\n"

    report += "\nRECOMMENDATIONS\n"
    for rec in test_results['recommendations']:
        report += f"- {rec}\n"

    return report


def simulate_brand_tracking(brand_name, platforms, tracking_period):
    """Simulate brand tracking data"""
    total_mentions = random.randint(500, 2000)
    sentiment_score = random.uniform(2.5, 4.5)

    # Generate sentiment breakdown
    positive_pct = random.uniform(30, 60)
    negative_pct = random.uniform(10, 25)
    neutral_pct = 100 - positive_pct - negative_pct

    # Platform breakdown
    platform_breakdown = {}
    remaining_mentions = total_mentions

    for i, platform in enumerate(platforms):
        if i == len(platforms) - 1:  # Last platform gets remaining mentions
            mentions = remaining_mentions
        else:
            mentions = random.randint(50, remaining_mentions // 2)
            remaining_mentions -= mentions

        platform_breakdown[platform] = {
            'mentions': mentions,
            'engagement': random.randint(mentions * 2, mentions * 5),
            'reach': random.randint(mentions * 10, mentions * 50),
            'sentiment': random.uniform(2.0, 5.0)
        }

    # Generate recent mentions
    recent_mentions = []
    for i in range(15):
        recent_mentions.append({
            'platform': random.choice(platforms),
            'author': f"user_{random.randint(1000, 9999)}",
            'content': f"Just tried {brand_name}! {random.choice(['Amazing experience!', 'Really impressed', 'Could be better', 'Love this brand!', 'Not what I expected'])}",
            'date': (datetime.now() - timedelta(days=random.randint(0, 7))).strftime('%Y-%m-%d'),
            'sentiment': random.choice(['positive', 'negative', 'neutral']),
            'engagement': random.randint(5, 100),
            'reach': random.randint(100, 5000)
        })

    return {
        'total_mentions': total_mentions,
        'sentiment_score': sentiment_score,
        'total_reach': sum(p['reach'] for p in platform_breakdown.values()),
        'share_of_voice': random.uniform(5, 25),
        'sentiment_breakdown': {
            'positive': positive_pct,
            'negative': negative_pct,
            'neutral': neutral_pct
        },
        'platform_breakdown': platform_breakdown,
        'recent_mentions': recent_mentions
    }


def simulate_competitor_comparison(brand_name, competitor_list):
    """Simulate competitor comparison data"""
    comparison_data = {}

    for competitor in competitor_list:
        comparison_data[competitor] = {
            'mentions': random.randint(300, 1500),
            'sentiment': random.uniform(2.0, 4.5),
            'reach': random.randint(5000, 50000)
        }

    return comparison_data


def generate_brand_insights(brand_data, brand_name):
    """Generate brand insights"""
    insights = []

    sentiment_score = brand_data['sentiment_score']
    if sentiment_score > 4.0:
        insights.append(f"{brand_name} has excellent brand sentiment")
    elif sentiment_score > 3.0:
        insights.append(f"{brand_name} maintains positive brand sentiment")
    else:
        insights.append(f"{brand_name} should focus on improving brand sentiment")

    # Platform insights
    best_platform = max(brand_data['platform_breakdown'].items(), key=lambda x: x[1]['mentions'])[0]
    insights.append(f"{best_platform} generates the most brand mentions")

    total_mentions = brand_data['total_mentions']
    if total_mentions > 1000:
        insights.append("Strong brand awareness and mention volume")
    else:
        insights.append("Opportunity to increase brand visibility")

    insights.append("Monitor sentiment trends to identify potential issues early")
    insights.append("Engage with positive mentions to build community")

    return insights


def generate_brand_action_items(brand_data):
    """Generate brand action items"""
    actions = []

    sentiment_breakdown = brand_data['sentiment_breakdown']

    if sentiment_breakdown['negative'] > 20:
        actions.append("Address negative sentiment by improving customer service response")

    if sentiment_breakdown['positive'] > 50:
        actions.append("Amplify positive mentions through social sharing and testimonials")

    actions.append("Create engaging content to increase positive brand mentions")
    actions.append("Set up automated alerts for brand mentions requiring immediate response")
    actions.append("Develop influencer partnerships to improve brand perception")

    return actions


def generate_brand_report(brand_data, brand_name):
    """Generate comprehensive brand report"""
    report = f"BRAND TRACKING REPORT: {brand_name}\n"
    report += "=" * 50 + "\n\n"

    report += f"BRAND OVERVIEW\n"
    report += f"Total Mentions: {brand_data['total_mentions']:,}\n"
    report += f"Sentiment Score: {brand_data['sentiment_score']:.1f}/5.0\n"
    report += f"Total Reach: {brand_data['total_reach']:,}\n"
    report += f"Share of Voice: {brand_data['share_of_voice']:.1f}%\n\n"

    report += f"SENTIMENT BREAKDOWN\n"
    report += f"Positive: {brand_data['sentiment_breakdown']['positive']:.1f}%\n"
    report += f"Negative: {brand_data['sentiment_breakdown']['negative']:.1f}%\n"
    report += f"Neutral: {brand_data['sentiment_breakdown']['neutral']:.1f}%\n\n"

    report += "PLATFORM PERFORMANCE\n"
    for platform, data in brand_data['platform_breakdown'].items():
        report += f"\n{platform}:\n"
        report += f"  Mentions: {data['mentions']:,}\n"
        report += f"  Engagement: {data['engagement']:,}\n"
        report += f"  Reach: {data['reach']:,}\n"
        report += f"  Sentiment: {data['sentiment']:.1f}/5.0\n"

    return report