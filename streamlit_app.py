import streamlit as st
import math

def hollow_cylinder_properties(outer_diameter, inner_diameter, height):
    outer_radius = outer_diameter / 2
    inner_radius = inner_diameter / 2
    volume = math.pi * (outer_radius**2 - inner_radius**2) * height
    outer_surface_area = 2 * math.pi * outer_radius * height
    inner_surface_area = 2 * math.pi * inner_radius * height
    top_bottom_area = math.pi * (outer_radius**2 - inner_radius**2) * 2
    surface_area = outer_surface_area + inner_surface_area + top_bottom_area
    return volume, surface_area

def hollow_rectangle_properties(outer_length, outer_width, inner_length, inner_width, height):
    outer_area = outer_length * outer_width
    inner_area = inner_length * inner_width
    volume = (outer_area - inner_area) * height
    outer_surface_area = 2 * height * (outer_length + outer_width)
    inner_surface_area = 2 * height * (inner_length + inner_width)
    top_bottom_area = 2 * (outer_area - inner_area)
    surface_area = outer_surface_area + inner_surface_area + top_bottom_area
    return volume, surface_area

st.title("Hollow Shape Calculator")

st.header("Hollow Cylinder")
outer_diameter = st.number_input("Outer Diameter (D)", min_value=0.0, format="%.2f")
inner_diameter = st.number_input("Inner Diameter (d)", min_value=0.0, format="%.2f")
cylinder_height = st.number_input("Height (h)", min_value=0.0, format="%.2f")

if st.button("Calculate Cylinder Properties"):
    cylinder_volume, cylinder_surface_area = hollow_cylinder_properties(outer_diameter, inner_diameter, cylinder_height)
    st.write(f"Volume: {cylinder_volume:.2f}")
    st.write(f"Surface Area: {cylinder_surface_area:.2f}")

st.header("Hollow Rectangle")
outer_length = st.number_input("Outer Length (L)", min_value=0.0, format="%.2f")
outer_width = st.number_input("Outer Width (W)", min_value=0.0, format="%.2f")
inner_length = st.number_input("Inner Length (l)", min_value=0.0, format="%.2f")
inner_width = st.number_input("Inner Width (w)", min_value=0.0, format="%.2f")
rectangle_height = st.number_input("Height (h)", min_value=0.0, format="%.2f")

if st.button("Calculate Rectangle Properties"):
    rectangle_volume, rectangle_surface_area = hollow_rectangle_properties(outer_length, outer_width, inner_length, inner_width, rectangle_height)
    st.write(f"Volume: {rectangle_volume:.2f}")
    st.write(f"Surface Area: {rectangle_surface_area:.2f}")
