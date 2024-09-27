import os
import importlib.util
from core.state import State

class AutoDiscoveryController:
    def __init__(self, state: State):
        self.state = state

    def discover_functions(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        functions_path = os.path.join(base_path, 'functions')
        self.discover_modules(functions_path, self.state.functions, is_auto=False)
        
        autofunctions_path = os.path.join(base_path, 'autofunctions')
        self.discover_modules(autofunctions_path, self.state.auto_functions, is_auto=True)

    def discover_modules(self, path, target_dict, is_auto):
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            return

        for filename in os.listdir(path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module_path = os.path.join(path, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                
                # Add py_stealth functions to the module's global namespace
                module.__dict__.update({name: func for name, func in globals().items() if callable(func) and not name.startswith('__')})
                
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Error loading module {module_name}: {str(e)}")
                    continue
                
                if hasattr(module, 'main'):
                    target_dict[module_name] = module.main
                    print(f"Discovered {'auto ' if is_auto else ''}function: {module_name}")
                    
                    if is_auto:
                        # Initialize auto function in state.auto_functions
                        self.state.auto_functions[module_name] = {
                            'enabled': False,
                            'variable1': '',
                            'variable2': '',
                            'variable3': '',
                            'hotkey': ''
                        }

    def discover_all_functions(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        autodiscovery_path = os.path.join(base_path, 'autodiscovery')
        for root, dirs, files in os.walk(autodiscovery_path):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            relative_path = os.path.relpath(root, autodiscovery_path)
            if relative_path == '.':
                continue
            category = relative_path.replace(os.path.sep, '_')
            self.state.discovered_functions[category] = {}
            self.discover_modules(root, self.state.discovered_functions[category], is_auto=False)
    
        # Flatten the discovered functions for easier access
        self.state.flattened_functions = {}
        for category, functions in self.state.discovered_functions.items():
            for func_name, func in functions.items():
                self.state.flattened_functions[f"{category}_{func_name}"] = func
    
        print(f"Discovered functions: {list(self.state.flattened_functions.keys())}")