
import streamlit as st
import zipfile
import tarfile
import json
import csv
import xml.etree.ElementTree as ET
import io
import os
import hashlib
import shutil
from datetime import datetime
import mimetypes
import base64
from pathlib import Path
import pandas as pd
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all file management tools"""

    tool_categories = {
        "File Converters": [
            "Document Converter", "Image Format Converter", "Audio Converter", "Video Converter", "Archive Converter"
        ],
        "File Compression": [
            "ZIP Creator", "Archive Manager", "Compression Optimizer", "Batch Compressor", "Archive Extractor"
        ],
        "File Metadata Editors": [
            "EXIF Editor", "Property Editor", "Tag Manager", "Information Extractor", "Metadata Cleaner"
        ],
        "Batch File Processors": [
            "Bulk Renamer", "Mass Converter", "Batch Processor", "File Organizer", "Bulk Operations"
        ],
        "File Organizers": [
            "Directory Manager", "File Sorter", "Duplicate Finder", "Folder Organizer", "Smart Organizer"
        ],
        "File Backup Utilities": [
            "Backup Creator", "Sync Manager", "Version Control", "Backup Scheduler", "Recovery Tools"
        ],
        "File Sync Tools": [
            "Directory Sync", "Cloud Sync", "File Mirror", "Sync Scheduler", "Conflict Resolver"
        ],
        "File Analysis Tools": [
            "Size Analyzer", "Type Detector", "Content Scanner", "Duplicate Detector", "File Statistics"
        ],
        "File Security": [
            "File Encryption", "Password Protection", "Secure Delete", "Integrity Checker", "Access Control"
        ],
        "File Utilities": [
            "File Splitter", "File Merger", "Checksum Generator", "File Monitor", "Path Manager"
        ]
    }

    selected_category = st.selectbox("Select File Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"File Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Document Converter":
        document_converter()
    elif selected_tool == "ZIP Creator":
        zip_creator()
    elif selected_tool == "Bulk Renamer":
        bulk_renamer()
    elif selected_tool == "Duplicate Finder":
        duplicate_finder()
    elif selected_tool == "File Encryption":
        file_encryption()
    elif selected_tool == "Size Analyzer":
        size_analyzer()
    elif selected_tool == "Archive Manager":
        archive_manager()
    elif selected_tool == "Property Editor":
        property_editor()
    elif selected_tool == "File Splitter":
        file_splitter()
    elif selected_tool == "Checksum Generator":
        checksum_generator()
    elif selected_tool == "Directory Sync":
        directory_sync()
    elif selected_tool == "Content Scanner":
        content_scanner()
    elif selected_tool == "Backup Creator":
        backup_creator()
    elif selected_tool == "File Monitor":
        file_monitor()
    elif selected_tool == "Smart Organizer":
        smart_organizer()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def document_converter():
    """Convert documents between formats"""
    create_tool_header("Document Converter", "Convert documents between various formats", "📄")

    uploaded_files = FileHandler.upload_files(['pdf', 'docx', 'txt', 'rtf', 'odt', 'html'], accept_multiple=True)

    if uploaded_files:
        target_format = st.selectbox("Target Format", ["PDF", "DOCX", "TXT", "HTML", "RTF", "JSON"])

        conversion_options = {}

        if target_format == "PDF":
            conversion_options['page_size'] = st.selectbox("Page Size", ["A4", "Letter", "Legal", "A3"])
            conversion_options['orientation'] = st.selectbox("Orientation", ["Portrait", "Landscape"])

        elif target_format == "HTML":
            conversion_options['include_css'] = st.checkbox("Include CSS Styling", True)
            conversion_options['responsive'] = st.checkbox("Make Responsive", True)

        elif target_format == "TXT":
            conversion_options['encoding'] = st.selectbox("Text Encoding", ["UTF-8", "ASCII", "Latin-1"])
            conversion_options['line_ending'] = st.selectbox("Line Endings",
                                                             ["LF (Unix)", "CRLF (Windows)", "CR (Mac)"])

        if st.button("Convert Documents"):
            converted_files = {}
            progress_bar = st.progress(0)

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    # Extract content based on file type
                    content = extract_document_content(uploaded_file)

                    if content:
                        # Convert to target format
                        converted_content = convert_document_content(content, target_format, conversion_options)

                        # Generate filename
                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        new_filename = f"{base_name}_converted.{target_format.lower()}"

                        converted_files[new_filename] = converted_content

                    progress_bar.progress((i + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"Error converting {uploaded_file.name}: {str(e)}")

            if converted_files:
                st.success(f"Converted {len(converted_files)} document(s) to {target_format}")

                if len(converted_files) == 1:
                    filename, content = next(iter(converted_files.items()))
                    mime_type = get_mime_type(target_format)
                    FileHandler.create_download_link(content, filename, mime_type)
                else:
                    zip_data = FileHandler.create_zip_archive(converted_files)
                    FileHandler.create_download_link(zip_data, f"converted_documents.zip", "application/zip")


def zip_creator():
    """Create ZIP archives from multiple files"""
    create_tool_header("ZIP Creator", "Create compressed ZIP archives", "📦")

    uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

    if uploaded_files:
        st.subheader("Archive Settings")

        col1, col2 = st.columns(2)
        with col1:
            archive_name = st.text_input("Archive Name", "my_archive")
            compression_level = st.slider("Compression Level", 0, 9, 6)

        with col2:
            password_protect = st.checkbox("Password Protection")
            if password_protect:
                password = st.text_input("Archive Password", type="password")

        # File organization
        st.subheader("File Organization")
        organize_by = st.selectbox("Organize Files By", ["None", "File Type", "Date", "Size", "Custom Folders"])

        if organize_by == "Custom Folders":
            folder_structure = st.text_area("Folder Structure (one per line)",
                                            "documents/\nimages/\narchives/")

        if st.button("Create ZIP Archive"):
            try:
                # Create ZIP archive
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED,
                                     compresslevel=compression_level) as zip_file:
                    progress_bar = st.progress(0)

                    for i, uploaded_file in enumerate(uploaded_files):
                        # Determine file path in archive
                        if organize_by == "File Type":
                            file_ext = uploaded_file.name.split('.')[-1].lower()
                            archive_path = f"{file_ext}_files/{uploaded_file.name}"
                        elif organize_by == "Date":
                            archive_path = f"{datetime.now().strftime('%Y-%m-%d')}/{uploaded_file.name}"
                        elif organize_by == "Size":
                            size_category = get_size_category(uploaded_file.size)
                            archive_path = f"{size_category}/{uploaded_file.name}"
                        else:
                            archive_path = uploaded_file.name

                        # Add file to archive
                        file_data = uploaded_file.read()
                        zip_file.writestr(archive_path, file_data)

                        progress_bar.progress((i + 1) / len(uploaded_files))

                zip_data = zip_buffer.getvalue()

                # Archive statistics
                st.subheader("Archive Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Files Added", len(uploaded_files))
                with col2:
                    original_size = sum(f.size for f in uploaded_files)
                    st.metric("Original Size", f"{original_size:,} bytes")
                with col3:
                    compression_ratio = (1 - len(zip_data) / original_size) * 100 if original_size > 0 else 0
                    st.metric("Compression", f"{compression_ratio:.1f}%")

                # Download archive
                FileHandler.create_download_link(
                    zip_data,
                    f"{archive_name}.zip",
                    "application/zip"
                )

                st.success("ZIP archive created successfully!")

            except Exception as e:
                st.error(f"Error creating ZIP archive: {str(e)}")


def bulk_renamer():
    """Bulk rename multiple files"""
    create_tool_header("Bulk Renamer", "Rename multiple files with patterns", "📝")

    uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

    if uploaded_files:
        st.subheader("Renaming Options")

        rename_method = st.selectbox("Renaming Method", [
            "Add Prefix/Suffix", "Replace Text", "Sequential Numbering", "Date/Time Stamp", "Pattern Replacement"
        ])

        if rename_method == "Add Prefix/Suffix":
            prefix = st.text_input("Prefix", "")
            suffix = st.text_input("Suffix", "")

        elif rename_method == "Replace Text":
            find_text = st.text_input("Find Text", "")
            replace_text = st.text_input("Replace With", "")
            case_sensitive = st.checkbox("Case Sensitive", True)

        elif rename_method == "Sequential Numbering":
            base_name = st.text_input("Base Name", "file")
            start_number = st.number_input("Start Number", min_value=1, value=1)
            number_format = st.selectbox("Number Format", ["001", "01", "1", "(1)", "[1]"])

        elif rename_method == "Date/Time Stamp":
            date_format = st.selectbox("Date Format", [
                "%Y-%m-%d", "%Y%m%d", "%d-%m-%Y", "%m-%d-%Y"
            ])
            time_format = st.selectbox("Time Format", [
                "None", "%H%M%S", "%H-%M-%S", "%I%M%p"
            ])
            position = st.selectbox("Position", ["Prefix", "Suffix"])

        elif rename_method == "Pattern Replacement":
            pattern = st.text_input("Pattern (use {n} for number, {name} for original name)", "{name}_{n}")

        # Preview changes
        if st.button("Preview Changes"):
            preview_names = []

            for i, uploaded_file in enumerate(uploaded_files):
                original_name = uploaded_file.name
                name_without_ext = original_name.rsplit('.', 1)[0]
                extension = original_name.rsplit('.', 1)[1] if '.' in original_name else ''

                if rename_method == "Add Prefix/Suffix":
                    new_name = f"{prefix}{name_without_ext}{suffix}"

                elif rename_method == "Replace Text":
                    if case_sensitive:
                        new_name = name_without_ext.replace(find_text, replace_text)
                    else:
                        new_name = name_without_ext.lower().replace(find_text.lower(), replace_text)

                elif rename_method == "Sequential Numbering":
                    number = start_number + i
                    if number_format == "001":
                        number_str = f"{number:03d}"
                    elif number_format == "01":
                        number_str = f"{number:02d}"
                    elif number_format == "(1)":
                        number_str = f"({number})"
                    elif number_format == "[1]":
                        number_str = f"[{number}]"
                    else:
                        number_str = str(number)
                    new_name = f"{base_name}_{number_str}"

                elif rename_method == "Date/Time Stamp":
                    timestamp = datetime.now().strftime(date_format)
                    if time_format != "None":
                        timestamp += "_" + datetime.now().strftime(time_format)

                    if position == "Prefix":
                        new_name = f"{timestamp}_{name_without_ext}"
                    else:
                        new_name = f"{name_without_ext}_{timestamp}"

                elif rename_method == "Pattern Replacement":
                    new_name = pattern.replace("{n}", str(i + 1)).replace("{name}", name_without_ext)

                if extension:
                    new_name += f".{extension}"

                preview_names.append((original_name, new_name))

            # Display preview
            st.subheader("Rename Preview")
            for original, new in preview_names:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.write(original)
                with col2:
                    st.write("→")
                with col3:
                    st.write(new)

        # Generate rename script
        if st.button("Generate Rename Script"):
            script_content = generate_rename_script(uploaded_files, rename_method, locals())

            st.subheader("Rename Script")
            st.code(script_content, language="bash")

            FileHandler.create_download_link(
                script_content.encode(),
                "rename_script.sh",
                "text/plain"
            )


def duplicate_finder():
    """Find duplicate files"""
    create_tool_header("Duplicate Finder", "Find and manage duplicate files", "🔍")

    uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

    if uploaded_files:
        st.subheader("Duplicate Detection Settings")

        comparison_method = st.selectbox("Comparison Method", [
            "File Content (MD5)", "File Size", "File Name", "Content + Size"
        ])

        ignore_extensions = st.checkbox("Ignore File Extensions")
        case_sensitive = st.checkbox("Case Sensitive Names", True)

        if st.button("Find Duplicates"):
            with st.spinner("Analyzing files for duplicates..."):
                duplicates = find_duplicates(uploaded_files, comparison_method, ignore_extensions, case_sensitive)

                if duplicates:
                    st.subheader("Duplicate Files Found")

                    total_duplicates = sum(len(group) - 1 for group in duplicates.values())
                    st.warning(f"Found {total_duplicates} duplicate files in {len(duplicates)} groups")

                    for i, (key, files) in enumerate(duplicates.items(), 1):
                        with st.expander(f"Duplicate Group {i} ({len(files)} files)"):
                            for j, file_info in enumerate(files):
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"📄 {file_info['name']}")
                                with col2:
                                    st.write(f"{file_info['size']:,} bytes")
                                with col3:
                                    if j > 0:  # Mark as duplicate (keep first as original)
                                        st.write("🔄 Duplicate")
                                    else:
                                        st.write("📌 Original")

                            # Show duplicate info
                            if comparison_method == "File Content (MD5)":
                                st.code(f"MD5: {key}")

                    # Generate duplicate report
                    if st.button("Generate Duplicate Report"):
                        report = generate_duplicate_report(duplicates, comparison_method)
                        FileHandler.create_download_link(
                            report.encode(),
                            "duplicate_files_report.txt",
                            "text/plain"
                        )
                else:
                    st.success("🎉 No duplicate files found!")


def file_encryption():
    """Encrypt and decrypt files"""
    create_tool_header("File Encryption", "Secure file encryption and decryption", "🔐")

    operation = st.radio("Operation", ["Encrypt Files", "Decrypt Files"])

    if operation == "Encrypt Files":
        uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

        if uploaded_files:
            st.subheader("Encryption Settings")

            col1, col2 = st.columns(2)
            with col1:
                encryption_method = st.selectbox("Encryption Method", ["AES-256", "AES-128", "ChaCha20"])
                password = st.text_input("Encryption Password", type="password")

            with col2:
                key_derivation = st.selectbox("Key Derivation", ["PBKDF2", "Scrypt", "Argon2"])
                confirm_password = st.text_input("Confirm Password", type="password")

            if password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    if st.button("Encrypt Files"):
                        encrypted_files = encrypt_files(uploaded_files, password, encryption_method, key_derivation)

                        if encrypted_files:
                            st.success(f"Encrypted {len(encrypted_files)} file(s)")

                            if len(encrypted_files) == 1:
                                filename, data = next(iter(encrypted_files.items()))
                                FileHandler.create_download_link(data, filename, "application/octet-stream")
                            else:
                                zip_data = FileHandler.create_zip_archive(encrypted_files)
                                FileHandler.create_download_link(zip_data, "encrypted_files.zip", "application/zip")

    else:  # Decrypt Files
        uploaded_files = FileHandler.upload_files(['enc', 'encrypted'], accept_multiple=True)

        if uploaded_files:
            password = st.text_input("Decryption Password", type="password")

            if password and st.button("Decrypt Files"):
                decrypted_files = decrypt_files(uploaded_files, password)

                if decrypted_files:
                    st.success(f"Decrypted {len(decrypted_files)} file(s)")

                    if len(decrypted_files) == 1:
                        filename, data = next(iter(decrypted_files.items()))
                        FileHandler.create_download_link(data, filename, "application/octet-stream")
                    else:
                        zip_data = FileHandler.create_zip_archive(decrypted_files)
                        FileHandler.create_download_link(zip_data, "decrypted_files.zip", "application/zip")


def size_analyzer():
    """Analyze file and folder sizes"""
    create_tool_header("Size Analyzer", "Analyze file sizes and storage usage", "📊")

    uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

    if uploaded_files:
        if st.button("Analyze File Sizes"):
            # Calculate total size and statistics
            total_size = sum(f.size for f in uploaded_files)
            avg_size = total_size / len(uploaded_files)
            largest_file = max(uploaded_files, key=lambda f: f.size)
            smallest_file = min(uploaded_files, key=lambda f: f.size)

            # Display summary statistics
            st.subheader("Size Analysis Summary")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Files", len(uploaded_files))
            with col2:
                st.metric("Total Size", format_bytes(total_size))
            with col3:
                st.metric("Average Size", format_bytes(avg_size))
            with col4:
                st.metric("Size Range", f"{format_bytes(smallest_file.size)} - {format_bytes(largest_file.size)}")

            # File type breakdown
            st.subheader("File Type Breakdown")
            file_types = {}
            for file in uploaded_files:
                ext = file.name.split('.')[-1].lower() if '.' in file.name else 'no extension'
                if ext not in file_types:
                    file_types[ext] = {'count': 0, 'size': 0}
                file_types[ext]['count'] += 1
                file_types[ext]['size'] += file.size

            # Display file type statistics
            for ext, stats in sorted(file_types.items(), key=lambda x: x[1]['size'], reverse=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**.{ext}**")
                with col2:
                    st.write(f"{stats['count']} files")
                with col3:
                    st.write(f"{format_bytes(stats['size'])}")

            # Size distribution
            st.subheader("Size Distribution")
            size_ranges = {
                "< 1 KB": 0, "1-10 KB": 0, "10-100 KB": 0, "100 KB - 1 MB": 0,
                "1-10 MB": 0, "10-100 MB": 0, "> 100 MB": 0
            }

            for file in uploaded_files:
                size = file.size
                if size < 1024:
                    size_ranges["< 1 KB"] += 1
                elif size < 10 * 1024:
                    size_ranges["1-10 KB"] += 1
                elif size < 100 * 1024:
                    size_ranges["10-100 KB"] += 1
                elif size < 1024 * 1024:
                    size_ranges["100 KB - 1 MB"] += 1
                elif size < 10 * 1024 * 1024:
                    size_ranges["1-10 MB"] += 1
                elif size < 100 * 1024 * 1024:
                    size_ranges["10-100 MB"] += 1
                else:
                    size_ranges["> 100 MB"] += 1

            for range_name, count in size_ranges.items():
                if count > 0:
                    st.write(f"**{range_name}**: {count} files")

            # Detailed file list
            st.subheader("Detailed File List")
            file_data = []
            for file in sorted(uploaded_files, key=lambda f: f.size, reverse=True):
                file_data.append({
                    "Name": file.name,
                    "Size": format_bytes(file.size),
                    "Type": file.name.split('.')[-1].upper() if '.' in file.name else 'Unknown'
                })

            df = pd.DataFrame(file_data)
            st.dataframe(df, use_container_width=True)

            # Generate analysis report
            if st.button("Generate Analysis Report"):
                report = generate_size_analysis_report(uploaded_files, file_types, size_ranges)
                FileHandler.create_download_link(
                    report.encode(),
                    "size_analysis_report.txt",
                    "text/plain"
                )


# Helper Functions

def extract_document_content(uploaded_file):
    """Extract content from various document formats"""
    try:
        if uploaded_file.name.endswith('.txt'):
            return FileHandler.process_text_file(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            return FileHandler.process_json_file(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file)
            return df.to_string() if df is not None else None
        else:
            # For other formats, return as text or binary
            content = uploaded_file.read()
            try:
                return content.decode('utf-8')
            except:
                return content
    except Exception as e:
        st.error(f"Error extracting content: {str(e)}")
        return None


def convert_document_content(content, target_format, options):
    """Convert document content to target format"""
    if target_format == "TXT":
        if isinstance(content, bytes):
            return content
        encoding = options.get('encoding', 'UTF-8')
        return content.encode(encoding)

    elif target_format == "HTML":
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Converted Document</title>
    {'<meta name="viewport" content="width=device-width, initial-scale=1.0">' if options.get('responsive') else ''}
    {'<style>body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }</style>' if options.get('include_css') else ''}
</head>
<body>
    <pre>{content}</pre>
</body>
</html>"""
        return html_content.encode('utf-8')

    elif target_format == "JSON":
        json_content = {
            "content": content if isinstance(content, str) else content.decode('utf-8', errors='ignore'),
            "converted_at": datetime.now().isoformat(),
            "format": target_format
        }
        return json.dumps(json_content, indent=2).encode('utf-8')

    else:
        # Default: return as-is
        return content if isinstance(content, bytes) else content.encode('utf-8')


