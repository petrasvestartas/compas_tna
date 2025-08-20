"""
Sphinx extension to extract content from paper.md and make it available to RST files.
"""
import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles


class PaperContentDirective(SphinxDirective):
    """Directive to include content from paper.md"""
    
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'section': str,  # 'summary' or 'statement'
    }

    def run(self):
        # Get the paper.md file path
        source_dir = self.env.srcdir
        # Support both new and old locations
        candidate_paths = [
            os.path.join(source_dir, 'paper', 'paper.md'),
            os.path.join(source_dir, 'paper.md'),
        ]
        paper_path = next((p for p in candidate_paths if os.path.exists(p)), None)

        # Which section to extract
        section = (self.options.get('section') or '').strip().lower()
        if section not in ('summary', 'statement'):
            return [nodes.warning(None, nodes.Text("paper-content: option :section: must be 'summary' or 'statement'"))]

        if not paper_path:
            return [nodes.warning(None, nodes.Text("paper.md not found (looked in docs/paper/paper.md and docs/paper.md)"))]

        # Read the paper.md content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Helper: extract between HTML markers or fall back to heading heuristics
        def extract_marked(md: str, sec: str) -> str:
            if sec == 'summary':
                start_marker = '<!-- SUMMARY-START -->'
                end_marker = '<!-- SUMMARY-END -->'
                heading_pat = r'^##\s+Summary\s*$'
            else:
                start_marker = '<!-- STATEMENT-START -->'
                end_marker = '<!-- STATEMENT-END -->'
                heading_pat = r'^##\s+Statement of need\s*$'

            if start_marker in md and end_marker in md:
                try:
                    md_part = md.split(start_marker, 1)[1].split(end_marker, 1)[0]
                    return md_part.strip('\n')
                except Exception:
                    pass

            # Fallback to heading-based extraction (from heading to next '## ' or EOF)
            m = re.search(heading_pat, md, flags=re.MULTILINE)
            if not m:
                return ''
            start = m.start()
            m2 = re.search(r'^##\s+.+$', md[m.end():], flags=re.MULTILINE)
            end = m.end() + (m2.start() if m2 else len(md[m.end():]))
            return md[start:end].strip('\n')

        md_section = extract_marked(content, section)
        if not md_section:
            return [nodes.warning(None, nodes.Text(f"paper-content: could not extract '{section}' from paper.md"))]

        # Convert Pandoc-style citations [@key; @key2] -> :cite:p:`key, key2`
        def convert_citations(text: str) -> str:
            # Only replace when the first non-space inside brackets is '@'
            def repl(match: re.Match) -> str:
                inner = match.group(1)
                # Reconstruct content with leading '@' to simplify splitting
                content_inner = '@' + inner
                parts = re.split(r'[;,]', content_inner)
                keys = []
                for p in parts:
                    k = p.strip().lstrip('@')
                    # Discard non-keys like empty strings or words
                    if k and re.match(r'^[A-Za-z0-9:_-]+$', k):
                        keys.append(k)
                if not keys:
                    return match.group(0)
                return f":cite:p:`{', '.join(keys)}`"

            return re.sub(r"\[\s*@([^\]]+)\]", repl, text)

        md_section = convert_citations(md_section)

        # Convert Markdown headings (#/##) to RST underlined headings
        lines = md_section.split('\n')
        rst_lines = []
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                rst_lines.append(title)
                rst_lines.append('=' * len(title))
                rst_lines.append('')
            elif line.startswith('## '):
                subtitle = line[3:].strip()
                rst_lines.append(subtitle)
                rst_lines.append('-' * len(subtitle))
                rst_lines.append('')
            else:
                rst_lines.append(line)

        text_content = '\n'.join(rst_lines)

        # Remove image references and fenced code blocks which are not RST
        text_content = re.sub(r'!\[.*?\]\(.*?\)', '', text_content)
        text_content = re.sub(r'```.*?```', '', text_content, flags=re.DOTALL)
        text_content = text_content.strip('\n')

        # Create RST nodes
        from docutils.statemachine import StringList

        content_lines = text_content.split('\n')
        content_stringlist = StringList(content_lines, source='paper.md')

        container = nodes.container()
        try:
            # Allow section titles within directive content
            nested_parse_with_titles(self.state, content_stringlist, container)
            return list(container.children)
        except Exception as e:
            return [nodes.warning(None, nodes.Text(f"Error parsing content: {e}"))]


def setup(app):
    """Setup function for the Sphinx extension"""
    app.add_directive('paper-content', PaperContentDirective)
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
