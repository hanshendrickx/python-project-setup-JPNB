from pathlib import Path
import os
from datetime import datetime
import argparse

class ProjectTreeViewer:
    def __init__(self):
        self.exclude_dirs = {
            '__pycache__', 
            '.git', 
            '.pytest_cache', 
            '.ipynb_checkpoints',
            'uv.venv',
            'node_modules'
        }
        
        self.include_extensions = {
            '.py',      # Python files
            '.ipynb',   # Jupyter notebooks
            '.md',      # Markdown files
            '.txt',     # Text files
            '.csv',     # CSV files
            '.xlsx',    # Excel files
            '.json',    # JSON files
            '.pdf',     # PDF files
            '.docx',     # Word documents
            '.bat'
        }
        
    def is_custom_file(self, path: Path) -> bool:
        return (path.suffix in self.include_extensions and 
                not any(excluded in path.parts for excluded in self.exclude_dirs))
    
    def generate_tree(self, start_path: Path, output_file: str = None,
                     max_depth: int = 3) -> str:
        def _add_to_tree(current_path: Path, prefix: str = '', depth: int = 0) -> list:
            if depth > max_depth:
                return []
                
            lines = []
            dirs = []
            files = []
            
            try:
                for path in sorted(current_path.iterdir()):
                    if path.name in self.exclude_dirs:
                        continue
                    if path.is_dir():
                        dirs.append(path)
                    elif self.is_custom_file(path):
                        files.append(path)
            except PermissionError:
                return [f"{prefix}!!! Permission Denied !!!"]
            
            for i, path in enumerate(dirs):
                is_last = (i == len(dirs) - 1) and not files
                connector = '└──' if is_last else '├──'
                lines.append(f"{prefix}{connector} 📁 {path.name}/")
                
                if path.is_dir():
                    extension = '    ' if is_last else '│   '
                    lines.extend(_add_to_tree(path, prefix + extension, depth + 1))
            
            for i, path in enumerate(files):
                is_last = i == len(files) - 1
                connector = '└──' if is_last else '├──'
                
                if path.suffix == '.py':
                    icon = '🐍'
                elif path.suffix == '.ipynb':
                    icon = '📓'
                elif path.suffix == '.md':
                    icon = '📝'
                elif path.suffix in ['.xlsx', '.csv']:
                    icon = '📊'
                elif path.suffix == '.pdf':
                    icon = '📄'
                elif path.suffix == '.docx':
                    icon = '📃'
                else:
                    icon = '📄'
                
                lines.append(f"{prefix}{connector} {icon} {path.name}")
            
            return lines
        
        header = [
            f"Project Tree Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Root: {start_path.absolute()}",
            "-" * 80,
            ""
        ]
        
        tree_lines = _add_to_tree(start_path)
        full_tree = header + tree_lines
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(full_tree))
        
        return '\n'.join(full_tree)

def main():
    parser = argparse.ArgumentParser(description='Generate custom project tree structure')
    parser.add_argument('--path', type=str, default='.',
                       help='Path to generate tree from')
    parser.add_argument('--output', type=str,
                       help='Output file path (optional)')
    parser.add_argument('--max-depth', type=int, default=3,
                       help='Maximum folder depth to display')
    
    args = parser.parse_args()
    
    viewer = ProjectTreeViewer()
    tree = viewer.generate_tree(
        Path(args.path),
        args.output,
        args.max_depth
    )
    
    print(tree)

if __name__ == "__main__":
    main()