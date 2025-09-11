import streamlit as st
import os
from utils.common import init_session_state, display_tool_grid, search_tools
from tools import (
    text_tools, image_tools, security_tools, css_tools, coding_tools,
    audio_video_tools, file_tools, ai_tools, social_media_tools,
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

# Add ultra-premium CSS styling
st.markdown("""
<style>
/* Ultra Premium Dark Background with Multiple Layers */
.stApp {
    background: 
        radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%),
        linear-gradient(-45deg, #0a0a0f, #1a1a2e, #16213e, #0f3460, #533483, #2d1b69, #0f0f23);
    background-size: 400% 400%, 400% 400%, 400% 400%, 400% 400%;
    animation: ultraGradientShift 20s ease infinite;
    position: relative;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,255,255,0.01) 2px, rgba(255,255,255,0.01) 4px);
    pointer-events: none;
    z-index: 1;
}

@keyframes ultraGradientShift {
    0% { background-position: 0% 50%, 0% 50%, 0% 50%, 0% 50%; }
    25% { background-position: 100% 50%, 25% 75%, 75% 25%, 25% 50%; }
    50% { background-position: 50% 100%, 100% 50%, 50% 75%, 100% 50%; }
    75% { background-position: 75% 25%, 75% 25%, 25% 50%, 75% 50%; }
    100% { background-position: 0% 50%, 0% 50%, 0% 50%, 0% 50%; }
}

/* Ultra Premium Glass Morphism Container */
.main .block-container {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
    backdrop-filter: blur(20px) saturate(200%);
    -webkit-backdrop-filter: blur(20px) saturate(200%);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 25px;
    padding: 2.5rem;
    margin: 1rem;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        0 1px 2px rgba(0, 0, 0, 0.1);
    animation: premiumFadeInUp 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative;
    z-index: 10;
    transform-style: preserve-3d;
    transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.main .block-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, rgba(120, 119, 198, 0.1), rgba(255, 119, 198, 0.1));
    border-radius: 25px;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: -1;
}

.main .block-container:hover::before {
    opacity: 1;
}

.main .block-container:hover {
    transform: translateY(-5px) rotateX(2deg);
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.3),
        0 1px 2px rgba(0, 0, 0, 0.2);
}

@keyframes premiumFadeInUp {
    0% {
        opacity: 0;
        transform: translateY(60px) rotateX(10deg) scale(0.95);
        filter: blur(10px);
    }
    50% {
        opacity: 0.8;
        transform: translateY(20px) rotateX(5deg) scale(0.98);
        filter: blur(3px);
    }
    100% {
        opacity: 1;
        transform: translateY(0) rotateX(0deg) scale(1);
        filter: blur(0px);
    }
}

/* Ultra Premium Sidebar */
.css-1d391kg {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.06) 100%);
    backdrop-filter: blur(25px) saturate(200%);
    -webkit-backdrop-filter: blur(25px) saturate(200%);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-left: none;
    border-radius: 0 25px 25px 0;
    box-shadow: 
        5px 0 30px rgba(0, 0, 0, 0.4),
        inset -1px 0 0 rgba(255, 255, 255, 0.1);
    position: relative;
    z-index: 100;
}

.css-1d391kg::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(120, 119, 198, 0.1), rgba(255, 119, 198, 0.05));
    border-radius: 0 25px 25px 0;
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: -1;
}

.css-1d391kg:hover::before {
    opacity: 1;
}

/* Ultra Premium Title Styling */
h1 {
    background: linear-gradient(45deg, #a8c8ff 0%, #c4a7ff 50%, #ff9a9e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% 200%;
    animation: ultraTitlePulse 3s ease-in-out infinite alternate, shimmer 4s ease-in-out infinite;
    text-align: center;
    font-size: 3.5rem !important;
    font-weight: 800;
    margin-bottom: 1.5rem;
    text-shadow: 
        0 0 20px rgba(168, 200, 255, 0.5),
        0 0 40px rgba(196, 167, 255, 0.3),
        0 0 60px rgba(255, 154, 158, 0.2);
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
    position: relative;
    z-index: 10;
}

@keyframes ultraTitlePulse {
    0% { 
        text-shadow: 
            0 0 20px rgba(168, 200, 255, 0.5),
            0 0 40px rgba(196, 167, 255, 0.3),
            0 0 60px rgba(255, 154, 158, 0.2);
        transform: scale(1);
    }
    50% {
        text-shadow: 
            0 0 30px rgba(168, 200, 255, 0.8),
            0 0 60px rgba(196, 167, 255, 0.6),
            0 0 90px rgba(255, 154, 158, 0.4);
        transform: scale(1.02);
    }
    100% { 
        text-shadow: 
            0 0 25px rgba(168, 200, 255, 0.6),
            0 0 50px rgba(196, 167, 255, 0.4),
            0 0 75px rgba(255, 154, 158, 0.3);
        transform: scale(1);
    }
}

@keyframes shimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Ultra Premium Button Styling */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a8c8ff 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    color: white;
    padding: 0.8rem 1.8rem;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    transform: translateY(0) translateZ(0);
    box-shadow: 
        0 4px 15px rgba(102, 126, 234, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        0 1px 2px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.6s ease;
}

.stButton > button:hover {
    transform: translateY(-5px) scale(1.05) rotateX(5deg);
    box-shadow: 
        0 15px 35px rgba(102, 126, 234, 0.6),
        inset 0 1px 0 rgba(255, 255, 255, 0.3),
        0 5px 15px rgba(0, 0, 0, 0.3);
    background: linear-gradient(135deg, #764ba2 0%, #a8c8ff 50%, #667eea 100%);
    border-color: rgba(255, 255, 255, 0.4);
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:active {
    transform: translateY(-2px) scale(0.98);
    transition: all 0.1s ease;
}

/* Tool category cards */
.element-container {
    animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Ultra Premium 3D Metric Cards */
.metric-container {
    background: linear-gradient(135deg, 
        rgba(255, 255, 255, 0.15) 0%, 
        rgba(255, 255, 255, 0.05) 50%, 
        rgba(255, 255, 255, 0.1) 100%);
    backdrop-filter: blur(20px) saturate(200%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 0.8rem 0;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        0 1px 2px rgba(0, 0, 0, 0.1);
    transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    transform-style: preserve-3d;
    position: relative;
    overflow: hidden;
}

.metric-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, 
        rgba(168, 200, 255, 0.1), 
        rgba(196, 167, 255, 0.1), 
        rgba(255, 154, 158, 0.1));
    border-radius: 20px;
    opacity: 0;
    transition: opacity 0.4s ease;
    z-index: -1;
}

.metric-container::after {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, 
        #a8c8ff, #c4a7ff, #ff9a9e, #a8c8ff);
    border-radius: 22px;
    opacity: 0;
    transition: opacity 0.4s ease;
    z-index: -2;
    animation: neonBorder 3s ease-in-out infinite;
}

.metric-container:hover {
    transform: translateY(-10px) rotateX(10deg) rotateY(5deg) scale(1.05);
    box-shadow: 
        0 25px 50px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3),
        0 5px 15px rgba(168, 200, 255, 0.3);
}

.metric-container:hover::before {
    opacity: 1;
}

.metric-container:hover::after {
    opacity: 0.6;
}

@keyframes neonBorder {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Premium Search Box Styling */
.stTextInput > div > div > input {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    padding: 1rem 1.5rem;
    color: white;
    font-size: 0.95rem;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.stTextInput > div > div > input:focus {
    border: 1px solid rgba(168, 200, 255, 0.6);
    box-shadow: 
        0 0 30px rgba(168, 200, 255, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
    transform: translateY(-2px);
}

/* Premium Selectbox Styling */
.stSelectbox > div > div {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.stSelectbox > div > div:hover {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
    border-color: rgba(168, 200, 255, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

/* Ultra Premium Info Boxes */
.stInfo {
    background: linear-gradient(135deg, 
        rgba(102, 126, 234, 0.2) 0%, 
        rgba(118, 75, 162, 0.2) 50%, 
        rgba(168, 200, 255, 0.2) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(168, 200, 255, 0.3);
    border-radius: 20px;
    color: white;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    animation: premiumGlow 3s ease-in-out infinite alternate;
    box-shadow: 
        0 8px 32px rgba(102, 126, 234, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.stInfo::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    animation: infoShimmer 4s ease-in-out infinite;
    transform: rotate(45deg);
}

@keyframes premiumGlow {
    0% { 
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 20px rgba(168, 200, 255, 0.4);
    }
    50% {
        box-shadow: 
            0 12px 40px rgba(102, 126, 234, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3),
            0 0 40px rgba(168, 200, 255, 0.6);
        transform: translateY(-2px);
    }
    100% { 
        box-shadow: 
            0 8px 32px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 20px rgba(168, 200, 255, 0.4);
    }
}

@keyframes infoShimmer {
    0% { transform: translateX(-100%) rotate(45deg); }
    50% { transform: translateX(-50%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

/* Ultra Premium Success Messages */
.stSuccess {
    background: linear-gradient(135deg, 
        rgba(76, 175, 80, 0.2) 0%, 
        rgba(69, 160, 73, 0.2) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(76, 175, 80, 0.4);
    border-radius: 20px;
    color: #a8ffa8;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    animation: successPulse 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 
        0 8px 32px rgba(76, 175, 80, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.stSuccess::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    animation: successShimmer 1s ease-out;
}

@keyframes successShimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

@keyframes successPulse {
    0% { 
        transform: scale(0.8) rotateY(-10deg); 
        opacity: 0;
        filter: blur(5px);
    }
    50% {
        transform: scale(1.02) rotateY(0deg);
        opacity: 0.8;
        filter: blur(2px);
    }
    100% { 
        transform: scale(1) rotateY(0deg); 
        opacity: 1;
        filter: blur(0px);
    }
}

/* Floating animations for decorative elements */
.floating {
    animation: floating 3s ease-in-out infinite;
}

@keyframes floating {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

/* Responsive design improvements */
@media (max-width: 768px) {
    .main .block-container {
        margin: 0.5rem;
        padding: 1rem;
    }

    h1 {
        font-size: 2rem !important;
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, #764ba2, #667eea);
}

/* Advanced Multi-Layer Particle System */
.particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 5;
    overflow: hidden;
}

.particle {
    position: absolute;
    border-radius: 50%;
    animation: particleFloat 20s infinite linear;
    filter: blur(0.5px);
}

.particle:nth-child(odd) {
    width: 3px;
    height: 3px;
    background: radial-gradient(circle, rgba(168, 200, 255, 0.8) 0%, rgba(168, 200, 255, 0.2) 70%, transparent 100%);
    box-shadow: 
        0 0 10px rgba(168, 200, 255, 0.6),
        0 0 20px rgba(168, 200, 255, 0.3),
        0 0 30px rgba(168, 200, 255, 0.1);
    animation-duration: 18s;
}

.particle:nth-child(even) {
    width: 5px;
    height: 5px;
    background: radial-gradient(circle, rgba(196, 167, 255, 0.7) 0%, rgba(196, 167, 255, 0.2) 70%, transparent 100%);
    box-shadow: 
        0 0 8px rgba(196, 167, 255, 0.5),
        0 0 16px rgba(196, 167, 255, 0.3),
        0 0 24px rgba(196, 167, 255, 0.1);
    animation-duration: 22s;
}

.particle:nth-child(3n) {
    width: 2px;
    height: 2px;
    background: radial-gradient(circle, rgba(255, 154, 158, 0.9) 0%, rgba(255, 154, 158, 0.3) 70%, transparent 100%);
    box-shadow: 
        0 0 6px rgba(255, 154, 158, 0.7),
        0 0 12px rgba(255, 154, 158, 0.4),
        0 0 18px rgba(255, 154, 158, 0.2);
    animation-duration: 16s;
}

@keyframes particleFloat {
    0% {
        transform: translateY(100vh) translateX(0px) rotate(0deg) scale(0);
        opacity: 0;
    }
    5% {
        opacity: 1;
        transform: translateY(95vh) translateX(0px) rotate(18deg) scale(1);
    }
    25% {
        transform: translateY(75vh) translateX(20px) rotate(90deg) scale(1.2);
        opacity: 0.8;
    }
    50% {
        transform: translateY(50vh) translateX(-10px) rotate(180deg) scale(1);
        opacity: 1;
    }
    75% {
        transform: translateY(25vh) translateX(15px) rotate(270deg) scale(0.8);
        opacity: 0.7;
    }
    95% {
        opacity: 0.3;
        transform: translateY(5vh) translateX(-5px) rotate(342deg) scale(0.5);
    }
    100% {
        transform: translateY(-10vh) translateX(0px) rotate(360deg) scale(0);
        opacity: 0;
    }
}

/* Enhanced hover effects */
.stButton > button:active {
    transform: translateY(-1px) scale(0.98);
    transition: all 0.1s ease;
}

/* Tool grid enhancements */
.element-container:nth-child(odd) {
    animation-delay: 0.1s;
}

.element-container:nth-child(even) {
    animation-delay: 0.2s;
}

/* Enhanced glow effect for interactive elements */
.interactive-glow:hover {
    box-shadow: 0 0 30px rgba(102, 126, 234, 0.6);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}

/* Typing animation for text */
.typing-animation {
    animation: typing 4s steps(40, end), blink-caret 0.75s step-end infinite;
    white-space: nowrap;
    overflow: hidden;
    border-right: 3px solid rgba(102, 126, 234, 0.75);
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes blink-caret {
    from, to { border-color: transparent; }
    50% { border-color: rgba(102, 126, 234, 0.75); }
}
</style>

<!-- Ultra Premium Multi-Layer Floating Effects -->
<div class="particles">
    <!-- Blue particles -->
    <div class="particle" style="left: 5%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 15%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 25%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 35%; animation-delay: 9s;"></div>
    <div class="particle" style="left: 45%; animation-delay: 12s;"></div>
    <div class="particle" style="left: 55%; animation-delay: 15s;"></div>
    <div class="particle" style="left: 65%; animation-delay: 18s;"></div>
    <div class="particle" style="left: 75%; animation-delay: 21s;"></div>
    <div class="particle" style="left: 85%; animation-delay: 24s;"></div>
    <div class="particle" style="left: 95%; animation-delay: 27s;"></div>

    <!-- Purple particles -->
    <div class="particle" style="left: 8%; animation-delay: 1.5s;"></div>
    <div class="particle" style="left: 18%; animation-delay: 4.5s;"></div>
    <div class="particle" style="left: 28%; animation-delay: 7.5s;"></div>
    <div class="particle" style="left: 38%; animation-delay: 10.5s;"></div>
    <div class="particle" style="left: 48%; animation-delay: 13.5s;"></div>
    <div class="particle" style="left: 58%; animation-delay: 16.5s;"></div>
    <div class="particle" style="left: 68%; animation-delay: 19.5s;"></div>
    <div class="particle" style="left: 78%; animation-delay: 22.5s;"></div>
    <div class="particle" style="left: 88%; animation-delay: 25.5s;"></div>

    <!-- Pink particles -->
    <div class="particle" style="left: 12%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 22%; animation-delay: 5s;"></div>
    <div class="particle" style="left: 32%; animation-delay: 8s;"></div>
    <div class="particle" style="left: 42%; animation-delay: 11s;"></div>
    <div class="particle" style="left: 52%; animation-delay: 14s;"></div>
    <div class="particle" style="left: 62%; animation-delay: 17s;"></div>
    <div class="particle" style="left: 72%; animation-delay: 20s;"></div>
    <div class="particle" style="left: 82%; animation-delay: 23s;"></div>
    <div class="particle" style="left: 92%; animation-delay: 26s;"></div>
</div>

<!-- Floating Action Elements -->
<div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
    <div style="background: linear-gradient(135deg, rgba(168, 200, 255, 0.2), rgba(196, 167, 255, 0.2));
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 50px;
                padding: 8px 15px;
                color: white;
                font-size: 0.8rem;
                animation: floating 3s ease-in-out infinite;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
        ✨ Premium Mode Active
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Tool categories configuration
TOOL_CATEGORIES = {
    "Text Tools": {
        "icon": "📝",
        "description": "Text processing, analysis, and manipulation tools",
        "module": text_tools,
        "color": "#FF6B6B"
    },
    "Image Tools": {
        "icon": "🖼️",
        "description": "Image editing, conversion, and analysis tools",
        "module": image_tools,
        "color": "#4ECDC4"
    },
    "Security/Privacy Tools": {
        "icon": "🔒",
        "description": "Cybersecurity, privacy, and encryption tools",
        "module": security_tools,
        "color": "#45B7D1"
    },
    "CSS Tools": {
        "icon": "🎨",
        "description": "CSS generators, validators, and design tools",
        "module": css_tools,
        "color": "#96CEB4"
    },
    "Coding Tools": {
        "icon": "💻",
        "description": "Programming utilities and development tools",
        "module": coding_tools,
        "color": "#FFEAA7"
    },
    "Audio/Video Tools": {
        "icon": "🎵",
        "description": "Media processing and editing tools",
        "module": audio_video_tools,
        "color": "#DDA0DD"
    },
    "File Tools": {
        "icon": "📁",
        "description": "File management and conversion utilities",
        "module": file_tools,
        "color": "#98D8C8"
    },
    "AI Tools": {
        "icon": "🤖",
        "description": "Artificial intelligence and machine learning tools",
        "module": ai_tools,
        "color": "#F7DC6F"
    },
    "Social Media Tools": {
        "icon": "📱",
        "description": "Social media management and analytics",
        "module": social_media_tools,
        "color": "#BB8FCE"
    },
    "Color Tools": {
        "icon": "🌈",
        "description": "Color palettes, converters, and design tools",
        "module": color_tools,
        "color": "#85C1E9"
    },
    "Web Developer Tools": {
        "icon": "🌐",
        "description": "Web development and testing utilities",
        "module": web_dev_tools,
        "color": "#F8C471"
    },
    "SEO/Marketing Tools": {
        "icon": "📈",
        "description": "Search optimization and marketing analytics",
        "module": seo_marketing_tools,
        "color": "#82E0AA"
    },
    "Data Tools": {
        "icon": "📊",
        "description": "Data analysis and visualization tools",
        "module": data_tools,
        "color": "#F1948A"
    },
    "Science/Math Tools": {
        "icon": "🧮",
        "description": "Scientific calculators and mathematical tools",
        "module": science_math_tools,
        "color": "#AED6F1"
    }
}


def main():
    # Header with dynamic elements
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="floating" style="margin-bottom: 0.5rem;">🛠️ Ultimate All-in-One Digital Toolkit</h1>
        <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                    background-clip: text; font-size: 1.2rem; font-weight: 500;">
            ✨ 500+ Professional Tools Across 14 Specialized Categories ✨
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")

        # Search functionality
        search_query = st.text_input("🔍 Search Tools", placeholder="Type to search...")
        if search_query:
            search_results = search_tools(search_query, TOOL_CATEGORIES)
            if search_results:
                st.subheader("Search Results")
                for category, tools in search_results.items():
                    st.write(f"**{category}**: {', '.join(tools)}")

        # Category selection
        selected_category = st.selectbox(
            "Select Category",
            ["Dashboard"] + list(TOOL_CATEGORIES.keys()),
            index=0 if 'selected_category' not in st.session_state else
            list(TOOL_CATEGORIES.keys()).index(
                st.session_state.selected_category) + 1 if st.session_state.selected_category in TOOL_CATEGORIES else 0
        )

        if selected_category != "Dashboard":
            st.session_state.selected_category = selected_category

        # Dynamic Statistics with animations
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <h3 style="background: linear-gradient(45deg, #667eea, #764ba2); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       background-clip: text;">📊 Platform Stats</h3>
        </div>
        """, unsafe_allow_html=True)

        # Animated metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-container" style="text-align: center; animation-delay: 0.1s;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{}</div>
                <div style="color: #666; font-size: 0.9rem;">Total Categories</div>
            </div>
            """.format(len(TOOL_CATEGORIES)), unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="metric-container" style="text-align: center; animation-delay: 0.2s;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">500+</div>
                <div style="color: #666; font-size: 0.9rem;">Total Tools</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="metric-container" style="text-align: center; animation-delay: 0.3s;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">1,000+</div>
                <div style="color: #666; font-size: 0.9rem;">Active Users</div>
            </div>
            """, unsafe_allow_html=True)

        # Quick access with theme switcher
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0;">
            <h4 style="background: linear-gradient(45deg, #667eea, #764ba2); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       background-clip: text;">⚡ Quick Access</h4>
        </div>
        """, unsafe_allow_html=True)

        # Theme selector
        theme_options = ["🌈 Gradient", "🌙 Dark", "☀️ Light", "🎨 Colorful"]
        selected_theme = st.selectbox("Theme", theme_options, key="theme_selector")

        # Apply theme changes immediately
        if selected_theme == "🌙 Dark":
            st.markdown("""
            <style>
            .stApp { background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483) !important; }
            .main .block-container { background: rgba(30, 30, 30, 0.95) !important; color: white; }
            </style>
            """, unsafe_allow_html=True)
        elif selected_theme == "☀️ Light":
            st.markdown("""
            <style>
            .stApp { background: linear-gradient(-45deg, #f7f7f7, #e8e8e8, #ffffff, #f0f0f0) !important; }
            .main .block-container { background: rgba(255, 255, 255, 0.98) !important; }
            </style>
            """, unsafe_allow_html=True)
        elif selected_theme == "🎨 Colorful":
            st.markdown("""
            <style>
            .stApp { background: linear-gradient(-45deg, #ff9a56, #ffad56, #ffd93d, #6bcf7f) !important; }
            </style>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset All", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

            if st.button("📥 Export Settings", use_container_width=True):
                st.success("Settings exported!")

        with col2:
            if st.button("📤 Import Settings", use_container_width=True):
                st.success("Settings imported!")

            if st.button("🎯 Favorites", use_container_width=True):
                st.info("Add tools to favorites!")

    # Top navigation bar with Connect button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("📞 Connect", type="secondary"):
            st.session_state.show_connect = True
            st.rerun()

    # Check if Connect page should be displayed
    if st.session_state.get('show_connect', False):
        display_connect_page()
        # Add a back button
        if st.button("← Back to Dashboard", type="primary"):
            st.session_state.show_connect = False
            st.rerun()
        return

    # Main content area
    if selected_category == "Dashboard" or 'selected_category' not in st.session_state:
        # Dashboard view with dynamic header
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="background: linear-gradient(45deg, #667eea, #764ba2); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       background-clip: text; animation: titlePulse 2s ease-in-out infinite alternate;">
                🏠 Welcome to Your Digital Toolkit Dashboard
            </h2>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced welcome message with progress bar
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                    color: white; padding: 1.5rem; border-radius: 15px; 
                    margin: 1rem 0; animation: glow 2s ease-in-out infinite alternate;
                    text-align: center;">
            <h4 style="margin: 0; color: white;">✨ Welcome to the Ultimate Digital Toolkit! ✨</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Select a category from the sidebar or click on any tool category below to get started.</p>
        </div>
        """, unsafe_allow_html=True)

        # Dynamic loading bar animation
        st.markdown("""
        <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 4px; overflow: hidden; margin: 1rem 0;">
            <div style="background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; 
                        animation: loadingBar 3s ease-in-out infinite; border-radius: 10px;"></div>
        </div>
        <style>
        @keyframes loadingBar {
            0% { width: 0%; }
            50% { width: 100%; }
            100% { width: 0%; }
        }
        </style>
        """, unsafe_allow_html=True)

        # Tool category grid
        display_tool_grid(TOOL_CATEGORIES)

        # Recent activity with enhanced styling
        if 'recent_tools' in st.session_state and st.session_state.recent_tools:
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0 1rem 0;">
                <h3 style="background: linear-gradient(45deg, #667eea, #764ba2); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                           background-clip: text;">🕒 Recently Used Tools</h3>
            </div>
            """, unsafe_allow_html=True)
            cols = st.columns(5)
            for i, tool in enumerate(st.session_state.recent_tools[-5:]):
                with cols[i % 5]:
                    if st.button(f"🔄 {tool}", key=f"recent_{i}"):
                        pass  # Add functionality to return to the tool

        # Enhanced Feature highlights with cards
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0 2rem 0;">
            <h3 style="background: linear-gradient(45deg, #667eea, #764ba2); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       background-clip: text;">✨ Platform Features</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="metric-container" style="height: 250px; display: flex; flex-direction: column; 
                                                justify-content: center; text-align: center; animation-delay: 0.1s;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔧</div>
                <h4 style="color: #667eea; margin-bottom: 1rem;">500+ Tools</h4>
                <ul style="text-align: left; color: #666; margin: 0; padding-left: 1rem;">
                    <li>Text processing & analysis</li>
                    <li>Image editing & conversion</li>
                    <li>Security & privacy tools</li>
                    <li>CSS & web development</li>
                    <li>AI & machine learning</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-container" style="height: 250px; display: flex; flex-direction: column; 
                                                justify-content: center; text-align: center; animation-delay: 0.2s;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔄</div>
                <h4 style="color: #667eea; margin-bottom: 1rem;">Cross-Tool Integration</h4>
                <ul style="text-align: left; color: #666; margin: 0; padding-left: 1rem;">
                    <li>Unified file management</li>
                    <li>Batch processing workflows</li>
                    <li>Universal search</li>
                    <li>Export/import capabilities</li>
                    <li>Template system</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="metric-container" style="height: 250px; display: flex; flex-direction: column; 
                                                justify-content: center; text-align: center; animation-delay: 0.3s;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                <h4 style="color: #667eea; margin-bottom: 1rem;">Advanced Features</h4>
                <ul style="text-align: left; color: #666; margin: 0; padding-left: 1rem;">
                    <li>Real-time processing</li>
                    <li>Progress tracking</li>
                    <li>History management</li>
                    <li>Favorites system</li>
                    <li>Custom workflows</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

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


def display_connect_page():
    """Display the Connect page"""
    st.header("📞 Connect")

    # Team photo
    st.image(
            "vatsal_photo.jpg",
            use_column_width=True,
            width=300,
            hight=400,
            caption="Hi there! I'm Vatsal, the creator of this toolkit.", use_container_width=True)

    # Page introduction
    st.markdown("""
    ### Hi, I'm Vatsal Varshney! 👋

    Welcome to my Ultimate Digital Toolkit! I've created this comprehensive platform to provide you with 500+ tools 
    for text processing, image editing, data analysis, and much more. Whether you have questions, feedback, feature 
    requests, or just want to connect, I'd love to hear from you.
    """)

    # Contact sections
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 💬 Feedback & Support

        **Found a bug?** Let me know and help me improve the toolkit!
        **Have a suggestion?** I'm always looking for ways to make it better.
        **Need help?** I'm here to support you with any of the tools.
        """)

        # Feedback form
        st.subheader("📝 Send Feedback")

        feedback_type = st.selectbox("Feedback Type", [
            "Bug Report", "Feature Request", "General Feedback", "Support Request", "Compliment"
        ])

        name = st.text_input("Your Name (optional)", placeholder="Vatsal Varshney")
        email = st.text_input("Your Email (optional)", placeholder="vastal@example.com")

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
        st.markdown("""
        #### 🌐 Connect With Me

        **Follow my updates** and join the community!
        **Share your creations** made with the toolkit.
        **Stay informed** about new features and releases.
        """)

        # Social media / connection links (placeholder)
        st.subheader("🔗 Find Me Online")

        # Social and contact links
        social_links = [
            ("🐙 GitHub", "https://github.com/VATSALVASRHNEY108", "View my projects and code"),
            ("💼 LinkedIn", "https://linkedin.com/in/vatsal-varshney108", "Connect professionally"),
            ("🐦 Twitter", "https://twitter.com/vatsalvarshney", "Follow me for updates"),
            ("📧 Email", "mailto:vatsalvarshneyhts@example.com", "Send me a direct email")
        ]

        for icon_name, link, description in social_links:
            with st.container():
                col_icon, col_desc = st.columns([3, 7])
                with col_icon:
                    st.markdown(f"**{icon_name}**")
                with col_desc:
                    st.markdown(f"[{description}]({link})")

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

    # Statistics (demo data)
    st.markdown("---")
    st.subheader("📊 Toolkit Stats")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🛠️ Total Tools", "500+")



if __name__ == "__main__":
    main()
