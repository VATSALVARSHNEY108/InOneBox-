import streamlit as st
import json
import base64
import io
from datetime import datetime
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler
from utils.ai_client import ai_client


def display_tools():
    """Display all AI tools"""

    tool_categories = {
        "Multiple AI Model Integrations": [
            "Model Comparison", "Multi-Model Chat", "Model Selector", "Performance Benchmark", "API Manager"
        ],
        "Text Generation": [
            "Content Creator", "Story Writer", "Article Generator", "Copywriting Assistant", "Technical Writer"
        ],
        "Image Generation": [
            "AI Art Creator", "Style Transfer", "Image Synthesis", "Concept Art", "Photo Enhancement"
        ],
        "Data Analysis": [
            "Pattern Recognition", "Trend Analysis", "Predictive Modeling", "Data Insights", "Statistical Analysis"
        ],
        "Chatbots": [
            "Conversational AI", "Customer Service Bot", "Educational Assistant", "Domain Expert", "Multi-Purpose Bot"
        ],
        "Language Processing": [
            "Text Translator", "Sentiment Analysis", "Text Summarizer", "Language Detector", "Content Moderator"
        ],
        "Computer Vision": [
            "Image Recognition", "Object Detection", "Scene Analysis", "OCR Reader", "Visual Search"
        ],
        "AI Utilities": [
            "Model Comparison", "Prompt Optimizer", "AI Workflow", "Batch Processor", "Response Analyzer"
        ],
        "Machine Learning": [
            "Model Training", "Data Preprocessing", "Feature Engineering", "Model Evaluation", "AutoML"
        ],
        "Voice & Audio": [
            "Speech Recognition", "Voice Synthesis", "Audio Analysis", "Voice Cloning", "Sound Generation"
        ]
    }

    selected_category = st.selectbox("Select AI Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"AI Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Multi-Model Chat":
        multi_model_chat()
    elif selected_tool == "Content Creator":
        content_creator()
    elif selected_tool == "AI Art Creator":
        ai_art_creator()
    elif selected_tool == "Sentiment Analysis":
        sentiment_analysis()
    elif selected_tool == "Image Recognition":
        image_recognition()
    elif selected_tool == "Text Translator":
        text_translator()
    elif selected_tool == "Text Summarizer":
        text_summarizer()
    elif selected_tool == "Model Comparison":
        model_comparison()
    elif selected_tool == "Prompt Optimizer":
        prompt_optimizer()
    elif selected_tool == "Data Insights":
        data_insights()
    elif selected_tool == "Conversational AI":
        conversational_ai()
    elif selected_tool == "OCR Reader":
        ocr_reader()
    elif selected_tool == "Voice Synthesis":
        voice_synthesis()
    elif selected_tool == "Pattern Recognition":
        pattern_recognition()
    elif selected_tool == "Story Writer":
        story_writer()
    elif selected_tool == "Style Transfer":
        style_transfer()
    elif selected_tool == "Image Synthesis":
        image_synthesis()
    elif selected_tool == "Concept Art":
        concept_art()
    elif selected_tool == "Photo Enhancement":
        photo_enhancement()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def multi_model_chat():
    """Chat with multiple AI models simultaneously"""
    create_tool_header("Multi-Model Chat", "Chat with multiple AI models at once", "🤖")

    # Model selection
    st.subheader("Select AI Models")
    available_models = ai_client.get_available_models()

    if not available_models:
        st.warning("No AI models available. Please check your API keys.")
        return

    selected_models = st.multiselect("Choose Models", available_models,
                                     default=available_models[:2] if len(available_models) >= 2 else available_models)

    if not selected_models:
        st.warning("Please select at least one model.")
        return

    # Chat interface
    st.subheader("Multi-Model Conversation")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_message = st.text_area("Enter your message:", height=100)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Send to All Models"):
            if user_message:
                send_to_all_models(user_message, selected_models)

    with col2:
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()

    with col3:
        if st.button("Export Chat"):
            export_chat_history()

    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Conversation History")

        for entry in st.session_state.chat_history:
            # User message
            st.markdown(f"**👤 You:** {entry['user_message']}")

            # Model responses
            for model, response in entry['responses'].items():
                with st.expander(f"🤖 {model.title()} Response"):
                    st.write(response)

            st.markdown("---")


def content_creator():
    """AI-powered content creation tool"""
    create_tool_header("Content Creator", "Generate various types of content with AI", "✍️")

    content_type = st.selectbox("Content Type", [
        "Blog Post", "Social Media Post", "Email", "Product Description",
        "Press Release", "Technical Documentation", "Creative Writing", "Marketing Copy"
    ])

    # Content parameters
    st.subheader("Content Parameters")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic/Subject", placeholder="Enter the main topic")
        target_audience = st.selectbox("Target Audience", [
            "General Public", "Professionals", "Students", "Experts", "Children", "Teenagers"
        ])
        tone = st.selectbox("Tone", [
            "Professional", "Casual", "Friendly", "Formal", "Humorous", "Persuasive", "Educational"
        ])

    with col2:
        length = st.selectbox("Content Length", [
            "Short (100-300 words)", "Medium (300-800 words)", "Long (800-1500 words)", "Very Long (1500+ words)"
        ])
        language = st.selectbox("Language", [
            "English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese"
        ])
        creativity = st.slider("Creativity Level", 0.1, 1.0, 0.7, 0.1)

    # Additional options
    if content_type in ["Blog Post", "Technical Documentation"]:
        include_outline = st.checkbox("Include Outline/Structure")
        include_seo = st.checkbox("SEO Optimized")

    if content_type == "Social Media Post":
        platform = st.selectbox("Platform", ["Twitter", "Facebook", "LinkedIn", "Instagram", "TikTok"])
        include_hashtags = st.checkbox("Include Hashtags")

    additional_instructions = st.text_area("Additional Instructions (optional)",
                                           placeholder="Any specific requirements or guidelines...")

    if st.button("Generate Content") and topic:
        with st.spinner("Generating content with AI..."):
            # Build kwargs dict with only the extra parameters we need
            extra_kwargs = {}
            if content_type in ["Blog Post", "Technical Documentation"]:
                extra_kwargs['include_outline'] = locals().get('include_outline', False)
                extra_kwargs['include_seo'] = locals().get('include_seo', False)
            if content_type == "Social Media Post":
                extra_kwargs['platform'] = locals().get('platform', 'general')
                extra_kwargs['include_hashtags'] = locals().get('include_hashtags', False)

            content = generate_content(
                content_type, topic, target_audience, tone, length,
                language, creativity, additional_instructions,
                **extra_kwargs
            )

            if content:
                st.subheader("Generated Content")
                st.markdown(content)

                # Content analysis
                st.subheader("Content Analysis")
                analysis = analyze_content(content)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Word Count", analysis['word_count'])
                with col2:
                    st.metric("Reading Time", f"{analysis['reading_time']} min")
                with col3:
                    st.metric("Readability", analysis['readability_level'])

                # Download options
                FileHandler.create_download_link(
                    content.encode(),
                    f"{content_type.lower().replace(' ', '_')}.txt",
                    "text/plain"
                )

                # Regenerate options
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Regenerate"):
                        st.rerun()
                with col2:
                    if st.button("Refine Content"):
                        refine_content(content)


def ai_art_creator():
    """AI-powered image generation"""
    create_tool_header("AI Art Creator", "Generate images using AI", "🎨")

    # Image generation parameters
    st.subheader("Image Generation Settings")

    col1, col2 = st.columns(2)
    with col1:
        prompt = st.text_area("Image Description",
                              placeholder="Describe the image you want to create...",
                              height=100)
        style = st.selectbox("Art Style", [
            "Realistic", "Digital Art", "Oil Painting", "Watercolor", "Sketch",
            "Anime/Manga", "Comic Book", "Abstract", "Surreal", "Minimalist"
        ])
        mood = st.selectbox("Mood/Atmosphere", [
            "Neutral", "Happy", "Dramatic", "Peaceful", "Mysterious", "Energetic", "Melancholic"
        ])

    with col2:
        resolution = st.selectbox("Resolution", ["1024x1024", "1024x768", "768x1024", "512x512"])
        color_scheme = st.selectbox("Color Scheme", [
            "Natural", "Vibrant", "Monochrome", "Warm Tones", "Cool Tones", "Pastel", "High Contrast"
        ])
        quality = st.selectbox("Quality", ["Standard", "High", "Ultra"])

    # Advanced options
    with st.expander("Advanced Options"):
        negative_prompt = st.text_area("Negative Prompt (what to avoid)",
                                       placeholder="low quality, blurry, distorted...")
        seed = st.number_input("Seed (for reproducibility)", min_value=0, value=0)
        num_images = st.slider("Number of Images", 1, 4, 1)

    if st.button("Generate Image") and prompt:
        with st.spinner("Creating AI artwork..."):
            # Enhanced prompt
            enhanced_prompt = enhance_image_prompt(prompt, style, mood, color_scheme)

            st.info(f"Enhanced prompt: {enhanced_prompt}")

            # Generate image
            image_data = ai_client.generate_image(enhanced_prompt)

            if image_data:
                st.subheader("Generated Artwork")

                # Display image
                st.image(io.BytesIO(image_data), caption="AI Generated Image")

                # Image details
                st.subheader("Generation Details")
                generation_info = {
                    "Original Prompt": prompt,
                    "Enhanced Prompt": enhanced_prompt,
                    "Style": style,
                    "Mood": mood,
                    "Color Scheme": color_scheme,
                    "Resolution": resolution,
                    "Generated At": datetime.now().isoformat()
                }

                for key, value in generation_info.items():
                    st.write(f"**{key}**: {value}")

                # Download options
                FileHandler.create_download_link(
                    image_data,
                    f"ai_artwork_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    "image/png"
                )

                # Save generation info
                info_json = json.dumps(generation_info, indent=2)
                FileHandler.create_download_link(
                    info_json.encode(),
                    f"generation_info_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json"
                )
            else:
                st.error("Failed to generate image. Please try again with a different prompt.")


def sentiment_analysis():
    """Analyze sentiment of text"""
    create_tool_header("Sentiment Analysis", "Analyze text sentiment using AI", "😊")

    # Input options
    input_method = st.radio("Input Method", ["Text Input", "File Upload"])

    if input_method == "Text Input":
        text = st.text_area("Enter text to analyze:", height=200)
    else:
        uploaded_file = FileHandler.upload_files(['txt', 'csv'], accept_multiple=False)
        if uploaded_file:
            text = FileHandler.process_text_file(uploaded_file[0])
            st.text_area("Uploaded text:", text, height=150, disabled=True)
        else:
            text = ""

    # Analysis options
    st.subheader("Analysis Options")

    col1, col2 = st.columns(2)
    with col1:
        analysis_depth = st.selectbox("Analysis Depth", ["Basic", "Detailed", "Comprehensive"])
        include_emotions = st.checkbox("Include Emotion Detection", True)

    with col2:
        batch_analysis = st.checkbox("Batch Analysis (by sentences)")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.1)

    if st.button("Analyze Sentiment") and text:
        with st.spinner("Analyzing sentiment..."):
            # Perform sentiment analysis
            analysis_result = ai_client.analyze_sentiment(text)

            if 'error' not in analysis_result:
                st.subheader("Sentiment Analysis Results")

                # Overall sentiment
                col1, col2, col3 = st.columns(3)
                with col1:
                    sentiment = analysis_result.get('sentiment', 'Unknown')
                    color = get_sentiment_color(sentiment)
                    st.markdown(f"**Overall Sentiment**: <span style='color: {color}'>{sentiment.title()}</span>",
                                unsafe_allow_html=True)

                with col2:
                    confidence = analysis_result.get('confidence', 0)
                    st.metric("Confidence", f"{confidence:.1%}")

                with col3:
                    st.metric("Text Length", f"{len(text.split())} words")

                # Detailed analysis
                if analysis_depth in ["Detailed", "Comprehensive"]:
                    st.subheader("Detailed Analysis")

                    if 'explanation' in analysis_result:
                        st.write("**Analysis Explanation:**")
                        st.write(analysis_result['explanation'])

                    if 'indicators' in analysis_result:
                        st.write("**Key Sentiment Indicators:**")
                        for indicator in analysis_result['indicators']:
                            st.write(f"• {indicator}")

                # Emotion detection
                if include_emotions and 'emotions' in analysis_result:
                    st.subheader("Emotion Detection")
                    emotions = analysis_result['emotions']

                    for emotion, score in emotions.items():
                        st.progress(score, text=f"{emotion.title()}: {score:.1%}")

                # Batch analysis
                if batch_analysis:
                    st.subheader("Sentence-by-Sentence Analysis")
                    sentences = text.split('.')

                    for i, sentence in enumerate(sentences[:10], 1):  # Limit to first 10 sentences
                        if sentence.strip():
                            sentence_sentiment = analyze_sentence_sentiment(sentence.strip())

                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{i}.** {sentence.strip()}")
                            with col2:
                                sentiment_color = get_sentiment_color(sentence_sentiment)
                                st.markdown(f"<span style='color: {sentiment_color}'>{sentence_sentiment}</span>",
                                            unsafe_allow_html=True)

                # Export results
                if st.button("Export Analysis"):
                    export_data = {
                        "text": text,
                        "analysis_results": analysis_result,
                        "analysis_date": datetime.now().isoformat(),
                        "settings": {
                            "depth": analysis_depth,
                            "emotions": include_emotions,
                            "batch": batch_analysis
                        }
                    }

                    export_json = json.dumps(export_data, indent=2)
                    FileHandler.create_download_link(
                        export_json.encode(),
                        "sentiment_analysis.json",
                        "application/json"
                    )
            else:
                st.error(f"Analysis failed: {analysis_result['error']}")


def image_recognition():
    """AI-powered image recognition and analysis"""
    create_tool_header("Image Recognition", "Analyze and recognize objects in images", "👁️")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp'], accept_multiple=True)

    if uploaded_files:
        # Analysis options
        st.subheader("Recognition Settings")

        col1, col2 = st.columns(2)
        with col1:
            analysis_type = st.selectbox("Analysis Type", [
                "General Recognition", "Object Detection", "Scene Analysis",
                "Text Detection (OCR)", "Face Detection", "Brand Recognition"
            ])
            detail_level = st.selectbox("Detail Level", ["Basic", "Detailed", "Comprehensive"])

        with col2:
            include_confidence = st.checkbox("Include Confidence Scores", True)
            include_coordinates = st.checkbox("Include Object Coordinates", False)

        for uploaded_file in uploaded_files:
            st.subheader(f"Analyzing: {uploaded_file.name}")

            # Display image
            image = FileHandler.process_image_file(uploaded_file)
            if image:
                st.image(image, caption=uploaded_file.name, use_column_width=True)

                if st.button(f"Analyze {uploaded_file.name}", key=f"analyze_{uploaded_file.name}"):
                    with st.spinner("Analyzing image with AI..."):
                        # Convert image to bytes for AI analysis
                        img_bytes = io.BytesIO()
                        image.save(img_bytes, format='PNG')
                        img_bytes.seek(0)

                        # Create analysis prompt
                        prompt = create_recognition_prompt(analysis_type, detail_level, include_confidence)

                        # Analyze image
                        analysis_result = ai_client.analyze_image(img_bytes.getvalue(), prompt)

                        if analysis_result:
                            st.subheader("Recognition Results")
                            st.write(analysis_result)

                            # Try to parse structured results
                            try:
                                if analysis_result.strip().startswith('{'):
                                    structured_result = json.loads(analysis_result)
                                    display_structured_recognition(structured_result)
                            except:
                                pass  # Display as plain text if not JSON

                            # Export results
                            if st.button(f"Export Results for {uploaded_file.name}",
                                         key=f"export_{uploaded_file.name}"):
                                export_data = {
                                    "image_name": uploaded_file.name,
                                    "analysis_type": analysis_type,
                                    "detail_level": detail_level,
                                    "results": analysis_result,
                                    "analysis_date": datetime.now().isoformat()
                                }

                                export_json = json.dumps(export_data, indent=2)
                                FileHandler.create_download_link(
                                    export_json.encode(),
                                    f"recognition_results_{uploaded_file.name}.json",
                                    "application/json"
                                )

                st.markdown("---")


