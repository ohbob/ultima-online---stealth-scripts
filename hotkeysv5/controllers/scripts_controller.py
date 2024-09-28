import time
import threading

class ScriptsController:
    def __init__(self, state, main_controller):
        self.state = state
        self.main_controller = main_controller
        self.scripts = {}
        self.current_loop_thread = None
        self.stop_loop = threading.Event()

    def add_script(self, name, script):
        self.scripts[name] = script
        self.state.update_scripts(self.scripts)

    def remove_script(self, name):
        if name in self.scripts:
            del self.scripts[name]
            self.state.update_scripts(self.scripts)

    def get_scripts(self):
        return self.scripts

    def run_script(self, func_name, loop=False, timeout=1000):
        if self.current_loop_thread and self.current_loop_thread.is_alive():
            self.stop_loop.set()
            self.current_loop_thread.join()

        self.stop_loop.clear()

        if loop:
            self.current_loop_thread = threading.Thread(target=self._run_script_loop, args=(func_name, timeout))
            self.current_loop_thread.start()
        else:
            self._run_script_once(func_name)

    def _run_script_once(self, func_name):
        self.main_controller.run_script(func_name, loop=False, timeout=None)

    def _run_script_loop(self, func_name, timeout):
        print(f"Starting loop for {func_name} with timeout {timeout}ms")
        while not self.stop_loop.is_set():
            start_time = time.time()
            self._run_script_once(func_name)
            elapsed_time = (time.time() - start_time) * 1000
            if elapsed_time < timeout:
                sleep_time = (timeout - elapsed_time) / 1000
                print(f"Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        print(f"Loop for {func_name} stopped")

    def stop_loop_execution(self):
        if self.current_loop_thread and self.current_loop_thread.is_alive():
            self.stop_loop.set()
            self.current_loop_thread.join()