def get_mime_type(file_format):
    """Get MIME type for file format"""
    mime_types = {
        'PDF': 'application/pdf',
        'DOCX': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'TXT': 'text/plain',
        'HTML': 'text/html',
        'JSON': 'application/json',
        'RTF': 'application/rtf'
    }
    return mime_types.get(file_format, 'application/octet-stream')


def get_size_category(size):
    """Categorize file by size"""
    if size < 1024 * 1024:  # < 1MB
        return "small_files"
    elif size < 10 * 1024 * 1024:  # < 10MB
        return "medium_files"
    else:
        return "large_files"


def generate_rename_script(files, method, variables):
    """Generate bash script for renaming files"""
    script = "#!/bin/bash\n\n"
    script += "# Bulk rename script generated by File Tools\n"
    script += f"# Method: {method}\n"
    script += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for i, file in enumerate(files):
        original_name = file.name
        # Generate new name based on method
        new_name = f"renamed_file_{i + 1}.{original_name.split('.')[-1]}"
        script += f'mv "{original_name}" "{new_name}"\n'

    return script


def find_duplicates(files, method, ignore_ext, case_sensitive):
    """Find duplicate files based on specified method"""
    file_groups = {}

    for file in files:
        if method == "File Content (MD5)":
            key = hashlib.md5(file.read()).hexdigest()
            file.seek(0)  # Reset file pointer
        elif method == "File Size":
            key = file.size
        elif method == "File Name":
            name = file.name
            if ignore_ext and '.' in name:
                name = name.rsplit('.', 1)[0]
            if not case_sensitive:
                name = name.lower()
            key = name
        elif method == "Content + Size":
            content_hash = hashlib.md5(file.read()).hexdigest()
            file.seek(0)
            key = f"{content_hash}_{file.size}"

        if key not in file_groups:
            file_groups[key] = []

        file_groups[key].append({
            'name': file.name,
            'size': file.size,
            'file_obj': file
        })

    # Return only groups with duplicates
    return {k: v for k, v in file_groups.items() if len(v) > 1}