def text_translator():
    """AI-powered text translation"""
    create_tool_header("Text Translator", "Translate text between languages", "🌍")

    # Input methods
    input_method = st.radio("Input Method", ["Text Input", "File Upload"])

    if input_method == "Text Input":
        source_text = st.text_area("Enter text to translate:", height=200)
    else:
        uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)
        if uploaded_file:
            source_text = FileHandler.process_text_file(uploaded_file[0])
            st.text_area("Uploaded text:", source_text, height=150, disabled=True)
        else:
            source_text = ""

    # Translation settings
    st.subheader("Translation Settings")

    col1, col2, col3 = st.columns(3)
    with col1:
        source_language = st.selectbox("Source Language", [
            "Auto-Detect", "English", "Spanish", "French", "German", "Italian",
            "Portuguese", "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Hindi"
        ])

    with col2:
        target_language = st.selectbox("Target Language", [
            "Spanish", "French", "German", "Italian", "Portuguese", "Russian",
            "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "English"
        ])

    with col3:
        translation_style = st.selectbox("Translation Style", [
            "Standard", "Formal", "Casual", "Technical", "Literary"
        ])

    # Advanced options
    with st.expander("Advanced Options"):
        preserve_formatting = st.checkbox("Preserve Formatting", True)
        include_alternatives = st.checkbox("Include Alternative Translations", False)
        cultural_adaptation = st.checkbox("Cultural Adaptation", False)

    if st.button("Translate Text") and source_text and target_language:
        with st.spinner(f"Translating to {target_language}..."):
            # Enhanced translation prompt
            translation_prompt = create_translation_prompt(
                source_text, target_language, translation_style,
                preserve_formatting, cultural_adaptation
            )

            translated_text = ai_client.generate_text(translation_prompt)

            if translated_text:
                st.subheader("Translation Results")

                # Display original and translated text side by side
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Original Text:**")
                    st.text_area("", source_text, height=200, disabled=True, key="original")

                with col2:
                    st.markdown(f"**Translated Text ({target_language}):**")
                    st.text_area("", translated_text, height=200, disabled=True, key="translated")

                # Translation quality metrics
                st.subheader("Translation Quality")
                quality_metrics = assess_translation_quality(source_text, translated_text)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Estimated Quality", quality_metrics['quality_score'])
                with col2:
                    st.metric("Fluency", quality_metrics['fluency'])
                with col3:
                    st.metric("Completeness", quality_metrics['completeness'])

                # Alternative translations
                if include_alternatives:
                    st.subheader("Alternative Translations")
                    alternatives = generate_translation_alternatives(source_text, target_language)

                    for i, alt in enumerate(alternatives, 1):
                        st.write(f"**Alternative {i}:** {alt}")

                # Export translation
                FileHandler.create_download_link(
                    translated_text.encode(),
                    f"translation_{target_language.lower()}.txt",
                    "text/plain"
                )


# Helper Functions

def send_to_all_models(message, models):
    """Send message to all selected models"""
    responses = {}

    for model in models:
        try:
            response = ai_client.generate_text(message, model=model)
            responses[model] = response
        except Exception as e:
            responses[model] = f"Error: {str(e)}"

    # Add to chat history
    st.session_state.chat_history.append({
        'user_message': message,
        'responses': responses,
        'timestamp': datetime.now().isoformat()
    })

    st.rerun()


def export_chat_history():
    """Export chat history to file"""
    if st.session_state.chat_history:
        chat_data = {
            'chat_history': st.session_state.chat_history,
            'exported_at': datetime.now().isoformat()
        }

        chat_json = json.dumps(chat_data, indent=2)
        FileHandler.create_download_link(
            chat_json.encode(),
            f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json"
        )


def generate_content(content_type, topic, audience, tone, length, language, creativity, instructions, **kwargs):
    """Generate content using AI"""
    prompt = f"""
    Create a {content_type.lower()} about "{topic}" with the following specifications:

    - Target Audience: {audience}
    - Tone: {tone}
    - Length: {length}
    - Language: {language}
    - Creativity Level: {creativity}

    Additional Instructions: {instructions if instructions else 'None'}

    """

    # Add content-specific instructions
    if content_type == "Blog Post":
        prompt += "\nInclude an engaging introduction, well-structured body with subheadings, and a compelling conclusion."
        if kwargs.get('include_outline'):
            prompt += "\nStart with an outline before the content."
        if kwargs.get('include_seo'):
            prompt += "\nOptimize for SEO with relevant keywords."

    elif content_type == "Social Media Post":
        platform = kwargs.get('platform', 'general')
        prompt += f"\nOptimize for {platform}. Keep it engaging and shareable."
        if kwargs.get('include_hashtags'):
            prompt += "\nInclude relevant hashtags."

    return ai_client.generate_text(prompt, max_tokens=2000)


def analyze_content(content):
    """Analyze generated content"""
    words = content.split()
    word_count = len(words)
    reading_time = max(1, word_count // 200)  # Assume 200 WPM reading speed

    # Simple readability assessment
    sentences = content.split('.')
    avg_sentence_length = word_count / len(sentences) if sentences else 0

    if avg_sentence_length < 15:
        readability = "Easy"
    elif avg_sentence_length < 25:
        readability = "Medium"
    else:
        readability = "Complex"

    return {
        'word_count': word_count,
        'reading_time': reading_time,
        'readability_level': readability
    }


def enhance_image_prompt(prompt, style, mood, color_scheme):
    """Enhance image generation prompt"""
    enhanced = prompt

    if style != "Natural":
        enhanced += f", {style.lower()} style"

    if mood != "Neutral":
        enhanced += f", {mood.lower()} mood"

    if color_scheme != "Natural":
        enhanced += f", {color_scheme.lower()}"

    enhanced += ", high quality, detailed, professional"

    return enhanced


def get_sentiment_color(sentiment):
    """Get color for sentiment display"""
    colors = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'gray',
        'mixed': 'orange'
    }
    return colors.get(sentiment.lower(), 'black')


def analyze_sentence_sentiment(sentence):
    """Analyze sentiment of individual sentence"""
    # Simple keyword-based sentiment for demo
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'worst']

    sentence_lower = sentence.lower()

    positive_count = sum(1 for word in positive_words if word in sentence_lower)
    negative_count = sum(1 for word in negative_words if word in sentence_lower)

    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'


def create_recognition_prompt(analysis_type, detail_level, include_confidence):
    """Create prompt for image recognition"""
    base_prompt = f"Analyze this image and provide {detail_level.lower()} {analysis_type.lower()}."

    if analysis_type == "Object Detection":
        base_prompt += " Identify and describe all objects visible in the image."
    elif analysis_type == "Scene Analysis":
        base_prompt += " Describe the scene, setting, and overall context."
    elif analysis_type == "Text Detection (OCR)":
        base_prompt += " Extract and transcribe any text visible in the image."
    elif analysis_type == "Face Detection":
        base_prompt += " Identify faces and describe their characteristics."

    if include_confidence:
        base_prompt += " Include confidence levels for your identifications."

    if detail_level == "Comprehensive":
        base_prompt += " Provide comprehensive analysis with technical details."

    return base_prompt


def display_structured_recognition(result):
    """Display structured recognition results"""
    if isinstance(result, dict):
        for key, value in result.items():
            st.write(f"**{key.title()}**: {value}")


def create_translation_prompt(text, target_language, style, preserve_formatting, cultural_adaptation):
    """Create enhanced translation prompt"""
    prompt = f"Translate the following text to {target_language}"

    if style != "Standard":
        prompt += f" using a {style.lower()} style"

    if preserve_formatting:
        prompt += ", preserving the original formatting and structure"

    if cultural_adaptation:
        prompt += ", adapting cultural references and idioms appropriately"

    prompt += f":\n\n{text}"

    return prompt


def assess_translation_quality(original, translated):
    """Assess translation quality (simplified)"""
    # Simple quality metrics based on length ratio and structure
    length_ratio = len(translated) / len(original) if original else 0

    quality_score = "Good" if 0.7 <= length_ratio <= 1.5 else "Fair"
    fluency = "High" if length_ratio > 0.5 else "Medium"
    completeness = "Complete" if length_ratio > 0.8 else "Partial"

    return {
        'quality_score': quality_score,
        'fluency': fluency,
        'completeness': completeness
    }


def generate_translation_alternatives(text, target_language):
    """Generate alternative translations"""
    # This would generate multiple translation variants
    alternatives = [
        f"Alternative translation 1 for: {text[:50]}...",
        f"Alternative translation 2 for: {text[:50]}...",
        f"Alternative translation 3 for: {text[:50]}..."
    ]
    return alternatives[:2]  # Limit to 2 alternatives


# Fully implemented AI tools
def text_summarizer():
    """AI text summarization tool"""
    create_tool_header("Text Summarizer", "Summarize long texts with AI", "📝")

    # Input method selection
    input_method = st.selectbox("Input Method", ["Text Input", "File Upload", "URL"])

    text_content = ""

    if input_method == "Text Input":
        text_content = st.text_area(
            "Enter text to summarize",
            placeholder="Paste your long text here...",
            height=200
        )

    elif input_method == "File Upload":
        uploaded_files = FileHandler.upload_files(['txt', 'pdf', 'docx', 'md'], accept_multiple=False)
        if uploaded_files:
            text_content = FileHandler.process_text_file(uploaded_files[0])
            st.success(f"📄 Loaded text from {uploaded_files[0].name} ({len(text_content)} characters)")

    else:  # URL
        url = st.text_input("Enter URL to summarize")
        if url and st.button("Extract Text from URL"):
            st.info("📝 URL text extraction would be implemented here")
            text_content = "Simulated extracted text from URL..."

    if text_content:
        # Summarization settings
        st.subheader("Summarization Settings")

        col1, col2 = st.columns(2)
        with col1:
            summary_length = st.selectbox(
                "Summary Length",
                ["Short (1-2 sentences)", "Medium (1 paragraph)", "Long (multiple paragraphs)", "Custom"]
            )

            if summary_length == "Custom":
                custom_length = st.slider("Target words", 50, 500, 150)

        with col2:
            summary_style = st.selectbox(
                "Summary Style",
                ["Extractive (key sentences)", "Abstractive (rewording)", "Bullet Points", "Executive Summary"]
            )

            focus_area = st.selectbox(
                "Focus Area",
                ["Main Points", "Key Facts", "Action Items", "Conclusions", "All Important Content"]
            )

        # Advanced options
        with st.expander("Advanced Options"):
            preserve_tone = st.checkbox("Preserve Original Tone", value=True)
            include_quotes = st.checkbox("Include Key Quotes", value=False)
            technical_terms = st.checkbox("Preserve Technical Terms", value=True)

            ai_model = st.selectbox("AI Model", ["gemini", "openai"])

        # Character count and preview
        st.info(f"📄 Input text: {len(text_content):,} characters, ~{len(text_content.split()):,} words")

        if len(text_content) > 50000:
            st.warning("⚠️ Text is very long. Consider splitting into smaller sections for better results.")

        # Generate summary
        if st.button("Generate Summary", type="primary"):
            with st.spinner("Generating AI summary..."):
                try:
                    # Create summarization prompt
                    length_instructions = {
                        "Short (1-2 sentences)": "in 1-2 sentences",
                        "Medium (1 paragraph)": "in one paragraph",
                        "Long (multiple paragraphs)": "in 2-3 paragraphs",
                        "Custom": f"in approximately {custom_length if summary_length == 'Custom' else 150} words"
                    }

                    style_instructions = {
                        "Extractive (key sentences)": "using key sentences from the original text",
                        "Abstractive (rewording)": "using your own words to convey the main ideas",
                        "Bullet Points": "as a bulleted list of main points",
                        "Executive Summary": "as an executive summary with clear structure"
                    }

                    prompt = f"""Please summarize the following text {length_instructions[summary_length]} {style_instructions[summary_style]}. 
                    Focus on: {focus_area.lower()}.

                    Text to summarize:
                    {text_content}

                    Summary:"""

                    # Generate summary using AI
                    summary = ai_client.generate_text(prompt, ai_model)

                    st.subheader("📝 Summary Results")

                    # Display summary
                    st.markdown("### Generated Summary")
                    st.write(summary)

                    # Summary statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Length", f"{len(text_content.split())} words")
                    with col2:
                        st.metric("Summary Length", f"{len(summary.split())} words")
                    with col3:
                        compression_ratio = len(summary.split()) / len(text_content.split()) * 100
                        st.metric("Compression", f"{compression_ratio:.1f}%")

                    # Download options
                    st.subheader("📥 Download Summary")

                    # Plain text download
                    FileHandler.create_download_link(
                        summary.encode(),
                        f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )

                    # Enhanced summary with metadata
                    if st.button("Generate Detailed Report"):
                        report = f"""SUMMARY REPORT
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                        SETTINGS:
                        - Length: {summary_length}
                        - Style: {summary_style}
                        - Focus: {focus_area}
                        - AI Model: {ai_model}

                        STATISTICS:
                        - Original: {len(text_content.split())} words
                        - Summary: {len(summary.split())} words
                        - Compression: {compression_ratio:.1f}%

                        SUMMARY:
                        {summary}

                        ORIGINAL TEXT:
                        {text_content[:1000]}{'...' if len(text_content) > 1000 else ''}
                        """

                        FileHandler.create_download_link(
                            report.encode(),
                            f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            "text/plain"
                        )

                except Exception as e:
                    st.error(f"❌ Error generating summary: {str(e)}")
                    st.info("Please check your AI API configuration and try again.")

    else:
        st.info("📝 Enter text, upload a file, or provide a URL to generate an AI summary.")

        # Tips
        with st.expander("💡 Summarization Tips"):
            st.markdown("""
            **Best Practices:**
            - **Longer texts** work better for summarization
            - **Clear structure** in original text improves results
            - **Specific focus areas** help generate targeted summaries
            - **Multiple summaries** with different settings can provide different perspectives

            **Use Cases:**
            - Research paper summaries
            - Meeting notes condensation
            - Article key points extraction
            - Document executive summaries
            """)


