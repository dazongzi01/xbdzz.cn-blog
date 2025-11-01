"""
Markdown processing utilities for workflow system
"""

import re
from typing import List, Tuple


class MarkdownUtils:
    """Utilities for Markdown content processing"""

    @staticmethod
    def extract_title(content: str) -> str:
        """Extract title from markdown content (first H1)"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else "Untitled"

    @staticmethod
    def extract_headings(content: str) -> List[Tuple[int, str]]:
        """Extract all headings with their levels"""
        headings = []
        for match in re.finditer(r'^(#+)\s+(.+)$', content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2)
            headings.append((level, title))
        return headings

    @staticmethod
    def extract_sections(content: str) -> dict:
        """Extract content sections by headings"""
        sections = {}
        current_section = None
        current_content = []

        for line in content.split('\n'):
            heading_match = re.match(r'^(#+)\s+(.+)$', line)

            if heading_match:
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()

                current_section = heading_match.group(2)
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    @staticmethod
    def extract_code_blocks(content: str) -> List[Tuple[str, str]]:
        """Extract code blocks with language"""
        blocks = []
        pattern = r'```(\w*)\n(.*?)\n```'
        for match in re.finditer(pattern, content, re.DOTALL):
            language = match.group(1) or 'text'
            code = match.group(2)
            blocks.append((language, code))
        return blocks

    @staticmethod
    def extract_links(content: str) -> List[Tuple[str, str]]:
        """Extract all links and their texts"""
        links = []
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(pattern, content):
            text = match.group(1)
            url = match.group(2)
            links.append((text, url))
        return links

    @staticmethod
    def extract_images(content: str) -> List[str]:
        """Extract all image URLs"""
        images = []
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        for match in re.finditer(pattern, content):
            url = match.group(2)
            images.append(url)
        return images

    @staticmethod
    def extract_tables(content: str) -> List[str]:
        """Extract markdown tables"""
        tables = []
        # Simple table detection
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i]
            if '|' in line and i + 1 < len(lines) and '-' in lines[i + 1]:
                table_lines = [line, lines[i + 1]]
                i += 2
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                tables.append('\n'.join(table_lines))
                continue
            i += 1
        return tables

    @staticmethod
    def count_words(content: str) -> int:
        """Count words in markdown (excluding markdown syntax)"""
        # Remove code blocks
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Remove links
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        # Remove images
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', content)
        # Remove markdown formatting
        content = re.sub(r'[#*`\-_\[\](){}]', '', content)
        # Count words (split by whitespace)
        words = content.split()
        return len(words)

    @staticmethod
    def get_word_count_estimate(content: str) -> int:
        """Get estimated Chinese/English word count"""
        # Count Chinese characters
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        # Count English words
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))
        # Rough estimate: Chinese chars ~ 1.5 words
        return int(chinese_chars * 1.5) + english_words

    @staticmethod
    def create_table_of_contents(content: str, max_level: int = 3) -> str:
        """Generate table of contents from headings"""
        lines = ['## 目录\n']
        headings = MarkdownUtils.extract_headings(content)

        for level, title in headings:
            if level > 1 and level <= max_level:  # Skip H1, only include H2-H3
                indent = '  ' * (level - 2)
                anchor = title.lower().replace(' ', '-')
                lines.append(f"{indent}- [{title}](#{anchor})")

        return '\n'.join(lines)

    @staticmethod
    def add_word_count_footer(content: str, word_count: int) -> str:
        """Add word count footer to content"""
        footer = f"\n\n---\n\n📊 **字数统计**: {word_count} 字\n"
        return content + footer

    @staticmethod
    def sanitize_markdown(content: str) -> str:
        """Clean up markdown content"""
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in content.split('\n')]
        # Remove multiple consecutive blank lines
        result = []
        prev_blank = False
        for line in lines:
            if line.strip():
                result.append(line)
                prev_blank = False
            elif not prev_blank:
                result.append(line)
                prev_blank = True

        return '\n'.join(result).strip()