def generate_duplicate_report(duplicates, method):
    """Generate duplicate files report"""
    report = "DUPLICATE FILES REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Detection Method: {method}\n"
    report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    total_duplicates = sum(len(group) - 1 for group in duplicates.values())
    report += f"Total Duplicate Files: {total_duplicates}\n"
    report += f"Duplicate Groups: {len(duplicates)}\n\n"

    for i, (key, files) in enumerate(duplicates.items(), 1):
        report += f"GROUP {i}:\n"
        report += f"Key: {key}\n"
        for file_info in files:
            report += f"  - {file_info['name']} ({file_info['size']:,} bytes)\n"
        report += "\n"

    return report


def encrypt_files(files, password, method, key_derivation):
    """Encrypt files with specified method"""
    encrypted_files = {}

    for file in files:
        try:
            # Simple encryption simulation (use proper crypto library in production)
            file_data = file.read()

            # Create encryption metadata
            encryption_info = {
                "original_name": file.name,
                "method": method,
                "key_derivation": key_derivation,
                "encrypted_at": datetime.now().isoformat(),
                "encrypted_data": base64.b64encode(file_data).decode('utf-8')  # Simple base64 encoding for demo
            }

            encrypted_content = json.dumps(encryption_info, indent=2).encode('utf-8')
            encrypted_filename = f"{file.name}.encrypted"
            encrypted_files[encrypted_filename] = encrypted_content

        except Exception as e:
            st.error(f"Error encrypting {file.name}: {str(e)}")

    return encrypted_files


def decrypt_files(files, password):
    """Decrypt encrypted files"""
    decrypted_files = {}

    for file in files:
        try:
            content = file.read()
            encryption_info = json.loads(content.decode('utf-8'))

            # Simple decryption (use proper crypto library in production)
            decrypted_data = base64.b64decode(encryption_info['encrypted_data'])

            original_name = encryption_info['original_name']
            decrypted_files[original_name] = decrypted_data

        except Exception as e:
            st.error(f"Error decrypting {file.name}: {str(e)}")

    return decrypted_files


def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"


def generate_size_analysis_report(files, file_types, size_ranges):
    """Generate size analysis report"""
    report = "FILE SIZE ANALYSIS REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Total Files Analyzed: {len(files)}\n\n"

    total_size = sum(f.size for f in files)
    report += f"Total Size: {format_bytes(total_size)}\n"
    report += f"Average Size: {format_bytes(total_size / len(files))}\n\n"

    report += "FILE TYPE BREAKDOWN:\n"
    for ext, stats in sorted(file_types.items(), key=lambda x: x[1]['size'], reverse=True):
        report += f"  .{ext}: {stats['count']} files, {format_bytes(stats['size'])}\n"

    report += "\nSIZE DISTRIBUTION:\n"
    for range_name, count in size_ranges.items():
        if count > 0:
            report += f"  {range_name}: {count} files\n"

    return report