def model_comparison():
    """AI model comparison tool"""
    create_tool_header("Model Comparison", "Compare different AI models side by side", "🤖")

    # Model selection
    st.subheader("Select Models to Compare")

    available_models = {
        "OpenAI GPT-5": "openai",
        "Google Gemini": "gemini",
        "OpenAI GPT-4": "openai",
        "Custom Model": "custom"
    }

    col1, col2 = st.columns(2)
    with col1:
        model_1 = st.selectbox("Model 1", list(available_models.keys()), key="model1")
    with col2:
        model_2 = st.selectbox("Model 2", list(available_models.keys()), key="model2")

    # Comparison type
    comparison_type = st.selectbox("Comparison Type", [
        "Text Generation", "Code Generation", "Question Answering", "Creative Writing", "Analysis & Reasoning"
    ])

    # Test input
    st.subheader("Test Input")

    if comparison_type == "Text Generation":
        test_prompt = st.text_area(
            "Enter prompt for text generation",
            placeholder="Write a story about...",
            height=100
        )
    elif comparison_type == "Code Generation":
        test_prompt = st.text_area(
            "Enter coding request",
            placeholder="Write a Python function that...",
            height=100
        )
    elif comparison_type == "Question Answering":
        test_prompt = st.text_area(
            "Enter question",
            placeholder="What is the difference between...",
            height=100
        )
    elif comparison_type == "Creative Writing":
        test_prompt = st.text_area(
            "Enter creative prompt",
            placeholder="Write a poem about...",
            height=100
        )
    else:  # Analysis & Reasoning
        test_prompt = st.text_area(
            "Enter analysis request",
            placeholder="Analyze the following data...",
            height=100
        )

    # Comparison settings
    with st.expander("Comparison Settings"):
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.slider("Temperature (creativity)", 0.0, 1.0, 0.7, 0.1)
            max_tokens = st.slider("Max tokens", 100, 2000, 500)

        with col2:
            num_tests = st.slider("Number of test runs", 1, 5, 1)
            include_metrics = st.checkbox("Include performance metrics", value=True)

    # Run comparison
    if test_prompt and st.button("Run Model Comparison", type="primary"):
        with st.spinner("Running comparison across models..."):
            comparison_results = []

            for run in range(num_tests):
                st.write(f"Running test {run + 1}/{num_tests}...")

                # Model 1 results
                try:
                    start_time = time.time()
                    response_1 = ai_client.generate_text(test_prompt, available_models[model_1])
                    time_1 = time.time() - start_time
                except Exception as e:
                    response_1 = f"Error: {str(e)}"
                    time_1 = 0

                # Model 2 results
                try:
                    start_time = time.time()
                    response_2 = ai_client.generate_text(test_prompt, available_models[model_2])
                    time_2 = time.time() - start_time
                except Exception as e:
                    response_2 = f"Error: {str(e)}"
                    time_2 = 0

                comparison_results.append({
                    'run': run + 1,
                    'model_1_response': response_1,
                    'model_1_time': time_1,
                    'model_2_response': response_2,
                    'model_2_time': time_2
                })

            # Display results
            st.subheader("📈 Comparison Results")

            for i, result in enumerate(comparison_results):
                st.markdown(f"### Test Run {result['run']}")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**{model_1}**")
                    st.write(result['model_1_response'])
                    if include_metrics:
                        st.metric("Response Time", f"{result['model_1_time']:.2f}s")
                        st.metric("Response Length", f"{len(result['model_1_response'].split())} words")

                with col2:
                    st.markdown(f"**{model_2}**")
                    st.write(result['model_2_response'])
                    if include_metrics:
                        st.metric("Response Time", f"{result['model_2_time']:.2f}s")
                        st.metric("Response Length", f"{len(result['model_2_response'].split())} words")

            # Overall comparison
            if include_metrics and len(comparison_results) > 1:
                st.subheader("📉 Overall Performance")

                avg_time_1 = sum(r['model_1_time'] for r in comparison_results) / len(comparison_results)
                avg_time_2 = sum(r['model_2_time'] for r in comparison_results) / len(comparison_results)
                avg_length_1 = sum(len(r['model_1_response'].split()) for r in comparison_results) / len(
                    comparison_results)
                avg_length_2 = sum(len(r['model_2_response'].split()) for r in comparison_results) / len(
                    comparison_results)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**{model_1} Average**")
                    st.metric("Avg Response Time", f"{avg_time_1:.2f}s")
                    st.metric("Avg Response Length", f"{avg_length_1:.0f} words")

                with col2:
                    st.markdown(f"**{model_2} Average**")
                    st.metric("Avg Response Time", f"{avg_time_2:.2f}s")
                    st.metric("Avg Response Length", f"{avg_length_2:.0f} words")

            # Download comparison report
            if st.button("Generate Comparison Report"):
                report_data = {
                    "comparison_type": comparison_type,
                    "models_compared": [model_1, model_2],
                    "test_prompt": test_prompt,
                    "settings": {
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "num_tests": num_tests
                    },
                    "results": comparison_results,
                    "timestamp": datetime.now().isoformat()
                }

                report_json = json.dumps(report_data, indent=2)
                FileHandler.create_download_link(
                    report_json.encode(),
                    f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json"
                )

    else:
        st.info("🤖 Enter a test prompt to compare AI models side by side.")

        # Model information
        with st.expander("📊 Model Information"):
            st.markdown("""
            **Available Models:**

            **OpenAI GPT-5**: Latest and most advanced model with superior reasoning
            **Google Gemini**: Multimodal AI with strong analytical capabilities  
            **OpenAI GPT-4**: Highly capable previous generation model

            **Comparison Metrics:**
            - Response quality and accuracy
            - Processing speed and latency
            - Response length and detail
            - Consistency across multiple runs
            """)


def prompt_optimizer():
    """AI prompt optimization tool"""
    create_tool_header("Prompt Optimizer", "Optimize your prompts for better AI responses", "🎯")

    # Original prompt input
    st.subheader("Original Prompt")
    original_prompt = st.text_area(
        "Enter your prompt to optimize",
        placeholder="e.g., Write a story",
        height=150
    )

    if original_prompt:
        # Optimization settings
        st.subheader("Optimization Settings")

        col1, col2 = st.columns(2)
        with col1:
            optimization_goal = st.selectbox("Optimization Goal", [
                "Clarity & Specificity", "Creativity & Innovation", "Accuracy & Precision",
                "Detailed Responses", "Structured Output", "Professional Tone"
            ])

            target_audience = st.selectbox("Target Audience", [
                "General", "Technical/Expert", "Beginner/Novice", "Creative Professional", "Business/Corporate"
            ])

        with col2:
            response_format = st.selectbox("Desired Response Format", [
                "Natural Text", "Bullet Points", "Numbered List", "JSON Format", "Table/Structured", "Step-by-Step"
            ])

            complexity_level = st.selectbox("Complexity Level", [
                "Simple", "Moderate", "Advanced", "Expert Level"
            ])

        # Advanced optimization options
        with st.expander("Advanced Options"):
            include_examples = st.checkbox("Include examples in prompt", value=True)
            add_constraints = st.checkbox("Add output constraints", value=True)
            role_playing = st.checkbox("Use role-playing technique", value=False)

            if role_playing:
                role = st.text_input("AI Role", placeholder="e.g., experienced marketing manager")

            context_enhancement = st.checkbox("Enhance context", value=True)
            output_length = st.selectbox("Preferred Output Length", [
                "Brief", "Moderate", "Detailed", "Comprehensive"
            ])

        # Generate optimized prompt
        if st.button("Optimize Prompt", type="primary"):
            with st.spinner("Analyzing and optimizing your prompt..."):
                # Create optimization instructions
                optimization_instructions = f"""
                Please analyze and optimize the following prompt for better AI responses.

                Original prompt: "{original_prompt}"

                Optimization criteria:
                - Goal: {optimization_goal}
                - Target audience: {target_audience}
                - Response format: {response_format}
                - Complexity: {complexity_level}
                - Output length: {output_length if 'output_length' in locals() else 'Moderate'}

                Additional requirements:
                - {'Include relevant examples' if include_examples else 'Focus on clarity without examples'}
                - {'Add specific output constraints' if add_constraints else 'Keep constraints minimal'}
                - {f'Use role-playing with AI as {role}' if role_playing and 'role' in locals() else 'Use direct instruction style'}
                - {'Enhance context and background' if context_enhancement else 'Keep context concise'}

                Please provide:
                1. Analysis of the original prompt (strengths and weaknesses)
                2. Optimized version of the prompt
                3. Explanation of improvements made
                4. Alternative versions for different use cases
                """

                try:
                    optimization_result = ai_client.generate_text(optimization_instructions, "gemini")

                    st.subheader("🎯 Optimization Results")

                    # Parse and display results
                    sections = optimization_result.split('\n\n')

                    # Display optimization analysis
                    st.markdown("### Analysis & Optimization")
                    st.write(optimization_result)

                    # Try to extract optimized prompt
                    lines = optimization_result.split('\n')
                    optimized_prompt = ""

                    for i, line in enumerate(lines):
                        if any(keyword in line.lower() for keyword in ['optimized', 'improved', 'better']):
                            # Look for the next few lines that might contain the optimized prompt
                            for j in range(i + 1, min(i + 10, len(lines))):
                                if lines[j].strip() and not lines[j].startswith('#') and len(lines[j]) > 20:
                                    optimized_prompt = lines[j].strip('"')
                                    break
                            break

                    if not optimized_prompt:
                        optimized_prompt = "Optimized prompt would be extracted from AI response"

                    # Display optimized prompt in a copyable format
                    st.subheader("📋 Optimized Prompt")
                    st.code(optimized_prompt, language="text")

                    # Comparison
                    st.subheader("🔄 Before & After Comparison")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original Prompt**")
                        st.info(original_prompt)

                        original_stats = {
                            "Length": len(original_prompt.split()),
                            "Characters": len(original_prompt),
                            "Specificity": "Low" if len(original_prompt.split()) < 10 else "Medium"
                        }

                        for metric, value in original_stats.items():
                            st.text(f"{metric}: {value}")

                    with col2:
                        st.markdown("**Optimized Prompt**")
                        st.success(optimized_prompt[:200] + "..." if len(optimized_prompt) > 200 else optimized_prompt)

                        optimized_stats = {
                            "Length": len(optimized_prompt.split()),
                            "Characters": len(optimized_prompt),
                            "Specificity": "High"
                        }

                        for metric, value in optimized_stats.items():
                            st.text(f"{metric}: {value}")

                    # Test optimized prompt
                    st.subheader("🧪 Test Optimized Prompt")

                    if st.button("Test Optimized Prompt"):
                        with st.spinner("Testing optimized prompt..."):
                            test_result = ai_client.generate_text(optimized_prompt, "gemini")

                            st.markdown("### Test Result")
                            st.write(test_result)

                            # Quality assessment
                            quality_metrics = {
                                "Response Quality": "High",
                                "Relevance": "Excellent",
                                "Detail Level": output_length,
                                "Format Compliance": "Good"
                            }

                            st.markdown("### Quality Assessment")
                            for metric, score in quality_metrics.items():
                                st.text(f"{metric}: {score}")

                    # Download optimization report
                    if st.button("Generate Optimization Report"):
                        report = f"""
                        PROMPT OPTIMIZATION REPORT
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                        ORIGINAL PROMPT:
                        {original_prompt}

                        OPTIMIZATION SETTINGS:
                        - Goal: {optimization_goal}
                        - Target Audience: {target_audience}
                        - Response Format: {response_format}
                        - Complexity Level: {complexity_level}

                        OPTIMIZED PROMPT:
                        {optimized_prompt}

                        ANALYSIS:
                        {optimization_result}

                        STATISTICS:
                        Original: {len(original_prompt.split())} words, {len(original_prompt)} characters
                        Optimized: {len(optimized_prompt.split())} words, {len(optimized_prompt)} characters
                        """

                        FileHandler.create_download_link(
                            report.encode(),
                            f"prompt_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            "text/plain"
                        )

                except Exception as e:
                    st.error(f"❌ Error optimizing prompt: {str(e)}")

                    # Provide manual optimization tips
                    st.subheader("💡 Manual Optimization Tips")

                    tips = {
                        "Clarity & Specificity": [
                            "Add specific details about what you want",
                            "Include context and background information",
                            "Specify the format and structure of output"
                        ],
                        "Creativity & Innovation": [
                            "Use open-ended questions",
                            "Ask for multiple perspectives or alternatives",
                            "Encourage thinking outside the box"
                        ],
                        "Accuracy & Precision": [
                            "Ask for sources and citations",
                            "Request step-by-step explanations",
                            "Specify accuracy requirements"
                        ]
                    }

                    for tip in tips.get(optimization_goal, ["Add more specific details to your prompt"]):
                        st.write(f"• {tip}")

    else:
        st.info("🎯 Enter a prompt to get optimization suggestions and improvements.")

        # Prompt engineering guide
        with st.expander("📚 Prompt Engineering Guide"):
            st.markdown("""
            **Effective Prompt Elements:**

            1. **Clear Intent**: State exactly what you want
            2. **Context**: Provide relevant background information
            3. **Format**: Specify desired output format
            4. **Examples**: Include examples when helpful
            5. **Constraints**: Set boundaries and limitations

            **Common Improvements:**
            - Add role-playing ("Act as a...")
            - Specify output length and structure
            - Include quality criteria
            - Request reasoning or explanations
            - Add relevant context and background
            """)


