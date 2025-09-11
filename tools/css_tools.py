
import streamlit as st
import re
import json
import colorsys
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all CSS tools"""

    tool_categories = {
        "CSS Generators": [
            "Gradient Generator", "Shadow Generator", "Border Radius Generator", "Flexbox Generator", "Grid Generator"
        ],
        "CSS Preprocessors": [
            "SASS/SCSS Compiler", "LESS Processor", "Stylus Compiler", "CSS Variables Generator"
        ],
        "CSS Validators": [
            "Syntax Validator", "Property Checker", "Browser Compatibility", "CSS Linter"
        ],
        "CSS Minifiers": [
            "Code Minifier", "Whitespace Remover", "Comment Stripper", "Property Optimizer"
        ],
        "CSS Beautifiers": [
            "Code Formatter", "Indentation Fixer", "Property Organizer", "Structure Improver"
        ],
        "CSS Color Tools": [
            "Color Picker", "Palette Generator", "Color Scheme Creator", "Accessibility Checker"
        ],
        "CSS Layout Tools": [
            "Flexbox Layout", "Grid Layout", "Responsive Layout", "CSS Framework Tools"
        ],
        "CSS Animation Tools": [
            "Keyframe Generator", "Transition Builder", "Animation Preview", "Easing Functions"
        ],
        "CSS Framework Utilities": [
            "Bootstrap Helper", "Tailwind Utilities", "Foundation Tools", "Custom Framework"
        ],
        "CSS Debugging Tools": [
            "Selector Tester", "Specificity Calculator", "Cascade Analyzer", "Property Inspector"
        ]
    }

    selected_category = st.selectbox("Select CSS Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"CSS Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Gradient Generator":
        gradient_generator()
    elif selected_tool == "Shadow Generator":
        shadow_generator()
    elif selected_tool == "Border Radius Generator":
        border_radius_generator()
    elif selected_tool == "Flexbox Generator":
        flexbox_generator()
    elif selected_tool == "Code Minifier":
        css_minifier()
    elif selected_tool == "Code Formatter":
        css_formatter()
    elif selected_tool == "Color Picker":
        css_color_picker()
    elif selected_tool == "Syntax Validator":
        css_validator()
    elif selected_tool == "Keyframe Generator":
        keyframe_generator()
    elif selected_tool == "Selector Tester":
        selector_tester()
    elif selected_tool == "Specificity Calculator":
        specificity_calculator()
    elif selected_tool == "Grid Generator":
        grid_generator()
    elif selected_tool == "Responsive Layout":
        responsive_layout()
    elif selected_tool == "Bootstrap Helper":
        bootstrap_helper()
    elif selected_tool == "Transition Builder":
        transition_builder()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def gradient_generator():
    """CSS gradient generator"""
    create_tool_header("Gradient Generator", "Create beautiful CSS gradients", "🌈")

    gradient_type = st.selectbox("Gradient Type", ["Linear", "Radial", "Conic"])

    # Initialize variables to avoid unbound errors
    direction = "to right"
    shape = "circle"
    position = "center"

    if gradient_type == "Linear":
        direction = st.selectbox("Direction", [
            "to right", "to left", "to top", "to bottom",
            "to top right", "to top left", "to bottom right", "to bottom left",
            "45deg", "90deg", "135deg", "180deg", "270deg"
        ])
    elif gradient_type == "Radial":
        shape = st.selectbox("Shape", ["circle", "ellipse"])
        position = st.selectbox("Position", ["center", "top", "bottom", "left", "right"])

    # Color stops
    st.subheader("Color Stops")

    num_colors = st.slider("Number of colors", 2, 8, 2)
    colors = []
    positions = []

    for i in range(num_colors):
        col1, col2 = st.columns(2)
        with col1:
            color = st.color_picker(f"Color {i + 1}", f"#{'ff0000' if i == 0 else '00ff00' if i == 1 else 'ff00ff'}",
                                    key=f"grad_color_{i}")
            colors.append(color)
        with col2:
            if i == 0:
                position = st.number_input(f"Position {i + 1} (%)", 0, 100, 0, key=f"grad_pos_{i}")
            elif i == num_colors - 1:
                position = st.number_input(f"Position {i + 1} (%)", 0, 100, 100, key=f"grad_pos_{i}")
            else:
                position = st.number_input(f"Position {i + 1} (%)", 0, 100, (100 // (num_colors - 1)) * i,
                                           key=f"grad_pos_{i}")
            positions.append(position)

    # Generate gradient CSS
    if gradient_type == "Linear":
        color_stops = [f"{colors[i]} {positions[i]}%" for i in range(num_colors)]
        gradient_css = f"background: linear-gradient({direction}, {', '.join(color_stops)});"
    elif gradient_type == "Radial":
        color_stops = [f"{colors[i]} {positions[i]}%" for i in range(num_colors)]
        gradient_css = f"background: radial-gradient({shape} at {position}, {', '.join(color_stops)});"
    else:  # Conic
        color_stops = [f"{colors[i]} {positions[i]}%" for i in range(num_colors)]
        gradient_css = f"background: conic-gradient({', '.join(color_stops)});"

    # Display preview
    st.subheader("Preview")
    preview_html = f"""
    <div style="{gradient_css} width: 300px; height: 200px; border: 1px solid #ccc; border-radius: 10px; margin: 20px 0;"></div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # Display CSS code
    st.subheader("CSS Code")
    st.code(gradient_css, language="css")

    # Additional CSS variations
    st.subheader("Complete CSS (with vendor prefixes)")
    complete_css = f"""/* Gradient CSS */
.gradient-element {{
    {gradient_css}
    /* Fallback for older browsers */
    background: {colors[0]};
}}"""

    st.code(complete_css, language="css")

    # Download
    FileHandler.create_download_link(complete_css.encode(), "gradient.css", "text/css")


def shadow_generator():
    """CSS box shadow generator"""
    create_tool_header("Shadow Generator", "Create CSS box shadows", "📦")

    shadow_type = st.selectbox("Shadow Type", ["Box Shadow", "Text Shadow", "Drop Shadow (filter)"])

    # Initialize shadow_css to avoid unbound errors
    shadow_css = ""

    if shadow_type == "Box Shadow":
        st.subheader("Box Shadow Properties")

        col1, col2 = st.columns(2)
        with col1:
            h_offset = st.slider("Horizontal Offset (px)", -100, 100, 10)
            v_offset = st.slider("Vertical Offset (px)", -100, 100, 10)
            blur_radius = st.slider("Blur Radius (px)", 0, 100, 10)
            spread_radius = st.slider("Spread Radius (px)", -100, 100, 0)

        with col2:
            shadow_color = st.color_picker("Shadow Color", "#000000")
            opacity = st.slider("Opacity", 0.0, 1.0, 0.5, 0.1)
            inset = st.checkbox("Inset Shadow")

        # Convert color to rgba
        hex_color = shadow_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        rgba_color = f"rgba({r}, {g}, {b}, {opacity})"

        # Generate shadow CSS
        inset_text = "inset " if inset else ""
        shadow_css = f"box-shadow: {inset_text}{h_offset}px {v_offset}px {blur_radius}px {spread_radius}px {rgba_color};"

        # Preview
        st.subheader("Preview")
        preview_html = f"""
        <div style="width: 200px; height: 150px; background: #f0f0f0; margin: 50px auto; {shadow_css} border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <span style="color: #666;">Preview Box</span>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)

    elif shadow_type == "Text Shadow":
        st.subheader("Text Shadow Properties")

        col1, col2 = st.columns(2)
        with col1:
            h_offset = st.slider("Horizontal Offset (px)", -50, 50, 2)
            v_offset = st.slider("Vertical Offset (px)", -50, 50, 2)
            blur_radius = st.slider("Blur Radius (px)", 0, 50, 4)

        with col2:
            shadow_color = st.color_picker("Shadow Color", "#000000")
            text_color = st.color_picker("Text Color", "#333333")
            font_size = st.slider("Font Size (px)", 16, 72, 36)

        shadow_css = f"text-shadow: {h_offset}px {v_offset}px {blur_radius}px {shadow_color};"

        # Preview
        st.subheader("Preview")
        preview_html = f"""
        <div style="text-align: center; padding: 30px;">
            <h2 style="color: {text_color}; font-size: {font_size}px; {shadow_css} margin: 0;">
                Sample Text
            </h2>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)

    # Display CSS
    st.subheader("CSS Code")
    st.code(shadow_css, language="css")

    FileHandler.create_download_link(shadow_css.encode(), "shadow.css", "text/css")


