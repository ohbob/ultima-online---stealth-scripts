import time
import threading
import logging
import traceback
import inspect
from core import uo_globals

class ScriptsController:
    def __init__(self, state, main_controller):
        self.state = state
        self.main_controller = main_controller
        self.logger = logging.getLogger(__name__)
        self.current_loops = {}
        self.stop_events = {}

    def run_script(self, func_name, loop=False, timeout=1000):
        self.logger.info(f"Attempting to run script: {func_name}, loop: {loop}, timeout: {timeout}")
        script_path = None
        for category, functions in self.state.discovered_functions.items():
            if func_name in functions:
                script_path = functions[func_name].get('path')
                break

        if script_path:
            self.logger.info(f"Found script path: {script_path}")
            try:
                with open(script_path, 'r') as script_file:
                    script_code = script_file.read()
                    self.logger.debug(f"Script content:\n{script_code}")
                    
                    script_namespace = self._prepare_script_namespace()
                    
                    exec(script_code, script_namespace)
                    
                    if 'main' in script_namespace:
                        main_func = script_namespace['main']
                        self.logger.info(f"Calling main() function in {func_name}")
                        
                        if loop:
                            self._start_loop(func_name, main_func, timeout)
                        else:
                            self._run_once(main_func)
                    else:
                        self.logger.warning(f"No main() function found in {func_name}")
                    
                self.logger.info(f"Script {func_name} executed successfully")
            except Exception as e:
                self.logger.error(f"Error executing script {func_name}: {str(e)}")
                self.logger.error(traceback.format_exc())
        else:
            self.logger.warning(f"Script for {func_name} not found.")

    def _prepare_script_namespace(self):
        script_namespace = {
            'main_controller': self.main_controller,
            'py_stealth': self.main_controller.py_stealth
        }
        
        # Add all py_stealth functions to the script namespace
        for attr_name in dir(self.main_controller.py_stealth):
            if not attr_name.startswith('__'):
                script_namespace[attr_name] = getattr(self.main_controller.py_stealth, attr_name)
        
        # Add all uo_globals functions to the script namespace
        for attr_name in dir(uo_globals):
            if not attr_name.startswith('__'):
                attr = getattr(uo_globals, attr_name)
                if callable(attr):
                    # If the function expects py_stealth as the first argument, bind it
                    if inspect.signature(attr).parameters:
                        first_param = next(iter(inspect.signature(attr).parameters.values()))
                        if first_param.name == 'py_stealth':
                            script_namespace[attr_name] = lambda *args, f=attr: f(self.main_controller.py_stealth, *args)
                        else:
                            script_namespace[attr_name] = attr
                    else:
                        script_namespace[attr_name] = attr
                else:
                    script_namespace[attr_name] = attr
        
        return script_namespace

    def _run_once(self, main_func):
        if inspect.signature(main_func).parameters:
            main_func(self.main_controller)
        else:
            main_func()

    def _start_loop(self, func_name, main_func, timeout):
        if func_name in self.current_loops:
            self.stop_loop_execution(func_name)
        
        stop_event = threading.Event()
        self.stop_events[func_name] = stop_event
        loop_thread = threading.Thread(target=self._loop_script, args=(func_name, main_func, timeout, stop_event))
        self.current_loops[func_name] = loop_thread
        loop_thread.start()

    def _loop_script(self, func_name, main_func, timeout, stop_event):
        while not stop_event.is_set():
            try:
                self._run_once(main_func)
                stop_event.wait(timeout / 1000)  # Convert milliseconds to seconds
            except Exception as e:
                self.logger.error(f"Error in loop execution for {func_name}: {str(e)}")
                self.logger.error(traceback.format_exc())
                break
        self.logger.info(f"Loop for {func_name} has ended")

    def stop_loop_execution(self, func_name=None):
        if func_name:
            if func_name in self.stop_events:
                self.stop_events[func_name].set()
                if func_name in self.current_loops:
                    self.current_loops[func_name].join(timeout=1)  # Wait for 1 second max
                    del self.current_loops[func_name]
                del self.stop_events[func_name]
                self.logger.info(f"Loop execution for {func_name} stopped")
            else:
                self.logger.info(f"No loop is currently running for {func_name}")
        else:
            for func_name in list(self.stop_events.keys()):
                self.stop_loop_execution(func_name)