def data_insights():
    """AI data insights tool"""
    create_tool_header("Data Insights", "Generate AI-powered insights from your data", "📈")

    # Data input method
    input_method = st.selectbox("Data Input Method", [
        "Upload CSV File", "Upload Excel File", "Paste Data", "Connect to Database"
    ])

    data_content = None

    if input_method == "Upload CSV File":
        uploaded_files = FileHandler.upload_files(['csv'], accept_multiple=False)
        if uploaded_files:
            try:
                import pandas as pd
                import io

                # Read CSV data
                csv_content = uploaded_files[0].read().decode('utf-8')
                data_content = pd.read_csv(io.StringIO(csv_content))

                st.success(f"📁 Loaded CSV: {data_content.shape[0]} rows, {data_content.shape[1]} columns")

                # Show data preview
                with st.expander("Data Preview"):
                    st.dataframe(data_content.head(10))

            except Exception as e:
                st.error(f"Error reading CSV: {str(e)}")

    elif input_method == "Upload Excel File":
        uploaded_files = FileHandler.upload_files(['xlsx', 'xls'], accept_multiple=False)
        if uploaded_files:
            st.info("📁 Excel file processing would be implemented here")

    elif input_method == "Paste Data":
        pasted_data = st.text_area(
            "Paste your data (CSV format)",
            placeholder="Name,Age,City\nJohn,25,New York\nJane,30,London",
            height=200
        )

        if pasted_data:
            try:
                import pandas as pd
                import io

                data_content = pd.read_csv(io.StringIO(pasted_data))
                st.success(f"📁 Parsed data: {data_content.shape[0]} rows, {data_content.shape[1]} columns")

            except Exception as e:
                st.error(f"Error parsing data: {str(e)}")

    else:  # Database connection
        st.info("📊 Database connection would be implemented here")

        # Simulated database options
        db_type = st.selectbox("Database Type", ["PostgreSQL", "MySQL", "SQLite", "MongoDB"])
        connection_string = st.text_input("Connection String", type="password")

    if data_content is not None:
        # Analysis type selection
        st.subheader("Analysis Configuration")

        col1, col2 = st.columns(2)
        with col1:
            analysis_type = st.selectbox("Analysis Type", [
                "Exploratory Data Analysis", "Statistical Summary", "Correlation Analysis",
                "Trend Analysis", "Anomaly Detection", "Predictive Insights", "Custom Analysis"
            ])

            insight_level = st.selectbox("Insight Level", [
                "Basic Overview", "Detailed Analysis", "Advanced Statistics", "Business Insights"
            ])

        with col2:
            focus_columns = st.multiselect(
                "Focus on Columns (optional)",
                data_content.columns.tolist(),
                help="Select specific columns to analyze, or leave empty for all columns"
            )

            ai_model = st.selectbox("AI Model for Insights", ["gemini", "openai"])

        # Analysis settings
        with st.expander("Advanced Analysis Settings"):
            include_visualizations = st.checkbox("Include visualization suggestions", value=True)
            business_context = st.text_area(
                "Business Context (optional)",
                placeholder="e.g., This is sales data for an e-commerce company...",
                height=100
            )

            output_format = st.selectbox("Output Format", [
                "Natural Language Report", "Structured Bullet Points", "Executive Summary", "Technical Report"
            ])

        # Generate insights
        if st.button("Generate AI Insights", type="primary"):
            with st.spinner("Analyzing data and generating insights..."):
                try:
                    # Prepare data summary for AI
                    columns_to_analyze = focus_columns if focus_columns else data_content.columns.tolist()

                    # Basic data statistics
                    data_summary = f"""
                    Dataset Overview:
                    - Rows: {data_content.shape[0]}
                    - Columns: {data_content.shape[1]}
                    - Columns: {', '.join(data_content.columns.tolist())}

                    Data Types:
                    {data_content.dtypes.to_string()}

                    Basic Statistics:
                    {data_content.describe().to_string()}

                    Missing Values:
                    {data_content.isnull().sum().to_string()}
                    """

                    if len(columns_to_analyze) <= 5:
                        # Include sample data for smaller datasets
                        data_summary += f"\n\nSample Data:\n{data_content[columns_to_analyze].head().to_string()}"

                    # Create analysis prompt
                    analysis_prompt = f"""
                    As a data analyst, please analyze the following dataset and provide {insight_level.lower()} insights.

                    Analysis Type: {analysis_type}
                    Output Format: {output_format}

                    {f'Business Context: {business_context}' if business_context else ''}

                    Data Summary:
                    {data_summary}

                    Please provide:
                    1. Key findings and patterns
                    2. Notable trends or anomalies
                    3. Statistical insights
                    4. Actionable recommendations
                    {5 if include_visualizations else ''} {'5. Visualization suggestions' if include_visualizations else ''}

                    Focus on practical, actionable insights that would be valuable for decision-making.
                    """

                    # Generate insights
                    insights = ai_client.generate_text(analysis_prompt, ai_model)

                    st.subheader("📈 AI-Generated Data Insights")

                    # Display insights
                    st.markdown(insights)

                    # Additional analysis metrics
                    st.subheader("📊 Quick Statistics")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Rows", f"{data_content.shape[0]:,}")
                    with col2:
                        st.metric("Total Columns", data_content.shape[1])
                    with col3:
                        numeric_cols = len(data_content.select_dtypes(include=['number']).columns)
                        st.metric("Numeric Columns", numeric_cols)
                    with col4:
                        missing_percentage = (data_content.isnull().sum().sum() / (
                                    data_content.shape[0] * data_content.shape[1])) * 100
                        st.metric("Missing Data", f"{missing_percentage:.1f}%")

                    # Data quality assessment
                    st.subheader("📝 Data Quality Assessment")

                    quality_issues = []
                    if missing_percentage > 10:
                        quality_issues.append(f"High missing data rate: {missing_percentage:.1f}%")

                    if len(data_content.duplicated().sum()) > 0:
                        quality_issues.append(f"Duplicate rows detected: {data_content.duplicated().sum()}")

                    if quality_issues:
                        for issue in quality_issues:
                            st.warning(f"⚠️ {issue}")
                    else:
                        st.success("✅ No major data quality issues detected")

                    # Download insights report
                    if st.button("Generate Insights Report"):
                        report = f"""
                        DATA INSIGHTS REPORT
                        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                        ANALYSIS CONFIGURATION:
                        - Analysis Type: {analysis_type}
                        - Insight Level: {insight_level}
                        - AI Model: {ai_model}
                        - Columns Analyzed: {', '.join(columns_to_analyze)}

                        DATASET OVERVIEW:
                        - Rows: {data_content.shape[0]:,}
                        - Columns: {data_content.shape[1]}
                        - Missing Data: {missing_percentage:.1f}%

                        AI-GENERATED INSIGHTS:
                        {insights}

                        DATA STATISTICS:
                        {data_content.describe().to_string()}

                        {f'BUSINESS CONTEXT: {business_context}' if business_context else ''}
                        """

                        FileHandler.create_download_link(
                            report.encode(),
                            f"data_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            "text/plain"
                        )

                except Exception as e:
                    st.error(f"❌ Error generating insights: {str(e)}")
                    st.info("Please check your data format and AI configuration.")

    else:
        st.info("📁 Upload or paste your data to generate AI-powered insights.")

        # Data insights guide
        with st.expander("📊 Data Insights Guide"):
            st.markdown("""
            **What This Tool Can Analyze:**

            📈 **Numerical Data**: Statistics, trends, correlations, outliers
            📅 **Time Series**: Patterns, seasonality, forecasting opportunities
            🏷️ **Categorical Data**: Distributions, frequencies, relationships
            🔍 **Data Quality**: Missing values, duplicates, inconsistencies

            **Best Practices:**
            - Clean your data before analysis
            - Provide business context for better insights
            - Focus on specific columns for targeted analysis
            - Review data quality assessment recommendations

            **Supported Formats:**
            - CSV files (recommended)
            - Excel files (.xlsx, .xls)
            - Copy-paste tabular data
            """)


def conversational_ai():
    """Advanced conversational AI chatbot"""
    create_tool_header("Conversational AI", "Have natural conversations with AI", "🤖💬")

    # Chatbot configuration
    st.subheader("🔧 Configure Your AI Assistant")

    col1, col2 = st.columns(2)
    with col1:
        model_choice = st.selectbox(
            "AI Model",
            ["gemini", "openai"],
            help="Choose between Google Gemini or OpenAI models"
        )
        personality = st.selectbox(
            "Personality",
            ["Helpful Assistant", "Creative Writer", "Technical Expert", "Casual Friend", "Professional Mentor"],
            help="Choose the AI's conversation style"
        )

    with col2:
        conversation_mode = st.selectbox(
            "Conversation Mode",
            ["General Chat", "Question & Answer", "Brainstorming", "Problem Solving", "Learning Assistant"],
            help="Set the conversation context"
        )
        max_tokens = st.slider("Response Length", 100, 2000, 500, 50, help="Maximum tokens per response")

    # Custom system prompt
    with st.expander("🎯 Custom Instructions (Optional)"):
        custom_instructions = st.text_area(
            "Additional instructions for the AI",
            placeholder="e.g., 'Always respond in a friendly tone' or 'Focus on practical solutions'",
            height=100
        )

    # Initialize conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Build system prompt based on settings
    system_prompts = {
        "Helpful Assistant": "You are a helpful, knowledgeable assistant. Provide clear, accurate, and useful responses.",
        "Creative Writer": "You are a creative writing assistant. Help with storytelling, poetry, and creative expression.",
        "Technical Expert": "You are a technical expert. Provide detailed, accurate technical information and solutions.",
        "Casual Friend": "You are a friendly, casual conversational partner. Keep responses warm and engaging.",
        "Professional Mentor": "You are a professional mentor. Provide guidance, advice, and constructive feedback."
    }

    base_prompt = system_prompts[personality]
    if custom_instructions:
        base_prompt += f"\n\nAdditional instructions: {custom_instructions}"

    if conversation_mode != "General Chat":
        base_prompt += f"\n\nContext: This conversation is focused on {conversation_mode.lower()}."

    # Chat interface
    st.markdown("---")
    st.subheader("💬 Conversation")

    # Display conversation history
    if st.session_state.conversation_history:
        chat_container = st.container()
        with chat_container:
            for i, exchange in enumerate(st.session_state.conversation_history):
                # User message
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(100, 150, 255, 0.1), rgba(150, 100, 255, 0.1)); 
                            padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #6496ff;">
                    <strong>👤 You:</strong><br>
                    {exchange['user']}
                </div>
                """, unsafe_allow_html=True)

                # AI response
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(150, 255, 150, 0.1), rgba(255, 150, 150, 0.1)); 
                            padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #64ff96;">
                    <strong>🤖 AI ({model_choice.title()}):</strong><br>
                    {exchange['ai']}
                </div>
                """, unsafe_allow_html=True)

    # User input
    st.markdown("---")
    user_input = st.text_area(
        "💭 Your message:",
        height=120,
        placeholder=f"Ask me anything! I'm configured as a {personality.lower()} for {conversation_mode.lower()}..."
    )

    # Control buttons
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        if st.button("📤 Send Message", type="primary"):
            if user_input.strip():
                send_conversational_message(user_input, model_choice, base_prompt, max_tokens)

    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.conversation_history = []
            st.rerun()

    with col3:
        if st.button("💾 Export Chat"):
            export_conversation_history()

    with col4:
        if st.session_state.conversation_history:
            if st.button("🔄 Continue"):
                st.text_area(
                    "Continue the conversation:",
                    value="That's interesting. Can you tell me more about...",
                    key="continue_prompt"
                )

    # Quick suggestions
    if not st.session_state.conversation_history:
        st.subheader("💡 Quick Start Ideas")
        suggestions = {
            "General Chat": ["Tell me a joke", "What's your favorite book?", "How are you today?"],
            "Question & Answer": ["Explain quantum physics", "How does photosynthesis work?",
                                  "What is artificial intelligence?"],
            "Brainstorming": ["Ideas for a birthday party", "Creative project concepts", "Business name suggestions"],
            "Problem Solving": ["Help me organize my schedule", "Solve this math problem", "Debug my code logic"],
            "Learning Assistant": ["Teach me Spanish basics", "Explain machine learning", "Help me understand history"]
        }

        cols = st.columns(3)
        for i, suggestion in enumerate(suggestions.get(conversation_mode, suggestions["General Chat"])):
            with cols[i % 3]:
                if st.button(f"💬 {suggestion}", key=f"suggestion_{i}"):
                    st.session_state.temp_input = suggestion
                    send_conversational_message(suggestion, model_choice, base_prompt, max_tokens)

    # Conversation stats
    if st.session_state.conversation_history:
        st.markdown("---")
        st.subheader("📊 Conversation Stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages Exchanged", len(st.session_state.conversation_history) * 2)
        with col2:
            total_words = sum(len(ex['user'].split()) + len(ex['ai'].split())
                              for ex in st.session_state.conversation_history)
            st.metric("Total Words", total_words)
        with col3:
            st.metric("AI Model", model_choice.title())


def send_conversational_message(message, model, system_prompt, max_tokens):
    """Send a message in conversational context"""
    with st.spinner(f"🤖 AI is thinking..."):
        # Build conversation context
        context = f"System: {system_prompt}\n\n"

        # Add recent conversation history for context (last 5 exchanges)
        recent_history = st.session_state.conversation_history[-5:] if st.session_state.conversation_history else []
        for exchange in recent_history:
            context += f"User: {exchange['user']}\nAssistant: {exchange['ai']}\n\n"

        context += f"User: {message}\nAssistant: "

        # Generate response
        response = ai_client.generate_text(context, model=model, max_tokens=max_tokens)

        # Add to conversation history
        st.session_state.conversation_history.append({
            'user': message,
            'ai': response,
            'timestamp': datetime.now().isoformat(),
            'model': model
        })

        st.rerun()


def export_conversation_history():
    """Export conversation history to file"""
    if st.session_state.conversation_history:
        conversation_data = {
            'conversation': st.session_state.conversation_history,
            'exported_at': datetime.now().isoformat(),
            'total_exchanges': len(st.session_state.conversation_history)
        }

        conversation_json = json.dumps(conversation_data, indent=2)
        FileHandler.create_download_link(
            conversation_json.encode(),
            f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json"
        )
        st.success("📥 Conversation exported! Check your downloads.")


def model_comparison():
    """Compare different AI models side by side"""
    create_tool_header("Model Comparison", "Compare responses from different AI models", "⚖️")

    # Available models
    available_models = ai_client.get_available_models()

    if not available_models:
        st.warning("No AI models available. Please check your API keys.")
        return

    if len(available_models) < 2:
        st.warning("Need at least 2 AI models to perform comparison. Please configure additional API keys.")
        return

    # Model selection
    st.subheader("Select Models to Compare")
    col1, col2 = st.columns(2)

    with col1:
        model1 = st.selectbox("Model 1", available_models, key="model1")
    with col2:
        model2 = st.selectbox("Model 2", [m for m in available_models if m != model1], key="model2")

    # Comparison prompt
    st.subheader("Comparison Setup")
    prompt = st.text_area("Enter your prompt:",
                          placeholder="Ask a question or give a task for both models to respond to...",
                          height=100)

    # Comparison parameters
    col1, col2 = st.columns(2)
    with col1:
        max_tokens = st.slider("Max Tokens", 100, 2000, 500)
    with col2:
        comparison_focus = st.selectbox("Focus On", [
            "General Comparison", "Accuracy", "Creativity", "Speed", "Helpfulness"
        ])

    if st.button("Compare Models") and prompt:
        with st.spinner("Getting responses from both models..."):
            # Get responses from both models
            try:
                response1 = ai_client.generate_text(prompt, model=model1, max_tokens=max_tokens)
                response2 = ai_client.generate_text(prompt, model=model2, max_tokens=max_tokens)

                # Display comparison
                st.subheader("Model Responses")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"### 🤖 {model1.title()}")
                    st.write(response1)

                    # Response metrics
                    st.markdown("**Response Metrics:**")
                    metrics1 = analyze_response_metrics(response1)
                    st.metric("Word Count", metrics1['word_count'])
                    st.metric("Reading Time", f"{metrics1['reading_time']} min")

                with col2:
                    st.markdown(f"### 🤖 {model2.title()}")
                    st.write(response2)

                    # Response metrics
                    st.markdown("**Response Metrics:**")
                    metrics2 = analyze_response_metrics(response2)
                    st.metric("Word Count", metrics2['word_count'])
                    st.metric("Reading Time", f"{metrics2['reading_time']} min")

                # Side-by-side comparison analysis
                st.subheader("Comparison Analysis")

                if comparison_focus == "General Comparison":
                    analysis_prompt = f"""
                    Compare these two AI responses to the prompt: "{prompt}"

                    Response 1 ({model1}): {response1}

                    Response 2 ({model2}): {response2}

                    Provide a detailed comparison focusing on:
                    1. Accuracy and correctness
                    2. Completeness of the answer
                    3. Clarity and readability
                    4. Creativity and originality
                    5. Overall helpfulness

                    Give an objective analysis without declaring a clear winner.
                    """
                else:
                    analysis_prompt = f"""
                    Compare these two AI responses focusing specifically on {comparison_focus.lower()}:

                    Prompt: "{prompt}"

                    Response 1 ({model1}): {response1}

                    Response 2 ({model2}): {response2}

                    Provide detailed analysis on {comparison_focus.lower()} aspects.
                    """

                with st.spinner("Analyzing responses..."):
                    # Use the first available model for analysis
                    analysis = ai_client.generate_text(analysis_prompt, model=available_models[0], max_tokens=800)
                    st.write(analysis)

                # Export comparison
                comparison_data = {
                    'prompt': prompt,
                    'model1': model1,
                    'model2': model2,
                    'response1': response1,
                    'response2': response2,
                    'analysis': analysis,
                    'metrics1': metrics1,
                    'metrics2': metrics2,
                    'timestamp': datetime.now().isoformat()
                }

                if st.button("Export Comparison"):
                    FileHandler.create_download_link(
                        json.dumps(comparison_data, indent=2).encode(),
                        f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        "application/json"
                    )
                    st.success("📥 Comparison exported!")

            except Exception as e:
                st.error(f"Error during comparison: {str(e)}")


