"""
Sphinx extension to extract content from paper.md and make it available to RST files.
"""
import os
import re
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective


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
        paper_path = os.path.join(source_dir, 'paper.md')
        
        if not os.path.exists(paper_path):
            return [nodes.warning(None, nodes.Text(f"paper.md not found at {paper_path}"))]
        
        # Read the paper.md content
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract content starting from first # heading
        # Find content after --- (end of YAML)
        yaml_end = content.find('---\n', content.find('---') + 1)
        if yaml_end == -1:
            return [nodes.warning(None, nodes.Text("Could not find YAML header end in paper.md"))]
        
        post_yaml_content = content[yaml_end + 4:]  # Skip past '---\n'
        
        # Find first # heading and extract everything from there
        first_heading_match = re.search(r'^# ', post_yaml_content, re.MULTILINE)
        if first_heading_match:
            main_content = post_yaml_content[first_heading_match.start():]
        else:
            main_content = post_yaml_content
        
        # Convert Markdown headings to RST format
        # # Title -> Title with === underline
        # ## Subtitle -> Subtitle with --- underline
        lines = main_content.split('\n')
        rst_lines = []
        
        for line in lines:
            if line.startswith('# '):
                # Convert # Title to RST format
                title = line[2:].strip()
                rst_lines.append(title)
                rst_lines.append('=' * len(title))
                rst_lines.append('')
            elif line.startswith('## '):
                # Convert ## Subtitle to RST format  
                subtitle = line[3:].strip()
                rst_lines.append(subtitle)
                rst_lines.append('-' * len(subtitle))
                rst_lines.append('')
            else:
                rst_lines.append(line)
        
        text_content = '\n'.join(rst_lines)
        
        # Remove image references and other non-RST content
        text_content = re.sub(r'!\[.*?\]\(.*?\)', '', text_content)
        text_content = re.sub(r'```.*?```', '', text_content, flags=re.DOTALL)
        text_content = text_content.strip()
        
        # Convert citations from :cite:p: to proper RST format
        text_content = re.sub(r':cite:p:`([^`]+)`', r':cite:p:`\1`', text_content)
        
        # Create RST nodes
        container = nodes.container()
        
        # Use the state machine to parse RST content properly
        from docutils.statemachine import StringList
        
        # Convert text to StringList for parsing
        content_lines = text_content.split('\n')
        content_stringlist = StringList(content_lines, source='paper.md')
        
        # Create container node
        container = nodes.container()
        
        try:
            # Use the directive's state to parse the content
            self.state.nested_parse(content_stringlist, 0, container)
            
            # Return the container's children
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
