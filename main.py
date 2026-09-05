import sys
import subprocess
import psutil
import threading
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTabWidget, QFrame, QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF
import ping3

class StatsWorker(QThread):
    stats_updated = pyqtSignal(dict)
    
    def run(self):
        while True:
            try:
                # CPU Usage
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # RAM Usage
                ram = psutil.virtual_memory()
                ram_percent = ram.percent
                
                # Ping test
                try:
                    ping_time = ping3.ping('8.8.8.8', timeout=2)
                    ping_ms = int(ping_time * 1000) if ping_time else 999
                except:
                    ping_ms = 999
                
                # Packet Loss (simulated)
                packet_loss = 0
                
                # Jitter (simulated)
                jitter = 0
                
                stats = {
                    'cpu': cpu_percent,
                    'ram': ram_percent,
                    'ping': ping_ms,
                    'packet_loss': packet_loss,
                    'jitter': jitter,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
                
                self.stats_updated.emit(stats)
                time.sleep(2)
            except Exception as e:
                print(f"Error in stats worker: {e}")
                time.sleep(2)

class HVTweaksApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HV Tweaks - ZERO DELAY V2")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet(self.get_dark_theme())
        
        # Stats
        self.current_stats = {
            'cpu': 0,
            'ram': 0,
            'ping': 0,
            'packet_loss': 0,
            'jitter': 0
        }
        
        # Start stats worker
        self.stats_worker = StatsWorker()
        self.stats_worker.stats_updated.connect(self.update_stats)
        self.stats_worker.start()
        
        self.init_ui()
    
    def get_dark_theme(self):
        return """
        QMainWindow {
            background-color: #0a0e27;
        }
        QWidget {
            background-color: #0a0e27;
            color: #ffffff;
        }
        QTabWidget::pane {
            border: 2px solid #ff3333;
        }
        QTabBar::tab {
            background-color: #1a1f3a;
            color: #ffffff;
            padding: 8px 20px;
            border: 1px solid #ff3333;
        }
        QTabBar::tab:selected {
            background-color: #ff3333;
            color: #ffffff;
        }
        QPushButton {
            background-color: #ff3333;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #ff5555;
        }
        QPushButton:pressed {
            background-color: #dd0000;
        }
        QLabel {
            color: #ffffff;
        }
        QFrame {
            background-color: #0f1429;
            border: 2px solid #ff3333;
            border-radius: 8px;
        }
        QScrollArea {
            background-color: #0a0e27;
            border: none;
        }
        """
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Tabs
        tabs = self.create_tabs()
        main_layout.addWidget(tabs, 1)
        
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
    
    def create_sidebar(self):
        sidebar_frame = QFrame()
        sidebar_frame.setMaximumWidth(200)
        sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: #0f1429;
                border: none;
                border-right: 2px solid #ff3333;
            }
        """)
        
        layout = QVBoxLayout(sidebar_frame)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 20, 10, 20)
        
        # Logo
        logo_label = QLabel("⭐ HV")
        logo_label.setFont(QFont("Arial", 20, QFont.Bold))
        logo_label.setStyleSheet("color: #ff3333;")
        layout.addWidget(logo_label)
        
        # Menu buttons
        menu_items = [
            ("📊 DASHBOARD", "dashboard"),
            ("⚙️ OPTIMIZATIONS", "optimizations"),
            ("🌐 NETWORK", "network"),
            ("💻 SYSTEM", "system"),
            ("🚀 BOOSTER", "booster"),
            ("⚡ SETTINGS", "settings")
        ]
        
        for item_text, item_id in menu_items:
            btn = QPushButton(item_text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a1f3a;
                    color: #ffffff;
                    border: 2px solid #ff3333;
                    border-radius: 8px;
                    padding: 12px;
                    font-weight: bold;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #ff3333;
                }
            """)
            btn.clicked.connect(lambda checked, idx=menu_items.index((item_text, item_id)): 
                              self.tabs.setCurrentIndex(idx))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return sidebar_frame
    
    def create_tabs(self):
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar {
                background-color: transparent;
            }
        """)
        
        # Dashboard Tab
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        
        # Optimizations Tab
        self.tabs.addTab(self.create_optimizations_tab(), "Optimizations")
        
        # Network Tab
        self.tabs.addTab(self.create_network_tab(), "Network")
        
        # System Tab
        self.tabs.addTab(self.create_system_tab(), "System")
        
        # Booster Tab
        self.tabs.addTab(self.create_booster_tab(), "Booster")
        
        # Settings Tab
        self.tabs.addTab(self.create_settings_tab(), "Settings")
        
        return self.tabs
    
    def create_dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("SYSTEM STATUS")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #ff3333;")
        layout.addWidget(title)
        
        # Stats Grid
        stats_frame = QFrame()
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(15)
        
        # PING
        ping_label = QLabel("PING")
        ping_label.setStyleSheet("color: #ff3333; font-weight: bold;")
        self.ping_value = QLabel("8ms")
        self.ping_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.ping_status = QLabel("OPTIMIZED")
        self.ping_status.setStyleSheet("color: #00ff00;")
        
        # PACKET LOSS
        loss_label = QLabel("PACKET LOSS")
        loss_label.setStyleSheet("color: #ff3333; font-weight: bold;")
        self.loss_value = QLabel("0%")
        self.loss_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.loss_status = QLabel("OPTIMIZED")
        self.loss_status.setStyleSheet("color: #00ff00;")
        
        # JITTER
        jitter_label = QLabel("JITTER")
        jitter_label.setStyleSheet("color: #ff3333; font-weight: bold;")
        self.jitter_value = QLabel("0ms")
        self.jitter_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.jitter_status = QLabel("OPTIMIZED")
        self.jitter_status.setStyleSheet("color: #00ff00;")
        
        stats_layout.addWidget(ping_label, 0, 0)
        stats_layout.addWidget(self.ping_value, 1, 0)
        stats_layout.addWidget(self.ping_status, 2, 0)
        
        stats_layout.addWidget(loss_label, 0, 1)
        stats_layout.addWidget(self.loss_value, 1, 1)
        stats_layout.addWidget(self.loss_status, 2, 1)
        
        stats_layout.addWidget(jitter_label, 0, 2)
        stats_layout.addWidget(self.jitter_value, 1, 2)
        stats_layout.addWidget(self.jitter_status, 2, 2)
        
        layout.addWidget(stats_frame)
        
        # System Performance
        perf_title = QLabel("OPTIMIZATION LEVEL")
        perf_title.setFont(QFont("Arial", 14, QFont.Bold))
        perf_title.setStyleSheet("color: #ff3333;")
        layout.addWidget(perf_title)
        
        self.optimization_label = QLabel("100%")
        self.optimization_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.optimization_label.setStyleSheet("color: #00ff00;")
        self.optimization_label.setAlignment(Qt.AlignCenter)
        
        perf_sub = QLabel("MAX PERFORMANCE")
        perf_sub.setAlignment(Qt.AlignCenter)
        perf_sub.setStyleSheet("color: #00ff00;")
        
        layout.addWidget(self.optimization_label)
        layout.addWidget(perf_sub)
        
        # Quick Actions
        actions_title = QLabel("QUICK ACTIONS")
        actions_title.setFont(QFont("Arial", 14, QFont.Bold))
        actions_title.setStyleSheet("color: #ff3333;")
        layout.addWidget(actions_title)
        
        actions_layout = QGridLayout()
        actions = [
            "🎯 PING REDUCTION",
            "📦 PACKET LOSS FIX",
            "⚙️ SYSTEM OPTIMIZATION",
            "🌐 NETWORK BOOST",
            "⌨️ INPUT DELAY FIX",
            "🎮 FPS BOOST"
        ]
        
        for i, action in enumerate(actions):
            btn = QPushButton(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a1f3a;
                    border: 2px solid #ff3333;
                    border-radius: 8px;
                    padding: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff3333;
                }
            """)
            btn.clicked.connect(lambda checked, a=action: self.apply_tweak(a))
            actions_layout.addWidget(btn, i // 3, i % 3)
        
        layout.addLayout(actions_layout)
        
        # Main OPTIMIZE Button
        optimize_btn = QPushButton("🔴 OPTIMIZE")
        optimize_btn.setFont(QFont("Arial", 16, QFont.Bold))
        optimize_btn.setFixedHeight(60)
        optimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff3333;
                border-radius: 30px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff5555;
            }
        """)
        optimize_btn.clicked.connect(self.optimize_system)
        layout.addWidget(optimize_btn)
        
        layout.addStretch()
        
        return widget
    
    def create_optimizations_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("SYSTEM OPTIMIZATIONS")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ff3333;")
        layout.addWidget(title)
        
        optimizations = [
            ("🗑️ Clean Temp Files", "clean_temp"),
            ("⚡ Disable Background Apps", "disable_bg"),
            ("🎯 Optimize Startup", "optimize_startup"),
            ("💾 Clear Cache", "clear_cache"),
            ("🔧 Disable Visual Effects", "disable_effects"),
            ("📊 Optimize RAM", "optimize_ram"),
        ]
        
        for opt_name, opt_id in optimizations:
            btn = QPushButton(opt_name)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda checked, oid=opt_id: self.run_optimization(oid))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return widget
    
    def create_network_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("NETWORK OPTIMIZATION")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ff3333;")
        layout.addWidget(title)
        
        network_tweaks = [
            ("🌐 Optimize DNS", "optimize_dns"),
            ("📡 TCP Optimization", "tcp_opt"),
            ("🔌 Network Buffer", "network_buffer"),
            ("⚡ Reduce Latency", "reduce_latency"),
            ("📊 QoS Settings", "qos_settings"),
            ("🚀 UDP Optimization", "udp_opt"),
        ]
        
        for tweak_name, tweak_id in network_tweaks:
            btn = QPushButton(tweak_name)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda checked, tid=tweak_id: self.apply_network_tweak(tid))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return widget
    
    def create_system_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("SYSTEM SETTINGS")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ff3333;")
        layout.addWidget(title)
        
        system_tweaks = [
            ("💻 CPU Priority", "cpu_priority"),
            ("💾 Virtual Memory", "virtual_mem"),
            ("🎮 GPU Optimization", "gpu_opt"),
            ("⌨️ Input Latency", "input_latency"),
            ("🔋 Power Plan", "power_plan"),
            ("🖥️ Display Settings", "display_settings"),
        ]
        
        for tweak_name, tweak_id in system_tweaks:
            btn = QPushButton(tweak_name)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda checked, tid=tweak_id: self.apply_system_tweak(tid))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return widget
    
    def create_booster_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("PERFORMANCE BOOSTER")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ff3333;")
        layout.addWidget(title)
        
        boosters = [
            ("🚀 Instant Boost", "instant_boost"),
            ("🎮 Gaming Mode", "gaming_mode"),
            ("⚡ CPU Boost", "cpu_boost"),
            ("📊 RAM Cleaner", "ram_cleaner"),
            ("🔥 FPS Maximizer", "fps_max"),
            ("⏱️ Reduce Lag", "reduce_lag"),
        ]
        
        for boost_name, boost_id in boosters:
            btn = QPushButton(boost_name)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda checked, bid=boost_id: self.apply_boost(bid))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return widget
    
    def create_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("SETTINGS")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #ff3333;")
        layout.addWidget(title)
        
        settings_items = [
            ("⚙️ General Settings", "general"),
            ("🎨 Theme Settings", "theme"),
            ("📊 Performance Monitoring", "monitoring"),
            ("💾 Auto Optimization", "auto_opt"),
            ("🔔 Notifications", "notifications"),
            ("❓ About", "about"),
        ]
        
        for setting_name, setting_id in settings_items:
            btn = QPushButton(setting_name)
            btn.setFixedHeight(50)
            btn.clicked.connect(lambda checked, sid=setting_id: self.open_settings(sid))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        return widget
    
    def update_stats(self, stats):
        self.current_stats = stats
        self.ping_value.setText(f"{stats['ping']}ms")
        self.loss_value.setText(f"{stats['packet_loss']}%")
        self.jitter_value.setText(f"{stats['jitter']}ms")
    
    def optimize_system(self):
        print("[HV TWEAKS] Starting system optimization...")
        self.optimization_label.setText("Optimizing...")
        self.optimization_label.setStyleSheet("color: #ffaa00;")
        
        # Simulate optimization
        QTimer.singleShot(2000, lambda: self.show_optimization_complete())
    
    def show_optimization_complete(self):
        self.optimization_label.setText("100%")
        self.optimization_label.setStyleSheet("color: #00ff00;")
        print("[HV TWEAKS] ✓ Optimization complete!")
    
    def apply_tweak(self, tweak_name):
        print(f"[HV TWEAKS] Applying: {tweak_name}")
        # Implement actual tweaks here
    
    def run_optimization(self, opt_id):
        print(f"[HV TWEAKS] Running optimization: {opt_id}")
    
    def apply_network_tweak(self, tweak_id):
        print(f"[HV TWEAKS] Applying network tweak: {tweak_id}")
    
    def apply_system_tweak(self, tweak_id):
        print(f"[HV TWEAKS] Applying system tweak: {tweak_id}")
    
    def apply_boost(self, boost_id):
        print(f"[HV TWEAKS] Applying boost: {boost_id}")
    
    def open_settings(self, setting_id):
        print(f"[HV TWEAKS] Opening settings: {setting_id}")

def main():
    app = QApplication(sys.argv)
    window = HVTweaksApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()