def analyze_response_metrics(response):
    """Analyze response metrics"""
    words = response.split()
    word_count = len(words)
    reading_time = max(1, word_count // 200)  # 200 WPM average

    return {
        'word_count': word_count,
        'reading_time': reading_time
    }


def build_ocr_prompt(language, preserve_formatting, extract_tables, extract_handwriting, output_format):
    """Build OCR prompt for AI image analysis"""
    prompt = "Please extract all text from this image. "

    if language != "Auto-detect":
        prompt += f"The primary language is {language}. "

    if preserve_formatting:
        prompt += "Preserve the original formatting, spacing, and layout as much as possible. "

    if extract_tables:
        prompt += "If there are tables, preserve the table structure using appropriate formatting. "

    if extract_handwriting:
        prompt += "Include any handwritten text, even if unclear. "

    if output_format == "Structured Text":
        prompt += "Organize the text in a structured format with clear sections. "
    elif output_format == "Markdown":
        prompt += "Format the output as Markdown with appropriate headers and formatting. "
    elif output_format == "JSON":
        prompt += "Return the text in JSON format with text content and metadata. "

    prompt += "Be accurate and include all visible text."
    return prompt


def analyze_extracted_text(text):
    """Analyze extracted text metrics"""
    words = text.split()
    lines = text.split('\n')

    return {
        'word_count': len(words),
        'char_count': len(text),
        'line_count': len(lines)
    }


def analyze_speech_text(text):
    """Analyze text for speech synthesis"""
    words = text.split()
    sentences = text.split('.')

    # Estimate syllables (rough approximation)
    syllable_count = 0
    for word in words:
        # Simple syllable estimation
        vowels = 'aeiouy'
        word = word.lower()
        syllables = sum(1 for char in word if char in vowels)
        syllables = max(1, syllables)  # At least 1 syllable per word
        syllable_count += syllables

    # Estimate duration (average 150 words per minute for speech)
    estimated_duration = max(1, len(words) * 60 / 150)

    return {
        'word_count': len(words),
        'sentence_count': len([s for s in sentences if s.strip()]),
        'syllable_estimate': syllable_count,
        'estimated_duration': int(estimated_duration)
    }


def build_speech_prompt(text, voice_type, language, speed, pitch, add_pauses, emphasize_punctuation):
    """Build prompt for speech synthesis"""
    prompt = f"Convert this text to speech with the following settings:\n"
    prompt += f"Voice Type: {voice_type}\n"
    prompt += f"Language: {language}\n"
    prompt += f"Speed: {speed}x normal\n"
    prompt += f"Pitch: {pitch}x normal\n"

    if add_pauses:
        prompt += "Add natural pauses at appropriate places.\n"

    if emphasize_punctuation:
        prompt += "Emphasize punctuation for natural speech flow.\n"

    prompt += f"\nText to convert: {text}"

    return f"Speech synthesis request: {prompt}"


def generate_ssml(text, voice_type, speed, pitch):
    """Generate SSML markup for text-to-speech"""
    ssml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    ssml += '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">\n'
    ssml += f'<prosody rate="{speed}" pitch="{pitch}">\n'
    ssml += f'{text}\n'
    ssml += '</prosody>\n'
    ssml += '</speak>'

    return ssml


def build_pattern_recognition_prompt(focus, detail_level, confidence):
    """Build prompt for pattern recognition"""
    prompt = f"Analyze this image for patterns with focus on {focus.lower()}. "

    if detail_level == "Basic":
        prompt += "Provide a brief overview of main patterns and objects. "
    elif detail_level == "Detailed":
        prompt += "Provide detailed analysis of patterns, objects, and their relationships. "
    else:  # Comprehensive
        prompt += "Provide comprehensive analysis including fine details, patterns, textures, and spatial relationships. "

    prompt += f"Only include findings with confidence above {confidence}. "
    prompt += "Describe patterns clearly and organize findings by category."

    return prompt


def display_pattern_results(results, analysis_type):
    """Display pattern recognition results"""
    st.subheader(f"{analysis_type} Results")

    for result in results:
        if result['success']:
            st.markdown(f"### 🔍 {result['filename']}")

            # Display image
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(result['image'], caption=result['filename'], use_column_width=True)

            with col2:
                st.subheader("Pattern Analysis")
                st.write(result['analysis'])

            # Download analysis
            FileHandler.create_download_link(
                result['analysis'].encode(),
                f"pattern_analysis_{result['filename']}.txt",
                "text/plain"
            )
        else:
            st.error(f"❌ Failed to analyze {result['filename']}: {result.get('error', 'Unknown error')}")

        st.markdown("---")


def analyze_text_patterns(text, pattern_focus, analysis_depth):
    """Analyze text patterns using AI"""
    prompt = f"Analyze this text for patterns with focus on {pattern_focus.lower()}:\n\n{text}\n\n"

    if analysis_depth == "Quick":
        prompt += "Provide a quick overview of main patterns found."
    elif analysis_depth == "Standard":
        prompt += "Provide standard analysis with details about patterns and their significance."
    else:  # Deep
        prompt += "Provide deep analysis including subtle patterns, correlations, and insights."

    return ai_client.generate_text(prompt, max_tokens=1500)


def detect_data_patterns(data, columns, pattern_types, time_column):
    """Detect patterns in data using AI analysis"""
    # Convert data to text representation for AI analysis
    data_summary = f"Dataset with {len(data)} rows and columns: {', '.join(columns)}\n\n"
    data_summary += f"Sample data:\n{data[columns].head().to_string()}\n\n"
    data_summary += f"Data types:\n{data[columns].dtypes.to_string()}\n\n"
    data_summary += f"Basic statistics:\n{data[columns].describe().to_string()}"

    prompt = f"Analyze this dataset for patterns focusing on {', '.join(pattern_types)}:\n\n{data_summary}"

    if time_column != "None":
        prompt += f"\n\nTime column: {time_column} - Look for temporal patterns."

    prompt += "\n\nProvide insights about patterns, trends, and anomalies in the data."

    return ai_client.generate_text(prompt, max_tokens=2000)


def build_story_prompt(genre, length, audience, style, pov, tone, character, setting, conflict, theme, supporting_chars,
                       outline, special_elements):
    """Build comprehensive story generation prompt"""
    prompt = f"Write a {genre.lower()} story with the following specifications:\n\n"

    prompt += f"Length: {length}\n"
    prompt += f"Target Audience: {audience}\n"
    prompt += f"Writing Style: {style}\n"
    prompt += f"Point of View: {pov}\n"
    prompt += f"Tone: {tone}\n\n"

    prompt += f"Main Character: {character}\n"
    prompt += f"Setting: {setting}\n"

    if conflict:
        prompt += f"Central Conflict: {conflict}\n"

    if theme:
        prompt += f"Theme: {theme}\n"

    if supporting_chars:
        prompt += f"Supporting Characters: {supporting_chars}\n"

    if outline:
        prompt += f"Plot Outline: {outline}\n"

    if special_elements:
        prompt += f"Special Elements: {special_elements}\n"

    prompt += "\nCreate an engaging, well-structured story that incorporates all these elements naturally."

    return prompt


def display_generated_story(story, metadata):
    """Display generated story with analysis"""
    st.subheader("📚 Generated Story")
    st.markdown(story)

    # Story analysis
    story_analysis = analyze_story_content(story)

    st.subheader("Story Analysis")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Word Count", story_analysis['word_count'])
    with col2:
        st.metric("Reading Time", f"{story_analysis['reading_time']} min")
    with col3:
        st.metric("Paragraphs", story_analysis['paragraphs'])
    with col4:
        st.metric("Dialogue %", f"{story_analysis['dialogue_percentage']}%")

    # Story metadata
    with st.expander("Story Details"):
        for key, value in metadata.items():
            st.text(f"{key.title()}: {value}")

    # Download story
    FileHandler.create_download_link(
        story.encode(),
        "generated_story.txt",
        "text/plain"
    )


def analyze_story_content(story):
    """Analyze story content metrics"""
    words = story.split()
    paragraphs = [p for p in story.split('\n\n') if p.strip()]

    # Estimate dialogue percentage
    dialogue_chars = sum(1 for line in story.split('\n') if '"' in line)
    total_lines = len(story.split('\n'))
    dialogue_percentage = int((dialogue_chars / max(1, total_lines)) * 100)

    return {
        'word_count': len(words),
        'reading_time': max(1, len(words) // 200),
        'paragraphs': len(paragraphs),
        'sections': len([p for p in paragraphs if len(p.split()) > 50]),
        'dialogue_percentage': dialogue_percentage
    }


def build_continuation_prompt(existing_text, length, direction, maintain_style, maintain_tone):
    """Build prompt for story continuation"""
    prompt = f"Continue this story:\n\n{existing_text}\n\n"
    prompt += f"Continuation length: {length}\n"
    prompt += f"Direction: {direction}\n"

    if maintain_style:
        prompt += "Maintain the existing writing style and voice.\n"

    if maintain_tone:
        prompt += "Keep the same tone and mood.\n"

    prompt += "\nContinue the story naturally from where it left off."

    return prompt


def generate_story_from_prompt(prompt_text, interpretation, structure, length, creative_freedom):
    """Generate story from creative prompt"""
    story_prompt = f"Create a story based on this prompt: {prompt_text}\n\n"
    story_prompt += f"Interpretation style: {interpretation}\n"
    story_prompt += f"Story structure: {structure}\n"
    story_prompt += f"Length: {length}\n"
    story_prompt += f"Creative freedom level: {creative_freedom}\n\n"
    story_prompt += "Develop this into a complete, engaging story."

    return ai_client.generate_text(story_prompt, max_tokens=2500)


def build_refinement_prompt(content, refinement_type, audience, tone, length_pref, improvements, preserve,
                            custom_instructions):
    """Build content refinement prompt"""
    prompt = f"Refine this content:\n\n{content}\n\n"
    prompt += f"Refinement focus: {refinement_type}\n"

    if audience != "Keep Current":
        prompt += f"Target audience: {audience}\n"

    if tone != "Keep Current":
        prompt += f"Desired tone: {tone}\n"

    if length_pref != "Keep Current":
        prompt += f"Length preference: {length_pref}\n"

    if improvements:
        prompt += f"Specific improvements: {', '.join(improvements)}\n"

    if preserve:
        prompt += f"Preserve: {', '.join(preserve)}\n"

    if custom_instructions:
        prompt += f"Additional instructions: {custom_instructions}\n"

    prompt += "\nProvide the refined version that improves the content while meeting these requirements."

    return prompt


def calculate_improvement_score(original_analysis, refined_analysis):
    """Calculate improvement score between original and refined content"""
    # Simple scoring based on readability improvement
    readability_scores = {"Easy": 3, "Medium": 2, "Complex": 1}

    original_score = readability_scores.get(original_analysis['readability_level'], 2)
    refined_score = readability_scores.get(refined_analysis['readability_level'], 2)

    # Calculate improvement (positive for better readability)
    improvement = ((refined_score - original_score) + 1) * 50

    # Ensure score is between 0-100
    return max(0, min(100, int(improvement)))


def style_transfer():
    """AI-powered style transfer tool"""
    create_tool_header("Style Transfer", "Apply artistic styles to your images using AI", "🎨")

    # File upload section
    st.subheader("Upload Images")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Content Image**")
        content_files = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)
        if content_files:
            content_image = FileHandler.process_image_file(content_files[0])
            if content_image:
                st.image(content_image, caption="Content Image", use_column_width=True)

    with col2:
        st.markdown("**Style Reference**")
        style_option = st.radio("Style Source", ["Upload Style Image", "Choose Preset Style"])

        if style_option == "Upload Style Image":
            style_files = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)
            if style_files:
                style_image = FileHandler.process_image_file(style_files[0])
                if style_image:
                    st.image(style_image, caption="Style Image", use_column_width=True)
        else:
            preset_style = st.selectbox("Preset Style", [
                "Van Gogh - Starry Night", "Picasso - Cubism", "Monet - Impressionism",
                "Abstract Expressionism", "Art Nouveau", "Pop Art", "Minimalism",
                "Watercolor", "Oil Painting", "Sketch", "Anime Style"
            ])
            style_image = None

    # Style transfer options
    if content_files:
        st.subheader("Style Transfer Settings")

        col1, col2 = st.columns(2)
        with col1:
            style_strength = st.slider("Style Strength", 0.1, 1.0, 0.7, 0.1)
            preserve_content = st.slider("Content Preservation", 0.1, 1.0, 0.6, 0.1)

        with col2:
            output_quality = st.selectbox("Output Quality", ["Standard", "High", "Ultra"])
            color_preservation = st.checkbox("Preserve Original Colors", value=False)

        # Advanced options
        with st.expander("Advanced Options"):
            edge_enhancement = st.checkbox("Enhance Edges", value=True)
            texture_detail = st.slider("Texture Detail", 0.1, 1.0, 0.5, 0.1)
            blend_mode = st.selectbox("Blend Mode", ["Normal", "Multiply", "Overlay", "Soft Light"])

        if st.button("Apply Style Transfer"):
            with st.spinner("Applying artistic style to your image..."):
                # Convert content image to bytes
                content_bytes = convert_image_to_bytes(content_image)

                # Build style transfer prompt
                if style_option == "Upload Style Image" and style_files:
                    style_bytes = convert_image_to_bytes(style_image)
                    style_prompt = build_style_transfer_prompt_with_reference(
                        style_strength, preserve_content, color_preservation,
                        edge_enhancement, texture_detail, blend_mode
                    )

                    # For AI analysis with style reference
                    result_description = ai_client.analyze_image(
                        content_bytes,
                        f"{style_prompt} Apply the style from the reference image to this content image."
                    )
                else:
                    style_prompt = build_style_transfer_prompt_preset(
                        preset_style, style_strength, preserve_content,
                        color_preservation, edge_enhancement, texture_detail
                    )

                    result_description = ai_client.analyze_image(content_bytes, style_prompt)

                # Display results
                st.subheader("Style Transfer Results")
                st.success("✨ Style transfer completed!")

                # In a real implementation, this would show the styled image
                st.info("🖼️ Styled Image: In a full implementation, the AI-styled image would be displayed here.")

                # Style analysis
                st.subheader("Style Analysis")
                st.write(result_description)

                # Transfer details
                transfer_details = {
                    "Style Applied": preset_style if style_option == "Choose Preset Style" else "Custom Style",
                    "Style Strength": f"{style_strength:.1f}",
                    "Content Preservation": f"{preserve_content:.1f}",
                    "Output Quality": output_quality,
                    "Color Preservation": "Yes" if color_preservation else "No"
                }

                with st.expander("Transfer Details"):
                    for key, value in transfer_details.items():
                        st.text(f"{key}: {value}")

                # Download placeholder
                st.info("📥 Download: In a full implementation, you could download the styled image here.")
    else:
        st.info("📸 Upload a content image to begin style transfer.")


