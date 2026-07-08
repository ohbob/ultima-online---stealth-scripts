import json
import os
import sys
import atexit
import time
import tkinter as tk

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui_config import UI_CONFIG, bind_ui_lifecycle

UI2_CONFIG = {
    'window_title': 'Assistants',
    'panel_width': 180,
    'header_h': 26,
    'header_pad_v': 4,
    'row_h': 22,
    'pad_h': 6,
    'body_pad_v': 6,
    'panel_gap': 0,
    'panel_sep': 0,
    'toggle_w': 32,
    'toggle_pad_right': 6,
    'checkbox_w': 18,
    'font': ('Arial', 10),
    'title_font': ('Arial', 10, 'bold'),
    'toggle_line_w': 2,
    'toggle_arm_half': 4,
    'tick_ms': 50,
    'tick_ms_offline': 500,
    'decorations': UI_CONFIG.get('decorations', 0),
    'drag_to_move': UI_CONFIG.get('drag_to_move', 1),
    'colors': {
        'header_inactive': '#a04040',
        'header_active': '#9cb896',
        'body': '#c8c4b8',
        'fg': 'black',
        'toggle_fg': 'black',
        'checkbox_select': '#9a9690',
    },
}

_REGISTRY = []
_LAUNCHED = False
_AUTO_LAUNCH_REGISTERED = False
_CONFIG_HOOKS = {'load': [], 'save': []}
_APP_INSTANCE = None
_TICK_CONNECTION_STATE = None


def get_tick_connection_state():
    return _TICK_CONNECTION_STATE


def _stealth_tick_state():
    try:
        from py_stealth import Connected, Dead
        if not Connected():
            return {'connected': False, 'ready': False}
        return {'connected': True, 'ready': not Dead()}
    except Exception:
        return {'connected': False, 'ready': False}


def register_config_hook(*, on_load=None, on_save=None):
    if on_load is not None:
        _CONFIG_HOOKS['load'].append(on_load)
    if on_save is not None:
        _CONFIG_HOOKS['save'].append(on_save)


def request_save_config():
    if _APP_INSTANCE is not None:
        _APP_INSTANCE.save_config()

_DRAG_IGNORE_CLASSES = ('Button', 'Listbox', 'Entry', 'Text', 'Spinbox', 'Scale', 'Menubutton', 'Checkbutton')