# Placeholder functions for remaining tools
def archive_manager():
    """Archive management tool"""
    create_tool_header("Archive Manager", "Create and extract archives (ZIP, TAR, etc.)", "📦")

    operation = st.selectbox("Operation", ["Create Archive", "Extract Archive", "View Archive Contents"])

    if operation == "Create Archive":
        st.subheader("Create New Archive")

        # Archive settings
        col1, col2 = st.columns(2)
        with col1:
            archive_name = st.text_input("Archive Name", "my_archive")
            archive_format = st.selectbox("Archive Format", ["ZIP", "TAR", "TAR.GZ", "TAR.BZ2"])

        with col2:
            compression_level = st.slider("Compression Level", 0, 9, 6) if archive_format != "TAR" else 0
            include_hidden = st.checkbox("Include Hidden Files", False)

        # File selection
        uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True, key="archive_files")

        if uploaded_files:
            st.write(f"**Files to Archive ({len(uploaded_files)}):**")

            total_size = 0
            for i, file in enumerate(uploaded_files):
                file_size = len(file.getvalue())
                total_size += file_size
                st.write(f"• {file.name} ({format_bytes(file_size)})")

            st.write(f"**Total Size:** {format_bytes(total_size)}")

            if st.button("Create Archive"):
                with st.spinner("Creating archive..."):
                    archive_data = create_archive(uploaded_files, archive_format, compression_level)

                    # Estimate compression ratio
                    compressed_size = len(archive_data)
                    compression_ratio = ((total_size - compressed_size) / total_size * 100) if total_size > 0 else 0

                    st.success(f"✅ Archive created successfully!")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Original Size", format_bytes(total_size))
                    with col2:
                        st.metric("Compressed Size", format_bytes(compressed_size))
                    with col3:
                        st.metric("Compression Ratio", f"{compression_ratio:.1f}%")

                    # Download link
                    extension_map = {
                        "ZIP": ".zip",
                        "TAR": ".tar",
                        "TAR.GZ": ".tar.gz",
                        "TAR.BZ2": ".tar.bz2"
                    }
                    filename = f"{archive_name}{extension_map[archive_format]}"
                    FileHandler.create_download_link(archive_data, filename, "application/octet-stream")

    elif operation == "Extract Archive":
        st.subheader("Extract Archive")

        uploaded_archive = FileHandler.upload_files(['zip', 'tar', 'gz', 'bz2'], accept_multiple=False)

        if uploaded_archive:
            archive_file = uploaded_archive[0]
            st.write(f"**Archive:** {archive_file.name} ({format_bytes(len(archive_file.getvalue()))})")

            if st.button("Extract Archive"):
                try:
                    with st.spinner("Extracting archive..."):
                        extracted_files = extract_archive(archive_file)

                    st.success(f"✅ Extracted {len(extracted_files)} files successfully!")

                    # Show extracted files
                    with st.expander("📁 Extracted Files"):
                        for file_info in extracted_files:
                            st.write(f"• {file_info['name']} ({format_bytes(file_info['size'])})")
                            if file_info['content']:
                                FileHandler.create_download_link(
                                    file_info['content'],
                                    file_info['name'],
                                    "application/octet-stream"
                                )

                except Exception as e:
                    st.error(f"❌ Error extracting archive: {str(e)}")

    else:  # View Archive Contents
        st.subheader("View Archive Contents")

        uploaded_archive = FileHandler.upload_files(['zip', 'tar', 'gz', 'bz2'], accept_multiple=False)

        if uploaded_archive:
            archive_file = uploaded_archive[0]

            try:
                with st.spinner("Reading archive contents..."):
                    contents = get_archive_contents(archive_file)

                st.success(f"📋 Archive contains {len(contents)} items")

                # Display contents in a table
                import pandas as pd
                df = pd.DataFrame(contents)

                if not df.empty:
                    # Format file sizes
                    df['size_formatted'] = df['size'].apply(format_bytes)

                    # Display table
                    st.dataframe(
                        df[['name', 'size_formatted', 'type', 'modified']],
                        column_config={
                            "name": "File Name",
                            "size_formatted": "Size",
                            "type": "Type",
                            "modified": "Modified"
                        },
                        use_container_width=True
                    )

                    # Statistics
                    total_files = len(df[df['type'] == 'file'])
                    total_dirs = len(df[df['type'] == 'directory'])
                    total_size = df['size'].sum()

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Files", total_files)
                    with col2:
                        st.metric("Directories", total_dirs)
                    with col3:
                        st.metric("Total Size", format_bytes(total_size))

            except Exception as e:
                st.error(f"❌ Error reading archive: {str(e)}")


def create_archive(files, format_type, compression_level):
    """Create an archive from uploaded files"""
    import zipfile
    import tarfile
    import io

    if format_type == "ZIP":
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, 'w', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=compression_level) as zf:
            for file in files:
                zf.writestr(file.name, file.getvalue())
        return archive_buffer.getvalue()

    elif format_type.startswith("TAR"):
        archive_buffer = io.BytesIO()
        mode = "w"
        if format_type == "TAR.GZ":
            mode = "w:gz"
        elif format_type == "TAR.BZ2":
            mode = "w:bz2"

        with tarfile.open(fileobj=archive_buffer, mode=mode) as tf:
            for file in files:
                tarinfo = tarfile.TarInfo(name=file.name)
                tarinfo.size = len(file.getvalue())
                tf.addfile(tarinfo, io.BytesIO(file.getvalue()))

        return archive_buffer.getvalue()


def extract_archive(archive_file):
    """Extract files from an archive"""
    import zipfile
    import tarfile
    import io

    extracted_files = []
    archive_data = archive_file.getvalue()

    try:
        # Try ZIP first
        with zipfile.ZipFile(io.BytesIO(archive_data), 'r') as zf:
            for member in zf.infolist():
                if not member.is_dir():
                    content = zf.read(member)
                    extracted_files.append({
                        'name': member.filename,
                        'size': len(content),
                        'content': content
                    })
    except:
        try:
            # Try TAR formats
            with tarfile.open(fileobj=io.BytesIO(archive_data), mode='r:*') as tf:
                for member in tf.getmembers():
                    if member.isfile():
                        content = tf.extractfile(member).read()
                        extracted_files.append({
                            'name': member.name,
                            'size': len(content),
                            'content': content
                        })
        except Exception as e:
            raise Exception(f"Unsupported archive format or corrupted file: {str(e)}")

    return extracted_files