def border_radius_generator():
    """CSS border radius generator"""
    create_tool_header("Border Radius Generator", "Create custom border radius", "📐")

    mode = st.radio("Mode", ["Simple", "Advanced"])

    if mode == "Simple":
        radius = st.slider("Border Radius (px)", 0, 100, 10)
        border_radius_css = f"border-radius: {radius}px;"
    else:
        st.subheader("Individual Corner Control")

        col1, col2 = st.columns(2)
        with col1:
            top_left = st.slider("Top Left (px)", 0, 100, 10)
            bottom_left = st.slider("Bottom Left (px)", 0, 100, 10)
        with col2:
            top_right = st.slider("Top Right (px)", 0, 100, 10)
            bottom_right = st.slider("Bottom Right (px)", 0, 100, 10)

        border_radius_css = f"border-radius: {top_left}px {top_right}px {bottom_right}px {bottom_left}px;"

    # Preview
    st.subheader("Preview")
    preview_html = f"""
    <div style="width: 200px; height: 150px; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
                margin: 30px auto; {border_radius_css} display: flex; align-items: center; justify-content: center;">
        <span style="color: white; font-weight: bold;">Preview</span>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # CSS Code
    st.subheader("CSS Code")
    st.code(border_radius_css, language="css")

    # Additional examples
    st.subheader("Common Shapes")
    examples = {
        "Circle": "border-radius: 50%;",
        "Pill": "border-radius: 25px;",
        "Rounded Rectangle": "border-radius: 15px;",
        "Leaf": "border-radius: 0 100% 0 100%;"
    }

    for shape, css in examples.items():
        if st.button(f"Use {shape}"):
            st.code(css, language="css")


def flexbox_generator():
    """CSS Flexbox generator"""
    create_tool_header("Flexbox Generator", "Generate CSS Flexbox layouts", "📏")

    st.subheader("Container Properties")

    col1, col2 = st.columns(2)
    with col1:
        flex_direction = st.selectbox("Flex Direction", ["row", "row-reverse", "column", "column-reverse"])
        flex_wrap = st.selectbox("Flex Wrap", ["nowrap", "wrap", "wrap-reverse"])
        justify_content = st.selectbox("Justify Content", [
            "flex-start", "flex-end", "center", "space-between", "space-around", "space-evenly"
        ])

    with col2:
        align_items = st.selectbox("Align Items", [
            "stretch", "flex-start", "flex-end", "center", "baseline"
        ])
        align_content = st.selectbox("Align Content", [
            "stretch", "flex-start", "flex-end", "center", "space-between", "space-around"
        ])
        gap = st.slider("Gap (px)", 0, 50, 10)

    # Generate container CSS
    container_css = f"""display: flex;
flex-direction: {flex_direction};
flex-wrap: {flex_wrap};
justify-content: {justify_content};
align-items: {align_items};
align-content: {align_content};
gap: {gap}px;"""

    # Item properties
    st.subheader("Item Properties")
    num_items = st.slider("Number of Items", 1, 6, 3)

    item_properties = []
    for i in range(num_items):
        with st.expander(f"Item {i + 1} Properties"):
            col1, col2, col3 = st.columns(3)
            with col1:
                flex_grow = st.number_input(f"Flex Grow", 0, 10, 1, key=f"grow_{i}")
            with col2:
                flex_shrink = st.number_input(f"Flex Shrink", 0, 10, 1, key=f"shrink_{i}")
            with col3:
                align_self = st.selectbox(f"Align Self",
                                          ["auto", "flex-start", "flex-end", "center", "baseline", "stretch"],
                                          key=f"align_{i}")

            item_properties.append({
                "flex_grow": flex_grow,
                "flex_shrink": flex_shrink,
                "align_self": align_self
            })

    # Preview
    st.subheader("Preview")

    items_html = ""
    for i, props in enumerate(item_properties):
        item_style = f"""
        flex: {props['flex_grow']} {props['flex_shrink']} auto;
        align-self: {props['align_self']};
        background: hsl({i * 60}, 70%, 60%);
        padding: 20px;
        margin: 5px;
        border-radius: 5px;
        color: white;
        text-align: center;
        """
        items_html += f'<div style="{item_style}">Item {i + 1}</div>'

    preview_html = f"""
    <div style="{container_css} border: 2px dashed #ccc; padding: 20px; min-height: 200px;">
        {items_html}
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # CSS Output
    st.subheader("CSS Code")

    complete_css = f""".flex-container {{
{container_css}
}}

/* Item styles */"""

    for i, props in enumerate(item_properties):
        complete_css += f"""
.flex-item-{i + 1} {{
    flex: {props['flex_grow']} {props['flex_shrink']} auto;
    align-self: {props['align_self']};
}}"""

    st.code(complete_css, language="css")

    FileHandler.create_download_link(complete_css.encode(), "flexbox.css", "text/css")


def css_minifier():
    """CSS minification tool"""
    create_tool_header("CSS Minifier", "Minify CSS code for production", "🗜️")

    # File upload option
    uploaded_file = FileHandler.upload_files(['css'], accept_multiple=False)

    if uploaded_file:
        css_content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded CSS", css_content, height=200, disabled=True)
    else:
        css_content = st.text_area("Enter CSS code to minify:", height=300, value="""/* Sample CSS */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    margin: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
}

.button {
    background: linear-gradient(45deg, #007bff, #0056b3);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}""")

    if css_content:
        # Minification options
        col1, col2 = st.columns(2)
        with col1:
            remove_comments = st.checkbox("Remove Comments", True)
            remove_whitespace = st.checkbox("Remove Whitespace", True)
            remove_empty_rules = st.checkbox("Remove Empty Rules", True)
        with col2:
            merge_selectors = st.checkbox("Merge Identical Selectors", True)
            shorten_colors = st.checkbox("Shorten Color Values", True)
            remove_semicolons = st.checkbox("Remove Last Semicolons", True)

        if st.button("Minify CSS"):
            minified_css = minify_css(css_content, {
                'remove_comments': remove_comments,
                'remove_whitespace': remove_whitespace,
                'remove_empty_rules': remove_empty_rules,
                'merge_selectors': merge_selectors,
                'shorten_colors': shorten_colors,
                'remove_semicolons': remove_semicolons
            })

            # Show results
            st.subheader("Minified CSS")
            st.code(minified_css, language="css")

            # Statistics
            original_size = len(css_content)
            minified_size = len(minified_css)
            reduction = ((original_size - minified_size) / original_size * 100) if original_size > 0 else 0

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Size", f"{original_size:,} bytes")
            with col2:
                st.metric("Minified Size", f"{minified_size:,} bytes")
            with col3:
                st.metric("Size Reduction", f"{reduction:.1f}%")

            FileHandler.create_download_link(minified_css.encode(), "minified.css", "text/css")


def css_formatter():
    """CSS code formatter"""
    create_tool_header("CSS Formatter", "Format and beautify CSS code", "✨")

    # File upload option
    uploaded_file = FileHandler.upload_files(['css'], accept_multiple=False)

    if uploaded_file:
        css_content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded CSS", css_content, height=200, disabled=True)
    else:
        css_content = st.text_area("Enter CSS code to format:", height=300,
                                   value=""".container{display:flex;justify-content:center;align-items:center;padding:20px;margin:10px;}.button{background:#007bff;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;}.button:hover{background:#0056b3;}""")

    if css_content:
        # Formatting options
        col1, col2 = st.columns(2)
        with col1:
            indent_size = st.selectbox("Indent Size", [2, 4, 8], index=1)
            indent_type = st.selectbox("Indent Type", ["Spaces", "Tabs"])
            brace_style = st.selectbox("Brace Style", ["Same Line", "New Line"])
        with col2:
            sort_properties = st.checkbox("Sort Properties Alphabetically", False)
            add_missing_semicolons = st.checkbox("Add Missing Semicolons", True)
            normalize_quotes = st.checkbox("Normalize Quotes", True)

        if st.button("Format CSS"):
            formatted_css = format_css(css_content, {
                'indent_size': indent_size,
                'indent_type': indent_type,
                'brace_style': brace_style,
                'sort_properties': sort_properties,
                'add_missing_semicolons': add_missing_semicolons,
                'normalize_quotes': normalize_quotes
            })

            st.subheader("Formatted CSS")
            st.code(formatted_css, language="css")

            FileHandler.create_download_link(formatted_css.encode(), "formatted.css", "text/css")


