import streamlit as st
import os
from utils.common import init_session_state, display_tool_grid, search_tools
from tools import (
    ai_tools,text_tools,audio_video_tools, image_tools, security_tools, css_tools, coding_tools,
     file_tools,  social_media_tools,
    color_tools, web_dev_tools, seo_marketing_tools, data_tools,
    science_math_tools
)

# Configure page
st.set_page_config(
    page_title="Ultimate All-in-One Digital Toolkit",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add beautiful but simpler CSS styling
st.markdown("""
<style>
# /* Dark animated background */
# .stApp {
#     background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483, #2d1b69, #0f0f23);
#     background-size: 400% 400%;
#     animation: gradientShift 15s ease infinite;
# }

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glass morphism content */
.main .block-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Sidebar styling */
.css-1d391kg {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0 20px 20px 0;
    box-shadow: 2px 0 15px rgba(0, 0, 0, 0.3);
}

/* Beautiful titles */
h1 {
    background: linear-gradient(45deg, #a8c8ff 0%, #c4a7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGlow 2s ease-in-out infinite alternate;
    text-align: center;
    font-size: 3rem !important;
    margin-bottom: 1rem;
}

@keyframes titleGlow {
    from { text-shadow: 0 0 20px rgba(168, 200, 255, 0.5); }
    to { text-shadow: 0 0 30px rgba(196, 167, 255, 0.8); }
}

/* Enhanced buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    color: white;
    padding: 0.8rem 1.8rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    background: linear-gradient(135deg, #764ba2 0%, #a8c8ff 100%);
}

/* Floating particles */
.particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
}

.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    animation: particleFloat 15s infinite linear;
}

@keyframes particleFloat {
    0% {
        transform: translateY(100vh) rotate(0deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(-100vh) rotate(360deg);
        opacity: 0;
    }
}

/* Responsive design */
@media (max-width: 768px) {
    .main .block-container {
        margin: 0.5rem;
        padding: 1rem;
    }
    h1 {
        font-size: 2rem !important;
    }
}
</style>

<!-- Floating particles -->
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Tool categories configuration
TOOL_CATEGORIES = {
    "AI Tools": {
        "icon": "🤖",
        "description": "Artificial intelligence and machine learning tools",
        "module": ai_tools,
        "color": "#F7DC6F"
    },
    "Audio/Video Tools": {
        "icon": "🎵",
        "description": "Media processing and editing tools",
        "module": audio_video_tools,
        "color": "#DDA0DD"
    },
    "Color Tools": {
        "icon": "🌈",
        "description": "Color palettes, converters, and design tools",
        "module": color_tools,
        "color": "#85C1E9"
    },
    "Coding Tools": {
        "icon": "💻",
        "description": "Programming utilities and development tools",
        "module": coding_tools,
        "color": "#FFEAA7"
    },
    "CSS Tools": {
        "icon": "🎨",
        "description": "CSS generators, validators, and design tools",
        "module": css_tools,
        "color": "#96CEB4"
    },
    "Data Tools": {
        "icon": "📊",
        "description": "Data analysis and visualization tools",
        "module": data_tools,
        "color": "#F1948A"
    },
    "File Tools": {
        "icon": "📁",
        "description": "File management and conversion utilities",
        "module": file_tools,
        "color": "#98D8C8"
    },
    "Image Tools": {
        "icon": "🖼️",
        "description": "Image editing, conversion, and analysis tools",
        "module": image_tools,
        "color": "#4ECDC4"
    },
    "Science/Math Tools": {
        "icon": "🧮",
        "description": "Scientific calculators and mathematical tools",
        "module": science_math_tools,
        "color": "#AED6F1"
    },
    "Security/Privacy Tools": {
        "icon": "🔒",
        "description": "Cybersecurity, privacy, and encryption tools",
        "module": security_tools,
        "color": "#45B7D1"
    },
    "SEO/Marketing Tools": {
        "icon": "📈",
        "description": "Search optimization and marketing analytics",
        "module": seo_marketing_tools,
        "color": "#82E0AA"
    },
    "Social Media Tools": {
        "icon": "📱",
        "description": "Social media management and analytics",
        "module": social_media_tools,
        "color": "#BB8FCE"
    },
    "Text Tools": {
        "icon": "📝",
        "description": "Text processing, analysis, and manipulation tools",
        "module": text_tools,
        "color": "#FF6B6B"
    },
    "Web Developer Tools": {
        "icon": "🌐",
        "description": "Web development and testing utilities",
        "module": web_dev_tools,
        "color": "#F8C471"
    }
}


def display_connect_page():
    """Display the Connect page with beautiful styling"""
    # Connect page header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>📞 Connect With Us</h1>
        <div style="background: linear-gradient(45deg, #a8c8ff, #c4a7ff); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text; font-size: 1.2rem; font-weight: 500;">
            ✨ Get in touch, share feedback, or connect with the community ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Introduction section
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(168, 200, 255, 0.2), rgba(196, 167, 255, 0.2)); 
                color: white; padding: 1.5rem; border-radius: 15px; 
                margin: 1rem 0; text-align: center;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
        <h3 style="margin: 0; color: white;">👋 Hi, I'm the creator of this toolkit!</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
            Welcome to my Ultimate Digital Toolkit! Whether you have questions, feedback, feature requests, 
            or just want to connect, I'd love to hear from you.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Contact sections
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💬 Feedback & Support")
        st.markdown("""
        **Found a bug?** Let me know and help me improve the toolkit!  
        **Have a suggestion?** I'm always looking for ways to make it better.  
        **Need help?** I'm here to support you with any of the tools.
        """)

        # Feedback form
        st.subheader("📝 Send Feedback")

        feedback_type = st.selectbox("Feedback Type", [
            "Bug Report", "Feature Request", "General Feedback", "Support Request", "Compliment"
        ])

        name = st.text_input("Your Name (optional)", placeholder="John Doe")
        email = st.text_input("Your Email (optional)", placeholder="john@example.com")

        subject = st.text_input("Subject", placeholder="Brief description of your message")
        message = st.text_area("Message", height=150,
                               placeholder="Tell us more about your feedback, issue, or suggestion...")

        if st.button("📤 Send Feedback", type="primary"):
            if message and subject:
                # Store feedback (in a real app, you'd send this to a backend)
                st.success("✅ Thank you for your feedback! I'll review it and get back to you if needed.")
                st.balloons()

                # Display what was submitted (for demo purposes)
                with st.expander("📋 Feedback Submitted"):
                    st.write(f"**Type:** {feedback_type}")
                    if name: st.write(f"**Name:** {name}")
                    if email: st.write(f"**Email:** {email}")
                    st.write(f"**Subject:** {subject}")
                    st.write(f"**Message:** {message}")
            else:
                st.error("Please fill in both subject and message fields.")

    with col2:
        st.markdown("### 🌐 Connect With Me")
        st.markdown("""
        **Follow my updates** and join the community!  
        **Share your creations** made with the toolkit.  
        **Stay informed** about new features and releases.
        """)

        # Social media / connection links
        st.subheader("🔗 Find Me Online")

        # Social and contact links
        social_links = [
            ("🐙 GitHub", "https://github.com/username", "View my projects and code"),
            ("💼 LinkedIn", "https://linkedin.com/in/username", "Connect professionally"),
            ("🐦 Twitter", "https://twitter.com/username", "Follow me for updates"),
            ("📧 Email", "mailto:contact@example.com", "Send me a direct email"),
            ("📚 Portfolio", "https://portfolio.dev", "Check out my other projects")
        ]

        for icon_name, link, description in social_links:
            st.markdown(f"**{icon_name}** [{description}]({link})")

        # Newsletter signup
        st.subheader("📰 Newsletter")
        newsletter_email = st.text_input("Subscribe for updates:", placeholder="your@email.com")
        if st.button("📮 Subscribe"):
            if newsletter_email and "@" in newsletter_email:
                st.success("✅ Subscribed! You'll receive updates about new tools and features.")
            else:
                st.error("Please enter a valid email address.")

    st.markdown("---")

    # FAQ Section
    st.subheader("❓ Frequently Asked Questions")

    faqs = [
        {
            "question": "Is this toolkit free to use?",
            "answer": "Yes! Most tools are completely free. Some AI-powered features require API keys from providers like Google (Gemini) or OpenAI."
        },
        {
            "question": "How do I report a bug or request a feature?",
            "answer": "Use the feedback form above or contact me through any of the social channels. I review all submissions personally!"
        },
        {
            "question": "Can I contribute to the project?",
            "answer": "Absolutely! Check out my GitHub repository to see how you can contribute code, documentation, or ideas."
        },
        {
            "question": "Are my files and data secure?",
            "answer": "Yes! All processing happens locally in your browser or on secure servers. I don't store your personal files or data."
        },
        {
            "question": "How often are new tools added?",
            "answer": "I'm constantly working on new tools and improvements. Follow my updates to stay informed about releases!"
        }
    ]

    for i, faq in enumerate(faqs):
        with st.expander(f"**{faq['question']}**"):
            st.write(faq['answer'])

    # Statistics section
    st.markdown("---")
    st.subheader("📊 Toolkit Stats")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🛠️ Total Tools", "500+")
    with col2:
        st.metric("📈 Tools Used Daily", "10,000+")


def main():
    # Beautiful header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🛠️ Ultimate All-in-One Digital Toolkit</h1>
        <div style="background: linear-gradient(45deg, #a8c8ff, #c4a7ff); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text; font-size: 1.2rem; font-weight: 500;">
            ✨ 500+ Professional Tools Across 14 Specialized Categories ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown(
            """
            <h1 style="
                background: linear-gradient(90deg, #ff7e5f, #feb47b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 50 px;
                font-weight: bold;
            ">
                वत्सल वार्ष्णेय
            </h1>
            """,
            unsafe_allow_html=True
        )
        st.header("🎯 Navigation")

        # Category selection
        selected_category = st.selectbox(
            "Select Category",
            ["Dashboard", "Connect"] + list(TOOL_CATEGORIES.keys()),
            index=0 if 'selected_category' not in st.session_state else
            (["Dashboard", "Connect"] + list(TOOL_CATEGORIES.keys())).index(
                st.session_state.selected_category) if st.session_state.selected_category in (
                        ["Dashboard", "Connect"] + list(TOOL_CATEGORIES.keys())) else 0
        )

        if selected_category != "Dashboard":
            st.session_state.selected_category = selected_category

        # Statistics
        st.markdown("---")
        st.subheader("📊 Platform Stats")
        st.metric("Total Categories", len(TOOL_CATEGORIES))
        st.metric("Total Tools", "500+")

    # Main content area
    if selected_category == "Connect":
        display_connect_page()
    elif selected_category == "Dashboard" or 'selected_category' not in st.session_state:
        # Dashboard view
        st.markdown(
            """
            <h1 style="
                background: linear-gradient(90deg, #ff7e5f, #feb47b);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 50 px;
                font-weight: bold;
            ">
                वत्सल वार्ष्णेय
            </h1>
            """,
            unsafe_allow_html=True
        )
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(168, 200, 255, 0.2), rgba(196, 167, 255, 0.2)); 
                    color: white; padding: 1.5rem; border-radius: 15px; 
                    margin: 1rem 0; text-align: center;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
            <h3 style="margin: 0; color: white;">✨ Welcome to the Ultimate Digital Toolkit! ✨</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Select a category from the sidebar or click on any tool category below to get started.</p>
        </div>
        """, unsafe_allow_html=True)

        # Tool category grid
        display_tool_grid(TOOL_CATEGORIES)

        # Feature highlights
        st.markdown("### ✨ Platform Features")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **🔧 500+ Tools**
            - Text processing & analysis
            - Image editing & conversion
            - Security & privacy tools
            - CSS & web development
            - AI & machine learning
            """)

        with col2:
            st.markdown("""
            **🔄 Cross-Tool Integration**
            - Unified file management
            - Batch processing workflows
            - Universal search
            - Export/import capabilities
            - Template system
            """)

        with col3:
            st.markdown("""
            **📈 Advanced Features**
            - Real-time processing
            - Progress tracking
            - History management
            - Favorites system
            - Custom workflows
            """)

    else:
        # Category-specific tool view
        category_info = TOOL_CATEGORIES[st.session_state.selected_category]

        # Category header
        st.header(f"{category_info['icon']} {st.session_state.selected_category}")
        st.markdown(f"*{category_info['description']}*")

        # Load and display category tools
        try:
            category_info['module'].display_tools()
        except Exception as e:
            st.error(f"Error loading {st.session_state.selected_category}: {str(e)}")
            st.info("Please try refreshing the page or selecting a different category.")


if __name__ == "__main__":
    main()