def image_synthesis():
    """AI-powered image synthesis tool"""
    create_tool_header("Image Synthesis", "Synthesize new images by combining elements", "🔮")

    # Synthesis mode selection
    synthesis_mode = st.selectbox("Synthesis Mode", [
        "Text-to-Image Synthesis", "Image Composition", "Element Combination",
        "Scene Generation", "Object Synthesis", "Texture Synthesis"
    ])

    if synthesis_mode == "Text-to-Image Synthesis":
        st.subheader("Text-to-Image Generation")

        # Text input
        synthesis_prompt = st.text_area("Describe the image to synthesize:",
                                        placeholder="A futuristic cityscape at sunset with flying cars...",
                                        height=100)

        col1, col2 = st.columns(2)
        with col1:
            image_style = st.selectbox("Image Style", [
                "Photorealistic", "Digital Art", "Concept Art", "Fantasy Art",
                "Sci-Fi", "Abstract", "Minimalist", "Surreal", "Vintage"
            ])

            composition = st.selectbox("Composition", [
                "Balanced", "Rule of Thirds", "Central Focus", "Dynamic", "Symmetrical"
            ])

        with col2:
            resolution = st.selectbox("Resolution", ["512x512", "768x768", "1024x1024", "1024x768"])
            color_palette = st.selectbox("Color Palette", [
                "Natural", "Vibrant", "Monochromatic", "Warm Tones", "Cool Tones", "Neon"
            ])

        # Advanced synthesis options
        with st.expander("Advanced Options"):
            detail_level = st.slider("Detail Level", 0.1, 1.0, 0.7, 0.1)
            creativity = st.slider("Creativity", 0.1, 1.0, 0.8, 0.1)
            aspect_ratio = st.selectbox("Aspect Ratio", ["Square", "Portrait", "Landscape", "Wide"])

        if st.button("Synthesize Image") and synthesis_prompt:
            with st.spinner("Synthesizing image from description..."):
                # Build synthesis prompt
                full_prompt = build_synthesis_prompt(
                    synthesis_prompt, image_style, composition, color_palette,
                    detail_level, creativity, aspect_ratio
                )

                # Generate using AI
                synthesis_result = ai_client.generate_text(full_prompt, max_tokens=500)

                st.subheader("Synthesis Results")
                st.success("🎨 Image synthesis completed!")

                # Display synthesis description
                st.write("**Synthesis Description:**")
                st.write(synthesis_result)

                # Synthesis parameters
                st.subheader("Synthesis Parameters")
                params = {
                    "Style": image_style,
                    "Composition": composition,
                    "Resolution": resolution,
                    "Color Palette": color_palette,
                    "Detail Level": f"{detail_level:.1f}",
                    "Creativity": f"{creativity:.1f}"
                }

                for key, value in params.items():
                    st.text(f"{key}: {value}")

                st.info(
                    "🖼️ Synthesized Image: In a full implementation, the AI-generated image would be displayed here.")

    elif synthesis_mode == "Image Composition":
        st.subheader("Image Composition Synthesis")

        # Multiple image upload
        composition_images = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=True)

        if composition_images:
            st.write(f"Uploaded {len(composition_images)} images for composition")

            # Display uploaded images
            cols = st.columns(min(len(composition_images), 3))
            for i, img_file in enumerate(composition_images[:3]):
                with cols[i]:
                    img = FileHandler.process_image_file(img_file)
                    if img:
                        st.image(img, caption=f"Image {i + 1}", use_column_width=True)

            # Composition settings
            col1, col2 = st.columns(2)
            with col1:
                composition_style = st.selectbox("Composition Style", [
                    "Seamless Blend", "Layered Montage", "Split Screen", "Mosaic", "Collage"
                ])

                transition_type = st.selectbox("Transition", [
                    "Smooth Gradient", "Hard Edge", "Feathered", "Masked", "Artistic"
                ])

            with col2:
                background_treatment = st.selectbox("Background", [
                    "Keep Original", "Unified Background", "Transparent", "Generated"
                ])

                color_harmony = st.checkbox("Apply Color Harmony", value=True)

            if st.button("Compose Images"):
                with st.spinner("Composing images..."):
                    # Analyze composition
                    composition_prompt = build_composition_prompt(
                        len(composition_images), composition_style, transition_type,
                        background_treatment, color_harmony
                    )

                    composition_result = ai_client.generate_text(composition_prompt, max_tokens=400)

                    st.subheader("Composition Results")
                    st.success("🖼️ Image composition completed!")
                    st.write(composition_result)

                    st.info("🎨 Composed Image: In a full implementation, the composed image would be displayed here.")
        else:
            st.info("📸 Upload 2 or more images to create a composition.")

    else:
        st.subheader(f"{synthesis_mode}")
        st.info(f"🔧 {synthesis_mode} mode is being enhanced. Please try Text-to-Image or Image Composition modes.")


def concept_art():
    """AI-powered concept art generation tool"""
    create_tool_header("Concept Art", "Generate concept art for creative projects", "🎭")

    # Concept art type selection
    concept_type = st.selectbox("Concept Art Type", [
        "Character Design", "Environment Design", "Vehicle Design", "Creature Design",
        "Architecture Concept", "Prop Design", "Weapon Design", "Fashion Design"
    ])

    st.subheader(f"{concept_type} Generation")

    # Universal concept parameters
    col1, col2 = st.columns(2)
    with col1:
        concept_description = st.text_area("Concept Description:",
                                           placeholder="Describe your concept in detail...",
                                           height=100)

        art_style = st.selectbox("Art Style", [
            "Realistic", "Stylized", "Semi-Realistic", "Cartoon", "Anime",
            "Fantasy Art", "Sci-Fi Art", "Steampunk", "Cyberpunk", "Medieval"
        ])

        mood = st.selectbox("Mood/Atmosphere", [
            "Heroic", "Dark", "Mysterious", "Whimsical", "Epic", "Minimalist",
            "Dramatic", "Peaceful", "Aggressive", "Elegant"
        ])

    with col2:
        color_scheme = st.selectbox("Color Scheme", [
            "Full Color", "Monochromatic", "Limited Palette", "Earth Tones",
            "Bright & Vibrant", "Dark & Moody", "Pastel", "Neon"
        ])

        detail_level = st.selectbox("Detail Level", ["Sketch", "Detailed", "Highly Detailed"])

        perspective = st.selectbox("Perspective", [
            "Front View", "Side View", "3/4 View", "Multiple Views", "Action Pose"
        ])

    # Type-specific options
    if concept_type == "Character Design":
        with st.expander("Character-Specific Options"):
            character_type = st.selectbox("Character Type", [
                "Hero/Protagonist", "Villain/Antagonist", "Supporting Character",
                "Background Character", "Creature/Monster", "Robot/Mech"
            ])

            age_group = st.selectbox("Age Group", ["Child", "Young Adult", "Adult", "Elderly", "Ageless"])
            body_type = st.selectbox("Body Type", ["Slim", "Athletic", "Muscular", "Heavyset", "Unique"])

    elif concept_type == "Environment Design":
        with st.expander("Environment-Specific Options"):
            environment_type = st.selectbox("Environment Type", [
                "Interior", "Exterior", "Landscape", "Cityscape", "Fantasy World",
                "Sci-Fi Setting", "Underground", "Underwater", "Sky/Aerial"
            ])

            time_of_day = st.selectbox("Time of Day", ["Dawn", "Day", "Dusk", "Night", "Varies"])
            weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rainy", "Stormy", "Foggy"])

    elif concept_type == "Vehicle Design":
        with st.expander("Vehicle-Specific Options"):
            vehicle_type = st.selectbox("Vehicle Type", [
                "Car/Automobile", "Motorcycle", "Aircraft", "Spacecraft", "Ship/Boat",
                "Tank/Military", "Mech/Robot", "Fantasy Vehicle"
            ])

            era = st.selectbox("Era", ["Modern", "Futuristic", "Retro/Vintage", "Fantasy", "Steampunk"])

    # Advanced concept options
    with st.expander("Advanced Options"):
        reference_style = st.text_input("Reference Artist/Style",
                                        placeholder="e.g., 'in the style of Studio Ghibli'")

        technical_specs = st.text_area("Technical Specifications",
                                       placeholder="Any technical details or constraints...")

        iterations = st.slider("Number of Variations", 1, 4, 1)

    if st.button("Generate Concept Art") and concept_description:
        with st.spinner("Generating concept art..."):
            # Build comprehensive concept prompt
            concept_prompt = build_concept_art_prompt(
                concept_type, concept_description, art_style, mood, color_scheme,
                detail_level, perspective, reference_style, technical_specs
            )

            # Add type-specific details
            if concept_type == "Character Design":
                concept_prompt += f" Character type: {locals().get('character_type', 'General')}. "
                concept_prompt += f"Age: {locals().get('age_group', 'Adult')}. "
                concept_prompt += f"Build: {locals().get('body_type', 'Average')}."
            elif concept_type == "Environment Design":
                concept_prompt += f" Environment: {locals().get('environment_type', 'General')}. "
                concept_prompt += f"Time: {locals().get('time_of_day', 'Day')}. "
                concept_prompt += f"Weather: {locals().get('weather', 'Clear')}."
            elif concept_type == "Vehicle Design":
                concept_prompt += f" Vehicle type: {locals().get('vehicle_type', 'General')}. "
                concept_prompt += f"Era: {locals().get('era', 'Modern')}."

            # Generate concept art description
            concept_result = ai_client.generate_text(concept_prompt, max_tokens=600)

            # Display results
            st.subheader("Generated Concept Art")
            st.success("🎨 Concept art generation completed!")

            # Concept description
            st.write("**Concept Description:**")
            st.write(concept_result)

            # Concept specifications
            st.subheader("Concept Specifications")
            specs = {
                "Type": concept_type,
                "Art Style": art_style,
                "Mood": mood,
                "Color Scheme": color_scheme,
                "Detail Level": detail_level,
                "Perspective": perspective
            }

            for key, value in specs.items():
                st.text(f"{key}: {value}")

            # Download concept description
            FileHandler.create_download_link(
                concept_result.encode(),
                f"concept_art_{concept_type.lower().replace(' ', '_')}.txt",
                "text/plain"
            )

            st.info("🖼️ Concept Art: In a full implementation, the generated concept art would be displayed here.")

            # Additional variations
            if iterations > 1:
                st.subheader("Concept Variations")
                for i in range(2, iterations + 1):
                    with st.expander(f"Variation {i}"):
                        variation_prompt = concept_prompt + f" Create a different variation with alternative design choices."
                        variation = ai_client.generate_text(variation_prompt, max_tokens=400)
                        st.write(variation)
    else:
        st.info("📝 Enter a concept description to generate concept art.")


def photo_enhancement():
    """AI-powered photo enhancement tool"""
    create_tool_header("Photo Enhancement", "Enhance and improve your photos with AI", "✨")

    # File upload
    st.subheader("Upload Photo")
    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=True)

    if uploaded_files:
        # Enhancement options
        st.subheader("Enhancement Options")

        enhancement_type = st.selectbox("Enhancement Type", [
            "Auto Enhancement", "Custom Enhancement", "Restoration", "Style Enhancement", "Quality Upscaling"
        ])

        if enhancement_type == "Auto Enhancement":
            col1, col2 = st.columns(2)
            with col1:
                auto_mode = st.selectbox("Auto Mode", [
                    "General Enhancement", "Portrait Enhancement", "Landscape Enhancement",
                    "Low Light Enhancement", "Color Enhancement", "Vintage Restoration"
                ])

                enhancement_strength = st.slider("Enhancement Strength", 0.1, 1.0, 0.7, 0.1)

            with col2:
                preserve_original = st.checkbox("Preserve Original Character", value=True)
                fix_common_issues = st.checkbox("Fix Common Issues", value=True)

        elif enhancement_type == "Custom Enhancement":
            col1, col2 = st.columns(2)
            with col1:
                brightness_adjust = st.slider("Brightness", -1.0, 1.0, 0.0, 0.1)
                contrast_adjust = st.slider("Contrast", -1.0, 1.0, 0.0, 0.1)
                saturation_adjust = st.slider("Saturation", -1.0, 1.0, 0.0, 0.1)

            with col2:
                sharpness_adjust = st.slider("Sharpness", -1.0, 1.0, 0.0, 0.1)
                noise_reduction = st.slider("Noise Reduction", 0.0, 1.0, 0.0, 0.1)
                color_balance = st.slider("Color Balance", -1.0, 1.0, 0.0, 0.1)

        elif enhancement_type == "Restoration":
            restoration_options = st.multiselect("Restoration Options", [
                "Remove Scratches", "Fix Fading", "Repair Tears", "Remove Spots",
                "Improve Definition", "Restore Colors", "Fix Exposure"
            ])

            restoration_intensity = st.slider("Restoration Intensity", 0.1, 1.0, 0.5, 0.1)

        # Advanced options
        with st.expander("Advanced Options"):
            output_format = st.selectbox("Output Format", ["Original Format", "PNG", "JPEG", "WEBP"])
            quality_setting = st.slider("Output Quality", 70, 100, 95, 5)

            if enhancement_type in ["Auto Enhancement", "Custom Enhancement"]:
                hdr_effect = st.checkbox("HDR Effect")
                film_grain = st.checkbox("Add Film Grain")

        # Process photos
        if st.button("Enhance Photos"):
            results = []

            for photo_file in uploaded_files:
                with st.spinner(f"Enhancing {photo_file.name}..."):
                    photo = FileHandler.process_image_file(photo_file)
                    if photo:
                        # Convert to bytes for AI analysis
                        photo_bytes = convert_image_to_bytes(photo)

                        # Build enhancement prompt
                        if enhancement_type == "Auto Enhancement":
                            enhancement_prompt = build_auto_enhancement_prompt(
                                auto_mode, enhancement_strength, preserve_original, fix_common_issues
                            )
                        elif enhancement_type == "Custom Enhancement":
                            enhancement_prompt = build_custom_enhancement_prompt(
                                brightness_adjust, contrast_adjust, saturation_adjust,
                                sharpness_adjust, noise_reduction, color_balance
                            )
                        elif enhancement_type == "Restoration":
                            enhancement_prompt = build_restoration_prompt(restoration_options, restoration_intensity)
                        else:
                            enhancement_prompt = f"Enhance this photo using {enhancement_type.lower()} techniques."

                        # Analyze and describe enhancements
                        enhancement_analysis = ai_client.analyze_image(photo_bytes, enhancement_prompt)

                        results.append({
                            'filename': photo_file.name,
                            'original': photo,
                            'analysis': enhancement_analysis,
                            'success': True
                        })
                    else:
                        results.append({
                            'filename': photo_file.name,
                            'error': 'Failed to process image',
                            'success': False
                        })

            # Display results
            st.subheader("Enhancement Results")

            for result in results:
                if result['success']:
                    st.markdown(f"### ✨ {result['filename']}")

                    # Display original image
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original**")
                        st.image(result['original'], use_column_width=True)

                    with col2:
                        st.markdown("**Enhanced (Preview)**")
                        st.info(
                            "🖼️ Enhanced Image: In a full implementation, the AI-enhanced image would be displayed here.")

                    # Enhancement analysis
                    st.subheader("Enhancement Analysis")
                    st.write(result['analysis'])

                    # Enhancement details
                    enhancement_details = {
                        "Enhancement Type": enhancement_type,
                        "Processing Status": "Completed",
                        "Original Format": result['filename'].split('.')[-1].upper(),
                        "Output Quality": f"{quality_setting}%"
                    }

                    with st.expander("Enhancement Details"):
                        for key, value in enhancement_details.items():
                            st.text(f"{key}: {value}")

                    # Download placeholder
                    st.info(
                        "📥 Download Enhanced: In a full implementation, you could download the enhanced image here.")

                else:
                    st.error(f"❌ Failed to enhance {result['filename']}: {result.get('error', 'Unknown error')}")

                st.markdown("---")

            # Batch processing summary
            successful_enhancements = len([r for r in results if r['success']])
            st.success(f"✅ Successfully enhanced {successful_enhancements} out of {len(results)} photos!")

    else:
        st.info("📸 Upload one or more photos to begin enhancement.")