def css_color_picker():
    """Advanced CSS color picker and palette generator"""
    create_tool_header("CSS Color Picker", "Pick colors and generate palettes", "🎨")

    tab1, tab2, tab3 = st.tabs(["Color Picker", "Palette Generator", "Color Converter"])

    with tab1:
        st.subheader("Color Selection")

        color = st.color_picker("Pick a color", "#007bff")

        # Convert to different formats
        hex_color = color
        hex_short = shorten_hex_color(hex_color)
        rgb = hex_to_rgb(hex_color)
        hsl = rgb_to_hsl(rgb)

        col1, col2 = st.columns(2)
        with col1:
            st.code(f"HEX: {hex_color}")
            st.code(f"HEX (short): {hex_short}")
            st.code(f"RGB: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
        with col2:
            st.code(f"HSL: hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)")
            st.code(f"CSS Variable: var(--primary-color)")
            st.code(f"RGBA: rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 1)")

        # Color variations
        st.subheader("Color Variations")
        variations = generate_color_variations(hex_color)

        for variation_name, variation_color in variations.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(
                    f'<div style="width:50px;height:30px;background-color:{variation_color};border:1px solid #000;"></div>',
                    unsafe_allow_html=True)
            with col2:
                st.code(f"{variation_name}: {variation_color}")

    with tab2:
        st.subheader("Color Palette Generator")

        base_color = st.color_picker("Base color", "#007bff", key="palette_base")
        palette_type = st.selectbox("Palette Type", [
            "Monochromatic", "Analogous", "Complementary", "Triadic", "Tetradic"
        ])

        if st.button("Generate Palette"):
            palette = generate_color_palette(base_color, palette_type)

            st.subheader(f"{palette_type} Palette")

            # Display palette
            palette_html = '<div style="display: flex; margin: 20px 0;">'
            for i, color in enumerate(palette):
                palette_html += f'''
                <div style="width: 80px; height: 80px; background-color: {color}; 
                           border: 1px solid #ccc; margin-right: 10px; 
                           display: flex; align-items: end; justify-content: center; color: white;">
                    <small style="background: rgba(0,0,0,0.7); padding: 2px 4px; margin: 5px;">{color}</small>
                </div>
                '''
            palette_html += '</div>'

            st.markdown(palette_html, unsafe_allow_html=True)

            # CSS Variables
            css_vars = ":root {\n"
            for i, color in enumerate(palette):
                css_vars += f"  --color-{i + 1}: {color};\n"
            css_vars += "}"

            st.subheader("CSS Variables")
            st.code(css_vars, language="css")

            FileHandler.create_download_link(css_vars.encode(), "color-palette.css", "text/css")

    with tab3:
        st.subheader("Color Format Converter")

        input_format = st.selectbox("Input Format", ["HEX", "RGB", "HSL"])

        if input_format == "HEX":
            hex_input = st.text_input("HEX Color", "#007bff")
            if hex_input:
                try:
                    rgb = hex_to_rgb(hex_input)
                    hsl = rgb_to_hsl(rgb)

                    st.write(f"**RGB**: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
                    st.write(f"**HSL**: hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)")
                except:
                    st.error("Invalid HEX color format")

        elif input_format == "RGB":
            col1, col2, col3 = st.columns(3)
            with col1:
                r = st.number_input("Red", 0, 255, 0)
            with col2:
                g = st.number_input("Green", 0, 255, 123)
            with col3:
                b = st.number_input("Blue", 0, 255, 255)

            hex_result = rgb_to_hex((r, g, b))
            hsl_result = rgb_to_hsl((r, g, b))

            st.write(f"**HEX**: {hex_result}")
            st.write(f"**HSL**: hsl({hsl_result[0]}, {hsl_result[1]}%, {hsl_result[2]}%)")


def css_validator():
    """CSS syntax validator"""
    create_tool_header("CSS Validator", "Validate CSS syntax and properties", "✅")

    # File upload option
    uploaded_file = FileHandler.upload_files(['css'], accept_multiple=False)

    if uploaded_file:
        css_content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded CSS", css_content, height=200, disabled=True)
    else:
        css_content = st.text_area("Enter CSS code to validate:", height=300)

    if css_content and st.button("Validate CSS"):
        validation_results = validate_css(css_content)

        # Display results
        if validation_results['errors']:
            st.subheader("❌ Errors Found")
            for error in validation_results['errors']:
                st.error(f"Line {error['line']}: {error['message']}")

        if validation_results['warnings']:
            st.subheader("⚠️ Warnings")
            for warning in validation_results['warnings']:
                st.warning(f"Line {warning['line']}: {warning['message']}")

        if not validation_results['errors'] and not validation_results['warnings']:
            st.success("✅ No issues found! Your CSS is valid.")

        # Statistics
        st.subheader("Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rules", validation_results['stats']['rules'])
        with col2:
            st.metric("Properties", validation_results['stats']['properties'])
        with col3:
            st.metric("Selectors", validation_results['stats']['selectors'])
        with col4:
            st.metric("Errors", len(validation_results['errors']))


def keyframe_generator():
    """CSS keyframe animation generator"""
    create_tool_header("Keyframe Generator", "Create CSS keyframe animations", "🎬")

    animation_name = st.text_input("Animation Name", "myAnimation")

    # Keyframes
    st.subheader("Animation Keyframes")

    num_keyframes = st.slider("Number of Keyframes", 2, 10, 3)
    keyframes = []

    for i in range(num_keyframes):
        with st.expander(f"Keyframe {i + 1}"):
            col1, col2 = st.columns(2)
            with col1:
                if i == 0:
                    percentage = st.number_input("Percentage", 0, 100, 0, key=f"kf_pct_{i}", disabled=True)
                elif i == num_keyframes - 1:
                    percentage = st.number_input("Percentage", 0, 100, 100, key=f"kf_pct_{i}", disabled=True)
                else:
                    percentage = st.number_input("Percentage", 0, 100, (100 // (num_keyframes - 1)) * i,
                                                 key=f"kf_pct_{i}")

            with col2:
                properties = st.text_area("CSS Properties", "transform: translateX(0px);\nopacity: 1;",
                                          height=100, key=f"kf_props_{i}")

            keyframes.append({
                'percentage': percentage,
                'properties': properties
            })

    # Animation properties
    st.subheader("Animation Properties")
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Duration (seconds)", 0.1, 60.0, 2.0, 0.1)
        iteration_count = st.selectbox("Iteration Count", ["1", "2", "3", "infinite"])
        direction = st.selectbox("Direction", ["normal", "reverse", "alternate", "alternate-reverse"])
    with col2:
        timing_function = st.selectbox("Timing Function", [
            "ease", "ease-in", "ease-out", "ease-in-out", "linear",
            "cubic-bezier(0.25, 0.1, 0.25, 1)"
        ])
        fill_mode = st.selectbox("Fill Mode", ["none", "forwards", "backwards", "both"])
        delay = st.number_input("Delay (seconds)", 0.0, 10.0, 0.0, 0.1)

    # Generate CSS
    if st.button("Generate Animation CSS"):
        # Sort keyframes by percentage
        keyframes.sort(key=lambda x: x['percentage'])

        # Generate keyframes CSS
        keyframes_css = f"@keyframes {animation_name} {{\n"
        for kf in keyframes:
            keyframes_css += f"  {kf['percentage']}% {{\n"
            for prop in kf['properties'].strip().split('\n'):
                if prop.strip():
                    keyframes_css += f"    {prop.strip()}\n"
            keyframes_css += "  }\n"
        keyframes_css += "}"

        # Generate animation property
        animation_css = f"""animation: {animation_name} {duration}s {timing_function} {delay}s {iteration_count} {direction} {fill_mode};"""

        complete_css = f"""{keyframes_css}

.animated-element {{
  {animation_css}
}}"""

        st.subheader("Generated CSS")
        st.code(complete_css, language="css")

        # Preview (simple)
        st.subheader("Preview")
        st.info(
            "Preview functionality would require JavaScript. Use the generated CSS in your project to see the animation.")

        FileHandler.create_download_link(complete_css.encode(), f"{animation_name}.css", "text/css")


# Helper functions
def minify_css(css_content, options):
    """Minify CSS content based on options"""
    result = css_content

    if options['remove_comments']:
        # Remove CSS comments
        result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)

    if options['remove_whitespace']:
        # Remove unnecessary whitespace
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r';\s*}', '}', result)
        result = re.sub(r'{\s*', '{', result)
        result = re.sub(r'}\s*', '}', result)
        result = re.sub(r':\s*', ':', result)
        result = re.sub(r';\s*', ';', result)
        result = result.strip()

    if options['shorten_colors']:
        # Shorten hex colors
        result = re.sub(r'#([0-9a-fA-F])\1([0-9a-fA-F])\2([0-9a-fA-F])\3', r'#\1\2\3', result)

    if options['remove_semicolons']:
        # Remove last semicolon before closing brace
        result = re.sub(r';(\s*})', r'\1', result)

    return result


def format_css(css_content, options):
    """Format CSS content based on options"""
    indent_char = '\t' if options['indent_type'] == 'Tabs' else ' ' * options['indent_size']

    # Basic formatting
    result = css_content

    # Remove existing formatting
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()

    # Add proper spacing and indentation
    formatted_lines = []
    indent_level = 0

    i = 0
    while i < len(result):
        char = result[i]

        if char == '{':
            formatted_lines.append(char)
            if options['brace_style'] == 'New Line':
                formatted_lines.append('\n')
            formatted_lines.append('\n')
            indent_level += 1
        elif char == '}':
            if formatted_lines and formatted_lines[-1] != '\n':
                formatted_lines.append('\n')
            indent_level -= 1
            formatted_lines.append(indent_char * indent_level + char + '\n')
        elif char == ';':
            formatted_lines.append(char + '\n')
        else:
            # Add indentation at start of line
            if formatted_lines and formatted_lines[-1] == '\n':
                formatted_lines.append(indent_char * indent_level)
            formatted_lines.append(char)

        i += 1

    return ''.join(formatted_lines)


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def rgb_to_hsl(rgb):
    """Convert RGB to HSL"""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (int(h * 360), int(s * 100), int(l * 100))


def shorten_hex_color(hex_color):
    """Shorten hex color if possible"""
    if len(hex_color) == 7:
        if hex_color[1] == hex_color[2] and hex_color[3] == hex_color[4] and hex_color[5] == hex_color[6]:
            return f"#{hex_color[1]}{hex_color[3]}{hex_color[5]}"
    return hex_color


def generate_color_variations(base_color):
    """Generate color variations"""
    rgb = hex_to_rgb(base_color)
    variations = {}

    # Lighter variations
    for i, percent in enumerate([20, 40, 60], 1):
        lighter_rgb = tuple(min(255, int(c + (255 - c) * percent / 100)) for c in rgb)
        variations[f"Lighter {percent}%"] = rgb_to_hex(lighter_rgb)

    # Darker variations
    for i, percent in enumerate([20, 40, 60], 1):
        darker_rgb = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        variations[f"Darker {percent}%"] = rgb_to_hex(darker_rgb)

    return variations


def generate_color_palette(base_color, palette_type):
    """Generate color palette based on type"""
    base_rgb = hex_to_rgb(base_color)
    base_hsl = rgb_to_hsl(base_rgb)

    palette = [base_color]

    if palette_type == "Monochromatic":
        # Different lightness values
        for lightness in [30, 50, 70, 90]:
            if lightness != base_hsl[2]:
                new_hsl = (base_hsl[0], base_hsl[1], lightness)
                new_rgb = colorsys.hls_to_rgb(new_hsl[0] / 360, new_hsl[2] / 100, new_hsl[1] / 100)
                new_rgb = tuple(int(c * 255) for c in new_rgb)
                palette.append(rgb_to_hex(new_rgb))

    elif palette_type == "Analogous":
        # Adjacent hues
        for offset in [-30, -15, 15, 30]:
            new_hue = (base_hsl[0] + offset) % 360
            new_hsl = (new_hue, base_hsl[1], base_hsl[2])
            new_rgb = colorsys.hls_to_rgb(new_hsl[0] / 360, new_hsl[2] / 100, new_hsl[1] / 100)
            new_rgb = tuple(int(c * 255) for c in new_rgb)
            palette.append(rgb_to_hex(new_rgb))

    elif palette_type == "Complementary":
        # Opposite hue
        comp_hue = (base_hsl[0] + 180) % 360
        comp_hsl = (comp_hue, base_hsl[1], base_hsl[2])
        comp_rgb = colorsys.hls_to_rgb(comp_hsl[0] / 360, comp_hsl[2] / 100, comp_hsl[1] / 100)
        comp_rgb = tuple(int(c * 255) for c in comp_rgb)
        palette.append(rgb_to_hex(comp_rgb))

        # Add variations
        for lightness in [30, 70]:
            for hue in [base_hsl[0], comp_hue]:
                new_hsl = (hue, base_hsl[1], lightness)
                new_rgb = colorsys.hls_to_rgb(new_hsl[0] / 360, new_hsl[2] / 100, new_hsl[1] / 100)
                new_rgb = tuple(int(c * 255) for c in new_rgb)
                palette.append(rgb_to_hex(new_rgb))

    return list(set(palette))[:6]  # Return unique colors, max 6


def validate_css(css_content):
    """Basic CSS validation"""
    errors = []
    warnings = []
    stats = {'rules': 0, 'properties': 0, 'selectors': 0}

    lines = css_content.split('\n')

    # Basic syntax checking
    brace_count = 0
    in_rule = False

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        if not line or line.startswith('/*'):
            continue

        # Count braces
        open_braces = line.count('{')
        close_braces = line.count('}')
        brace_count += open_braces - close_braces

        if open_braces > 0:
            stats['rules'] += open_braces
            in_rule = True

        if close_braces > 0:
            in_rule = False

        # Check for properties
        if in_rule and ':' in line and not line.endswith('{'):
            stats['properties'] += 1

            # Check for missing semicolon
            if not line.rstrip().endswith(';') and not line.rstrip().endswith('{') and not line.rstrip().endswith('}'):
                warnings.append({
                    'line': line_num,
                    'message': 'Missing semicolon'
                })

        # Check for invalid characters
        if re.search(r'[^\w\s\-_.:;{}()#,>+~\[\]="\'@%/\*]', line):
            errors.append({
                'line': line_num,
                'message': 'Invalid characters detected'
            })

    # Check for unmatched braces
    if brace_count != 0:
        errors.append({
            'line': len(lines),
            'message': f'Unmatched braces (difference: {brace_count})'
        })

    return {
        'errors': errors,
        'warnings': warnings,
        'stats': stats
    }


# Additional placeholder functions for remaining tools
def grid_generator():
    """CSS Grid generator"""
    create_tool_header("CSS Grid Generator", "Create CSS Grid layouts with visual editor", "📊")

    st.subheader("Grid Container Settings")

    col1, col2 = st.columns(2)
    with col1:
        grid_rows = st.number_input("Number of Rows", 1, 10, 3)
        grid_columns = st.number_input("Number of Columns", 1, 10, 3)
        gap_size = st.slider("Gap Size (px)", 0, 50, 10)

    with col2:
        justify_items = st.selectbox("Justify Items", ["stretch", "start", "end", "center"])
        align_items = st.selectbox("Align Items", ["stretch", "start", "end", "center"])
        grid_auto_flow = st.selectbox("Auto Flow", ["row", "column", "row dense", "column dense"])

    # Track definition
    st.subheader("Track Definitions")

    # Row tracks
    st.write("**Row Tracks:**")
    row_tracks = []
    for i in range(grid_rows):
        col1, col2 = st.columns(2)
        with col1:
            track_type = st.selectbox(f"Row {i + 1} Type", ["fr", "px", "auto", "min-content", "max-content"],
                                      key=f"row_type_{i}")
        with col2:
            if track_type in ["fr", "px"]:
                track_value = st.number_input(f"Row {i + 1} Value", 0.1 if track_type == "fr" else 1,
                                              1000.0 if track_type == "fr" else 1000, 1.0, key=f"row_val_{i}")
                row_tracks.append(f"{track_value}{track_type}")
            else:
                row_tracks.append(track_type)

    # Column tracks
    st.write("**Column Tracks:**")
    column_tracks = []
    for i in range(grid_columns):
        col1, col2 = st.columns(2)
        with col1:
            track_type = st.selectbox(f"Col {i + 1} Type", ["fr", "px", "auto", "min-content", "max-content"],
                                      key=f"col_type_{i}")
        with col2:
            if track_type in ["fr", "px"]:
                track_value = st.number_input(f"Col {i + 1} Value", 0.1 if track_type == "fr" else 1,
                                              1000.0 if track_type == "fr" else 1000, 1.0, key=f"col_val_{i}")
                column_tracks.append(f"{track_value}{track_type}")
            else:
                column_tracks.append(track_type)

    # Generate CSS
    grid_css = f"""display: grid;
grid-template-rows: {' '.join(row_tracks)};
grid-template-columns: {' '.join(column_tracks)};
gap: {gap_size}px;
justify-items: {justify_items};
align-items: {align_items};
grid-auto-flow: {grid_auto_flow};"""

    # Visual Preview
    st.subheader("Grid Preview")

    grid_items = ""
    for i in range(grid_rows * grid_columns):
        grid_items += f'<div style="background: hsl({(i * 30) % 360}, 70%, 60%); padding: 20px; text-align: center; color: white; border-radius: 4px;">Item {i + 1}</div>'

    preview_html = f"""
    <div style="{grid_css} border: 2px dashed #ccc; padding: 20px; margin: 20px 0;">
        {grid_items}
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # CSS Output
    st.subheader("CSS Code")
    complete_css = f""".grid-container {{
{grid_css}
}}

.grid-item {{
    /* Individual item styles */
    background: #f0f0f0;
    padding: 20px;
    text-align: center;
    border-radius: 4px;
}}"""

    st.code(complete_css, language="css")

    # Additional grid areas
    with st.expander("Advanced: Named Grid Areas"):
        st.write("Define named grid areas for complex layouts:")

        area_name = st.text_input("Area Name", "header")
        start_row = st.number_input("Start Row", 1, grid_rows, 1)
        end_row = st.number_input("End Row", 1, grid_rows + 1, 2)
        start_col = st.number_input("Start Column", 1, grid_columns, 1)
        end_col = st.number_input("End Column", 1, grid_columns + 1, 2)

        if st.button("Add Grid Area"):
            area_css = f""".{area_name} {{
    grid-row: {start_row} / {end_row};
    grid-column: {start_col} / {end_col};
}}"""
            st.code(area_css, language="css")

    FileHandler.create_download_link(complete_css.encode(), "grid-layout.css", "text/css")


def responsive_layout():
    """Responsive layout generator"""
    create_tool_header("Responsive Layout Generator", "Create responsive CSS layouts with media queries", "📱")

    layout_type = st.selectbox("Layout Type", ["Mobile First", "Desktop First", "Custom Breakpoints"])

    # Predefined breakpoints
    breakpoints = {
        "Mobile First": {
            "mobile": 320,
            "tablet": 768,
            "desktop": 1024,
            "large": 1200
        },
        "Desktop First": {
            "large": 1200,
            "desktop": 1024,
            "tablet": 768,
            "mobile": 320
        }
    }

    if layout_type == "Custom Breakpoints":
        st.subheader("Custom Breakpoints")
        custom_breakpoints = {}
        num_breakpoints = st.slider("Number of Breakpoints", 2, 6, 4)

        for i in range(num_breakpoints):
            col1, col2 = st.columns(2)
            with col1:
                bp_name = st.text_input(f"Breakpoint {i + 1} Name", f"bp{i + 1}", key=f"bp_name_{i}")
            with col2:
                bp_size = st.number_input(f"Min Width (px)", 320, 2000, 320 + (i * 200), key=f"bp_size_{i}")
            custom_breakpoints[bp_name] = bp_size

        current_breakpoints = custom_breakpoints
    else:
        current_breakpoints = breakpoints[layout_type]

    st.subheader("Layout Configuration")

    # Layout settings for each breakpoint
    layout_config = {}

    for bp_name, bp_size in current_breakpoints.items():
        with st.expander(f"📐 {bp_name.title()} Layout ({bp_size}px+)"):
            col1, col2 = st.columns(2)

            with col1:
                container_width = st.selectbox(f"Container Width", ["100%", "90%", "Fixed"], key=f"{bp_name}_width")
                if container_width == "Fixed":
                    fixed_width = st.number_input(f"Fixed Width (px)", 300, 1400, min(bp_size * 0.9, 1200),
                                                  key=f"{bp_name}_fixed")
                    container_width = f"{fixed_width}px"

                display_type = st.selectbox(f"Display", ["block", "flex", "grid"], key=f"{bp_name}_display")

            with col2:
                padding = st.slider(f"Padding (px)", 0, 50, 20, key=f"{bp_name}_padding")
                margin = st.selectbox(f"Margin", ["0 auto", "0", "auto"], key=f"{bp_name}_margin")

            # Flex/Grid specific settings
            flex_settings = {}
            if display_type == "flex":
                col1, col2 = st.columns(2)
                with col1:
                    flex_direction = st.selectbox(f"Flex Direction", ["row", "column"], key=f"{bp_name}_flex_dir")
                    flex_wrap = st.selectbox(f"Flex Wrap", ["nowrap", "wrap"], key=f"{bp_name}_flex_wrap")
                with col2:
                    justify_content = st.selectbox(f"Justify Content",
                                                   ["flex-start", "center", "space-between", "space-around"],
                                                   key=f"{bp_name}_justify")
                    align_items = st.selectbox(f"Align Items", ["stretch", "center", "flex-start", "flex-end"],
                                               key=f"{bp_name}_align")

                flex_settings = {
                    "flex-direction": flex_direction,
                    "flex-wrap": flex_wrap,
                    "justify-content": justify_content,
                    "align-items": align_items
                }

            elif display_type == "grid":
                col1, col2 = st.columns(2)
                with col1:
                    grid_columns = st.number_input(f"Grid Columns", 1, 12, 1 if bp_name == "mobile" else 3,
                                                   key=f"{bp_name}_grid_cols")
                with col2:
                    grid_gap = st.slider(f"Grid Gap (px)", 0, 50, 20, key=f"{bp_name}_grid_gap")

                flex_settings = {
                    "grid-template-columns": f"repeat({grid_columns}, 1fr)",
                    "gap": f"{grid_gap}px"
                }

            layout_config[bp_name] = {
                "breakpoint": bp_size,
                "container_width": container_width,
                "display": display_type,
                "padding": padding,
                "margin": margin,
                "additional": flex_settings
            }

    # Generate CSS
    st.subheader("Generated CSS")

    css_output = "/* Responsive Layout CSS */\n\n"

    # Base styles
    css_output += ".responsive-container {\n"
    css_output += "  box-sizing: border-box;\n"
    css_output += "}\n\n"

    # Media queries
    sorted_breakpoints = sorted(current_breakpoints.items(), key=lambda x: x[1])

    if layout_type == "Mobile First":
        # Mobile first approach
        for i, (bp_name, bp_size) in enumerate(sorted_breakpoints):
            config = layout_config[bp_name]

            if i == 0:
                # Base mobile styles (no media query)
                css_output += f"/* Base styles ({bp_name}) */\n"
                css_output += ".responsive-container {\n"
            else:
                css_output += f"/* {bp_name.title()} styles */\n"
                css_output += f"@media (min-width: {bp_size}px) {{\n"
                css_output += "  .responsive-container {\n"

            css_output += f"    width: {config['container_width']};\n"
            css_output += f"    margin: {config['margin']};\n"
            css_output += f"    padding: {config['padding']}px;\n"
            css_output += f"    display: {config['display']};\n"

            for prop, value in config['additional'].items():
                css_output += f"    {prop}: {value};\n"

            if i == 0:
                css_output += "}\n\n"
            else:
                css_output += "  }\n}\n\n"

    else:
        # Desktop first approach
        for i, (bp_name, bp_size) in enumerate(reversed(sorted_breakpoints)):
            config = layout_config[bp_name]

            if i == 0:
                # Base desktop styles
                css_output += f"/* Base styles ({bp_name}) */\n"
                css_output += ".responsive-container {\n"
            else:
                css_output += f"/* {bp_name.title()} styles */\n"
                css_output += f"@media (max-width: {bp_size - 1}px) {{\n"
                css_output += "  .responsive-container {\n"

            css_output += f"    width: {config['container_width']};\n"
            css_output += f"    margin: {config['margin']};\n"
            css_output += f"    padding: {config['padding']}px;\n"
            css_output += f"    display: {config['display']};\n"

            for prop, value in config['additional'].items():
                css_output += f"    {prop}: {value};\n"

            if i == 0:
                css_output += "}\n\n"
            else:
                css_output += "  }\n}\n\n"

    # Common responsive utilities
    css_output += "/* Responsive Utilities */\n"
    css_output += ".hide-mobile { display: block; }\n"
    css_output += ".hide-desktop { display: none; }\n\n"

    css_output += "@media (max-width: 767px) {\n"
    css_output += "  .hide-mobile { display: none; }\n"
    css_output += "  .hide-desktop { display: block; }\n"
    css_output += "}\n\n"

    css_output += "/* Image responsiveness */\n"
    css_output += ".responsive-img {\n"
    css_output += "  max-width: 100%;\n"
    css_output += "  height: auto;\n"
    css_output += "}\n"

    st.code(css_output, language="css")

    # HTML Example
    with st.expander("📄 HTML Example"):
        html_example = '''<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Your generated CSS goes here */
    </style>
</head>
<body>
    <div class="responsive-container">
        <h1>Responsive Layout</h1>
        <p>This layout adapts to different screen sizes.</p>
        <img src="image.jpg" class="responsive-img" alt="Responsive image">
    </div>
</body>
</html>'''
        st.code(html_example, language="html")

    FileHandler.create_download_link(css_output.encode(), "responsive-layout.css", "text/css")


def bootstrap_helper():
    """Bootstrap helper tools"""
    create_tool_header("Bootstrap Helper", "Generate Bootstrap CSS classes and components", "🧩")

    tool_type = st.selectbox("Bootstrap Tool", [
        "Grid System", "Components", "Utilities", "Custom Theme", "Layout Helper"
    ])

    if tool_type == "Grid System":
        st.subheader("Bootstrap Grid Generator")

        container_type = st.selectbox("Container Type", ["container", "container-fluid"])
        num_rows = st.number_input("Number of Rows", 1, 10, 1)

        grid_html = f'<div class="{container_type}">\n'

        for row in range(num_rows):
            st.write(f"**Row {row + 1}:**")
            num_cols = st.number_input(f"Number of Columns in Row {row + 1}", 1, 12, 3, key=f"row_{row}_cols")

            col_sizes = []
            remaining_cols = 12

            for col in range(num_cols):
                if col == num_cols - 1:
                    # Last column gets remaining space
                    col_size = remaining_cols
                else:
                    max_size = min(remaining_cols - (num_cols - col - 1), 12)
                    col_size = st.slider(f"Column {col + 1} Size", 1, max_size, min(4, max_size),
                                         key=f"row_{row}_col_{col}")
                    remaining_cols -= col_size

                col_sizes.append(col_size)

            # Generate row HTML
            grid_html += '  <div class="row">\n'
            for i, size in enumerate(col_sizes):
                grid_html += f'    <div class="col-md-{size}">\n'
                grid_html += f'      Column {i + 1}\n'
                grid_html += '    </div>\n'
            grid_html += '  </div>\n'

        grid_html += '</div>'

        st.subheader("Generated HTML")
        st.code(grid_html, language="html")

        # Preview
        st.subheader("Visual Preview")
        preview_css = """
        <style>
        .bootstrap-preview { margin: 20px 0; }
        .bootstrap-preview .container, .bootstrap-preview .container-fluid { background: #f8f9fa; padding: 15px; border: 1px solid #dee2e6; }
        .bootstrap-preview .row { margin-bottom: 10px; }
        .bootstrap-preview [class*="col-"] { background: #007bff; color: white; padding: 10px; margin-bottom: 5px; text-align: center; border-radius: 4px; }
        </style>
        """
        st.markdown(preview_css + f'<div class="bootstrap-preview">{grid_html}</div>', unsafe_allow_html=True)

    elif tool_type == "Components":
        st.subheader("Bootstrap Components")

        component_type = st.selectbox("Component Type", [
            "Button", "Card", "Alert", "Badge", "Navigation", "Modal", "Form"
        ])

        if component_type == "Button":
            button_variant = st.selectbox("Button Variant", [
                "primary", "secondary", "success", "danger", "warning", "info", "light", "dark"
            ])
            button_size = st.selectbox("Button Size", ["btn-lg", "(normal)", "btn-sm"])
            button_text = st.text_input("Button Text", "Click me")
            outline = st.checkbox("Outline Style")

            btn_class = f"btn btn{'---outline' if outline else ''}-{button_variant}"
            if button_size != "(normal)":
                btn_class += f" {button_size}"

            component_html = f'<button type="button" class="{btn_class}">{button_text}</button>'

        elif component_type == "Card":
            card_title = st.text_input("Card Title", "Card Title")
            card_text = st.text_area("Card Text", "This is card content.")
            include_image = st.checkbox("Include Image")
            include_footer = st.checkbox("Include Footer")

            component_html = '<div class="card" style="width: 18rem;">\n'
            if include_image:
                component_html += '  <img src="..." class="card-img-top" alt="...">\n'
            component_html += '  <div class="card-body">\n'
            component_html += f'    <h5 class="card-title">{card_title}</h5>\n'
            component_html += f'    <p class="card-text">{card_text}</p>\n'
            component_html += '    <a href="#" class="btn btn-primary">Go somewhere</a>\n'
            component_html += '  </div>\n'
            if include_footer:
                component_html += '  <div class="card-footer text-muted">\n'
                component_html += '    Card footer\n'
                component_html += '  </div>\n'
            component_html += '</div>'

        elif component_type == "Alert":
            alert_type = st.selectbox("Alert Type", [
                "primary", "secondary", "success", "danger", "warning", "info", "light", "dark"
            ])
            alert_text = st.text_input("Alert Text", "This is an alert message!")
            dismissible = st.checkbox("Dismissible")

            alert_class = f"alert alert-{alert_type}"
            if dismissible:
                alert_class += " alert-dismissible fade show"

            component_html = f'<div class="{alert_class}" role="alert">\n'
            component_html += f'  {alert_text}\n'
            if dismissible:
                component_html += '  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>\n'
            component_html += '</div>'

        else:
            component_html = f"<!-- {component_type} component code will be generated here -->"

        st.subheader("Generated HTML")
        st.code(component_html, language="html")

    elif tool_type == "Utilities":
        st.subheader("Bootstrap Utility Classes")

        utility_category = st.selectbox("Utility Category", [
            "Spacing", "Colors", "Display", "Flexbox", "Text", "Position"
        ])

        if utility_category == "Spacing":
            property_type = st.selectbox("Property", ["margin", "padding"])
            sides = st.multiselect("Sides", ["top", "bottom", "left", "right", "x (left+right)", "y (top+bottom)"],
                                   ["all"])
            size = st.selectbox("Size", ["0", "1", "2", "3", "4", "5", "auto"])

            prefix = "m" if property_type == "margin" else "p"
            classes = []

            for side in sides:
                if side == "all":
                    classes.append(f"{prefix}-{size}")
                elif side == "x (left+right)":
                    classes.append(f"{prefix}x-{size}")
                elif side == "y (top+bottom)":
                    classes.append(f"{prefix}y-{size}")
                else:
                    side_letter = side[0]
                    classes.append(f"{prefix}{side_letter}-{size}")

            utility_html = f'<div class="{" ".join(classes)}">Element with spacing</div>'

        elif utility_category == "Colors":
            color_type = st.selectbox("Color Type", ["text", "background"])
            color_name = st.selectbox("Color", [
                "primary", "secondary", "success", "danger", "warning", "info", "light", "dark"
            ])

            if color_type == "text":
                utility_html = f'<p class="text-{color_name}">Text with color</p>'
                classes = [f"text-{color_name}"]
            else:
                utility_html = f'<div class="bg-{color_name} p-3">Background with color</div>'
                classes = [f"bg-{color_name}"]

        else:
            utility_html = f"<!-- {utility_category} utility classes will be generated here -->"
            classes = []

        st.subheader("Generated HTML")
        st.code(utility_html, language="html")

        st.subheader("Class Reference")
        st.code(" ".join(classes) if classes else "utility-class", language="css")

    elif tool_type == "Custom Theme":
        st.subheader("Bootstrap Theme Customizer")

        # Color customization
        st.write("**Primary Colors:**")
        primary_color = st.color_picker("Primary Color", "#007bff")
        secondary_color = st.color_picker("Secondary Color", "#6c757d")
        success_color = st.color_picker("Success Color", "#28a745")
        danger_color = st.color_picker("Danger Color", "#dc3545")

        # Typography
        st.write("**Typography:**")
        font_family = st.selectbox("Font Family", [
            "System Default", "Arial", "Helvetica", "Georgia", "Times", "Custom"
        ])
        if font_family == "Custom":
            custom_font = st.text_input("Custom Font Family", "'Custom Font', sans-serif")
            font_family = custom_font

        base_font_size = st.slider("Base Font Size (rem)", 0.8, 1.4, 1.0, 0.1)

        # Generate custom CSS
        theme_css = f"""
/* Custom Bootstrap Theme */
:root {{
  --bs-primary: {primary_color};
  --bs-secondary: {secondary_color};
  --bs-success: {success_color};
  --bs-danger: {danger_color};
  --bs-font-family-base: {font_family if font_family != 'System Default' else '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'};
  --bs-body-font-size: {base_font_size}rem;
}}

/* Update button styles */
.btn-primary {{
  background-color: {primary_color};
  border-color: {primary_color};
}}

.btn-secondary {{
  background-color: {secondary_color};
  border-color: {secondary_color};
}}

body {{
  font-family: var(--bs-font-family-base);
  font-size: var(--bs-body-font-size);
}}
"""

        st.subheader("Custom Theme CSS")
        st.code(theme_css, language="css")

        FileHandler.create_download_link(theme_css.encode(), "bootstrap-custom-theme.css", "text/css")

    # Download for all components except Custom Theme
    if tool_type != "Custom Theme":
        # Initialize default content
        download_content = "<!-- Bootstrap component will be generated here -->"

        # Set download content based on what was generated
        if tool_type in ["Grid System"] and 'grid_html' in locals():
            download_content = grid_html
        elif tool_type in ["Components"] and 'component_html' in locals():
            download_content = component_html
        elif tool_type in ["Utilities"] and 'utility_html' in locals():
            download_content = utility_html

        FileHandler.create_download_link(download_content.encode(), "bootstrap-component.html", "text/html")


def transition_builder():
    """CSS transition builder"""
    create_tool_header("CSS Transition Builder", "Create smooth CSS transitions and animations", "✨")

    transition_type = st.selectbox("Transition Type",
                                   ["Simple Transition", "Multiple Properties", "Keyframe Animation"])

    if transition_type == "Simple Transition":
        st.subheader("Simple Transition")

        col1, col2 = st.columns(2)
        with col1:
            property_name = st.selectbox("Property to Animate", [
                "all", "opacity", "transform", "background-color", "color", "width", "height",
                "margin", "padding", "border-radius", "box-shadow", "filter"
            ])
            duration = st.slider("Duration (seconds)", 0.1, 5.0, 0.3, 0.1)
            timing_function = st.selectbox("Timing Function", [
                "ease", "ease-in", "ease-out", "ease-in-out", "linear",
                "cubic-bezier(0.25, 0.1, 0.25, 1)", "custom"
            ])

        with col2:
            delay = st.slider("Delay (seconds)", 0.0, 2.0, 0.0, 0.1)
            if timing_function == "custom":
                st.write("Custom Cubic Bezier:")
                x1 = st.slider("X1", 0.0, 1.0, 0.25, 0.01)
                y1 = st.slider("Y1", -2.0, 2.0, 0.1, 0.01)
                x2 = st.slider("X2", 0.0, 1.0, 0.25, 0.01)
                y2 = st.slider("Y2", -2.0, 2.0, 1.0, 0.01)
                timing_function = f"cubic-bezier({x1}, {y1}, {x2}, {y2})"

        # Generate transition CSS
        transition_css = f"transition: {property_name} {duration}s {timing_function}"
        if delay > 0:
            transition_css += f" {delay}s"
        transition_css += ";"

        # Interactive states
        st.subheader("Hover/Focus States")

        # Initialize default values
        hover_opacity = 1.0
        hover_transform = "none"
        original_bg = "#007bff"
        hover_bg = "#0056b3"

        if property_name in ["opacity", "all"]:
            hover_opacity = st.slider("Hover Opacity", 0.0, 1.0, 0.8, 0.1)

        if property_name in ["transform", "all"]:
            transform_type = st.selectbox("Transform on Hover", [
                "None", "Scale", "Rotate", "Translate", "Skew"
            ])

            if transform_type == "Scale":
                scale_value = st.slider("Scale Factor", 0.5, 2.0, 1.1, 0.1)
                hover_transform = f"scale({scale_value})"
            elif transform_type == "Rotate":
                rotate_value = st.slider("Rotation (degrees)", -360, 360, 15, 5)
                hover_transform = f"rotate({rotate_value}deg)"
            elif transform_type == "Translate":
                translate_x = st.slider("Translate X (px)", -100, 100, 10, 5)
                translate_y = st.slider("Translate Y (px)", -100, 100, -5, 5)
                hover_transform = f"translate({translate_x}px, {translate_y}px)"

        if property_name in ["background-color", "all"]:
            original_bg = st.color_picker("Original Background", "#007bff")
            hover_bg = st.color_picker("Hover Background", "#0056b3")

        # Generate complete CSS
        complete_css = ".transition-element {\n"
        complete_css += f"  {transition_css}\n"

        if property_name in ["background-color", "all"]:
            complete_css += f"  background-color: {original_bg};\n"
        if property_name in ["opacity", "all"]:
            complete_css += "  opacity: 1;\n"

        complete_css += "}\n\n"
        complete_css += ".transition-element:hover {\n"

        if property_name in ["opacity", "all"]:
            complete_css += f"  opacity: {hover_opacity};\n"
        if property_name in ["transform", "all"]:
            complete_css += f"  transform: {hover_transform};\n"
        if property_name in ["background-color", "all"]:
            complete_css += f"  background-color: {hover_bg};\n"

        complete_css += "}"

        # Live preview
        st.subheader("Interactive Preview")

        preview_styles = f"""
        <style>
        .preview-element {{
            width: 100px;
            height: 100px;
            background-color: {original_bg};
            margin: 20px auto;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            cursor: pointer;
            {transition_css}
        }}

        .preview-element:hover {{
            opacity: {hover_opacity};
            transform: {hover_transform};
            background-color: {hover_bg};
        }}
        </style>

        <div class="preview-element">
            Hover me!
        </div>
        """

        st.markdown(preview_styles, unsafe_allow_html=True)

    elif transition_type == "Multiple Properties":
        st.subheader("Multiple Property Transitions")

        num_properties = st.slider("Number of Properties", 1, 5, 2)

        transitions = []
        for i in range(num_properties):
            with st.expander(f"Property {i + 1}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    prop = st.selectbox(f"Property", [
                        "opacity", "transform", "background-color", "color", "width", "height"
                    ], key=f"prop_{i}")
                with col2:
                    duration = st.slider(f"Duration (s)", 0.1, 3.0, 0.3, 0.1, key=f"dur_{i}")
                with col3:
                    easing = st.selectbox(f"Easing", ["ease", "ease-in", "ease-out", "linear"], key=f"ease_{i}")

                transitions.append(f"{prop} {duration}s {easing}")

        transition_css = f"transition: {', '.join(transitions)};"
        complete_css = f".multi-transition {{\n  {transition_css}\n}}"

    else:  # Keyframe Animation
        st.subheader("Keyframe Animation")

        animation_name = st.text_input("Animation Name", "customAnimation")
        duration = st.slider("Duration (seconds)", 0.5, 10.0, 2.0, 0.1)
        iteration_count = st.selectbox("Iteration Count", ["1", "2", "3", "infinite"])
        direction = st.selectbox("Direction", ["normal", "reverse", "alternate", "alternate-reverse"])
        timing_function = st.selectbox("Timing Function", ["ease", "ease-in", "ease-out", "linear"])

        # Keyframe points
        st.write("**Keyframe Points:**")
        num_keyframes = st.slider("Number of Keyframes", 2, 6, 3)

        keyframes = []
        for i in range(num_keyframes):
            with st.expander(f"Keyframe {i + 1}"):
                if i == 0:
                    percentage = 0
                    st.write("Percentage: 0% (start)")
                elif i == num_keyframes - 1:
                    percentage = 100
                    st.write("Percentage: 100% (end)")
                else:
                    percentage = st.slider(f"Percentage", 1, 99, (100 // num_keyframes) * i, key=f"kf_pct_{i}")

                col1, col2 = st.columns(2)
                with col1:
                    opacity = st.slider(f"Opacity", 0.0, 1.0, 1.0, 0.1, key=f"kf_opacity_{i}")
                    scale = st.slider(f"Scale", 0.1, 2.0, 1.0, 0.1, key=f"kf_scale_{i}")
                with col2:
                    rotate = st.slider(f"Rotation (deg)", 0, 360, 0, 15, key=f"kf_rotate_{i}")
                    translate_y = st.slider(f"Translate Y (px)", -100, 100, 0, 10, key=f"kf_ty_{i}")

                keyframes.append({
                    'percentage': percentage,
                    'opacity': opacity,
                    'scale': scale,
                    'rotate': rotate,
                    'translate_y': translate_y
                })

        # Generate keyframe CSS
        keyframe_css = f"@keyframes {animation_name} {{\n"
        for kf in sorted(keyframes, key=lambda x: x['percentage']):
            keyframe_css += f"  {kf['percentage']}% {{\n"
            keyframe_css += f"    opacity: {kf['opacity']};\n"
            keyframe_css += f"    transform: translateY({kf['translate_y']}px) scale({kf['scale']}) rotate({kf['rotate']}deg);\n"
            keyframe_css += "  }\n"
        keyframe_css += "}\n\n"

        # Animation property
        animation_css = f"animation: {animation_name} {duration}s {timing_function} {iteration_count} {direction};"

        complete_css = keyframe_css + f".animated-element {{\n  {animation_css}\n}}"

    # Display CSS output
    st.subheader("Generated CSS")
    st.code(complete_css, language="css")

    # Common transition examples
    with st.expander("🎨 Common Transition Examples"):
        examples = {
            "Fade In/Out": "transition: opacity 0.3s ease;",
            "Scale on Hover": "transition: transform 0.2s ease;\n/* Add to :hover */\ntransform: scale(1.05);",
            "Slide Up": "transition: transform 0.4s ease;\n/* Add to :hover */\ntransform: translateY(-10px);",
            "Color Change": "transition: background-color 0.3s ease;\n/* Add to :hover */\nbackground-color: #newcolor;",
            "Smooth Box Shadow": "transition: box-shadow 0.3s ease;\n/* Add to :hover */\nbox-shadow: 0 10px 20px rgba(0,0,0,0.2);"
        }

        for name, css in examples.items():
            st.write(f"**{name}:**")
            st.code(css, language="css")

    FileHandler.create_download_link(complete_css.encode(), "transitions.css", "text/css")


def specificity_calculator():
    """CSS specificity calculator"""
    create_tool_header("CSS Specificity Calculator", "Calculate and compare CSS selector specificity", "🎯")

    st.markdown("""
    **CSS Specificity** determines which styles are applied when multiple rules target the same element.
    The specificity is calculated based on the number of:
    - **IDs** (most specific)
    - **Classes, attributes, and pseudo-classes**
    - **Elements and pseudo-elements** (least specific)
    """)

    # Input for selectors
    st.subheader("Selector Input")

    input_method = st.radio("Input Method", ["Single Selector", "Multiple Selectors", "CSS Rule"])

    if input_method == "Single Selector":
        selector = st.text_input("Enter CSS Selector", "#header .nav-menu li a:hover")

        if selector:
            specificity = calculate_specificity(selector)
            display_specificity_result(selector, specificity)

    elif input_method == "Multiple Selectors":
        st.write("Compare multiple selectors:")

        selectors = []
        num_selectors = st.number_input("Number of Selectors", 2, 10, 3)

        for i in range(num_selectors):
            selector = st.text_input(f"Selector {i + 1}",
                                     placeholder=f"Example: {'#main .content' if i == 0 else '.button' if i == 1 else 'div p'}",
                                     key=f"selector_{i}")
            if selector:
                selectors.append(selector)

        if len(selectors) >= 2:
            st.subheader("Specificity Comparison")

            results = []
            for selector in selectors:
                specificity = calculate_specificity(selector)
                results.append((selector, specificity))

            # Sort by specificity (highest first)
            results.sort(key=lambda x: (x[1]['ids'], x[1]['classes'], x[1]['elements']), reverse=True)

            for i, (selector, specificity) in enumerate(results):
                priority_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔸"
                st.write(f"**{priority_icon} Priority {i + 1}:** `{selector}`")
                display_specificity_result(selector, specificity, show_header=False)
                st.write("---")

    else:  # CSS Rule
        st.write("Paste a complete CSS rule:")
        css_rule = st.text_area("CSS Rule",
                                placeholder="""#header .navigation li a:hover {
    color: blue;
    text-decoration: underline;
}""", height=150)

        if css_rule:
            # Extract selector from CSS rule
            lines = css_rule.strip().split('\n')
            selector_line = lines[0].strip()

            # Remove opening brace if present
            if '{' in selector_line:
                selector = selector_line.split('{')[0].strip()
            else:
                selector = selector_line

            if selector:
                specificity = calculate_specificity(selector)
                st.subheader("Extracted Selector")
                st.code(selector)
                display_specificity_result(selector, specificity)

    # Specificity tips
    with st.expander("💡 Specificity Tips & Best Practices"):
        st.markdown("""
        ### Understanding Specificity Values

        - **Inline styles**: Specificity of 1000 (highest)
        - **IDs**: Specificity of 100 each
        - **Classes, attributes, pseudo-classes**: Specificity of 10 each
        - **Elements and pseudo-elements**: Specificity of 1 each

        ### Best Practices

        1. **Avoid using !important** - It breaks the natural cascade
        2. **Keep specificity low** - Use classes instead of IDs when possible
        3. **Be consistent** - Follow a naming convention like BEM
        4. **Use cascade wisely** - Order your CSS rules thoughtfully
        5. **Prefer classes over complex selectors** - Easier to maintain

        ### Common Specificity Issues

        - **Overly specific selectors**: `#main .content .sidebar .widget .title`
        - **Fighting specificity with !important**: Creates maintenance nightmares
        - **Inconsistent naming**: Makes it hard to predict specificity
        """)


def calculate_specificity(selector):
    """Calculate CSS specificity for a given selector"""
    import re

    # Remove whitespace and normalize
    selector = selector.strip()

    # Count different types of selectors
    ids = len(re.findall(r'#[\w-]+', selector))

    # Classes, attributes, and pseudo-classes
    classes = len(re.findall(r'\.[\w-]+', selector))  # Classes
    classes += len(re.findall(r'\[[^\]]*\]', selector))  # Attributes
    classes += len(re.findall(r':[\w-]+(?:\([^)]*\))?', selector))  # Pseudo-classes

    # Elements and pseudo-elements
    # First remove IDs, classes, attributes, and pseudo-classes to avoid double counting
    cleaned_selector = re.sub(r'#[\w-]+', '', selector)  # Remove IDs
    cleaned_selector = re.sub(r'\.[\w-]+', '', cleaned_selector)  # Remove classes
    cleaned_selector = re.sub(r'\[[^\]]*\]', '', cleaned_selector)  # Remove attributes
    cleaned_selector = re.sub(r':[\w-]+(?:\([^)]*\))?', '', cleaned_selector)  # Remove pseudo-classes

    # Count remaining element selectors
    elements = len(re.findall(r'\b[a-zA-Z][\w-]*\b', cleaned_selector))

    # Calculate total specificity
    total = (ids * 100) + (classes * 10) + elements

    return {
        'ids': ids,
        'classes': classes,
        'elements': elements,
        'total': total,
        'notation': f"{ids},{classes},{elements}"
    }


def display_specificity_result(selector, specificity, show_header=True):
    """Display specificity calculation results"""

    if show_header:
        st.subheader("Specificity Calculation")

    # Visual representation
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("IDs", specificity['ids'], help="Worth 100 points each")
    with col2:
        st.metric("Classes/Attrs/Pseudo", specificity['classes'], help="Worth 10 points each")
    with col3:
        st.metric("Elements", specificity['elements'], help="Worth 1 point each")
    with col4:
        st.metric("Total Specificity", specificity['total'])

    # Breakdown
    if specificity['total'] > 0:
        calculation = []
        if specificity['ids'] > 0:
            calculation.append(f"{specificity['ids']} × 100 = {specificity['ids'] * 100}")
        if specificity['classes'] > 0:
            calculation.append(f"{specificity['classes']} × 10 = {specificity['classes'] * 10}")
        if specificity['elements'] > 0:
            calculation.append(f"{specificity['elements']} × 1 = {specificity['elements']}")

        st.write(f"**Calculation:** {' + '.join(calculation)} = **{specificity['total']}**")
        st.write(f"**Specificity Notation:** `{specificity['notation']}`")


def selector_tester():
    """CSS selector tester"""
    create_tool_header("CSS Selector Tester", "Test and validate CSS selectors against HTML", "🎯")

    # Input modes
    input_mode = st.radio("Input Mode", ["Interactive Builder", "Manual Input", "Upload Files"])

    if input_mode == "Interactive Builder":
        st.subheader("HTML Structure Builder")

        # Simple HTML builder
        with st.expander("🏠 Build Sample HTML Structure"):
            structure_type = st.selectbox("HTML Structure Template", [
                "Simple Page", "Navigation Menu", "Article Layout", "Form Elements", "Custom"
            ])

            if structure_type == "Simple Page":
                sample_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <header id="main-header" class="site-header">
        <h1 class="site-title">My Website</h1>
        <nav class="main-navigation">
            <ul class="nav-menu">
                <li class="menu-item"><a href="#home">Home</a></li>
                <li class="menu-item current"><a href="#about">About</a></li>
                <li class="menu-item"><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main id="content" class="main-content">
        <article class="post featured">
            <h2 class="post-title">Welcome to My Site</h2>
            <p class="post-excerpt">This is a sample paragraph.</p>
            <a href="#read-more" class="btn btn-primary">Read More</a>
        </article>
    </main>

    <footer id="site-footer" class="site-footer">
        <p class="copyright">&copy; 2024 My Website</p>
    </footer>
</body>
</html>"""

            elif structure_type == "Navigation Menu":
                sample_html = """
<nav class="navbar navbar-main">
    <div class="navbar-brand">
        <a href="#" class="brand-link">
            <img src="logo.png" alt="Logo" class="brand-logo">
            <span class="brand-text">Brand</span>
        </a>
    </div>

    <ul class="navbar-nav">
        <li class="nav-item active">
            <a href="#home" class="nav-link">Home</a>
        </li>
        <li class="nav-item dropdown">
            <a href="#services" class="nav-link dropdown-toggle">Services</a>
            <ul class="dropdown-menu">
                <li><a href="#web-design" class="dropdown-link">Web Design</a></li>
                <li><a href="#development" class="dropdown-link">Development</a></li>
            </ul>
        </li>
        <li class="nav-item">
            <a href="#contact" class="nav-link">Contact</a>
        </li>
    </ul>
</nav>"""

            elif structure_type == "Form Elements":
                sample_html = """
<form class="contact-form" id="contact-form">
    <div class="form-group">
        <label for="name" class="form-label required">Name</label>
        <input type="text" id="name" name="name" class="form-control" required>
    </div>

    <div class="form-group">
        <label for="email" class="form-label required">Email</label>
        <input type="email" id="email" name="email" class="form-control" required>
    </div>

    <div class="form-group">
        <label for="message" class="form-label">Message</label>
        <textarea id="message" name="message" class="form-control" rows="4"></textarea>
    </div>

    <div class="form-actions">
        <button type="submit" class="btn btn-primary">Send Message</button>
        <button type="reset" class="btn btn-secondary">Reset</button>
    </div>
</form>"""

            else:
                sample_html = st.text_area("Enter Custom HTML", height=200,
                                           value="<div class='container'>\n  <p class='text'>Hello World</p>\n</div>")

        if structure_type != "Custom":
            st.code(sample_html, language="html")

    elif input_mode == "Manual Input":
        st.subheader("Manual HTML Input")
        sample_html = st.text_area("Enter HTML code to test against:", height=300,
                                   value="""<div id="container" class="main-container">
    <header class="site-header">
        <h1 class="title">Page Title</h1>
        <nav class="navigation">
            <ul class="nav-list">
                <li class="nav-item active"><a href="#home">Home</a></li>
                <li class="nav-item"><a href="#about">About</a></li>
            </ul>
        </nav>
    </header>
    <main class="content">
        <article class="post featured">
            <h2 class="post-title">Article Title</h2>
            <p class="post-content">Article content goes here.</p>
        </article>
    </main>
</div>""")

    else:  # Upload Files
        st.subheader("Upload HTML File")
        uploaded_file = FileHandler.upload_files(['html', 'htm'], accept_multiple=False)

        if uploaded_file:
            sample_html = FileHandler.process_text_file(uploaded_file[0])
            st.code(sample_html, language="html")
        else:
            sample_html = ""

    if sample_html:
        st.markdown("---")
        st.subheader("CSS Selector Testing")

        # Selector input
        col1, col2 = st.columns([2, 1])

        with col1:
            selector_input = st.text_input(
                "Enter CSS Selector to Test",
                placeholder="e.g., .nav-item.active a, #container .post-title"
            )

        with col2:
            test_type = st.selectbox("Test Type", ["Find Elements", "Validate Syntax", "Specificity"])

        if selector_input:
            if test_type == "Find Elements":
                # Simple element matching (basic implementation)
                try:
                    # Parse HTML and extract basic elements
                    import re

                    # Find all HTML tags with their attributes
                    tag_pattern = r'<(\w+)([^>]*)>'
                    matches = re.finditer(tag_pattern, sample_html)

                    found_elements = []
                    for match in matches:
                        tag = match.group(1)
                        attrs = match.group(2)

                        # Extract id and class attributes
                        id_match = re.search(r'id=["\']([^"\']*)["\']', attrs)
                        class_match = re.search(r'class=["\']([^"\']*)["\']', attrs)

                        element_id = id_match.group(1) if id_match else ''
                        element_classes = class_match.group(1).split() if class_match else []

                        # Basic selector matching
                        matches_selector = False

                        # ID selector
                        if selector_input.startswith('#'):
                            matches_selector = element_id == selector_input[1:]
                        # Class selector
                        elif selector_input.startswith('.'):
                            matches_selector = selector_input[1:] in element_classes
                        # Element selector
                        elif selector_input.isalnum():
                            matches_selector = tag == selector_input
                        # Combined selectors (basic support)
                        elif '.' in selector_input:
                            parts = selector_input.split('.')
                            if len(parts) >= 2:
                                tag_part = parts[0] if parts[0] else None
                                class_parts = parts[1:]

                                tag_matches = (not tag_part) or (tag == tag_part)
                                class_matches = all(cls in element_classes for cls in class_parts)
                                matches_selector = tag_matches and class_matches

                        if matches_selector:
                            found_elements.append({
                                'tag': tag,
                                'id': element_id,
                                'classes': element_classes,
                                'html': match.group(0)
                            })

                    if found_elements:
                        st.success(f"✅ Found {len(found_elements)} matching element(s)")

                        for i, element in enumerate(found_elements[:5]):  # Show first 5
                            with st.expander(f"Match {i + 1}: {element['tag']}"):
                                st.write(f"**Tag:** `{element['tag']}`")
                                if element['id']:
                                    st.write(f"**ID:** `{element['id']}`")
                                if element['classes']:
                                    st.write(f"**Classes:** `{' '.join(element['classes'])}`")
                                st.code(element['html'], language="html")
                    else:
                        st.warning("⚠️ No elements match this selector")

                except Exception as e:
                    st.error(f"❌ Error testing selector: {str(e)}")

            elif test_type == "Validate Syntax":
                # Basic syntax validation
                import re
                is_valid = True
                error_msg = ""

                if not selector_input.strip():
                    is_valid = False
                    error_msg = "Selector cannot be empty"
                elif re.search(r'[<>"\']', selector_input):
                    is_valid = False
                    error_msg = "Invalid characters in selector"
                elif selector_input.count('[') != selector_input.count(']'):
                    is_valid = False
                    error_msg = "Unmatched square brackets"

                if is_valid:
                    st.success("✅ Selector syntax is valid")
                else:
                    st.error(f"❌ {error_msg}")

            else:  # Specificity
                specificity = calculate_specificity(selector_input)
                display_specificity_result(selector_input, specificity)

        # Selector examples
        with st.expander("💡 Selector Examples & Tips"):
            st.markdown("""
            ### Common CSS Selectors

            **Basic Selectors:**
            - `div` - All div elements
            - `.class-name` - Elements with class "class-name"
            - `#element-id` - Element with ID "element-id"

            **Combinators:**
            - `.parent .child` - Descendant selector
            - `.parent > .child` - Direct child selector
            - `.element + .sibling` - Adjacent sibling
            - `.element ~ .sibling` - General sibling

            **Pseudo-classes:**
            - `a:hover` - Link on hover
            - `li:first-child` - First list item
            - `input:not([disabled])` - Enabled inputs

            **Attribute Selectors:**
            - `[href]` - Elements with href attribute
            - `[class*="nav"]` - Class contains "nav"
            - `[href^="https"]` - Href starts with "https"
            """)

            # Quick test buttons
            st.write("**Quick Tests:**")
            quick_tests = [
                "div",  # Element
                ".nav-item",  # Class
                "#container",  # ID
                ".nav-item.active",  # Multiple classes
            ]

            cols = st.columns(len(quick_tests))
            for i, test in enumerate(quick_tests):
                with cols[i]:
                    if st.button(f"`{test}`", key=f"quick_{i}"):
                        st.session_state.test_selector = test
