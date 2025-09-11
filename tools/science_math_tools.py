import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all science and math tools"""

    tool_categories = {
        "Basic Math": [
            "Calculator", "Unit Converter", "Percentage Calculator", "Fraction Calculator", "Ratio Calculator"
        ],
        "Algebra": [
            "Equation Solver", "Quadratic Formula", "System of Equations", "Polynomial Calculator",
            "Logarithm Calculator"
        ],
        "Geometry": [
            "Area Calculator", "Volume Calculator", "Perimeter Calculator", "Triangle Calculator", "Circle Calculator"
        ],
        "Trigonometry": [
            "Trigonometric Functions", "Angle Converter", "Law of Cosines", "Law of Sines", "Unit Circle"
        ],
        "Calculus": [
            "Derivative Calculator", "Integral Calculator", "Limit Calculator", "Series Calculator", "Function Plotter"
        ],
        "Statistics": [
            "Descriptive Statistics", "Probability Calculator", "Distribution Calculator", "Hypothesis Testing",
            "Confidence Intervals"
        ],
        "Physics": [
            "Motion Calculator", "Force Calculator", "Energy Calculator", "Wave Calculator", "Electricity Calculator"
        ],
        "Chemistry": [
            "Molecular Weight", "Chemical Equation Balancer", "pH Calculator", "Concentration Calculator", "Gas Laws"
        ],
        "Engineering": [
            "Ohm's Law Calculator", "Beam Calculator", "Stress Calculator", "Fluid Mechanics", "Heat Transfer"
        ],
        "Number Theory": [
            "Prime Numbers", "GCD/LCM Calculator", "Factorization", "Number Base Converter", "Fibonacci Sequence"
        ]
    }

    selected_category = st.selectbox("Select Science/Math Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Science/Math Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Calculator":
        advanced_calculator()
    elif selected_tool == "Unit Converter":
        unit_converter()
    elif selected_tool == "Quadratic Formula":
        quadratic_formula()
    elif selected_tool == "Area Calculator":
        area_calculator()
    elif selected_tool == "Trigonometric Functions":
        trig_functions()
    elif selected_tool == "Function Plotter":
        function_plotter()
    elif selected_tool == "Descriptive Statistics":
        descriptive_statistics()
    elif selected_tool == "Motion Calculator":
        motion_calculator()
    elif selected_tool == "Molecular Weight":
        molecular_weight()
    elif selected_tool == "Prime Numbers":
        prime_numbers()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def advanced_calculator():
    """Advanced scientific calculator"""
    create_tool_header("Advanced Calculator", "Perform complex mathematical calculations", "🧮")

    # Calculator interface
    st.markdown("### 🧮 Scientific Calculator")

    expression = st.text_input("Enter mathematical expression:", placeholder="2 + 3 * sin(pi/4)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Available Functions:**")
        st.write("Basic: +, -, *, /, **, (), abs()")
        st.write("Trigonometric: sin(), cos(), tan(), asin(), acos(), atan()")
        st.write("Logarithmic: log(), log10(), ln() (natural log)")
        st.write("Other: sqrt(), exp(), factorial(), pi, e")

    with col2:
        st.markdown("**Examples:**")
        st.code("2 + 3 * 4")
        st.code("sin(pi/2)")
        st.code("log(100)")
        st.code("sqrt(16)")
        st.code("2**3")

    if expression and st.button("Calculate"):
        result = calculate_expression(expression)
        if result is not None:
            st.success(f"**Result:** {result}")
        else:
            st.error("Invalid expression. Please check your syntax.")


def calculate_expression(expression):
    """Safely evaluate mathematical expressions"""
    try:
        # Replace common mathematical functions
        expression = expression.replace("ln(", "log(")
        expression = expression.replace("factorial(", "math.factorial(")
        expression = expression.replace("pi", "math.pi")
        expression = expression.replace("e", "math.e")

        # Add math. prefix to functions
        math_functions = ["sin", "cos", "tan", "asin", "acos", "atan", "log", "log10",
                          "sqrt", "exp", "abs", "floor", "ceil"]
        for func in math_functions:
            expression = expression.replace(f"{func}(", f"math.{func}(")

        # Evaluate safely
        allowed_names = {
            "__builtins__": {},
            "math": math,
        }

        result = eval(expression, allowed_names)
        return result
    except:
        return None


def unit_converter():
    """Convert between different units"""
    create_tool_header("Unit Converter", "Convert between various units of measurement", "📏")

    category = st.selectbox("Unit Category:", [
        "Length", "Weight/Mass", "Temperature", "Area", "Volume", "Speed", "Energy", "Pressure"
    ])

    if category == "Length":
        convert_length()
    elif category == "Weight/Mass":
        convert_weight()
    elif category == "Temperature":
        convert_temperature()
    elif category == "Area":
        convert_area()
    elif category == "Volume":
        convert_volume()
    elif category == "Speed":
        convert_speed()
    else:
        st.info(f"{category} conversion coming soon!")


def convert_length():
    """Convert length units"""
    st.markdown("### 📏 Length Conversion")

    value = st.number_input("Enter value:", value=1.0)

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From:",
                                 ["meters", "kilometers", "centimeters", "millimeters", "inches", "feet", "yards",
                                  "miles"])
    with col2:
        to_unit = st.selectbox("To:", ["meters", "kilometers", "centimeters", "millimeters", "inches", "feet", "yards",
                                       "miles"])

    if st.button("Convert"):
        result = convert_length_units(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")


def convert_length_units(value, from_unit, to_unit):
    """Convert between length units"""
    # Convert to meters first
    to_meters = {
        "meters": 1,
        "kilometers": 1000,
        "centimeters": 0.01,
        "millimeters": 0.001,
        "inches": 0.0254,
        "feet": 0.3048,
        "yards": 0.9144,
        "miles": 1609.344
    }

    meters = value * to_meters[from_unit]
    result = meters / to_meters[to_unit]
    return result


def convert_weight():
    """Convert weight units"""
    st.markdown("### ⚖️ Weight/Mass Conversion")

    value = st.number_input("Enter value:", value=1.0)

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From:", ["kilograms", "grams", "pounds", "ounces", "tons", "stones"])
    with col2:
        to_unit = st.selectbox("To:", ["kilograms", "grams", "pounds", "ounces", "tons", "stones"])

    if st.button("Convert"):
        result = convert_weight_units(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")


def convert_weight_units(value, from_unit, to_unit):
    """Convert between weight units"""
    # Convert to kilograms first
    to_kg = {
        "kilograms": 1,
        "grams": 0.001,
        "pounds": 0.453592,
        "ounces": 0.0283495,
        "tons": 1000,
        "stones": 6.35029
    }

    kg = value * to_kg[from_unit]
    result = kg / to_kg[to_unit]
    return result


def convert_temperature():
    """Convert temperature units"""
    st.markdown("### 🌡️ Temperature Conversion")

    value = st.number_input("Enter temperature:", value=0.0)

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From:", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To:", ["Celsius", "Fahrenheit", "Kelvin"])

    if st.button("Convert"):
        result = convert_temperature_units(value, from_unit, to_unit)
        st.success(f"{value}° {from_unit} = {result:.2f}° {to_unit}")


def convert_temperature_units(value, from_unit, to_unit):
    """Convert between temperature units"""
    # Convert to Celsius first
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:  # Celsius
        celsius = value

    # Convert from Celsius to target
    if to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:  # Celsius
        return celsius


def convert_area():
    """Convert area units"""
    create_tool_header("Area Converter", "Convert between different area units", "📐")

    st.markdown("### 📐 Area Unit Conversion")

    # Area conversion factors (to square meters)
    area_units = {
        "Square Meters (m²)": 1.0,
        "Square Kilometers (km²)": 1000000.0,
        "Square Centimeters (cm²)": 0.0001,
        "Square Millimeters (mm²)": 0.000001,
        "Square Inches (in²)": 0.00064516,
        "Square Feet (ft²)": 0.092903,
        "Square Yards (yd²)": 0.836127,
        "Square Miles (mi²)": 2589988.11,
        "Acres": 4046.86,
        "Hectares (ha)": 10000.0,
        "Square Rods": 25.2929,
        "Square Chains": 404.686,
        "Barns (nuclear)": 1e-28
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        value = st.number_input("Value to convert:", value=1.0, step=0.1, format="%.6f")

    with col2:
        from_unit = st.selectbox("From unit:", list(area_units.keys()))

    with col3:
        to_unit = st.selectbox("To unit:", list(area_units.keys()))

    if st.button("Convert Area"):
        # Convert to square meters first, then to target unit
        meters_squared = value * area_units[from_unit]
        result = meters_squared / area_units[to_unit]

        st.markdown("### 🎯 Conversion Result")
        st.success(f"**{value:,.6f} {from_unit} = {result:,.6f} {to_unit}**")

        # Show intermediate conversion
        st.info(f"Intermediate: {meters_squared:,.6f} m²")

        # Show conversion factor
        factor = area_units[from_unit] / area_units[to_unit]
        st.info(f"Conversion factor: 1 {from_unit} = {factor:,.6f} {to_unit}")

    # Quick conversion table for common units
    with st.expander("🔍 Quick Reference Table"):
        st.markdown("**Common Area Conversions (1 unit =):**")
        ref_conversions = [
            ("1 m²", "10.764 ft²", "1.196 yd²", "1550 in²"),
            ("1 km²", "100 hectares", "247.1 acres", "0.386 mi²"),
            ("1 hectare", "10,000 m²", "2.471 acres", "107,639 ft²"),
            ("1 acre", "4,047 m²", "43,560 ft²", "4,840 yd²"),
            ("1 ft²", "144 in²", "0.111 yd²", "0.0929 m²"),
            ("1 yd²", "9 ft²", "1,296 in²", "0.836 m²")
        ]

        for conversion in ref_conversions:
            st.markdown(f"- {conversion[0]} = {conversion[1]} = {conversion[2]} = {conversion[3]}")


def convert_volume():
    """Convert volume units"""
    create_tool_header("Volume Converter", "Convert between different volume units", "🧪")

    st.markdown("### 🧪 Volume Unit Conversion")

    # Volume conversion factors (to cubic meters)
    volume_units = {
        "Cubic Meters (m³)": 1.0,
        "Cubic Kilometers (km³)": 1e9,
        "Cubic Centimeters (cm³)": 1e-6,
        "Cubic Millimeters (mm³)": 1e-9,
        "Liters (L)": 0.001,
        "Milliliters (mL)": 1e-6,
        "Cubic Inches (in³)": 1.6387064e-5,
        "Cubic Feet (ft³)": 0.0283168,
        "Cubic Yards (yd³)": 0.764555,
        "US Gallons (gal)": 0.00378541,
        "US Quarts (qt)": 0.000946353,
        "US Pints (pt)": 0.000473176,
        "US Cups": 0.000236588,
        "US Fluid Ounces (fl oz)": 2.95735e-5,
        "US Tablespoons (tbsp)": 1.47868e-5,
        "US Teaspoons (tsp)": 4.92892e-6,
        "Imperial Gallons (UK gal)": 0.00454609,
        "Imperial Quarts (UK qt)": 0.00113652,
        "Imperial Pints (UK pt)": 0.000568261,
        "Imperial Fluid Ounces (UK fl oz)": 2.84131e-5,
        "Barrels (Oil, 42 gal)": 0.158987,
        "Barrels (US, 31.5 gal)": 0.119241
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        value = st.number_input("Value to convert:", value=1.0, step=0.001, format="%.6f", key="volume_value")

    with col2:
        from_unit = st.selectbox("From unit:", list(volume_units.keys()), key="volume_from")

    with col3:
        to_unit = st.selectbox("To unit:", list(volume_units.keys()), key="volume_to")

    if st.button("Convert Volume"):
        # Convert to cubic meters first, then to target unit
        cubic_meters = value * volume_units[from_unit]
        result = cubic_meters / volume_units[to_unit]

        st.markdown("### 🎯 Conversion Result")
        st.success(f"**{value:,.6f} {from_unit} = {result:,.6f} {to_unit}**")

        # Show intermediate conversion
        st.info(f"Intermediate: {cubic_meters:,.9f} m³")

        # Show conversion factor
        factor = volume_units[from_unit] / volume_units[to_unit]
        st.info(f"Conversion factor: 1 {from_unit} = {factor:,.6f} {to_unit}")

        # Additional helpful information
        if "Liters" in to_unit or "mL" in to_unit:
            liters = cubic_meters * 1000
            st.info(f"Also equals: {liters:,.3f} liters")

        if "Gallons" in to_unit:
            us_gallons = cubic_meters / 0.00378541
            st.info(f"Also equals: {us_gallons:,.3f} US gallons")

    # Quick conversion tables
    with st.expander("🔍 Quick Reference Tables"):
        st.markdown("**Metric Volume Conversions:**")
        metric_conversions = [
            ("1 m³", "1,000 L", "1,000,000 mL", "1,000,000 cm³"),
            ("1 L", "1,000 mL", "1,000 cm³", "0.001 m³"),
            ("1 mL", "1 cm³", "0.001 L", "0.000001 m³")
        ]

        for conversion in metric_conversions:
            st.markdown(f"- {conversion[0]} = {conversion[1]} = {conversion[2]} = {conversion[3]}")

        st.markdown("**US Liquid Conversions:**")
        us_conversions = [
            ("1 gallon", "4 quarts", "8 pints", "16 cups"),
            ("1 quart", "2 pints", "4 cups", "32 fl oz"),
            ("1 pint", "2 cups", "16 fl oz", "32 tbsp"),
            ("1 cup", "8 fl oz", "16 tbsp", "48 tsp")
        ]

        for conversion in us_conversions:
            st.markdown(f"- {conversion[0]} = {conversion[1]} = {conversion[2]} = {conversion[3]}")


def convert_speed():
    """Convert speed units"""
    create_tool_header("Speed Converter", "Convert between different speed and velocity units", "🏃")

    st.markdown("### 🏃 Speed Unit Conversion")

    # Speed conversion factors (to meters per second)
    speed_units = {
        "Meters per Second (m/s)": 1.0,
        "Kilometers per Hour (km/h)": 1 / 3.6,
        "Miles per Hour (mph)": 0.44704,
        "Feet per Second (ft/s)": 0.3048,
        "Knots (nautical)": 0.514444,
        "Mach (speed of sound)": 343.0,
        "Speed of Light (c)": 299792458.0,
        "Centimeters per Second (cm/s)": 0.01,
        "Inches per Second (in/s)": 0.0254,
        "Yards per Second (yd/s)": 0.9144,
        "Kilometers per Second (km/s)": 1000.0,
        "Miles per Second (mi/s)": 1609.34,
        "Furlongs per Fortnight": 1.663095e-4
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        value = st.number_input("Value to convert:", value=1.0, step=0.001, format="%.6f", key="speed_value")

    with col2:
        from_unit = st.selectbox("From unit:", list(speed_units.keys()), key="speed_from")

    with col3:
        to_unit = st.selectbox("To unit:", list(speed_units.keys()), key="speed_to")

    if st.button("Convert Speed"):
        # Convert to m/s first, then to target unit
        meters_per_second = value * speed_units[from_unit]
        result = meters_per_second / speed_units[to_unit]

        st.markdown("### 🎯 Conversion Result")
        st.success(f"**{value:,.6f} {from_unit} = {result:,.6f} {to_unit}**")

        # Show intermediate conversion
        st.info(f"Intermediate: {meters_per_second:,.6f} m/s")

        # Show conversion factor
        factor = speed_units[from_unit] / speed_units[to_unit]
        st.info(f"Conversion factor: 1 {from_unit} = {factor:,.6f} {to_unit}")

        # Additional helpful conversions
        col1, col2, col3 = st.columns(3)
        with col1:
            kmh = meters_per_second * 3.6
            st.metric("km/h", f"{kmh:.2f}")
        with col2:
            mph = meters_per_second / 0.44704
            st.metric("mph", f"{mph:.2f}")
        with col3:
            knots = meters_per_second / 0.514444
            st.metric("knots", f"{knots:.2f}")

        # Speed categories for context
        if meters_per_second > 0:
            st.markdown("### 📊 Speed Context")

            speed_categories = [
                ("Walking speed", 1.4, "👶"),
                ("Running speed", 5.0, "🏃"),
                ("Bicycle speed", 8.3, "🚴"),
                ("Car speed (city)", 13.9, "🚗"),
                ("Car speed (highway)", 27.8, "🛣️"),
                ("High-speed train", 83.3, "🚄"),
                ("Commercial aircraft", 250.0, "✈️"),
                ("Speed of sound", 343.0, "💥"),
                ("Escape velocity (Earth)", 11180.0, "🚀")
            ]

            closest_category = None
            min_ratio = float('inf')

            for category, speed, emoji in speed_categories:
                ratio = abs(meters_per_second - speed) / speed
                if ratio < min_ratio:
                    min_ratio = ratio
                    closest_category = (category, speed, emoji)

            if closest_category and min_ratio < 2.0:  # Within 200% of reference speed
                category, ref_speed, emoji = closest_category
                st.info(f"{emoji} **Comparable to:** {category} (~{ref_speed:.1f} m/s)")

    # Quick conversion table
    with st.expander("🔍 Quick Reference Table"):
        st.markdown("**Common Speed Conversions:**")
        common_conversions = [
            ("1 m/s", "3.6 km/h", "2.237 mph", "1.944 knots"),
            ("1 km/h", "0.278 m/s", "0.621 mph", "0.540 knots"),
            ("1 mph", "0.447 m/s", "1.609 km/h", "0.869 knots"),
            ("1 knot", "0.514 m/s", "1.852 km/h", "1.151 mph"),
            ("1 ft/s", "0.305 m/s", "1.097 km/h", "0.682 mph"),
            ("Mach 1", "343 m/s", "1,235 km/h", "767 mph")
        ]

        for conversion in common_conversions:
            st.markdown(f"- {conversion[0]} = {conversion[1]} = {conversion[2]} = {conversion[3]}")

        st.markdown("**Reference Speeds:**")
        st.markdown("- 🚶 Walking: ~5 km/h (1.4 m/s)")
        st.markdown("- 🏃 Running: ~18 km/h (5 m/s)")
        st.markdown("- 🚴 Cycling: ~30 km/h (8.3 m/s)")
        st.markdown("- 🚗 City driving: ~50 km/h (13.9 m/s)")
        st.markdown("- 🛣️ Highway: ~100 km/h (27.8 m/s)")
        st.markdown("- ✈️ Commercial jet: ~900 km/h (250 m/s)")
        st.markdown("- 💥 Sound: 1,235 km/h (343 m/s)")
        st.markdown("- 🌍 Earth escape: ~40,300 km/h (11,180 m/s)")


def quadratic_formula():
    """Solve quadratic equations"""
    create_tool_header("Quadratic Formula", "Solve quadratic equations ax² + bx + c = 0", "📐")

    st.markdown("### Quadratic Equation: ax² + bx + c = 0")

    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Coefficient a:", value=1.0)
    with col2:
        b = st.number_input("Coefficient b:", value=0.0)
    with col3:
        c = st.number_input("Coefficient c:", value=0.0)

    if a != 0 and st.button("Solve"):
        discriminant = b ** 2 - 4 * a * c

        st.markdown(f"### Equation: {a}x² + {b}x + {c} = 0")
        st.markdown(f"**Discriminant (Δ):** {discriminant}")

        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            st.success(f"**Two real solutions:**")
            st.write(f"x₁ = {x1:.6f}")
            st.write(f"x₂ = {x2:.6f}")
        elif discriminant == 0:
            x = -b / (2 * a)
            st.success(f"**One real solution:**")
            st.write(f"x = {x:.6f}")
        else:
            real_part = -b / (2 * a)
            imaginary_part = math.sqrt(-discriminant) / (2 * a)
            st.success(f"**Two complex solutions:**")
            st.write(f"x₁ = {real_part:.6f} + {imaginary_part:.6f}i")
            st.write(f"x₂ = {real_part:.6f} - {imaginary_part:.6f}i")
    elif a == 0:
        st.error("Coefficient 'a' cannot be zero for a quadratic equation")


def area_calculator():
    """Calculate areas of various shapes"""
    create_tool_header("Area Calculator", "Calculate areas of geometric shapes", "📐")

    shape = st.selectbox("Select shape:", [
        "Rectangle", "Square", "Triangle", "Circle", "Parallelogram", "Trapezoid", "Ellipse"
    ])

    if shape == "Rectangle":
        calculate_rectangle_area()
    elif shape == "Square":
        calculate_square_area()
    elif shape == "Triangle":
        calculate_triangle_area()
    elif shape == "Circle":
        calculate_circle_area()
    elif shape == "Parallelogram":
        calculate_parallelogram_area()
    elif shape == "Trapezoid":
        calculate_trapezoid_area()
    elif shape == "Ellipse":
        calculate_ellipse_area()


def calculate_rectangle_area():
    """Calculate rectangle area"""
    st.markdown("### 📐 Rectangle Area")

    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input("Length:", min_value=0.0, value=5.0)
    with col2:
        width = st.number_input("Width:", min_value=0.0, value=3.0)

    if st.button("Calculate Area"):
        area = length * width
        perimeter = 2 * (length + width)
        st.success(f"**Area:** {area} square units")
        st.info(f"**Perimeter:** {perimeter} units")


def calculate_square_area():
    """Calculate square area"""
    st.markdown("### ⬜ Square Area")

    side = st.number_input("Side length:", min_value=0.0, value=4.0)

    if st.button("Calculate Area"):
        area = side ** 2
        perimeter = 4 * side
        diagonal = side * math.sqrt(2)
        st.success(f"**Area:** {area} square units")
        st.info(f"**Perimeter:** {perimeter} units")
        st.info(f"**Diagonal:** {diagonal:.6f} units")


def calculate_triangle_area():
    """Calculate triangle area"""
    st.markdown("### 🔺 Triangle Area")

    method = st.selectbox("Calculation method:", ["Base and Height", "Three Sides (Heron's Formula)"])

    if method == "Base and Height":
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Base:", min_value=0.0, value=6.0)
        with col2:
            height = st.number_input("Height:", min_value=0.0, value=4.0)

        if st.button("Calculate Area"):
            area = 0.5 * base * height
            st.success(f"**Area:** {area} square units")

    else:  # Three Sides
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("Side a:", min_value=0.0, value=3.0)
        with col2:
            b = st.number_input("Side b:", min_value=0.0, value=4.0)
        with col3:
            c = st.number_input("Side c:", min_value=0.0, value=5.0)

        if st.button("Calculate Area"):
            # Check if triangle is valid
            if a + b > c and b + c > a and a + c > b:
                s = (a + b + c) / 2  # Semi-perimeter
                area = math.sqrt(s * (s - a) * (s - b) * (s - c))
                st.success(f"**Area:** {area:.6f} square units")
                st.info(f"**Perimeter:** {a + b + c} units")
            else:
                st.error("Invalid triangle! The sum of any two sides must be greater than the third side.")


def calculate_circle_area():
    """Calculate circle area"""
    st.markdown("### ⭕ Circle Area")

    radius = st.number_input("Radius:", min_value=0.0, value=5.0)

    if st.button("Calculate Area"):
        area = math.pi * radius ** 2
        circumference = 2 * math.pi * radius
        diameter = 2 * radius
        st.success(f"**Area:** {area:.6f} square units")
        st.info(f"**Circumference:** {circumference:.6f} units")
        st.info(f"**Diameter:** {diameter} units")


def calculate_parallelogram_area():
    """Calculate parallelogram area"""
    st.markdown("### ▱ Parallelogram Area")

    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("Base:", min_value=0.0, value=6.0)
    with col2:
        height = st.number_input("Height:", min_value=0.0, value=4.0)

    if st.button("Calculate Area"):
        area = base * height
        st.success(f"**Area:** {area} square units")


def calculate_trapezoid_area():
    """Calculate trapezoid area"""
    st.markdown("### 🔺 Trapezoid Area")

    col1, col2, col3 = st.columns(3)
    with col1:
        base1 = st.number_input("Base 1:", min_value=0.0, value=5.0)
    with col2:
        base2 = st.number_input("Base 2:", min_value=0.0, value=3.0)
    with col3:
        height = st.number_input("Height:", min_value=0.0, value=4.0)

    if st.button("Calculate Area"):
        area = 0.5 * (base1 + base2) * height
        st.success(f"**Area:** {area} square units")


def calculate_ellipse_area():
    """Calculate ellipse area"""
    st.markdown("### ⬭ Ellipse Area")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Semi-major axis (a):", min_value=0.0, value=5.0)
    with col2:
        b = st.number_input("Semi-minor axis (b):", min_value=0.0, value=3.0)

    if st.button("Calculate Area"):
        area = math.pi * a * b
        st.success(f"**Area:** {area:.6f} square units")


def trig_functions():
    """Calculate trigonometric functions"""
    create_tool_header("Trigonometric Functions", "Calculate sin, cos, tan and their inverses", "📐")

    angle_unit = st.selectbox("Angle unit:", ["Degrees", "Radians"])
    angle = st.number_input("Enter angle:", value=45.0 if angle_unit == "Degrees" else math.pi / 4)

    if st.button("Calculate"):
        if angle_unit == "Degrees":
            rad_angle = math.radians(angle)
        else:
            rad_angle = angle

        try:
            sin_val = math.sin(rad_angle)
            cos_val = math.cos(rad_angle)
            tan_val = math.tan(rad_angle)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("sin", f"{sin_val:.6f}")
                if abs(sin_val) <= 1:
                    asin_val = math.degrees(math.asin(sin_val)) if angle_unit == "Degrees" else math.asin(sin_val)
                    st.metric("arcsin", f"{asin_val:.6f}")

            with col2:
                st.metric("cos", f"{cos_val:.6f}")
                if abs(cos_val) <= 1:
                    acos_val = math.degrees(math.acos(cos_val)) if angle_unit == "Degrees" else math.acos(cos_val)
                    st.metric("arccos", f"{acos_val:.6f}")

            with col3:
                if abs(tan_val) < 1e10:  # Avoid displaying very large numbers
                    st.metric("tan", f"{tan_val:.6f}")
                else:
                    st.metric("tan", "undefined")

                atan_val = math.degrees(math.atan(tan_val)) if angle_unit == "Degrees" else math.atan(tan_val)
                st.metric("arctan", f"{atan_val:.6f}")

        except Exception as e:
            st.error(f"Error in calculation: {str(e)}")


def function_plotter():
    """Plot mathematical functions"""
    create_tool_header("Function Plotter", "Plot mathematical functions", "📈")

    function = st.text_input("Enter function f(x):", value="x**2", placeholder="x**2, sin(x), exp(x)")

    col1, col2 = st.columns(2)
    with col1:
        x_min = st.number_input("X minimum:", value=-10.0)
        x_max = st.number_input("X maximum:", value=10.0)

    with col2:
        num_points = st.slider("Number of points:", 100, 1000, 500)

    if function and st.button("Plot Function"):
        plot_function(function, x_min, x_max, num_points)


def plot_function(function, x_min, x_max, num_points):
    """Plot mathematical function"""
    try:
        x = np.linspace(x_min, x_max, num_points)

        # Replace common functions for numpy
        func_str = function.replace("^", "**")
        func_str = func_str.replace("ln(", "np.log(")
        func_str = func_str.replace("log(", "np.log10(")
        func_str = func_str.replace("sin(", "np.sin(")
        func_str = func_str.replace("cos(", "np.cos(")
        func_str = func_str.replace("tan(", "np.tan(")
        func_str = func_str.replace("exp(", "np.exp(")
        func_str = func_str.replace("sqrt(", "np.sqrt(")
        func_str = func_str.replace("abs(", "np.abs(")
        func_str = func_str.replace("pi", "np.pi")
        func_str = func_str.replace("e", "np.e")

        # Evaluate function
        allowed_names = {
            "x": x,
            "np": np,
            "__builtins__": {},
        }

        y = eval(func_str, allowed_names)

        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel("x")
        plt.ylabel(f"f(x) = {function}")
        plt.title(f"Plot of f(x) = {function}")

        # Add axis lines
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)

        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

    except Exception as e:
        st.error(f"Error plotting function: {str(e)}")
        st.info("Make sure to use valid Python/NumPy syntax. Examples: x**2, np.sin(x), np.exp(x)")


def descriptive_statistics():
    """Calculate descriptive statistics"""
    create_tool_header("Descriptive Statistics", "Calculate statistical measures", "📊")

    data_input_method = st.selectbox("Data input method:", ["Manual Entry", "Upload File"])

    if data_input_method == "Manual Entry":
        data_text = st.text_area("Enter numbers (separated by commas or spaces):",
                                 placeholder="1, 2, 3, 4, 5 or 1 2 3 4 5")

        if data_text and st.button("Calculate Statistics"):
            try:
                # Parse data
                data = []
                for item in data_text.replace(',', ' ').split():
                    try:
                        data.append(float(item))
                    except ValueError:
                        continue

                if data:
                    calculate_stats(data)
                else:
                    st.error("No valid numbers found in input")

            except Exception as e:
                st.error(f"Error parsing data: {str(e)}")

    else:  # Upload File
        uploaded_file = FileHandler.upload_files(['csv', 'txt'], accept_multiple=False)

        if uploaded_file:
            try:
                if uploaded_file[0].name.endswith('.csv'):
                    df = FileHandler.process_csv_file(uploaded_file[0])
                    numeric_cols = df.select_dtypes(include=[np.number]).columns

                    if len(numeric_cols) > 0:
                        selected_col = st.selectbox("Select column:", numeric_cols)
                        if st.button("Calculate Statistics"):
                            data = df[selected_col].dropna().tolist()
                            calculate_stats(data)
                    else:
                        st.error("No numeric columns found in CSV file")
                else:
                    content = FileHandler.process_text_file(uploaded_file[0])
                    if st.button("Calculate Statistics"):
                        data = []
                        for line in content.split('\n'):
                            for item in line.replace(',', ' ').split():
                                try:
                                    data.append(float(item))
                                except ValueError:
                                    continue

                        if data:
                            calculate_stats(data)
                        else:
                            st.error("No valid numbers found in file")

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")


def calculate_stats(data):
    """Calculate and display statistics"""
    if not data:
        st.error("No data provided")
        return

    data = np.array(data)

    # Basic statistics
    st.markdown("### 📊 Descriptive Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Count", len(data))
        st.metric("Mean", f"{np.mean(data):.4f}")

    with col2:
        st.metric("Median", f"{np.median(data):.4f}")
        st.metric("Mode", f"{stats.mode(data)[0]:.4f}")

    with col3:
        st.metric("Std Dev", f"{np.std(data, ddof=1):.4f}")
        st.metric("Variance", f"{np.var(data, ddof=1):.4f}")

    with col4:
        st.metric("Min", f"{np.min(data):.4f}")
        st.metric("Max", f"{np.max(data):.4f}")

    # Quartiles
    st.markdown("### 📈 Quartiles")
    q1 = np.percentile(data, 25)
    q2 = np.percentile(data, 50)  # Median
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Q1 (25%)", f"{q1:.4f}")
    with col2:
        st.metric("Q2 (50%)", f"{q2:.4f}")
    with col3:
        st.metric("Q3 (75%)", f"{q3:.4f}")
    with col4:
        st.metric("IQR", f"{iqr:.4f}")

    # Histogram
    st.markdown("### 📊 Data Distribution")
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=min(30, len(data) // 2), alpha=0.7, color='skyblue', edgecolor='black')
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Data")
    plt.grid(True, alpha=0.3)
    st.pyplot(plt)
    plt.close()

    # Box plot
    plt.figure(figsize=(10, 4))
    plt.boxplot(data, vert=False)
    plt.xlabel("Value")
    plt.title("Box Plot of Data")
    plt.grid(True, alpha=0.3)
    st.pyplot(plt)
    plt.close()


def motion_calculator():
    """Calculate motion physics"""
    create_tool_header("Motion Calculator", "Calculate motion and kinematics", "🚀")

    motion_type = st.selectbox("Motion type:", [
        "Uniform Motion", "Uniformly Accelerated Motion", "Projectile Motion", "Circular Motion"
    ])

    if motion_type == "Uniform Motion":
        calculate_uniform_motion()
    elif motion_type == "Uniformly Accelerated Motion":
        calculate_accelerated_motion()
    elif motion_type == "Projectile Motion":
        calculate_projectile_motion()
    elif motion_type == "Circular Motion":
        calculate_circular_motion()


def calculate_uniform_motion():
    """Calculate uniform motion"""
    st.markdown("### 🚗 Uniform Motion: v = d/t")

    # Input two values, calculate the third
    col1, col2, col3 = st.columns(3)

    with col1:
        distance = st.number_input("Distance (m):", value=0.0, help="Leave as 0 to calculate")
    with col2:
        time = st.number_input("Time (s):", value=0.0, help="Leave as 0 to calculate")
    with col3:
        velocity = st.number_input("Velocity (m/s):", value=0.0, help="Leave as 0 to calculate")

    if st.button("Calculate"):
        # Count non-zero values
        values = [distance, time, velocity]
        non_zero_count = sum(1 for v in values if v != 0)

        if non_zero_count == 2:
            if distance == 0:
                distance = velocity * time
                st.success(f"**Distance:** {distance} m")
            elif time == 0:
                time = distance / velocity if velocity != 0 else 0
                st.success(f"**Time:** {time} s")
            elif velocity == 0:
                velocity = distance / time if time != 0 else 0
                st.success(f"**Velocity:** {velocity} m/s")
        else:
            st.error("Please provide exactly 2 values and leave the third as 0 to calculate")


def calculate_accelerated_motion():
    """Calculate uniformly accelerated motion"""
    st.markdown("### 🏎️ Uniformly Accelerated Motion")

    st.markdown("**Equations:**")
    st.latex(r"v = u + at")
    st.latex(r"s = ut + \frac{1}{2}at^2")
    st.latex(r"v^2 = u^2 + 2as")

    col1, col2 = st.columns(2)

    with col1:
        u = st.number_input("Initial velocity (u) m/s:", value=0.0)
        v = st.number_input("Final velocity (v) m/s:", value=0.0, help="Leave as 0 if unknown")
        a = st.number_input("Acceleration (a) m/s²:", value=0.0, help="Leave as 0 if unknown")

    with col2:
        t = st.number_input("Time (t) s:", value=0.0, help="Leave as 0 if unknown")
        s = st.number_input("Displacement (s) m:", value=0.0, help="Leave as 0 if unknown")

    if st.button("Calculate"):
        # Try different equations based on known values
        if t != 0 and a != 0:
            v_calc = u + a * t
            s_calc = u * t + 0.5 * a * t ** 2
            st.success(f"**Final velocity:** {v_calc} m/s")
            st.success(f"**Displacement:** {s_calc} m")
        elif v != 0 and a != 0:
            t_calc = (v - u) / a if a != 0 else 0
            s_calc = (v ** 2 - u ** 2) / (2 * a) if a != 0 else 0
            st.success(f"**Time:** {t_calc} s")
            st.success(f"**Displacement:** {s_calc} m")
        else:
            st.error("Please provide sufficient known values")


def calculate_projectile_motion():
    """Calculate projectile motion"""
    create_tool_header("Projectile Motion Calculator",
                       "Calculate trajectory, range, height, and time for projectile motion", "🚀")

    st.markdown("### 🎯 Projectile Motion Parameters")

    # Show key equations
    with st.expander("📚 Key Equations"):
        st.markdown("**Horizontal Motion:**")
        st.latex(r"x = v_0 \cos(\theta) \cdot t")
        st.latex(r"v_x = v_0 \cos(\theta)")

        st.markdown("**Vertical Motion:**")
        st.latex(r"y = v_0 \sin(\theta) \cdot t - \frac{1}{2}gt^2")
        st.latex(r"v_y = v_0 \sin(\theta) - gt")

        st.markdown("**Key Results:**")
        st.latex(r"\text{Time of flight: } T = \frac{2v_0 \sin(\theta)}{g}")
        st.latex(r"\text{Maximum range: } R = \frac{v_0^2 \sin(2\theta)}{g}")
        st.latex(r"\text{Maximum height: } H = \frac{v_0^2 \sin^2(\theta)}{2g}")

    # Input parameters
    col1, col2, col3 = st.columns(3)

    with col1:
        v0 = st.number_input("Initial velocity (v₀) m/s:", min_value=0.0, value=20.0, step=0.1)
        angle_deg = st.number_input("Launch angle (degrees):", min_value=0.0, max_value=90.0, value=45.0, step=0.1)
        g = st.number_input("Gravity (g) m/s²:", value=9.81, step=0.01)

    with col2:
        h0 = st.number_input("Initial height (h₀) m:", value=0.0, step=0.1)
        target_x = st.number_input("Target horizontal distance (m):", value=0.0, step=0.1,
                                   help="Optional: Calculate time to reach this distance")
        target_y = st.number_input("Target height (m):", value=0.0, step=0.1,
                                   help="Optional: Calculate time to reach this height")

    with col3:
        calculation_type = st.selectbox("Calculation Type:", [
            "Complete Trajectory", "Time to Target", "Velocity at Time", "Position at Time"
        ])
        specific_time = 1.0  # Default value
        if calculation_type in ["Velocity at Time", "Position at Time"]:
            specific_time = st.number_input("Specific time (s):", min_value=0.0, value=1.0, step=0.1)

    if st.button("Calculate Projectile Motion"):
        import math

        # Convert angle to radians
        angle_rad = math.radians(angle_deg)

        # Calculate velocity components
        vx0 = v0 * math.cos(angle_rad)
        vy0 = v0 * math.sin(angle_rad)

        if calculation_type == "Complete Trajectory":
            # Calculate key trajectory parameters
            time_of_flight = (vy0 + math.sqrt(vy0 ** 2 + 2 * g * h0)) / g
            max_height = h0 + (vy0 ** 2) / (2 * g)
            max_range = vx0 * time_of_flight
            time_to_max_height = vy0 / g

            # Results
            st.markdown("### 📊 Trajectory Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Time of Flight", f"{time_of_flight:.2f} s")
                st.metric("Maximum Height", f"{max_height:.2f} m")
            with col2:
                st.metric("Maximum Range", f"{max_range:.2f} m")
                st.metric("Time to Max Height", f"{time_to_max_height:.2f} s")
            with col3:
                st.metric("Horizontal Velocity", f"{vx0:.2f} m/s")
                st.metric("Initial Vertical Velocity", f"{vy0:.2f} m/s")

            # Generate trajectory data for plotting
            import numpy as np
            t_points = np.linspace(0, time_of_flight, 100)
            x_points = vx0 * t_points
            y_points = h0 + vy0 * t_points - 0.5 * g * t_points ** 2

            # Create trajectory plot
            try:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(x_points, y_points, 'b-', linewidth=2, label='Trajectory')
                ax.axhline(y=0, color='k', linestyle='-', alpha=0.3, label='Ground')
                ax.scatter([max_range], [0], color='red', s=100, label='Landing Point', zorder=5)
                ax.scatter([vx0 * time_to_max_height], [max_height], color='green', s=100, label='Maximum Height',
                           zorder=5)

                ax.set_xlabel('Horizontal Distance (m)')
                ax.set_ylabel('Height (m)')
                ax.set_title(f'Projectile Trajectory (v₀={v0} m/s, θ={angle_deg}°)')
                ax.grid(True, alpha=0.3)
                ax.legend()
                ax.set_ylim(bottom=0)

                st.pyplot(fig)
                plt.close(fig)
            except ImportError:
                st.info("Install matplotlib to see trajectory visualization")

        elif calculation_type == "Time to Target":
            if target_x > 0:
                time_to_target_x = target_x / vx0
                y_at_target_x = h0 + vy0 * time_to_target_x - 0.5 * g * time_to_target_x ** 2

                st.success(f"**Time to reach x = {target_x} m:** {time_to_target_x:.2f} s")
                st.success(f"**Height at that distance:** {y_at_target_x:.2f} m")

            if target_y >= h0:
                # Solve quadratic equation: h0 + vy0*t - 0.5*g*t² = target_y
                a = -0.5 * g
                b = vy0
                c = h0 - target_y
                discriminant = b ** 2 - 4 * a * c

                if discriminant >= 0:
                    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

                    valid_times = [t for t in [t1, t2] if t >= 0]

                    if valid_times:
                        st.success(
                            f"**Time(s) to reach y = {target_y} m:** {', '.join([f'{t:.2f} s' for t in valid_times])}")
                        for t in valid_times:
                            x_at_time = vx0 * t
                            st.info(f"At t = {t:.2f} s: horizontal distance = {x_at_time:.2f} m")
                    else:
                        st.error("Target height not reachable")
                else:
                    st.error("Target height not reachable")

        elif calculation_type == "Velocity at Time":
            if specific_time >= 0:
                vx_t = vx0  # Horizontal velocity remains constant
                vy_t = vy0 - g * specific_time
                v_magnitude = math.sqrt(vx_t ** 2 + vy_t ** 2)
                v_angle = math.degrees(math.atan2(vy_t, vx_t))

                st.markdown(f"### 🏃 Velocity at t = {specific_time} s")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Horizontal Velocity", f"{vx_t:.2f} m/s")
                    st.metric("Vertical Velocity", f"{vy_t:.2f} m/s")
                with col2:
                    st.metric("Total Velocity", f"{v_magnitude:.2f} m/s")
                    st.metric("Velocity Angle", f"{v_angle:.1f}°")

        elif calculation_type == "Position at Time":
            if specific_time >= 0:
                x_t = vx0 * specific_time
                y_t = h0 + vy0 * specific_time - 0.5 * g * specific_time ** 2

                st.markdown(f"### 📍 Position at t = {specific_time} s")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Horizontal Position", f"{x_t:.2f} m")
                with col2:
                    st.metric("Vertical Position", f"{y_t:.2f} m")

                if y_t < 0:
                    st.warning("⚠️ Projectile has hit the ground before this time!")


def calculate_circular_motion():
    """Calculate circular motion"""
    create_tool_header("Circular Motion Calculator", "Calculate velocity, acceleration, and forces in circular motion",
                       "🌀")

    st.markdown("### ⭕ Circular Motion Parameters")

    # Show key equations
    with st.expander("📚 Key Equations"):
        st.markdown("**Linear and Angular Relationships:**")
        st.latex(r"v = \omega r")
        st.latex(r"\omega = \frac{2\pi}{T} = 2\pi f")

        st.markdown("**Centripetal Acceleration and Force:**")
        st.latex(r"a_c = \frac{v^2}{r} = \omega^2 r")
        st.latex(r"F_c = m a_c = \frac{mv^2}{r} = m\omega^2 r")

        st.markdown("**Where:**")
        st.markdown("- v = linear velocity, ω = angular velocity")
        st.markdown("- r = radius, T = period, f = frequency")
        st.markdown("- aᶜ = centripetal acceleration, Fᶜ = centripetal force")

    # Input parameters
    motion_type = st.selectbox("Motion Type:", [
        "Uniform Circular Motion", "Vertical Circular Motion", "Conical Pendulum", "Banked Curve"
    ])

    if motion_type == "Uniform Circular Motion":
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Given Parameters:**")
            input_type = st.selectbox("Calculate from:", [
                "Linear velocity and radius", "Angular velocity and radius",
                "Period and radius", "Frequency and radius"
            ])

        with col2:
            # Initialize all variables with defaults
            v = 10.0
            omega_input = 2.0
            T = 1.0
            f = 1.0

            if "Linear velocity" in input_type:
                v = st.number_input("Linear velocity (v) m/s:", min_value=0.0, value=10.0, step=0.1)
            if "Angular velocity" in input_type:
                omega_input = st.number_input("Angular velocity (ω) rad/s:", min_value=0.0, value=2.0, step=0.1)
            if "Period" in input_type:
                T = st.number_input("Period (T) s:", min_value=0.001, value=1.0, step=0.1)
            if "Frequency" in input_type:
                f = st.number_input("Frequency (f) Hz:", min_value=0.001, value=1.0, step=0.1)

            r = st.number_input("Radius (r) m:", min_value=0.001, value=5.0, step=0.1)

        with col3:
            mass = st.number_input("Mass (m) kg:", min_value=0.001, value=1.0, step=0.1, help="For force calculations")
            include_forces = st.checkbox("Calculate forces", value=True)

        if st.button("Calculate Uniform Circular Motion"):
            import math

            # Calculate missing parameters based on input
            if "Linear velocity" in input_type:
                omega = v / r
                T = 2 * math.pi / omega
                f = 1 / T
            elif "Angular velocity" in input_type:
                omega = omega_input
                v = omega * r
                T = 2 * math.pi / omega
                f = 1 / T
            elif "Period" in input_type:
                omega = 2 * math.pi / T
                v = omega * r
                f = 1 / T
            elif "Frequency" in input_type:
                omega = 2 * math.pi * f
                v = omega * r
                T = 1 / f

            # Calculate accelerations and forces
            ac = v ** 2 / r  # or omega**2 * r
            Fc = 0.0  # Initialize

            if include_forces:
                Fc = mass * ac

            # Display results
            st.markdown("### 📊 Motion Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Linear Velocity", f"{v:.2f} m/s")
                st.metric("Angular Velocity", f"{omega:.3f} rad/s")
            with col2:
                st.metric("Period", f"{T:.3f} s")
                st.metric("Frequency", f"{f:.3f} Hz")
            with col3:
                st.metric("Centripetal Acceleration", f"{ac:.2f} m/s²")
                if include_forces:
                    st.metric("Centripetal Force", f"{Fc:.2f} N")

            # Additional calculations
            st.markdown("### 🔢 Additional Information")
            col1, col2 = st.columns(2)
            with col1:
                circumference = 2 * math.pi * r
                st.info(f"**Circumference:** {circumference:.2f} m")
                st.info(f"**Angular velocity in RPM:** {omega * 60 / (2 * math.pi):.1f} RPM")
            with col2:
                if include_forces:
                    st.info(f"**Weight of object:** {mass * 9.81:.2f} N")
                    st.info(f"**Fc/Weight ratio:** {Fc / (mass * 9.81):.2f}")

    elif motion_type == "Vertical Circular Motion":
        st.markdown("### 🎡 Vertical Circular Motion")
        col1, col2 = st.columns(2)

        with col1:
            r_vert = st.number_input("Radius (r) m:", min_value=0.001, value=2.0, step=0.1, key="vert_r")
            v_vert = st.number_input("Speed (v) m/s:", min_value=0.0, value=5.0, step=0.1, key="vert_v")
            mass_vert = st.number_input("Mass (m) kg:", min_value=0.001, value=1.0, step=0.1, key="vert_m")

        with col2:
            g = st.number_input("Gravity (g) m/s²:", value=9.81, step=0.01, key="vert_g")
            position = st.selectbox("Calculate forces at:", ["Top of circle", "Bottom of circle", "Side of circle"])

        if st.button("Calculate Vertical Circular Motion"):
            import math

            # Minimum speed for complete loop
            v_min_top = math.sqrt(g * r_vert)

            # Centripetal acceleration
            ac_vert = v_vert ** 2 / r_vert

            # Forces at different positions
            if position == "Top of circle":
                # At top: Fc = mg + N (both point toward center)
                N_top = mass_vert * ac_vert - mass_vert * g
                st.markdown("### 🔝 Forces at Top of Circle")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Normal Force", f"{N_top:.2f} N")
                    st.metric("Weight", f"{mass_vert * g:.2f} N")
                with col2:
                    st.metric("Centripetal Force", f"{mass_vert * ac_vert:.2f} N")
                    st.metric("Minimum Speed for Loop", f"{v_min_top:.2f} m/s")

                if N_top < 0:
                    st.error(f"⚠️ Speed too low! Object will fall. Minimum speed: {v_min_top:.2f} m/s")
                else:
                    st.success("✅ Object maintains contact with track")

            elif position == "Bottom of circle":
                # At bottom: Fc = N - mg (N points up, mg points down)
                N_bottom = mass_vert * ac_vert + mass_vert * g
                st.markdown("### 🔽 Forces at Bottom of Circle")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Normal Force", f"{N_bottom:.2f} N")
                    st.metric("Weight", f"{mass_vert * g:.2f} N")
                with col2:
                    st.metric("Centripetal Force", f"{mass_vert * ac_vert:.2f} N")
                    st.metric("Apparent Weight", f"{N_bottom:.2f} N")

                g_force = N_bottom / (mass_vert * g)
                st.info(f"**G-force experienced:** {g_force:.2f} g")

            elif position == "Side of circle":
                # At side: Fc = N (horizontal), weight is separate
                N_side = mass_vert * ac_vert
                st.markdown("### ↔️ Forces at Side of Circle")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Normal Force (horizontal)", f"{N_side:.2f} N")
                    st.metric("Weight (vertical)", f"{mass_vert * g:.2f} N")
                with col2:
                    st.metric("Centripetal Force", f"{mass_vert * ac_vert:.2f} N")
                    resultant = math.sqrt(N_side ** 2 + (mass_vert * g) ** 2)
                    st.metric("Resultant Force", f"{resultant:.2f} N")

    elif motion_type == "Conical Pendulum":
        st.markdown("### 🎪 Conical Pendulum")
        col1, col2 = st.columns(2)

        with col1:
            L = st.number_input("String length (L) m:", min_value=0.001, value=1.0, step=0.1)
            theta_deg = st.number_input("Angle with vertical (θ) degrees:", min_value=0.1, max_value=89.9, value=30.0,
                                        step=0.1)
            mass_pendulum = st.number_input("Mass (m) kg:", min_value=0.001, value=0.5, step=0.1, key="pendulum_m")

        with col2:
            g_pendulum = st.number_input("Gravity (g) m/s²:", value=9.81, step=0.01, key="pendulum_g")

        if st.button("Calculate Conical Pendulum"):
            import math

            theta_rad = math.radians(theta_deg)
            r_pendulum = L * math.sin(theta_rad)
            h = L * math.cos(theta_rad)  # Height below pivot

            # Period and angular velocity
            T_pendulum = 2 * math.pi * math.sqrt(h / g_pendulum)
            omega_pendulum = 2 * math.pi / T_pendulum
            v_pendulum = omega_pendulum * r_pendulum

            # Forces
            tension = mass_pendulum * g_pendulum / math.cos(theta_rad)
            centripetal_force = tension * math.sin(theta_rad)

            st.markdown("### 📊 Conical Pendulum Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Radius of circle", f"{r_pendulum:.3f} m")
                st.metric("Height below pivot", f"{h:.3f} m")
            with col2:
                st.metric("Period", f"{T_pendulum:.3f} s")
                st.metric("Linear speed", f"{v_pendulum:.3f} m/s")
            with col3:
                st.metric("String tension", f"{tension:.2f} N")
                st.metric("Centripetal force", f"{centripetal_force:.2f} N")

    elif motion_type == "Banked Curve":
        st.markdown("### 🛣️ Banked Curve")
        col1, col2 = st.columns(2)

        with col1:
            r_bank = st.number_input("Radius of curve (r) m:", min_value=0.001, value=50.0, step=1.0)
            bank_angle_deg = st.number_input("Banking angle (θ) degrees:", min_value=0.0, max_value=45.0, value=15.0,
                                             step=0.1)
            mu = st.number_input("Coefficient of friction (μ):", min_value=0.0, max_value=2.0, value=0.3, step=0.01)

        with col2:
            mass_car = st.number_input("Mass of vehicle (m) kg:", min_value=1.0, value=1500.0, step=10.0)
            g_bank = st.number_input("Gravity (g) m/s²:", value=9.81, step=0.01, key="bank_g")

        if st.button("Calculate Banked Curve"):
            import math

            bank_angle_rad = math.radians(bank_angle_deg)

            # Speed for no friction needed
            v_no_friction = math.sqrt(g_bank * r_bank * math.tan(bank_angle_rad))

            # Maximum safe speeds
            numerator_max = g_bank * r_bank * (math.sin(bank_angle_rad) + mu * math.cos(bank_angle_rad))
            denominator_max = math.cos(bank_angle_rad) - mu * math.sin(bank_angle_rad)

            numerator_min = g_bank * r_bank * (math.sin(bank_angle_rad) - mu * math.cos(bank_angle_rad))
            denominator_min = math.cos(bank_angle_rad) + mu * math.sin(bank_angle_rad)

            if denominator_max > 0:
                v_max = math.sqrt(numerator_max / denominator_max)
            else:
                v_max = float('inf')

            if denominator_min > 0 and numerator_min > 0:
                v_min = math.sqrt(numerator_min / denominator_min)
            else:
                v_min = 0

            st.markdown("### 📊 Banked Curve Results")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Speed (no friction needed)", f"{v_no_friction:.1f} m/s ({v_no_friction * 3.6:.1f} km/h)")
                st.metric("Minimum safe speed", f"{v_min:.1f} m/s ({v_min * 3.6:.1f} km/h)")
            with col2:
                if v_max != float('inf'):
                    st.metric("Maximum safe speed", f"{v_max:.1f} m/s ({v_max * 3.6:.1f} km/h)")
                else:
                    st.metric("Maximum safe speed", "No limit")

                st.info(f"**Banking angle:** {bank_angle_deg}°")
                st.info(f"**Friction coefficient:** {mu}")


def molecular_weight():
    """Calculate molecular weight"""
    create_tool_header("Molecular Weight Calculator", "Calculate molecular weight of compounds", "⚛️")

    # Common atomic weights
    atomic_weights = {
        'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
        'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
        'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.380, 'Br': 79.904, 'I': 126.905
    }

    st.markdown("### ⚛️ Enter Chemical Formula")
    formula = st.text_input("Chemical formula:", placeholder="H2O, NaCl, C6H12O6", value="H2O")

    if formula and st.button("Calculate Molecular Weight"):
        mol_weight = calculate_molecular_weight(formula, atomic_weights)
        if mol_weight:
            st.success(f"**Molecular weight of {formula}:** {mol_weight:.3f} g/mol")
        else:
            st.error("Invalid chemical formula or unknown elements")

    # Show available elements
    with st.expander("Available Elements"):
        cols = st.columns(5)
        elements = list(atomic_weights.keys())
        for i, element in enumerate(elements):
            with cols[i % 5]:
                st.write(f"**{element}:** {atomic_weights[element]}")


def calculate_molecular_weight(formula, atomic_weights):
    """Calculate molecular weight from chemical formula"""
    import re

    try:
        # Find all element-number pairs
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula)

        total_weight = 0

        for element, count in matches:
            if element in atomic_weights:
                count = int(count) if count else 1
                total_weight += atomic_weights[element] * count
            else:
                return None  # Unknown element

        return total_weight
    except:
        return None


def prime_numbers():
    """Generate and check prime numbers"""
    create_tool_header("Prime Numbers", "Generate and check prime numbers", "🔢")

    option = st.selectbox("Choose option:", [
        "Check if number is prime",
        "Generate prime numbers up to N",
        "Find prime factors"
    ])

    if option == "Check if number is prime":
        number = st.number_input("Enter number:", min_value=2, value=17, step=1)

        if st.button("Check Prime"):
            if is_prime(int(number)):
                st.success(f"✅ {int(number)} is a prime number!")
            else:
                st.error(f"❌ {int(number)} is not a prime number")

    elif option == "Generate prime numbers up to N":
        n = st.number_input("Generate primes up to:", min_value=2, value=100, step=1)

        if st.button("Generate Primes"):
            primes = generate_primes(int(n))
            st.success(f"Found {len(primes)} prime numbers up to {int(n)}")

            # Display primes in columns
            cols = st.columns(5)
            for i, prime in enumerate(primes):
                with cols[i % 5]:
                    st.write(prime)

    elif option == "Find prime factors":
        number = st.number_input("Enter number to factor:", min_value=2, value=60, step=1)

        if st.button("Find Prime Factors"):
            factors = prime_factors(int(number))
            st.success(f"Prime factors of {int(number)}: {factors}")

            # Show factorization
            factor_str = " × ".join(map(str, factors))
            st.write(f"**Factorization:** {int(number)} = {factor_str}")


def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_primes(n):
    """Generate all prime numbers up to n using Sieve of Eratosthenes"""
    if n < 2:
        return []

    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    return [i for i in range(2, n + 1) if sieve[i]]


def prime_factors(n):
    """Find prime factors of a number"""
    factors = []
    d = 2

    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1

    if n > 1:
        factors.append(n)

    return factors