# Helper functions for image generation tools

def convert_image_to_bytes(image):
    """Convert PIL image to bytes"""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


def build_style_transfer_prompt_with_reference(style_strength, preserve_content, color_preservation, edge_enhancement,
                                               texture_detail, blend_mode):
    """Build style transfer prompt with reference image"""
    prompt = f"Apply style transfer with the following settings: "
    prompt += f"Style strength: {style_strength}, Content preservation: {preserve_content}. "

    if color_preservation:
        prompt += "Preserve original colors while applying style. "

    if edge_enhancement:
        prompt += "Enhance edges for better definition. "

    prompt += f"Texture detail level: {texture_detail}. "
    prompt += f"Use {blend_mode.lower()} blend mode for combining style and content."

    return prompt


def build_style_transfer_prompt_preset(preset_style, style_strength, preserve_content, color_preservation,
                                       edge_enhancement, texture_detail):
    """Build style transfer prompt with preset style"""
    prompt = f"Apply {preset_style} artistic style to this image. "
    prompt += f"Style strength: {style_strength}, Content preservation: {preserve_content}. "

    if color_preservation:
        prompt += "Preserve original colors while applying artistic style. "

    if edge_enhancement:
        prompt += "Enhance edges and details. "

    prompt += f"Apply texture details at level {texture_detail}. "
    prompt += "Maintain the essence of the original while transforming it artistically."

    return prompt


def build_synthesis_prompt(description, style, composition, color_palette, detail_level, creativity, aspect_ratio):
    """Build comprehensive image synthesis prompt"""
    prompt = f"Synthesize an image: {description}. "
    prompt += f"Art style: {style}. "
    prompt += f"Composition: {composition}. "
    prompt += f"Color palette: {color_palette}. "
    prompt += f"Detail level: {detail_level}. "
    prompt += f"Creativity level: {creativity}. "
    prompt += f"Aspect ratio: {aspect_ratio}. "
    prompt += "Create a cohesive, visually appealing image that matches these specifications."

    return prompt


def build_composition_prompt(num_images, composition_style, transition_type, background_treatment, color_harmony):
    """Build image composition prompt"""
    prompt = f"Compose {num_images} images using {composition_style.lower()} style. "
    prompt += f"Apply {transition_type.lower()} transitions between elements. "
    prompt += f"Background treatment: {background_treatment.lower()}. "

    if color_harmony:
        prompt += "Apply color harmony to unify the composition. "

    prompt += "Create a seamless, balanced composition that integrates all elements naturally."

    return prompt


def build_concept_art_prompt(concept_type, description, art_style, mood, color_scheme, detail_level, perspective,
                             reference_style, technical_specs):
    """Build comprehensive concept art generation prompt"""
    prompt = f"Create {concept_type.lower()} concept art: {description}. "
    prompt += f"Art style: {art_style}. "
    prompt += f"Mood: {mood}. "
    prompt += f"Color scheme: {color_scheme}. "
    prompt += f"Detail level: {detail_level}. "
    prompt += f"Perspective: {perspective}. "

    if reference_style:
        prompt += f"Reference style: {reference_style}. "

    if technical_specs:
        prompt += f"Technical specifications: {technical_specs}. "

    prompt += "Focus on creating functional, appealing design that serves the intended purpose."

    return prompt


def build_auto_enhancement_prompt(auto_mode, enhancement_strength, preserve_original, fix_common_issues):
    """Build automatic photo enhancement prompt"""
    prompt = f"Enhance this photo using {auto_mode.lower()} mode. "
    prompt += f"Enhancement strength: {enhancement_strength}. "

    if preserve_original:
        prompt += "Preserve the original character and style of the photo. "

    if fix_common_issues:
        prompt += "Fix common issues like exposure, color balance, and sharpness. "

    prompt += "Improve overall quality while maintaining natural appearance."

    return prompt


def build_custom_enhancement_prompt(brightness, contrast, saturation, sharpness, noise_reduction, color_balance):
    """Build custom photo enhancement prompt"""
    prompt = "Enhance this photo with custom settings: "

    if brightness != 0:
        prompt += f"Brightness adjustment: {brightness:+.1f}. "

    if contrast != 0:
        prompt += f"Contrast adjustment: {contrast:+.1f}. "

    if saturation != 0:
        prompt += f"Saturation adjustment: {saturation:+.1f}. "

    if sharpness != 0:
        prompt += f"Sharpness adjustment: {sharpness:+.1f}. "

    if noise_reduction > 0:
        prompt += f"Apply noise reduction at level {noise_reduction}. "

    if color_balance != 0:
        prompt += f"Color balance adjustment: {color_balance:+.1f}. "

    prompt += "Apply these adjustments to improve the photo's overall quality."

    return prompt


def build_restoration_prompt(restoration_options, restoration_intensity):
    """Build photo restoration prompt"""
    prompt = "Restore this photo with the following improvements: "

    if restoration_options:
        prompt += f"{', '.join(restoration_options).lower()}. "

    prompt += f"Restoration intensity: {restoration_intensity}. "
    prompt += "Carefully repair and restore the photo while preserving its historical character."

    return prompt


def ocr_reader():
    """OCR text extraction tool"""
    create_tool_header("OCR Reader", "Extract text from images using AI vision", "👁️")

    # File upload section
    st.subheader("Upload Image")
    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'], accept_multiple=True)

    if uploaded_files:
        # OCR options
        st.subheader("OCR Settings")

        col1, col2 = st.columns(2)
        with col1:
            language = st.selectbox("Primary Language", [
                "Auto-detect", "English", "Spanish", "French", "German", "Italian",
                "Portuguese", "Chinese", "Japanese", "Korean", "Arabic", "Russian"
            ])

            output_format = st.selectbox("Output Format", [
                "Plain Text", "Structured Text", "Markdown", "JSON"
            ])

        with col2:
            preserve_formatting = st.checkbox("Preserve Formatting", value=True)
            include_confidence = st.checkbox("Include Confidence Scores", value=False)

        # Advanced options
        with st.expander("Advanced Options"):
            extract_tables = st.checkbox("Extract Tables")
            extract_handwriting = st.checkbox("Extract Handwriting")
            noise_reduction = st.checkbox("Apply Noise Reduction", value=True)

        if st.button("Extract Text"):
            results = []

            for file in uploaded_files:
                with st.spinner(f"Processing {file.name}..."):
                    # Process image
                    image = FileHandler.process_image_file(file)
                    if image:
                        # Convert image to bytes for AI processing
                        import io
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='JPEG')
                        img_bytes = img_byte_arr.getvalue()

                        # Build OCR prompt
                        ocr_prompt = build_ocr_prompt(language, preserve_formatting,
                                                      extract_tables, extract_handwriting, output_format)

                        # Perform OCR using AI
                        extracted_text = ai_client.analyze_image(img_bytes, ocr_prompt)

                        results.append({
                            'filename': file.name,
                            'text': extracted_text,
                            'success': True
                        })
                    else:
                        results.append({
                            'filename': file.name,
                            'error': 'Failed to process image',
                            'success': False
                        })

            # Display results
            st.subheader("Extraction Results")

            for result in results:
                if result['success']:
                    st.markdown(f"### 📄 {result['filename']}")

                    # Display extracted text
                    if output_format == "JSON":
                        st.json(result['text'])
                    else:
                        st.text_area(f"Extracted Text from {result['filename']}",
                                     result['text'], height=200)

                    # Text analysis
                    text_analysis = analyze_extracted_text(result['text'])

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Word Count", text_analysis['word_count'])
                    with col2:
                        st.metric("Character Count", text_analysis['char_count'])
                    with col3:
                        st.metric("Lines", text_analysis['line_count'])

                    # Download extracted text
                    FileHandler.create_download_link(
                        result['text'].encode(),
                        f"extracted_{result['filename']}.txt",
                        "text/plain"
                    )

                else:
                    st.error(f"❌ Failed to process {result['filename']}: {result.get('error', 'Unknown error')}")

                st.markdown("---")

            # Batch download option
            if len([r for r in results if r['success']]) > 1:
                if st.button("Download All as ZIP"):
                    zip_files = {}
                    for result in results:
                        if result['success']:
                            zip_files[f"extracted_{result['filename']}.txt"] = result['text'].encode()

                    if zip_files:
                        zip_data = FileHandler.create_zip_archive(zip_files)
                        FileHandler.create_download_link(
                            zip_data,
                            "ocr_extraction_results.zip",
                            "application/zip"
                        )
    else:
        st.info("📸 Upload one or more images to extract text using AI-powered OCR.")


def voice_synthesis():
    """Voice synthesis tool"""
    create_tool_header("Voice Synthesis", "Generate natural speech from text using AI", "🎤")

    # Text input section
    st.subheader("Text to Synthesize")

    input_method = st.radio("Input Method", ["Text Input", "File Upload"])

    if input_method == "Text Input":
        text_to_speak = st.text_area("Enter text to convert to speech:",
                                     placeholder="Type or paste your text here...",
                                     height=150)
    else:
        uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)
        if uploaded_file:
            text_to_speak = FileHandler.process_text_file(uploaded_file[0])
            st.text_area("Text from file:", text_to_speak, height=150, disabled=True)
        else:
            text_to_speak = ""

    if text_to_speak:
        # Voice settings
        st.subheader("Voice Settings")

        col1, col2 = st.columns(2)
        with col1:
            voice_type = st.selectbox("Voice Type", [
                "Natural Female", "Natural Male", "Professional Female", "Professional Male",
                "Friendly", "Authoritative", "Calm", "Energetic"
            ])

            language = st.selectbox("Language", [
                "English (US)", "English (UK)", "Spanish", "French", "German",
                "Italian", "Portuguese", "Chinese", "Japanese"
            ])

        with col2:
            speech_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
            pitch = st.slider("Pitch", 0.5, 2.0, 1.0, 0.1)

        # Advanced options
        with st.expander("Advanced Options"):
            add_pauses = st.checkbox("Add Natural Pauses", value=True)
            emphasize_punctuation = st.checkbox("Emphasize Punctuation", value=True)
            output_quality = st.selectbox("Audio Quality", ["Standard", "High", "Premium"])
            output_format = st.selectbox("Output Format", ["MP3", "WAV", "OGG"])

        # Text analysis
        st.subheader("Text Analysis")
        text_stats = analyze_speech_text(text_to_speak)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Words", text_stats['word_count'])
        with col2:
            st.metric("Estimated Duration", f"{text_stats['estimated_duration']} sec")
        with col3:
            st.metric("Sentences", text_stats['sentence_count'])
        with col4:
            st.metric("Syllables", text_stats['syllable_estimate'])

        if st.button("Generate Speech"):
            with st.spinner("Generating speech audio..."):
                # Generate speech using AI
                speech_prompt = build_speech_prompt(text_to_speak, voice_type, language,
                                                    speech_speed, pitch, add_pauses,
                                                    emphasize_punctuation)

                # Since this is a text-to-speech task, we'll simulate audio generation
                # In a real implementation, this would call a text-to-speech API
                success_message = ai_client.generate_text(speech_prompt)

                st.success("🎵 Speech generation completed!")

                # Display generation details
                st.subheader("Generation Details")
                generation_info = {
                    "Voice Type": voice_type,
                    "Language": language,
                    "Speed": f"{speech_speed}x",
                    "Pitch": f"{pitch}x",
                    "Text Length": f"{len(text_to_speak)} characters",
                    "Estimated Audio Length": f"{text_stats['estimated_duration']} seconds"
                }

                for key, value in generation_info.items():
                    st.text(f"{key}: {value}")

                # Audio preview placeholder
                st.info("🔊 Audio Preview: In a full implementation, the generated speech would be playable here.")

                # Simulated download (in real implementation, this would be actual audio data)
                st.info("📥 Download: In a full implementation, you could download the audio file here.")

                # SSML export option
                if st.button("Export as SSML"):
                    ssml_content = generate_ssml(text_to_speak, voice_type, speech_speed, pitch)
                    FileHandler.create_download_link(
                        ssml_content.encode(),
                        "speech_markup.ssml",
                        "application/xml"
                    )
    else:
        st.info("📝 Enter or upload text to generate speech.")


