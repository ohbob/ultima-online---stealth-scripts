import os
import importlib.util
from core.state import State
import inspect

class AutoDiscoveryController:
    def __init__(self, state: State):
        self.state = state
        self.core_functions_path = os.path.join('core', 'functions')
        self.user_scripts_path = os.path.join('user', 'scripts')
        self.user_auto_path = os.path.join('user', 'auto')

    def discover_all_functions(self):
        discovered_functions = {}
        auto_functions = {}

        # Discover core functions
        self.discover_functions(self.core_functions_path, discovered_functions)

        # Discover user scripts
        self.discover_functions(self.user_scripts_path, discovered_functions)

        # Discover user auto functions
        self.discover_functions(self.user_auto_path, auto_functions)

        self.state.update_discovered_functions(discovered_functions)
        self.state.update_auto_functions(auto_functions)

    def discover_functions(self, base_path, target_dict):
        for root, dirs, files in os.walk(base_path):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']

            category = os.path.relpath(root, base_path).replace(os.path.sep, '.')
            if category == '.':
                category = os.path.basename(base_path)

            if category not in target_dict:
                target_dict[category] = {}

            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]
                    module_path = os.path.join(root, file)
                    function = self.load_function(module_path, module_name)
                    if function:
                        target_dict[category][module_name] = function

        # Remove empty categories
        target_dict = {k: v for k, v in target_dict.items() if v}

    def load_function(self, module_path, module_name):
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'main'):
                main_func = module.main
                params = list(inspect.signature(main_func).parameters.keys())
                return {
                    'function': main_func,
                    'description': getattr(module, 'description', ''),
                    'hotkey': '',
                    'enabled': False,
                    'path': module_path,
                    'variable1': params[0] if len(params) > 0 else '',
                    'variable2': params[1] if len(params) > 1 else '',
                    'variable3': params[2] if len(params) > 2 else '',
                    'param_count': len(params)
                }
        except Exception as e:
            print(f"Error loading module {module_name}: {str(e)}")
        return None