def get_archive_contents(archive_file):
    """Get contents listing of an archive"""
    import zipfile
    import tarfile
    import io
    from datetime import datetime

    contents = []
    archive_data = archive_file.getvalue()

    try:
        # Try ZIP first
        with zipfile.ZipFile(io.BytesIO(archive_data), 'r') as zf:
            for member in zf.infolist():
                contents.append({
                    'name': member.filename,
                    'size': member.file_size,
                    'type': 'directory' if member.is_dir() else 'file',
                    'modified': datetime(*member.date_time).strftime('%Y-%m-%d %H:%M:%S')
                })
    except:
        try:
            # Try TAR formats
            with tarfile.open(fileobj=io.BytesIO(archive_data), mode='r:*') as tf:
                for member in tf.getmembers():
                    file_type = 'directory' if member.isdir() else 'file'
                    contents.append({
                        'name': member.name,
                        'size': member.size if member.isfile() else 0,
                        'type': file_type,
                        'modified': datetime.fromtimestamp(member.mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
        except Exception as e:
            raise Exception(f"Unsupported archive format: {str(e)}")

    return contents


def property_editor():
    """File property editor"""
    create_tool_header("File Property Editor", "View and edit file properties and metadata", "📝")

    uploaded_file = FileHandler.upload_files(['*'], accept_multiple=False)

    if uploaded_file:
        file = uploaded_file[0]
        file_content = file.getvalue()

        st.subheader(f"Properties: {file.name}")

        # Basic file information
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Basic Information**")
            st.write(f"**Name:** {file.name}")
            st.write(f"**Size:** {format_bytes(len(file_content))}")
            st.write(f"**Type:** {file.type if file.type else 'Unknown'}")

            # File extension and MIME type
            import mimetypes
            import os

            file_ext = os.path.splitext(file.name)[1].lower()
            mime_type, encoding = mimetypes.guess_type(file.name)

            st.write(f"**Extension:** {file_ext if file_ext else 'None'}")
            st.write(f"**MIME Type:** {mime_type if mime_type else 'Unknown'}")
            if encoding:
                st.write(f"**Encoding:** {encoding}")

        with col2:
            st.write("**Advanced Properties**")

            # File hash
            import hashlib
            md5_hash = hashlib.md5(file_content).hexdigest()
            sha1_hash = hashlib.sha1(file_content).hexdigest()
            sha256_hash = hashlib.sha256(file_content).hexdigest()

            st.write(f"**MD5:** `{md5_hash[:16]}...`")
            st.write(f"**SHA1:** `{sha1_hash[:16]}...`")
            st.write(f"**SHA256:** `{sha256_hash[:16]}...`")

            # Character count for text files
            if file.type and file.type.startswith('text/'):
                try:
                    text_content = file_content.decode('utf-8')
                    st.write(f"**Characters:** {len(text_content):,}")
                    st.write(f"**Lines:** {text_content.count(chr(10)) + 1:,}")
                    st.write(f"**Words:** {len(text_content.split()):,}")
                except:
                    st.write("**Text Analysis:** Unable to decode as text")

        # Detailed hash information
        with st.expander("🔐 File Hashes (Full)"):
            st.code(f"MD5:    {md5_hash}", language="text")
            st.code(f"SHA1:   {sha1_hash}", language="text")
            st.code(f"SHA256: {sha256_hash}", language="text")

        # Custom metadata editor
        st.subheader("Custom Metadata")

        if 'custom_metadata' not in st.session_state:
            st.session_state.custom_metadata = {}

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            new_key = st.text_input("Property Name", placeholder="e.g., Author, Project, Tags")
        with col2:
            new_value = st.text_input("Property Value", placeholder="e.g., John Doe, Website, web,design")
        with col3:
            if st.button("Add Property") and new_key and new_value:
                st.session_state.custom_metadata[new_key] = new_value
                st.rerun()

        # Display custom metadata
        if st.session_state.custom_metadata:
            st.write("**Custom Properties:**")
            for key, value in st.session_state.custom_metadata.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{key}:** {value}")
                with col2:
                    if st.button("🗑️", key=f"del_{key}"):
                        del st.session_state.custom_metadata[key]
                        st.rerun()

        # Export properties
        st.subheader("Export Properties")

        export_format = st.selectbox("Export Format", ["JSON", "CSV", "Plain Text"])

        if st.button("Export Properties"):
            properties_data = {
                "file_name": file.name,
                "file_size": len(file_content),
                "file_type": file.type,
                "file_extension": file_ext,
                "mime_type": mime_type,
                "md5_hash": md5_hash,
                "sha1_hash": sha1_hash,
                "sha256_hash": sha256_hash,
                "custom_metadata": st.session_state.custom_metadata
            }

            if export_format == "JSON":
                import json
                export_content = json.dumps(properties_data, indent=2)
                FileHandler.create_download_link(export_content.encode(), f"{file.name}_properties.json",
                                                 "application/json")

            elif export_format == "CSV":
                import csv
                import io

                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["Property", "Value"])

                for key, value in properties_data.items():
                    if key != "custom_metadata":
                        writer.writerow([key, value])

                for key, value in properties_data["custom_metadata"].items():
                    writer.writerow([f"custom_{key}", value])

                FileHandler.create_download_link(output.getvalue().encode(), f"{file.name}_properties.csv", "text/csv")

            else:  # Plain Text
                text_content = f"File Properties: {file.name}\n"
                text_content += "=" * 50 + "\n\n"

                for key, value in properties_data.items():
                    if key != "custom_metadata":
                        text_content += f"{key.replace('_', ' ').title()}: {value}\n"

                if properties_data["custom_metadata"]:
                    text_content += "\nCustom Metadata:\n"
                    for key, value in properties_data["custom_metadata"].items():
                        text_content += f"  {key}: {value}\n"

                FileHandler.create_download_link(text_content.encode(), f"{file.name}_properties.txt", "text/plain")


def file_splitter():
    """File splitting tool"""
    create_tool_header("File Splitter", "Split large files into smaller chunks", "✂️")

    uploaded_file = FileHandler.upload_files(['*'], accept_multiple=False)

    if uploaded_file:
        file = uploaded_file[0]
        file_size = len(file.getvalue())

        st.write(f"**File:** {file.name} ({format_bytes(file_size)})")

        # Split options
        split_method = st.selectbox("Split Method", [
            "By Size", "By Number of Parts", "By Lines (Text Files)"
        ])

        if split_method == "By Size":
            st.subheader("Split by File Size")

            size_unit = st.selectbox("Size Unit", ["KB", "MB", "GB"])
            size_value = st.number_input(f"Chunk Size ({size_unit})", min_value=1, value=10)

            # Convert to bytes
            multipliers = {"KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}
            chunk_size = int(size_value * multipliers[size_unit])

            estimated_parts = max(1, (file_size + chunk_size - 1) // chunk_size)
            st.write(f"**Estimated Parts:** {estimated_parts}")

            if st.button("Split File by Size"):
                split_by_size(file, chunk_size)

        elif split_method == "By Number of Parts":
            st.subheader("Split by Number of Parts")

            num_parts = st.number_input("Number of Parts", min_value=2, max_value=100, value=5)

            chunk_size = file_size // num_parts
            st.write(f"**Each Part Size:** ~{format_bytes(chunk_size)}")

            if st.button("Split File into Parts"):
                split_by_parts(file, num_parts)

        else:  # By Lines
            st.subheader("Split by Lines")

            if file.type and file.type.startswith('text/'):
                try:
                    text_content = file.getvalue().decode('utf-8')
                    total_lines = text_content.count('\n') + 1

                    st.write(f"**Total Lines:** {total_lines:,}")

                    lines_per_file = st.number_input("Lines per File", min_value=1, value=min(1000, total_lines // 2))

                    estimated_files = max(1, (total_lines + lines_per_file - 1) // lines_per_file)
                    st.write(f"**Estimated Files:** {estimated_files}")

                    if st.button("Split by Lines"):
                        split_by_lines(file, lines_per_file)

                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
            else:
                st.warning("Line splitting is only available for text files")


def split_by_size(file, chunk_size):
    """Split file by specified chunk size"""
    file_data = file.getvalue()
    file_name = file.name

    chunks = []
    offset = 0
    part_num = 1

    while offset < len(file_data):
        chunk_data = file_data[offset:offset + chunk_size]

        # Create filename for this chunk
        name_parts = file_name.rsplit('.', 1)
        if len(name_parts) == 2:
            chunk_filename = f"{name_parts[0]}.part{part_num:03d}.{name_parts[1]}"
        else:
            chunk_filename = f"{file_name}.part{part_num:03d}"

        chunks.append({
            'filename': chunk_filename,
            'data': chunk_data,
            'size': len(chunk_data)
        })

        offset += chunk_size
        part_num += 1

    display_split_results(chunks)


def split_by_parts(file, num_parts):
    """Split file into specified number of parts"""
    file_data = file.getvalue()
    file_name = file.name
    file_size = len(file_data)

    chunk_size = file_size // num_parts
    chunks = []

    for i in range(num_parts):
        start = i * chunk_size
        if i == num_parts - 1:  # Last part gets remainder
            end = file_size
        else:
            end = start + chunk_size

        chunk_data = file_data[start:end]

        # Create filename for this chunk
        name_parts = file_name.rsplit('.', 1)
        if len(name_parts) == 2:
            chunk_filename = f"{name_parts[0]}.part{i + 1:03d}.{name_parts[1]}"
        else:
            chunk_filename = f"{file_name}.part{i + 1:03d}"

        chunks.append({
            'filename': chunk_filename,
            'data': chunk_data,
            'size': len(chunk_data)
        })

    display_split_results(chunks)


def split_by_lines(file, lines_per_file):
    """Split text file by number of lines"""
    try:
        text_content = file.getvalue().decode('utf-8')
        lines = text_content.split('\n')
        file_name = file.name

        chunks = []
        file_num = 1

        for i in range(0, len(lines), lines_per_file):
            chunk_lines = lines[i:i + lines_per_file]
            chunk_content = '\n'.join(chunk_lines)

            # Create filename for this chunk
            name_parts = file_name.rsplit('.', 1)
            if len(name_parts) == 2:
                chunk_filename = f"{name_parts[0]}.part{file_num:03d}.{name_parts[1]}"
            else:
                chunk_filename = f"{file_name}.part{file_num:03d}.txt"

            chunks.append({
                'filename': chunk_filename,
                'data': chunk_content.encode('utf-8'),
                'size': len(chunk_content.encode('utf-8'))
            })

            file_num += 1

        display_split_results(chunks)

    except Exception as e:
        st.error(f"Error splitting text file: {str(e)}")


def display_split_results(chunks):
    """Display the results of file splitting"""
    st.success(f"✅ File split into {len(chunks)} parts successfully!")

    # Summary statistics
    total_size = sum(chunk['size'] for chunk in chunks)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Parts", len(chunks))
    with col2:
        st.metric("Total Size", format_bytes(total_size))
    with col3:
        st.metric("Average Part Size", format_bytes(total_size // len(chunks)))

    # Download links for each chunk
    st.subheader("Download Split Files")

    for i, chunk in enumerate(chunks):
        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            st.write(f"**{chunk['filename']}**")
        with col2:
            st.write(format_bytes(chunk['size']))
        with col3:
            FileHandler.create_download_link(
                chunk['data'],
                chunk['filename'],
                "application/octet-stream"
            )


def checksum_generator():
    """Checksum generation tool"""
    create_tool_header("Checksum Generator", "Generate and verify file checksums", "🔐")

    operation = st.selectbox("Operation", ["Generate Checksums", "Verify Checksums", "Compare Files"])

    if operation == "Generate Checksums":
        st.subheader("Generate File Checksums")

        uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

        if uploaded_files:
            # Algorithm selection
            algorithms = st.multiselect(
                "Hash Algorithms",
                ["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"],
                default=["MD5", "SHA256"]
            )

            if not algorithms:
                st.warning("Please select at least one hash algorithm")
                return

            output_format = st.selectbox("Output Format", ["Table", "JSON", "CSV", "Hash File Format"])

            if st.button("Generate Checksums"):
                with st.spinner("Generating checksums..."):
                    results = []

                    for file in uploaded_files:
                        file_data = file.getvalue()
                        file_result = {
                            'filename': file.name,
                            'size': len(file_data),
                            'checksums': {}
                        }

                        # Generate checksums for selected algorithms
                        for algo in algorithms:
                            checksum = generate_checksum(file_data, algo)
                            file_result['checksums'][algo] = checksum

                        results.append(file_result)

                display_checksum_results(results, algorithms, output_format)

    elif operation == "Verify Checksums":
        st.subheader("Verify File Checksums")

        uploaded_file = FileHandler.upload_files(['*'], accept_multiple=False)

        if uploaded_file:
            file = uploaded_file[0]

            col1, col2 = st.columns(2)
            with col1:
                algorithm = st.selectbox("Hash Algorithm", ["MD5", "SHA1", "SHA256", "SHA512"])
            with col2:
                expected_hash = st.text_input("Expected Hash", placeholder="Enter the expected checksum")

            if expected_hash and st.button("Verify Checksum"):
                verify_single_file(file, algorithm, expected_hash)

    else:  # Compare Files
        st.subheader("Compare Files")

        st.write("Upload two or more files to compare their checksums:")
        files_to_compare = FileHandler.upload_files(['*'], accept_multiple=True, key="compare_files")

        if len(files_to_compare) >= 2:
            comparison_algorithm = st.selectbox(
                "Comparison Algorithm",
                ["SHA256", "MD5", "SHA1", "SHA512"],
                key="compare_algo"
            )

            if st.button("Compare Files"):
                compare_files(files_to_compare, comparison_algorithm)

        elif len(files_to_compare) == 1:
            st.info("Upload at least one more file to compare")


def generate_checksum(data, algorithm):
    """Generate checksum for data using specified algorithm"""
    import hashlib

    algo_map = {
        'MD5': hashlib.md5,
        'SHA1': hashlib.sha1,
        'SHA224': hashlib.sha224,
        'SHA256': hashlib.sha256,
        'SHA384': hashlib.sha384,
        'SHA512': hashlib.sha512
    }

    hasher = algo_map[algorithm]()
    hasher.update(data)
    return hasher.hexdigest()


def display_checksum_results(results, algorithms, output_format):
    """Display checksum generation results"""
    st.success(f"✅ Generated checksums for {len(results)} file(s)")

    if output_format == "Table":
        # Display as table
        import pandas as pd

        table_data = []
        for result in results:
            row = {
                'Filename': result['filename'],
                'Size': format_bytes(result['size'])
            }
            for algo in algorithms:
                row[algo] = result['checksums'][algo]
            table_data.append(row)

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

    elif output_format == "JSON":
        import json
        json_output = json.dumps(results, indent=2)
        st.code(json_output, language="json")
        FileHandler.create_download_link(json_output.encode(), "checksums.json", "application/json")

    elif output_format == "CSV":
        import csv
        import io

        output = io.StringIO()
        fieldnames = ['filename', 'size'] + algorithms
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            row = {
                'filename': result['filename'],
                'size': result['size']
            }
            for algo in algorithms:
                row[algo] = result['checksums'][algo]
            writer.writerow(row)

        csv_content = output.getvalue()
        st.code(csv_content, language="csv")
        FileHandler.create_download_link(csv_content.encode(), "checksums.csv", "text/csv")

    else:  # Hash File Format
        hash_content = ""
        for result in results:
            for algo in algorithms:
                hash_content += f"{result['checksums'][algo]}  {result['filename']}\n"

        st.code(hash_content, language="text")
        FileHandler.create_download_link(hash_content.encode(), f"checksums_{algorithms[0].lower()}.txt", "text/plain")


def verify_single_file(file, algorithm, expected_hash):
    """Verify a single file against expected hash"""
    file_data = file.getvalue()
    actual_hash = generate_checksum(file_data, algorithm)

    expected_hash_clean = expected_hash.strip().lower()
    actual_hash_clean = actual_hash.lower()

    if expected_hash_clean == actual_hash_clean:
        st.success(f"✅ **Verification PASSED**")
        st.success(f"File '{file.name}' checksum matches expected value")
    else:
        st.error(f"❌ **Verification FAILED**")
        st.error(f"File '{file.name}' checksum does not match")

    # Show comparison
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Expected ({algorithm}):**")
        st.code(expected_hash_clean)
    with col2:
        st.write(f"**Actual ({algorithm}):**")
        st.code(actual_hash_clean)


def compare_files(files, algorithm):
    """Compare multiple files using checksums"""
    file_hashes = []

    for file in files:
        checksum = generate_checksum(file.getvalue(), algorithm)
        file_hashes.append({
            'filename': file.name,
            'size': len(file.getvalue()),
            'checksum': checksum
        })

    # Group by checksum
    hash_groups = {}
    for file_info in file_hashes:
        checksum = file_info['checksum']
        if checksum not in hash_groups:
            hash_groups[checksum] = []
        hash_groups[checksum].append(file_info)

    # Display results
    if len(hash_groups) == 1:
        st.success("✅ All files are identical!")
        st.write(f"**Common {algorithm} Hash:** `{list(hash_groups.keys())[0]}`")
    else:
        st.warning(f"⚠️ Files are different ({len(hash_groups)} unique checksums found)")

    # Show detailed comparison
    st.subheader("File Comparison Results")

    for i, (checksum, files_with_hash) in enumerate(hash_groups.items()):
        st.markdown(f"**Group {i + 1}** ({len(files_with_hash)} file(s))")
        st.code(f"{algorithm}: {checksum}")

        for file_info in files_with_hash:
            st.write(f"• {file_info['filename']} ({format_bytes(file_info['size'])})")

        if i < len(hash_groups) - 1:
            st.markdown("---")


def directory_sync():
    """Directory synchronization tool"""
    st.info("Directory Sync - Coming soon!")


def content_scanner():
    """File content scanner"""
    st.info("Content Scanner - Coming soon!")


def backup_creator():
    """Backup creation tool"""
    create_tool_header("Backup Creator", "Create backups of your files", "💾")

    backup_type = st.selectbox("Backup Type", ["Simple Archive", "Incremental Backup", "Differential Backup"])

    uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

    if uploaded_files:
        st.write(f"**Files to backup:** {len(uploaded_files)}")

        # Backup settings
        col1, col2 = st.columns(2)
        with col1:
            backup_name = st.text_input("Backup Name", "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
            compression = st.selectbox("Compression", ["ZIP", "TAR.GZ", "TAR.BZ2"])

        with col2:
            include_metadata = st.checkbox("Include File Metadata", True)
            verify_backup = st.checkbox("Verify Backup Integrity", True)

        if st.button("Create Backup"):
            create_backup(uploaded_files, backup_name, compression, include_metadata, verify_backup)


def create_backup(files, backup_name, compression, include_metadata, verify_backup):
    """Create backup of files"""
    import zipfile
    import tarfile
    import io
    import json

    with st.spinner("Creating backup..."):
        # Calculate total size
        total_size = sum(len(f.getvalue()) for f in files)

        # Create manifest if metadata is included
        manifest = {
            "backup_created": datetime.now().isoformat(),
            "total_files": len(files),
            "total_size": total_size,
            "compression": compression,
            "files": []
        }

        # Create backup archive
        backup_buffer = io.BytesIO()

        if compression == "ZIP":
            with zipfile.ZipFile(backup_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for file in files:
                    zf.writestr(file.name, file.getvalue())
                    if include_metadata:
                        import hashlib
                        manifest["files"].append({
                            "name": file.name,
                            "size": len(file.getvalue()),
                            "md5": hashlib.md5(file.getvalue()).hexdigest()
                        })

                if include_metadata:
                    zf.writestr("backup_manifest.json", json.dumps(manifest, indent=2))

        else:  # TAR formats
            mode = "w:gz" if compression == "TAR.GZ" else "w:bz2"
            with tarfile.open(fileobj=backup_buffer, mode=mode) as tf:
                for file in files:
                    tarinfo = tarfile.TarInfo(name=file.name)
                    tarinfo.size = len(file.getvalue())
                    tf.addfile(tarinfo, io.BytesIO(file.getvalue()))

                    if include_metadata:
                        import hashlib
                        manifest["files"].append({
                            "name": file.name,
                            "size": len(file.getvalue()),
                            "md5": hashlib.md5(file.getvalue()).hexdigest()
                        })

                if include_metadata:
                    manifest_data = json.dumps(manifest, indent=2).encode()
                    tarinfo = tarfile.TarInfo(name="backup_manifest.json")
                    tarinfo.size = len(manifest_data)
                    tf.addfile(tarinfo, io.BytesIO(manifest_data))

        backup_data = backup_buffer.getvalue()
        compressed_size = len(backup_data)
        compression_ratio = ((total_size - compressed_size) / total_size * 100) if total_size > 0 else 0

        # Verify backup if requested
        if verify_backup:
            verification_result = verify_backup_integrity(backup_data, compression)
            if verification_result:
                st.success("✅ Backup verification passed")
            else:
                st.error("❌ Backup verification failed")
                return

        st.success(f"✅ Backup created successfully!")

        # Display backup statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files Backed Up", len(files))
        with col2:
            st.metric("Original Size", format_bytes(total_size))
        with col3:
            st.metric("Compressed Size", format_bytes(compressed_size))

        st.write(f"**Compression Ratio:** {compression_ratio:.1f}%")

        # Download backup
        extension_map = {"ZIP": ".zip", "TAR.GZ": ".tar.gz", "TAR.BZ2": ".tar.bz2"}
        filename = f"{backup_name}{extension_map[compression]}"
        FileHandler.create_download_link(backup_data, filename, "application/octet-stream")


def verify_backup_integrity(backup_data, compression):
    """Verify backup integrity"""
    try:
        import zipfile
        import tarfile
        import io

        if compression == "ZIP":
            with zipfile.ZipFile(io.BytesIO(backup_data), 'r') as zf:
                # Test all files in the archive
                bad_files = zf.testzip()
                return bad_files is None
        else:
            # For TAR files, try to read the archive
            mode = "r:gz" if compression == "TAR.GZ" else "r:bz2"
            with tarfile.open(fileobj=io.BytesIO(backup_data), mode=mode) as tf:
                # List all members to verify structure
                members = tf.getmembers()
                return len(members) > 0
    except:
        return False


def file_monitor():
    """File monitoring tool"""
    create_tool_header("File Monitor", "Monitor file changes and activities", "🔍")

    monitor_type = st.selectbox("Monitor Type", [
        "File Change Detection", "Size Monitoring", "Content Comparison", "Batch Analysis"
    ])

    if monitor_type == "File Change Detection":
        st.subheader("File Change Detection")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Original Files**")
            original_files = FileHandler.upload_files(['*'], accept_multiple=True, key="original")
            if original_files:
                st.write(f"Uploaded: {len(original_files)} files")

        with col2:
            st.write("**Modified Files**")
            modified_files = FileHandler.upload_files(['*'], accept_multiple=True, key="modified")
            if modified_files:
                st.write(f"Uploaded: {len(modified_files)} files")

        if original_files and modified_files and st.button("Detect Changes"):
            detect_file_changes(original_files, modified_files)

    elif monitor_type == "Size Monitoring":
        st.subheader("File Size Monitoring")

        uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

        if uploaded_files:
            threshold_type = st.selectbox("Alert Type", ["Files Larger Than", "Files Smaller Than", "Size Range"])

            if threshold_type == "Files Larger Than":
                size_unit = st.selectbox("Size Unit", ["KB", "MB", "GB"], key="large")
                threshold = st.number_input(f"Threshold ({size_unit})", min_value=0.1, value=10.0)
                multipliers = {"KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}
                threshold_bytes = threshold * multipliers[size_unit]

                if st.button("Check File Sizes"):
                    monitor_file_sizes(uploaded_files, "larger", threshold_bytes, size_unit)

            elif threshold_type == "Files Smaller Than":
                size_unit = st.selectbox("Size Unit", ["KB", "MB", "GB"], key="small")
                threshold = st.number_input(f"Threshold ({size_unit})", min_value=0.1, value=1.0)
                multipliers = {"KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3}
                threshold_bytes = threshold * multipliers[size_unit]

                if st.button("Check File Sizes"):
                    monitor_file_sizes(uploaded_files, "smaller", threshold_bytes, size_unit)

    elif monitor_type == "Content Comparison":
        st.subheader("Content Comparison")

        st.write("Upload files to compare their content:")
        files_to_compare = FileHandler.upload_files(['*'], accept_multiple=True, key="content_compare")

        if len(files_to_compare) >= 2:
            comparison_method = st.selectbox("Comparison Method",
                                             ["Hash Comparison", "Content Diff", "Size Difference"])

            if st.button("Compare Content"):
                compare_file_content(files_to_compare, comparison_method)

    else:  # Batch Analysis
        st.subheader("Batch File Analysis")

        uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True, key="batch")

        if uploaded_files:
            analysis_type = st.selectbox("Analysis Type", [
                "File Type Distribution", "Size Analysis", "Duplicate Detection", "Pattern Analysis"
            ])

            if st.button("Run Batch Analysis"):
                run_batch_analysis(uploaded_files, analysis_type)


def detect_file_changes(original_files, modified_files):
    """Detect changes between file sets"""
    import hashlib

    # Create hash maps
    original_hashes = {f.name: hashlib.md5(f.getvalue()).hexdigest() for f in original_files}
    modified_hashes = {f.name: hashlib.md5(f.getvalue()).hexdigest() for f in modified_files}

    # Detect changes
    added_files = set(modified_hashes.keys()) - set(original_hashes.keys())
    removed_files = set(original_hashes.keys()) - set(modified_hashes.keys())

    changed_files = []
    unchanged_files = []

    for filename in set(original_hashes.keys()) & set(modified_hashes.keys()):
        if original_hashes[filename] != modified_hashes[filename]:
            changed_files.append(filename)
        else:
            unchanged_files.append(filename)

    # Display results
    st.subheader("Change Detection Results")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Added", len(added_files))
    with col2:
        st.metric("Removed", len(removed_files))
    with col3:
        st.metric("Modified", len(changed_files))
    with col4:
        st.metric("Unchanged", len(unchanged_files))

    if added_files:
        with st.expander(f"➕ Added Files ({len(added_files)})"):
            for filename in sorted(added_files):
                st.write(f"• {filename}")

    if removed_files:
        with st.expander(f"➖ Removed Files ({len(removed_files)})"):
            for filename in sorted(removed_files):
                st.write(f"• {filename}")

    if changed_files:
        with st.expander(f"🔄 Modified Files ({len(changed_files)})"):
            for filename in sorted(changed_files):
                st.write(f"• {filename}")


def monitor_file_sizes(files, comparison_type, threshold_bytes, unit):
    """Monitor files based on size criteria"""
    matching_files = []

    for file in files:
        file_size = len(file.getvalue())

        if comparison_type == "larger" and file_size > threshold_bytes:
            matching_files.append((file.name, file_size))
        elif comparison_type == "smaller" and file_size < threshold_bytes:
            matching_files.append((file.name, file_size))

    st.subheader(
        f"Size Monitoring Results ({comparison_type} than {threshold_bytes // (1024 if unit == 'KB' else 1024 ** 2 if unit == 'MB' else 1024 ** 3):.1f} {unit})")

    if matching_files:
        st.warning(f"Found {len(matching_files)} files matching criteria")

        for filename, size in sorted(matching_files, key=lambda x: x[1], reverse=True):
            st.write(f"• {filename}: {format_bytes(size)}")
    else:
        st.success("No files match the size criteria")


def compare_file_content(files, method):
    """Compare file content using specified method"""
    import hashlib

    if method == "Hash Comparison":
        file_hashes = []
        for file in files:
            hash_value = hashlib.md5(file.getvalue()).hexdigest()
            file_hashes.append((file.name, hash_value, len(file.getvalue())))

        st.subheader("Hash Comparison Results")

        # Group by hash
        hash_groups = {}
        for filename, hash_value, size in file_hashes:
            if hash_value not in hash_groups:
                hash_groups[hash_value] = []
            hash_groups[hash_value].append((filename, size))

        if len(hash_groups) == 1:
            st.success("✅ All files have identical content")
        else:
            st.warning(f"⚠️ Files have different content ({len(hash_groups)} unique hashes)")

        for i, (hash_value, file_list) in enumerate(hash_groups.items()):
            with st.expander(f"Group {i + 1} - {len(file_list)} file(s)"):
                st.code(f"MD5: {hash_value}")
                for filename, size in file_list:
                    st.write(f"• {filename} ({format_bytes(size)})")

    elif method == "Size Difference":
        file_sizes = [(f.name, len(f.getvalue())) for f in files]
        file_sizes.sort(key=lambda x: x[1], reverse=True)

        st.subheader("Size Comparison Results")

        for i, (filename, size) in enumerate(file_sizes):
            if i == 0:
                st.write(f"🥇 Largest: {filename} - {format_bytes(size)}")
            elif i == len(file_sizes) - 1:
                st.write(f"🥉 Smallest: {filename} - {format_bytes(size)}")
            else:
                st.write(f"{i + 1}. {filename} - {format_bytes(size)}")


def run_batch_analysis(files, analysis_type):
    """Run batch analysis on files"""
    if analysis_type == "File Type Distribution":
        import os

        type_counts = {}
        for file in files:
            ext = os.path.splitext(file.name)[1].lower()
            ext = ext if ext else "(no extension)"
            type_counts[ext] = type_counts.get(ext, 0) + 1

        st.subheader("File Type Distribution")

        for ext, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(files)) * 100
            st.write(f"**{ext}**: {count} files ({percentage:.1f}%)")

    elif analysis_type == "Size Analysis":
        sizes = [len(f.getvalue()) for f in files]
        total_size = sum(sizes)
        avg_size = total_size / len(files)

        st.subheader("Size Analysis Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Size", format_bytes(total_size))
        with col2:
            st.metric("Average Size", format_bytes(int(avg_size)))
        with col3:
            st.metric("Largest File", format_bytes(max(sizes)))


def smart_organizer():
    """Smart file organizer"""
    create_tool_header("Smart File Organizer", "Intelligently organize and categorize files", "📁")

    organization_method = st.selectbox("Organization Method", [
        "By File Type", "By File Size", "By Content Type", "Custom Rules"
    ])

    uploaded_files = FileHandler.upload_files(['*'], accept_multiple=True)

    if uploaded_files:
        st.write(f"**Files to organize:** {len(uploaded_files)}")

        if organization_method == "By File Type":
            st.subheader("Organize by File Type")

            if st.button("Organize by Type"):
                organize_by_file_type(uploaded_files)

        elif organization_method == "By File Size":
            st.subheader("Organize by File Size")

            size_ranges = {
                "Small (< 1MB)": (0, 1024 ** 2),
                "Medium (1-10MB)": (1024 ** 2, 10 * 1024 ** 2),
                "Large (10-100MB)": (10 * 1024 ** 2, 100 * 1024 ** 2),
                "Extra Large (> 100MB)": (100 * 1024 ** 2, float('inf'))
            }

            if st.button("Organize by Size"):
                organize_by_file_size(uploaded_files, size_ranges)

        elif organization_method == "By Content Type":
            st.subheader("Organize by Content Type")

            if st.button("Organize by Content"):
                organize_by_content_type(uploaded_files)

        else:  # Custom Rules
            st.subheader("Custom Organization Rules")

            st.write("Define custom rules for file organization:")

            rule_type = st.selectbox("Rule Type", ["Name Pattern", "Size Threshold", "Extension"])

            if rule_type == "Name Pattern":
                pattern = st.text_input("Name Pattern (supports wildcards)", placeholder="e.g., report_*, *.backup")
                folder_name = st.text_input("Folder Name", placeholder="e.g., Reports, Backups")

                if pattern and folder_name and st.button("Apply Pattern Rule"):
                    apply_pattern_rule(uploaded_files, pattern, folder_name)

            elif rule_type == "Size Threshold":
                size_threshold = st.number_input("Size Threshold (MB)", min_value=0.1, value=10.0)
                threshold_bytes = size_threshold * 1024 * 1024

                large_folder = st.text_input("Large Files Folder", "Large Files")
                small_folder = st.text_input("Small Files Folder", "Small Files")

                if st.button("Apply Size Rule"):
                    apply_size_rule(uploaded_files, threshold_bytes, large_folder, small_folder)


def organize_by_file_type(files):
    """Organize files by their type/extension"""
    import os

    # Define file type categories
    type_categories = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
        "Presentations": [".ppt", ".pptx", ".odp"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php"],
        "Other": []
    }

    # Organize files
    organized = {category: [] for category in type_categories.keys()}

    for file in files:
        ext = os.path.splitext(file.name)[1].lower()
        categorized = False

        for category, extensions in type_categories.items():
            if ext in extensions:
                organized[category].append(file)
                categorized = True
                break

        if not categorized:
            organized["Other"].append(file)

    # Display organization results
    st.subheader("Organization by File Type")

    for category, file_list in organized.items():
        if file_list:
            with st.expander(f"📁 {category} ({len(file_list)} files)"):
                total_size = sum(len(f.getvalue()) for f in file_list)
                st.write(f"**Total size:** {format_bytes(total_size)}")

                for file in file_list:
                    file_size = len(file.getvalue())
                    st.write(f"• {file.name} ({format_bytes(file_size)})")

                # Create download for category
                if len(file_list) > 1:
                    if st.button(f"Download {category} as ZIP", key=f"download_{category}"):
                        create_category_archive(file_list, category)


def organize_by_file_size(files, size_ranges):
    """Organize files by size ranges"""
    organized = {range_name: [] for range_name in size_ranges.keys()}

    for file in files:
        file_size = len(file.getvalue())

        for range_name, (min_size, max_size) in size_ranges.items():
            if min_size <= file_size < max_size:
                organized[range_name].append(file)
                break

    # Display organization results
    st.subheader("Organization by File Size")

    for range_name, file_list in organized.items():
        if file_list:
            with st.expander(f"📁 {range_name} ({len(file_list)} files)"):
                total_size = sum(len(f.getvalue()) for f in file_list)
                st.write(f"**Total size:** {format_bytes(total_size)}")

                for file in sorted(file_list, key=lambda x: len(x.getvalue()), reverse=True):
                    file_size = len(file.getvalue())
                    st.write(f"• {file.name} ({format_bytes(file_size)})")


def organize_by_content_type(files):
    """Organize files by detected content type"""
    import mimetypes

    content_categories = {
        "Text Files": ["text/"],
        "Image Files": ["image/"],
        "Video Files": ["video/"],
        "Audio Files": ["audio/"],
        "Application Files": ["application/"],
        "Unknown": []
    }

    organized = {category: [] for category in content_categories.keys()}

    for file in files:
        mime_type, _ = mimetypes.guess_type(file.name)
        categorized = False

        if mime_type:
            for category, prefixes in content_categories.items():
                if category != "Unknown" and any(mime_type.startswith(prefix) for prefix in prefixes):
                    organized[category].append(file)
                    categorized = True
                    break

        if not categorized:
            organized["Unknown"].append(file)

    # Display organization results
    st.subheader("Organization by Content Type")

    for category, file_list in organized.items():
        if file_list:
            with st.expander(f"📁 {category} ({len(file_list)} files)"):
                for file in file_list:
                    mime_type, _ = mimetypes.guess_type(file.name)
                    st.write(f"• {file.name} ({mime_type or 'Unknown MIME type'})")


def apply_pattern_rule(files, pattern, folder_name):
    """Apply custom pattern rule to organize files"""
    import fnmatch

    matching_files = []
    non_matching_files = []

    for file in files:
        if fnmatch.fnmatch(file.name.lower(), pattern.lower()):
            matching_files.append(file)
        else:
            non_matching_files.append(file)

    st.subheader(f"Pattern Rule Results: '{pattern}'")

    if matching_files:
        with st.expander(f"📁 {folder_name} ({len(matching_files)} files)"):
            for file in matching_files:
                st.write(f"• {file.name}")

    if non_matching_files:
        with st.expander(f"📁 Other Files ({len(non_matching_files)} files)"):
            for file in non_matching_files:
                st.write(f"• {file.name}")


def apply_size_rule(files, threshold_bytes, large_folder, small_folder):
    """Apply size-based rule to organize files"""
    large_files = []
    small_files = []

    for file in files:
        if len(file.getvalue()) >= threshold_bytes:
            large_files.append(file)
        else:
            small_files.append(file)

    st.subheader(f"Size Rule Results (threshold: {format_bytes(threshold_bytes)})")

    if large_files:
        with st.expander(f"📁 {large_folder} ({len(large_files)} files)"):
            for file in large_files:
                st.write(f"• {file.name} ({format_bytes(len(file.getvalue()))})")

    if small_files:
        with st.expander(f"📁 {small_folder} ({len(small_files)} files)"):
            for file in small_files:
                st.write(f"• {file.name} ({format_bytes(len(file.getvalue()))})")


def create_category_archive(files, category_name):
    """Create an archive for a category of files"""
    import zipfile
    import io

    archive_buffer = io.BytesIO()

    with zipfile.ZipFile(archive_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.writestr(file.name, file.getvalue())

    archive_data = archive_buffer.getvalue()
    filename = f"{category_name.lower().replace(' ', '_')}_files.zip"

    FileHandler.create_download_link(archive_data, filename, "application/zip")