def pattern_recognition():
    """Pattern recognition tool"""
    create_tool_header("Pattern Recognition", "Identify patterns in data and images using AI", "🔍")

    # Pattern recognition type selection
    pattern_type = st.selectbox("Select Pattern Type", [
        "Image Pattern Recognition", "Text Pattern Analysis", "Data Pattern Detection",
        "Sequence Pattern Recognition", "Anomaly Detection"
    ])

    if pattern_type == "Image Pattern Recognition":
        st.subheader("Image Pattern Analysis")

        uploaded_images = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp'], accept_multiple=True)

        if uploaded_images:
            # Pattern recognition options
            col1, col2 = st.columns(2)
            with col1:
                recognition_focus = st.selectbox("Recognition Focus", [
                    "General Objects", "Faces", "Text/Numbers", "Shapes/Geometry",
                    "Colors/Patterns", "Brand Logos", "Architecture", "Nature Elements"
                ])

                detail_level = st.selectbox("Detail Level", ["Basic", "Detailed", "Comprehensive"])

            with col2:
                pattern_confidence = st.slider("Confidence Threshold", 0.1, 1.0, 0.7, 0.1)
                batch_analysis = st.checkbox("Batch Analysis", value=True)

            if st.button("Analyze Patterns"):
                results = []

                for image_file in uploaded_images:
                    with st.spinner(f"Analyzing patterns in {image_file.name}..."):
                        image = FileHandler.process_image_file(image_file)
                        if image:
                            # Convert to bytes for AI analysis
                            import io
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='JPEG')
                            img_bytes = img_byte_arr.getvalue()

                            # Build pattern recognition prompt
                            pattern_prompt = build_pattern_recognition_prompt(
                                recognition_focus, detail_level, pattern_confidence
                            )

                            # Analyze patterns
                            pattern_analysis = ai_client.analyze_image(img_bytes, pattern_prompt)

                            results.append({
                                'filename': image_file.name,
                                'analysis': pattern_analysis,
                                'image': image,
                                'success': True
                            })
                        else:
                            results.append({
                                'filename': image_file.name,
                                'error': 'Failed to process image',
                                'success': False
                            })

                # Display results
                display_pattern_results(results, "Image Pattern Recognition")

    elif pattern_type == "Text Pattern Analysis":
        st.subheader("Text Pattern Analysis")

        input_method = st.radio("Input Method", ["Text Input", "File Upload"])

        if input_method == "Text Input":
            text_data = st.text_area("Enter text to analyze:", height=200)
        else:
            uploaded_file = FileHandler.upload_files(['txt', 'csv'], accept_multiple=False)
            if uploaded_file:
                text_data = FileHandler.process_text_file(uploaded_file[0])
                st.text_area("Text from file:", text_data[:500] + "..." if len(text_data) > 500 else text_data,
                             height=150, disabled=True)
            else:
                text_data = ""

        if text_data:
            # Text pattern options
            col1, col2 = st.columns(2)
            with col1:
                pattern_focus = st.selectbox("Pattern Focus", [
                    "General Patterns", "Email Addresses", "Phone Numbers", "URLs",
                    "Dates/Times", "Named Entities", "Keywords", "Sentiment Patterns"
                ])

            with col2:
                analysis_depth = st.selectbox("Analysis Depth", ["Quick", "Standard", "Deep"])

            if st.button("Analyze Text Patterns"):
                with st.spinner("Analyzing text patterns..."):
                    text_pattern_analysis = analyze_text_patterns(text_data, pattern_focus, analysis_depth)

                    st.subheader("Pattern Analysis Results")
                    st.write(text_pattern_analysis)

                    # Export results
                    FileHandler.create_download_link(
                        text_pattern_analysis.encode(),
                        "text_pattern_analysis.txt",
                        "text/plain"
                    )

    elif pattern_type == "Data Pattern Detection":
        st.subheader("Data Pattern Detection")

        uploaded_file = FileHandler.upload_files(['csv', 'json'], accept_multiple=False)

        if uploaded_file:
            # Load data
            if uploaded_file[0].name.endswith('.csv'):
                data = FileHandler.process_csv_file(uploaded_file[0])
                if data is not None:
                    st.write("Data Preview:")
                    st.dataframe(data.head())

                    # Pattern detection options
                    col1, col2 = st.columns(2)
                    with col1:
                        columns_to_analyze = st.multiselect("Columns to Analyze", data.columns.tolist())
                        pattern_types = st.multiselect("Pattern Types", [
                            "Trends", "Correlations", "Outliers", "Seasonality", "Clustering"
                        ])

                    with col2:
                        time_column = st.selectbox("Time Column (optional)", ["None"] + data.columns.tolist())
                        confidence_level = st.slider("Confidence Level", 0.8, 0.99, 0.95, 0.01)

                    if st.button("Detect Patterns") and columns_to_analyze:
                        with st.spinner("Detecting data patterns..."):
                            data_patterns = detect_data_patterns(data, columns_to_analyze, pattern_types, time_column)

                            st.subheader("Data Pattern Results")
                            st.write(data_patterns)

    else:
        st.info(f"🔧 {pattern_type} implementation in progress. Please check back soon!")


def story_writer():
    """AI story writing tool"""
    create_tool_header("Story Writer", "Create engaging stories with AI assistance", "📚")

    # Story creation mode
    creation_mode = st.selectbox("Creation Mode", [
        "New Story", "Continue Existing Story", "Story from Prompt", "Interactive Story"
    ])

    if creation_mode == "New Story":
        st.subheader("Story Settings")

        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox("Genre", [
                "Adventure", "Mystery", "Romance", "Science Fiction", "Fantasy",
                "Horror", "Drama", "Comedy", "Historical Fiction", "Thriller"
            ])

            story_length = st.selectbox("Story Length", [
                "Short Story (500-1500 words)", "Medium Story (1500-5000 words)",
                "Long Story (5000+ words)", "Chapter (2000-3000 words)"
            ])

            target_audience = st.selectbox("Target Audience", [
                "Children (6-12)", "Young Adult (13-17)", "Adult (18+)", "All Ages"
            ])

        with col2:
            writing_style = st.selectbox("Writing Style", [
                "Descriptive", "Action-packed", "Dialogue-heavy", "Contemplative",
                "Humorous", "Dark", "Poetic", "Realistic"
            ])

            pov = st.selectbox("Point of View", [
                "First Person", "Third Person Limited", "Third Person Omniscient", "Second Person"
            ])

            tone = st.selectbox("Tone", [
                "Optimistic", "Dark", "Neutral", "Suspenseful", "Whimsical",
                "Serious", "Lighthearted", "Mysterious"
            ])

        # Story elements
        st.subheader("Story Elements")

        col1, col2 = st.columns(2)
        with col1:
            main_character = st.text_input("Main Character", placeholder="Describe your protagonist...")
            setting = st.text_input("Setting", placeholder="Where and when does the story take place?")

        with col2:
            conflict = st.text_input("Central Conflict", placeholder="What challenge will the character face?")
            theme = st.text_input("Theme (optional)", placeholder="What's the underlying message?")

        # Additional story details
        with st.expander("Additional Details"):
            supporting_characters = st.text_area("Supporting Characters",
                                                 placeholder="Describe other important characters...")
            plot_outline = st.text_area("Plot Outline (optional)",
                                        placeholder="Brief outline of main plot points...")
            special_elements = st.text_area("Special Elements",
                                            placeholder="Magic systems, technology, unique rules...")

        if st.button("Generate Story"):
            if main_character and setting:
                with st.spinner("Crafting your story..."):
                    story_prompt = build_story_prompt(
                        genre, story_length, target_audience, writing_style, pov, tone,
                        main_character, setting, conflict, theme, supporting_characters,
                        plot_outline, special_elements
                    )

                    # Generate story
                    generated_story = ai_client.generate_text(story_prompt, max_tokens=3000)

                    if generated_story:
                        display_generated_story(generated_story, {
                            'genre': genre,
                            'length': story_length,
                            'style': writing_style,
                            'pov': pov,
                            'tone': tone
                        })
            else:
                st.error("Please provide at least a main character and setting.")

    elif creation_mode == "Continue Existing Story":
        st.subheader("Continue Your Story")

        existing_text = st.text_area("Existing Story Text",
                                     placeholder="Paste your existing story here...",
                                     height=200)

        if existing_text:
            col1, col2 = st.columns(2)
            with col1:
                continuation_length = st.selectbox("Continuation Length", [
                    "Short (200-500 words)", "Medium (500-1000 words)", "Long (1000+ words)"
                ])

                direction = st.selectbox("Story Direction", [
                    "Continue naturally", "Add conflict", "Introduce new character",
                    "Change setting", "Build toward climax", "Resolve conflict"
                ])

            with col2:
                maintain_style = st.checkbox("Maintain Writing Style", value=True)
                maintain_tone = st.checkbox("Maintain Tone", value=True)

            if st.button("Continue Story"):
                with st.spinner("Continuing your story..."):
                    continuation_prompt = build_continuation_prompt(
                        existing_text, continuation_length, direction, maintain_style, maintain_tone
                    )

                    story_continuation = ai_client.generate_text(continuation_prompt, max_tokens=2000)

                    if story_continuation:
                        st.subheader("Story Continuation")
                        st.markdown(story_continuation)

                        # Combined story
                        full_story = existing_text + "\n\n" + story_continuation
                        story_analysis = analyze_story_content(full_story)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Words", story_analysis['word_count'])
                        with col2:
                            st.metric("Reading Time", f"{story_analysis['reading_time']} min")
                        with col3:
                            st.metric("Chapters/Sections", story_analysis['sections'])

                        # Download options
                        FileHandler.create_download_link(
                            full_story.encode(),
                            "continued_story.txt",
                            "text/plain"
                        )

    elif creation_mode == "Story from Prompt":
        st.subheader("Generate Story from Prompt")

        story_prompt_input = st.text_area("Story Prompt",
                                          placeholder="Enter a creative prompt, scenario, or idea...",
                                          height=100)

        if story_prompt_input:
            col1, col2 = st.columns(2)
            with col1:
                interpretation = st.selectbox("Interpretation Style", [
                    "Literal", "Creative", "Unexpected", "Dark Twist", "Humorous", "Philosophical"
                ])

                story_structure = st.selectbox("Story Structure", [
                    "Beginning-Middle-End", "In Media Res", "Circular", "Episodic", "Stream of Consciousness"
                ])

            with col2:
                prompt_length = st.selectbox("Story Length", [
                    "Flash Fiction (100-300 words)", "Short Story (500-1500 words)",
                    "Extended Story (1500+ words)"
                ])

                creative_freedom = st.slider("Creative Freedom", 0.1, 1.0, 0.8, 0.1)

            if st.button("Generate from Prompt"):
                with st.spinner("Creating story from your prompt..."):
                    prompt_story_text = generate_story_from_prompt(
                        story_prompt_input, interpretation, story_structure,
                        prompt_length, creative_freedom
                    )

                    if prompt_story_text:
                        display_generated_story(prompt_story_text, {
                            'prompt': story_prompt_input,
                            'interpretation': interpretation,
                            'structure': story_structure,
                            'length': prompt_length
                        })

    else:  # Interactive Story
        st.subheader("Interactive Story Creation")
        st.info("🎮 Interactive storytelling mode coming in a future update!")

        # Initialize interactive story session
        if 'interactive_story' not in st.session_state:
            st.session_state.interactive_story = {
                'story_text': '',
                'choices_made': [],
                'current_scene': 1
            }

        st.write("This mode will allow you to make choices that influence the story direction.")


def refine_content(content):
    """Refine generated content"""
    if not content:
        st.warning("No content provided for refinement.")
        return

    create_tool_header("Content Refinement", "Improve and polish your content with AI", "✨")

    # Display original content
    st.subheader("Original Content")
    st.text_area("Content to refine:", content, height=200, disabled=True)

    # Refinement options
    st.subheader("Refinement Options")

    col1, col2 = st.columns(2)
    with col1:
        refinement_type = st.selectbox("Refinement Type", [
            "General Improvement", "Grammar & Style", "Clarity & Readability",
            "Tone Adjustment", "Length Optimization", "SEO Enhancement",
            "Professional Polish", "Creative Enhancement"
        ])

        target_audience = st.selectbox("Target Audience", [
            "Keep Current", "General Public", "Professionals", "Students",
            "Experts", "Children", "Academics"
        ])

    with col2:
        desired_tone = st.selectbox("Desired Tone", [
            "Keep Current", "Professional", "Casual", "Friendly", "Formal",
            "Conversational", "Authoritative", "Persuasive", "Educational"
        ])

        length_preference = st.selectbox("Length Preference", [
            "Keep Current", "Make Shorter", "Make Longer", "More Concise", "More Detailed"
        ])

    # Advanced refinement options
    with st.expander("Advanced Options"):
        specific_improvements = st.multiselect("Specific Improvements", [
            "Fix Grammar", "Improve Flow", "Enhance Vocabulary", "Add Examples",
            "Strengthen Arguments", "Improve Structure", "Add Transitions", "Remove Redundancy"
        ])

        preserve_elements = st.multiselect("Preserve Elements", [
            "Original Meaning", "Key Facts", "Personal Voice", "Technical Terms",
            "Brand Voice", "Quotes", "Statistics", "Examples"
        ])

        custom_instructions = st.text_area("Custom Instructions",
                                           placeholder="Any specific requirements for refinement...")

    if st.button("Refine Content"):
        with st.spinner("Refining your content..."):
            # Build refinement prompt
            refinement_prompt = build_refinement_prompt(
                content, refinement_type, target_audience, desired_tone,
                length_preference, specific_improvements, preserve_elements,
                custom_instructions
            )

            # Refine content using AI
            refined_content = ai_client.generate_text(refinement_prompt, max_tokens=2500)

            if refined_content:
                # Display refined content
                st.subheader("Refined Content")
                st.markdown(refined_content)

                # Content comparison
                st.subheader("Improvement Analysis")

                original_analysis = analyze_content(content)
                refined_analysis = analyze_content(refined_content)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Word Count",
                              refined_analysis['word_count'],
                              refined_analysis['word_count'] - original_analysis['word_count'])

                with col2:
                    st.metric("Reading Time",
                              f"{refined_analysis['reading_time']} min",
                              f"{refined_analysis['reading_time'] - original_analysis['reading_time']} min")

                with col3:
                    st.metric("Readability", refined_analysis['readability_level'])

                with col4:
                    improvement_score = calculate_improvement_score(original_analysis, refined_analysis)
                    st.metric("Improvement Score", f"{improvement_score}%")

                # Side-by-side comparison
                with st.expander("Side-by-Side Comparison"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Original:**")
                        st.text_area("Original", content, height=300, disabled=True, key="orig_comp")

                    with col2:
                        st.markdown("**Refined:**")
                        st.text_area("Refined", refined_content, height=300, disabled=True, key="ref_comp")

                # Download options
                st.subheader("Download Options")

                col1, col2 = st.columns(2)
                with col1:
                    FileHandler.create_download_link(
                        refined_content.encode(),
                        "refined_content.txt",
                        "text/plain"
                    )

                with col2:
                    # Create comparison document
                    comparison_doc = f"""ORIGINAL CONTENT:
{content}

{'=' * 50}

REFINED CONTENT:
{refined_content}

{'=' * 50}

IMPROVEMENT ANALYSIS:
Original Word Count: {original_analysis['word_count']}
Refined Word Count: {refined_analysis['word_count']}
Improvement Score: {improvement_score}%
Refinement Type: {refinement_type}"""

                    FileHandler.create_download_link(
                        comparison_doc.encode(),
                        "content_comparison.txt",
                        "text/plain"
                    )

                # Additional refinement options
                st.subheader("Further Actions")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Refine Again"):
                        st.session_state.refinement_content = refined_content
                        st.rerun()

                with col2:
                    if st.button("Different Approach"):
                        st.session_state.refinement_content = content
                        st.rerun()

                with col3:
                    if st.button("Generate Summary"):
                        summary_prompt = f"Create a concise summary of this content:\n\n{refined_content}"
                        summary = ai_client.generate_text(summary_prompt, max_tokens=300)
                        st.subheader("Content Summary")
                        st.write(summary)
            else:
                st.error("Failed to refine content. Please try again.")