def parse_window_options(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    decorations = UI2_CONFIG.get('decorations', 0)
    for arg in argv:
        if arg in ('--no-decorations', '--borderless', '--frameless'):
            decorations = 0
        elif arg.startswith('--decorations='):
            decorations = int(arg.split('=', 1)[1])
        elif arg.startswith('decorations='):
            decorations = int(arg.split('=', 1)[1])
    return {'decorations': decorations}


class AssistantTask:
    def __init__(self, label, callback, interval_ms=100, *, on_enable=None, oneshot=False):
        self.label = label
        self.callback = callback
        self.interval_ms = interval_ms
        self.enabled = True
        self.last_run_ms = 0.0
        self.on_enable = on_enable
        self.oneshot = oneshot


class AssistantDefinition:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        self.expanded = False
        self.active = False


def _auto_launch_at_exit():
    if _LAUNCHED or not _REGISTRY:
        return
    launch()


def _maybe_schedule_auto_launch():
    global _AUTO_LAUNCH_REGISTERED
    if _AUTO_LAUNCH_REGISTERED or _LAUNCHED:
        return
    if sys.modules.get('__main__') is None:
        return
    _AUTO_LAUNCH_REGISTERED = True
    atexit.register(_auto_launch_at_exit)


def Assistant(name, items, on_activate=None):
    tasks = []
    for entry in items:
        label = entry[0]
        callback = entry[1]
        interval_ms = entry[2] if len(entry) > 2 else 100
        opts = entry[3] if len(entry) > 3 else {}
        if not isinstance(opts, dict):
            opts = {}
        tasks.append(AssistantTask(
            label, callback, interval_ms,
            on_enable=opts.get('on_enable'),
            oneshot=bool(opts.get('oneshot', False)),
        ))
    definition = AssistantDefinition(name, tasks)
    definition.on_activate = on_activate
    _REGISTRY.append(definition)
    _maybe_schedule_auto_launch()
    return definition


class AssistantPanel(tk.Frame):
    def __init__(self, master, definition, app, **kwargs):
        colors = UI2_CONFIG['colors']
        panel_width = UI2_CONFIG['panel_width']
        super().__init__(
            master, bg=colors['header_inactive'], bd=0, highlightthickness=0,
            width=panel_width, **kwargs,
        )
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.definition = definition
        self.app = app
        self.colors = colors
        self.font = UI2_CONFIG['font']
        self.title_font = UI2_CONFIG['title_font']
        self.task_vars = {}

        self.columnconfigure(0, minsize=panel_width, weight=0)

        self.header = tk.Frame(
            self, bg=self._header_color(), height=UI2_CONFIG['header_h'],
            width=panel_width, bd=0, highlightthickness=0,
        )
        self.header.grid(row=0, column=0, sticky='new')
        self.header.grid_propagate(False)
        self.header.grid_rowconfigure(0, weight=1)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(1, weight=0, minsize=UI2_CONFIG['toggle_w'])

        self.title_label = tk.Label(
            self.header,
            text=definition.name,
            bg=self._header_color(),
            fg=self.colors['fg'],
            font=self.title_font,
            anchor='w',
            bd=0,
            highlightthickness=0,
            pady=0,
            cursor='hand2',
        )
        self.title_label.grid(
            row=0, column=0, sticky='nsw',
            padx=(UI2_CONFIG['pad_h'], 0),
            pady=(UI2_CONFIG['header_pad_v'], UI2_CONFIG['header_pad_v']),
        )
        self.title_label.bind('<ButtonRelease-1>', self._on_title_release)
        self.title_label._no_drag = True
        self.header.bind('<ButtonRelease-1>', self._on_header_release)

        self.toggle_hit = tk.Frame(
            self.header,
            bg=self._header_color(),
            width=UI2_CONFIG['toggle_w'],
            height=UI2_CONFIG['header_h'],
            bd=0,
            highlightthickness=0,
            cursor='hand2',
        )
        self.toggle_hit.grid(
            row=0, column=1, sticky='e',
            padx=(0, UI2_CONFIG['toggle_pad_right']),
        )
        self.toggle_hit.grid_propagate(False)
        self.toggle_hit._no_drag = True

        toggle_w = UI2_CONFIG['toggle_w']
        header_h = UI2_CONFIG['header_h']
        self.toggle_canvas = tk.Canvas(
            self.toggle_hit,
            width=toggle_w,
            height=header_h,
            bg=self._header_color(),
            highlightthickness=0,
            bd=0,
            cursor='hand2',
        )
        self.toggle_canvas.pack(expand=True, fill='both')
        self.toggle_hit.bind('<ButtonRelease-1>', self._on_toggle_click)
        self.toggle_canvas.bind('<ButtonRelease-1>', self._on_toggle_click)
        self.toggle_canvas._no_drag = True
        self._draw_toggle_glyph()

        self.body = tk.Frame(
            self,
            bg=self.colors['body'],
            width=panel_width,
            bd=0,
            highlightthickness=0,
        )
        self.body.pack_propagate(False)
        self.body.grid_propagate(False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self._build_body_rows()

        if definition.expanded:
            body_h = self._body_height()
            self.body.configure(width=panel_width, height=body_h)
            self.grid_rowconfigure(1, minsize=body_h, weight=0)
            self.body.grid(row=1, column=0, sticky='new')
        self._refresh_header()

    def _header_color(self):
        return self.colors['header_active'] if self.definition.active else self.colors['header_inactive']

    def _draw_toggle_glyph(self):
        canvas = self.toggle_canvas
        canvas.delete('all')
        toggle_w = UI2_CONFIG['toggle_w']
        header_h = UI2_CONFIG['header_h']
        cx = toggle_w // 2
        cy = header_h // 2
        color = self.colors['toggle_fg']
        line_w = UI2_CONFIG['toggle_line_w']
        arm = UI2_CONFIG['toggle_arm_half']
        canvas.create_line(
            cx - arm, cy, cx + arm, cy,
            fill=color, width=line_w, capstyle=tk.ROUND,
        )
        if not self.definition.expanded:
            canvas.create_line(
                cx, cy - arm, cx, cy + arm,
                fill=color, width=line_w, capstyle=tk.ROUND,
            )

    def _on_toggle_click(self, _event=None):
        self._toggle_expanded()

    def _inner_body_height(self):
        return len(self.definition.tasks) * UI2_CONFIG['row_h']

    def _body_height(self):
        if not self.definition.expanded:
            return 0
        return 2 * UI2_CONFIG['body_pad_v'] + self._inner_body_height()

    def pixel_height(self):
        height = UI2_CONFIG['header_h']
        if self.definition.expanded:
            height += self._body_height()
        return height

    def _build_body_rows(self):
        for widget in self.body.winfo_children():
            widget.destroy()
        self.task_vars = {}

        body_pad_v = UI2_CONFIG['body_pad_v']
        pad_h = UI2_CONFIG['pad_h']
        row_h = UI2_CONFIG['row_h']
        panel_width = UI2_CONFIG['panel_width']
        content_w = panel_width - 2 * pad_h

        for index, task in enumerate(self.definition.tasks):
            row_y = body_pad_v + index * row_h
            row = tk.Frame(
                self.body, bg=self.colors['body'], height=row_h,
                bd=0, highlightthickness=0,
            )
            row.pack_propagate(False)
            row.place(x=pad_h, y=row_y, width=content_w, height=row_h)
            row.grid_columnconfigure(0, weight=1)
            row.grid_columnconfigure(1, weight=0, minsize=UI2_CONFIG['checkbox_w'])

            tk.Label(
                row,
                text=task.label,
                bg=self.colors['body'],
                fg=self.colors['fg'],
                font=self.font,
                anchor='w',
                bd=0,
                highlightthickness=0,
                pady=0,
            ).grid(row=0, column=0, sticky='w')

            cb_col = tk.Frame(
                row, bg=self.colors['body'], width=UI2_CONFIG['checkbox_w'],
                height=row_h, bd=0, highlightthickness=0,
            )
            cb_col.grid_propagate(False)
            cb_col.place(x=content_w - UI2_CONFIG['checkbox_w'], y=0, width=UI2_CONFIG['checkbox_w'], height=row_h)

            var = tk.BooleanVar(value=task.enabled)
            self.task_vars[task.label] = var
            cb = tk.Checkbutton(
                cb_col,
                variable=var,
                command=lambda t=task, v=var: self._task_toggled(t, v),
                bg=self.colors['body'],
                activebackground=self.colors['body'],
                selectcolor=self.colors['checkbox_select'],
                highlightthickness=0,
                bd=0,
                relief=tk.FLAT,
                padx=0,
                pady=0,
            )
            cb.place(relx=1.0, rely=0.5, anchor='e')
            cb._no_drag = True

    def _task_toggled(self, task, var):
        enabled = bool(var.get())
        if enabled and task.oneshot:
            try:
                task.callback()
            except Exception as error:
                print(f'[{self.definition.name}] {task.label} failed: {error}')
            enabled = False
            var.set(False)
        elif enabled and task.on_enable is not None:
            try:
                task.on_enable()
            except Exception as error:
                print(f'[{self.definition.name}] {task.label} enable failed: {error}')
        task.enabled = enabled
        self.app.save_config()

    def _on_title_release(self, _event=None):
        self._toggle_active()

    def _on_header_release(self, event=None):
        if self.app.drag_moved:
            return
        self._toggle_active()

    def _toggle_expanded(self):
        self.definition.expanded = not self.definition.expanded
        if self.definition.expanded:
            body_h = self._body_height()
            panel_width = UI2_CONFIG['panel_width']
            self.body.configure(width=panel_width, height=body_h)
            self.grid_rowconfigure(1, minsize=body_h, weight=0)
            self.body.grid(row=1, column=0, sticky='new')
        else:
            self.grid_rowconfigure(1, minsize=0, weight=0)
            self.body.grid_remove()
        self._refresh_header()
        self.app.save_config()
        self.app.resize_window()

    def _toggle_active(self, _event=None):
        was_active = self.definition.active
        self.definition.active = not self.definition.active
        if self.definition.active and not was_active:
            on_activate = getattr(self.definition, 'on_activate', None)
            if on_activate is not None:
                try:
                    on_activate()
                except Exception as error:
                    print(f'[{self.definition.name}] activate failed: {error}')
        self._refresh_header()
        self.app.save_config()

    def _refresh_header(self):
        color = self._header_color()
        panel_bg = self.colors['body'] if self.definition.expanded else color
        self.configure(bg=panel_bg)
        self.header.configure(bg=color)
        self.title_label.configure(bg=color)
        self.toggle_hit.configure(bg=color)
        self.toggle_canvas.configure(bg=color)
        self._draw_toggle_glyph()

    def apply_config(self, panel_config):
        self.definition.expanded = bool(panel_config.get('expanded', False))
        self.definition.active = bool(panel_config.get('active', False))
        task_states = panel_config.get('tasks', {})
        for task in self.definition.tasks:
            if task.label in task_states:
                task.enabled = bool(task_states[task.label])
        self._build_body_rows()
        if self.definition.expanded:
            body_h = self._body_height()
            panel_width = UI2_CONFIG['panel_width']
            self.body.configure(width=panel_width, height=body_h)
            self.grid_rowconfigure(1, minsize=body_h, weight=0)
            self.body.grid(row=1, column=0, sticky='new')
        else:
            self.grid_rowconfigure(1, minsize=0, weight=0)
            self.body.grid_remove()
        self._refresh_header()

    def export_config(self):
        return {
            'expanded': self.definition.expanded,
            'active': self.definition.active,
            'tasks': {task.label: task.enabled for task in self.definition.tasks},
        }


class AssistantApp:
    def __init__(self, master, decorations=None, script_name=None):
        global _APP_INSTANCE
        _APP_INSTANCE = self
        self.master = master
        if decorations is None:
            decorations = UI2_CONFIG.get('decorations', 0)
        self.decorations = decorations
        self.drag_to_move = decorations == 0 and bool(UI2_CONFIG.get('drag_to_move', 1))
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._drag_start_x = 0
        self._drag_start_y = 0
        self.drag_moved = False

        colors = UI2_CONFIG['colors']
        panel_width = UI2_CONFIG['panel_width']
        master.title(UI2_CONFIG['window_title'])
        master.configure(
            bg=colors['header_inactive'], bd=0, highlightthickness=0,
        )
        master.resizable(False, False)
        if decorations == 0:
            master.overrideredirect(True)
        master.wm_attributes('-topmost', True)

        if script_name is None:
            script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        self.script_name = script_name
        self.config_file = self._config_path()
        self.panels = []
        self.separators = []

        self.content = tk.Frame(
            master, bg=colors['header_inactive'], bd=0, highlightthickness=0,
            width=panel_width,
        )
        self.content.pack_propagate(False)
        self.content.grid_propagate(False)
        self.content.pack(anchor='nw', padx=0, pady=0)

        self.load_config()
        self.rebuild_panels()
        self.master.after(0, self._tick)

    def _config_path(self):
        char_name = 'demo'
        script_name = self.script_name
        try:
            from py_stealth import CharName
            char_name = CharName()
        except Exception:
            pass
        try:
            from py_astealth.utilites import config as stealth_config
            script_path = getattr(stealth_config, 'STEALTH_SCRIPT_NAME', '') or ''
            if script_path:
                script_name = os.path.splitext(os.path.basename(script_path))[0]
        except Exception:
            pass
        return os.path.join(current_dir, f'{script_name}_{char_name}_config.json')

    def rebuild_panels(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.panels = []
        self.separators = []
        panel_sep = UI2_CONFIG['panel_sep']
        panel_width = UI2_CONFIG['panel_width']
        y_offset = 0
        for index, definition in enumerate(_REGISTRY):
            panel = AssistantPanel(self.content, definition, self)
            panel_height = panel.pixel_height()
            panel.place(x=0, y=y_offset, width=panel_width, height=panel_height, anchor='nw')
            y_offset += panel_height
            if panel_sep > 0 and index < len(_REGISTRY) - 1:
                sep_color = UI2_CONFIG['colors'].get('panel_sep', '#8aaa84')
                sep = tk.Frame(
                    self.content, bg=sep_color, height=panel_sep,
                    width=panel_width, bd=0, highlightthickness=0,
                )
                sep.place(x=0, y=y_offset, width=panel_width, height=panel_sep, anchor='nw')
                self.separators.append(sep)
                y_offset += panel_sep
            self.panels.append(panel)
        self.resize_window()
        if self.drag_to_move:
            self.bind_drag_to_move()

    def _content_height(self):
        panel_sep = UI2_CONFIG['panel_sep']
        height = 0
        for index, panel in enumerate(self.panels):
            height += panel.pixel_height()
            if panel_sep > 0 and index < len(self.panels) - 1:
                height += panel_sep
        return max(UI2_CONFIG['header_h'], height)

    def _layout_panels(self):
        panel_sep = UI2_CONFIG['panel_sep']
        panel_width = UI2_CONFIG['panel_width']
        y_offset = 0
        for index, panel in enumerate(self.panels):
            panel_height = panel.pixel_height()
            panel.place(x=0, y=y_offset, width=panel_width, height=panel_height, anchor='nw')
            panel.configure(height=panel_height)
            y_offset += panel_height
            if panel_sep > 0 and index < len(self.panels) - 1:
                self.separators[index].place(
                    x=0, y=y_offset, width=panel_width, height=panel_sep, anchor='nw',
                )
                y_offset += panel_sep

    def resize_window(self):
        width = UI2_CONFIG['panel_width']
        height = self._content_height()
        self._layout_panels()
        self.content.configure(width=width, height=height)
        self.master.geometry(f'{width}x{height}')
        self.master.minsize(width, height)
        self.master.maxsize(width, height)
        self.master.update_idletasks()

    def bind_drag_to_move(self):
        self._bind_drag_recursive(self.master)
        self._bind_drag_recursive(self.content)
        for panel in self.panels:
            self._bind_drag_recursive(panel)

    def _bind_drag_recursive(self, widget):
        if widget.winfo_class() in _DRAG_IGNORE_CLASSES:
            return
        if getattr(widget, '_no_drag', False):
            return
        widget.bind('<ButtonPress-1>', self._drag_start)
        widget.bind('<B1-Motion>', self._drag_motion)
        widget.bind('<ButtonRelease-1>', self._drag_end)
        for child in widget.winfo_children():
            self._bind_drag_recursive(child)

    def _drag_start(self, event):
        self.drag_moved = False
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root
        self._drag_offset_x = event.x_root - self.master.winfo_x()
        self._drag_offset_y = event.y_root - self.master.winfo_y()

    def _drag_motion(self, event):
        dx = abs(event.x_root - self._drag_start_x)
        dy = abs(event.y_root - self._drag_start_y)
        if dx <= 3 and dy <= 3:
            return
        self.drag_moved = True
        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        self.master.geometry(f'+{x}+{y}')

    def _drag_end(self, _event=None):
        self.master.after_idle(lambda: setattr(self, 'drag_moved', False))

    def load_config(self):
        try:
            with open(self.config_file, 'r') as handle:
                config = json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {}

        for hook in _CONFIG_HOOKS['load']:
            hook(config)

        assistants = config.get('assistants', {})
        for definition in _REGISTRY:
            panel_config = assistants.get(definition.name, {})
            definition.expanded = bool(panel_config.get('expanded', False))
            definition.active = bool(panel_config.get('active', False))
            task_states = panel_config.get('tasks', {})
            for task in definition.tasks:
                if task.label in task_states:
                    task.enabled = bool(task_states[task.label])

    def save_config(self):
        config = {
            'assistants': {
                panel.definition.name: panel.export_config()
                for panel in self.panels
            },
        }
        for hook in _CONFIG_HOOKS['save']:
            hook(config)
        with open(self.config_file, 'w') as handle:
            json.dump(config, handle, indent=4)

    def apply_loaded_config(self):
        try:
            with open(self.config_file, 'r') as handle:
                config = json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        assistants = config.get('assistants', {})
        for panel in self.panels:
            panel_config = assistants.get(panel.definition.name, {})
            panel.apply_config(panel_config)
        self.resize_window()
        if self.drag_to_move:
            self.bind_drag_to_move()

    def _schedule_tick(self, *, connected=False):
        delay_ms = UI2_CONFIG['tick_ms'] if connected else UI2_CONFIG['tick_ms_offline']
        self.master.after(delay_ms, self._tick)

    def _tick(self):
        global _TICK_CONNECTION_STATE
        state = _stealth_tick_state()
        _TICK_CONNECTION_STATE = state
        connected = state['connected']
        if connected:
            now_ms = time.time() * 1000
            for definition in _REGISTRY:
                if not definition.active:
                    continue
                for task in definition.tasks:
                    if task.oneshot:
                        continue
                    if not task.enabled:
                        continue
                    if now_ms - task.last_run_ms < task.interval_ms:
                        continue
                    task.last_run_ms = now_ms
                    try:
                        task.callback()
                    except Exception as error:
                        print(f'[{definition.name}] {task.label} failed: {error}')
        self._schedule_tick(connected=connected)


def launch(script_name=None, argv=None):
    global _LAUNCHED
    if _LAUNCHED:
        return None
    _LAUNCHED = True
    if not _REGISTRY:
        print('Warning: no assistants registered; UI will be empty.')
    window_opts = parse_window_options(argv)
    root = tk.Tk()
    app = AssistantApp(root, decorations=window_opts['decorations'], script_name=script_name)
    bind_ui_lifecycle(root)
    root.mainloop()
    return app
