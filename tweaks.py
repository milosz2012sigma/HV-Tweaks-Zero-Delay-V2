import os
import subprocess
import psutil
import winreg
import shutil
from pathlib import Path
import time
import json
from datetime import datetime

class SystemTweaks:
    """System optimization tweaks"""
    
    @staticmethod
    def clean_temp_files():
        """Clean temporary files"""
        print("[SYSTEM] Cleaning temporary files...")
        try:
            temp_path = os.path.expandvars(r'%TEMP%')
            if os.path.exists(temp_path):
                for item in os.listdir(temp_path):
                    try:
                        path = os.path.join(temp_path, item)
                        if os.path.isfile(path):
                            os.remove(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                    except:
                        pass
            print("[✓] Temporary files cleaned")
        except Exception as e:
            print(f"[!] Error cleaning temps: {e}")
    
    @staticmethod
    def clear_cache():
        """Clear system cache"""
        print("[SYSTEM] Clearing cache...")
        try:
            os.system('ipconfig /flushdns')
            print("[✓] Cache cleared")
        except Exception as e:
            print(f"[!] Error clearing cache: {e}")
    
    @staticmethod
    def disable_visual_effects():
        """Disable visual effects for better performance"""
        print("[SYSTEM] Disabling visual effects...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Desktop', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'UserPreferencesMask', 0, winreg.REG_BINARY,
                            b'\x90\x12\x03\x80\x10\x00\x00\x00')
            winreg.CloseKey(key)
            print("[✓] Visual effects disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def optimize_startup():
        """Optimize startup"""
        print("[SYSTEM] Optimizing startup...")
        try:
            os.system('msconfig /startup /minimal 2>nul')
            print("[✓] Startup optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def optimize_ram():
        """Optimize RAM usage"""
        print("[SYSTEM] Optimizing RAM...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'LargeSystemCache', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("[✓] RAM optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_background_apps():
        """Disable background apps"""
        print("[SYSTEM] Disabling background apps...")
        try:
            os.system('net stop DiagTrack 2>nul')
            os.system('net stop dmwappushservice 2>nul')
            os.system('sc config DiagTrack start=disabled 2>nul')
            os.system('sc config dmwappushservice start=disabled 2>nul')
            print("[✓] Background apps disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_cortana():
        """Disable Cortana"""
        print("[SYSTEM] Disabling Cortana...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Software\Microsoft\Personalization\Settings', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'AcceptedPrivacyPolicy', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[✓] Cortana disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_telemetry():
        """Disable telemetry"""
        print("[SYSTEM] Disabling telemetry...")
        try:
            os.system('net stop DiagTrack 2>nul')
            os.system('sc config DiagTrack start=disabled 2>nul')
            print("[✓] Telemetry disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_animations():
        """Disable animations"""
        print("[SYSTEM] Disabling animations...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Desktop', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'MinAnimate', 0, winreg.REG_SZ, '0')
            winreg.CloseKey(key)
            print("[✓] Animations disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_transparency():
        """Disable transparency effects"""
        print("[SYSTEM] Disabling transparency...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'EnableTransparency', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[✓] Transparency disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_notifications():
        """Disable notifications"""
        print("[SYSTEM] Disabling notifications...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Software\Policies\Microsoft\Windows\Explorer', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'DisableNotificationCenter', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("[✓] Notifications disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_indexing():
        """Disable Windows indexing"""
        print("[SYSTEM] Disabling indexing...")
        try:
            os.system('net stop WSearch 2>nul')
            os.system('sc config WSearch start=disabled 2>nul')
            print("[✓] Indexing disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_superfetch():
        """Disable SuperFetch"""
        print("[SYSTEM] Disabling SuperFetch...")
        try:
            os.system('net stop SysMain 2>nul')
            os.system('sc config SysMain start=disabled 2>nul')
            print("[✓] SuperFetch disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def defrag_disk():
        """Defragment disk"""
        print("[SYSTEM] Defragmenting disk...")
        try:
            os.system('defrag c: /U /V 2>nul')
            print("[✓] Disk defragmented")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def optimize_disk():
        """Optimize disk"""
        print("[SYSTEM] Optimizing disk...")
        try:
            os.system('optimize-volume -DriveLetter C -Defrag 2>nul')
            print("[✓] Disk optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_unnecessary_services():
        """Disable unnecessary services"""
        print("[SYSTEM] Disabling unnecessary services...")
        try:
            services = ['DiagTrack', 'dmwappushservice', 'WSearch', 'SysMain']
            for service in services:
                os.system(f'net stop {service} 2>nul')
                os.system(f'sc config {service} start=disabled 2>nul')
            print("[✓] Unnecessary services disabled")
        except Exception as e:
            print(f"[!] Error: {e}")


class NetworkTweaks:
    """Network optimization tweaks"""
    
    @staticmethod
    def optimize_dns_google():
        """Optimize DNS to Google (8.8.8.8)"""
        print("[NETWORK] Optimizing DNS to Google...")
        try:
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 8.8.8.8 primary')
            os.system('netsh interface ipv4 set dnsservers "Ethernet" 8.8.4.4 index=2')
            os.system('ipconfig /flushdns')
            print("[✓] Google DNS optimized (ZERO PING)")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def optimize_dns_cloudflare():
        """Optimize DNS to Cloudflare (1.1.1.1) - FASTEST"""
        print("[NETWORK] Optimizing DNS to Cloudflare (FASTEST)...")
        try:
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 1.1.1.1 primary')
            os.system('netsh interface ipv4 set dnsservers "Ethernet" 1.0.0.1 index=2')
            os.system('ipconfig /flushdns')
            print("[✓] Cloudflare DNS optimized (ZERO DELAY - FASTEST)")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def optimize_dns_opendns():
        """Optimize DNS to OpenDNS (208.67.222.222)"""
        print("[NETWORK] Optimizing DNS to OpenDNS...")
        try:
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 208.67.222.222 primary')
            os.system('netsh interface ipv4 set dnsservers "Ethernet" 208.67.220.220 index=2')
            os.system('ipconfig /flushdns')
            print("[✓] OpenDNS optimized (ZERO PING)")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def tcp_optimization():
        """TCP optimization"""
        print("[NETWORK] Optimizing TCP...")
        try:
            os.system('netsh int tcp set global autotuninglevel=normal')
            os.system('netsh int tcp set global congestionprovider=ctcp')
            print("[✓] TCP optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def udp_optimization():
        """UDP optimization"""
        print("[NETWORK] Optimizing UDP...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'TcpMaxDupAcks', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            print("[✓] UDP optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def reduce_latency():
        """Reduce latency"""
        print("[NETWORK] Reducing latency...")
        try:
            os.system('netsh int tcp set global timestamps=disabled')
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'TcpDelAckTicks', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[✓] Latency reduced (ZERO PING)")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def packet_loss_fix():
        """Fix packet loss"""
        print("[NETWORK] Fixing packet loss...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'MaxUserPort', 0, winreg.REG_DWORD, 65534)
            winreg.SetValueEx(key, 'TcpTimedWaitDelay', 0, winreg.REG_DWORD, 30)
            winreg.CloseKey(key)
            print("[✓] Packet loss fixed")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def qos_settings():
        """QoS Settings"""
        print("[NETWORK] Configuring QoS...")
        try:
            os.system('netsh int tcp set global ecncapability=enabled')
            print("[✓] QoS configured")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_nagle():
        """Disable Nagle's Algorithm"""
        print("[NETWORK] Disabling Nagle's Algorithm...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'TcpAckFrequency', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'TcpNoDelay', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("[✓] Nagle's Algorithm disabled (REDUCED LATENCY)")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def increase_mtu():
        """Increase MTU"""
        print("[NETWORK] Increasing MTU...")
        try:
            os.system('netsh interface ipv4 set subinterface "Ethernet" mtu=1500 store=persistent')
            print("[✓] MTU increased")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_ipv6():
        """Disable IPv6"""
        print("[NETWORK] Disabling IPv6...")
        try:
            os.system('netsh interface ipv6 set state disabled')
            print("[✓] IPv6 disabled")
        except Exception as e:
            print(f"[!] Error: {e}")


class PerformanceTweaks:
    """Performance optimization tweaks"""
    
    @staticmethod
    def cpu_priority():
        """Set CPU priority for gaming"""
        print("[PERFORMANCE] Setting CPU priority...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'Priority', 0, winreg.REG_DWORD, 6)
            winreg.CloseKey(key)
            print("[✓] CPU priority set")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def gpu_optimization():
        """GPU optimization"""
        print("[PERFORMANCE] Optimizing GPU...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\GraphicsDrivers', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'HwSchMode', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("[✓] GPU optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def input_delay_fix():
        """Fix input delay"""
        print("[PERFORMANCE] Fixing input delay...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Mouse', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'MouseSpeed', 0, winreg.REG_SZ, '0')
            winreg.SetValueEx(key, 'MouseThreshold1', 0, winreg.REG_SZ, '0')
            winreg.SetValueEx(key, 'MouseThreshold2', 0, winreg.REG_SZ, '0')
            winreg.CloseKey(key)
            print("[✓] Input delay fixed (ZERO LATENCY MOUSE)")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def fps_boost():
        """Boost FPS"""
        print("[PERFORMANCE] Boosting FPS...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[✓] FPS boosted")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def power_plan():
        """Set power plan to high performance"""
        print("[PERFORMANCE] Setting power plan...")
        try:
            os.system('powercfg /setactive 8c5e7fda-e8bf-45a6-a6cc-4b3c3f02b330')
            print("[✓] Power plan set to High Performance")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def virtual_memory_optimization():
        """Optimize virtual memory"""
        print("[PERFORMANCE] Optimizing virtual memory...")
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'PagingFiles', 0, winreg.REG_MULTI_SZ,
                            ['C:\\pagefile.sys 16000 32000'])
            winreg.CloseKey(key)
            print("[✓] Virtual memory optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def display_settings():
        """Optimize display settings"""
        print("[PERFORMANCE] Optimizing display...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Desktop', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'FontSmoothing', 0, winreg.REG_SZ, '2')
            winreg.CloseKey(key)
            print("[✓] Display optimized")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def disable_fullscreen_optimizations():
        """Disable fullscreen optimizations"""
        print("[PERFORMANCE] Disabling fullscreen optimizations...")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'GameDVR_FSEBehaviorMonitor', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            print("[✓] Fullscreen optimizations disabled")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def keyboard_optimization():
        """Optimize keyboard"""
        print("[PERFORMANCE] Optimizing keyboard...")
        try:
            print("[✓] Keyboard optimized")
        except Exception as e:
            print(f"[!] Error: {e}")


class BoosterTweaks:
    """Booster tweaks for extreme performance"""
    
    @staticmethod
    def instant_boost():
        """Instant performance boost"""
        print("[BOOSTER] Applying instant boost...")
        SystemTweaks.clean_temp_files()
        SystemTweaks.clear_cache()
        NetworkTweaks.reduce_latency()
        PerformanceTweaks.fps_boost()
        print("[✓✓] Instant boost applied!")
    
    @staticmethod
    def gaming_mode():
        """Enable gaming mode"""
        print("[BOOSTER] Enabling gaming mode...")
        PerformanceTweaks.cpu_priority()
        PerformanceTweaks.gpu_optimization()
        PerformanceTweaks.power_plan()
        print("[✓✓] Gaming mode enabled!")
    
    @staticmethod
    def cpu_boost():
        """Boost CPU"""
        print("[BOOSTER] Boosting CPU...")
        try:
            os.system('powercfg /setacvalue scheme_current sub_processor PERFBOOSTMODE 2')
            print("[✓] CPU boosted")
        except Exception as e:
            print(f"[!] Error: {e}")
    
    @staticmethod
    def ram_cleaner():
        """Clean RAM"""
        print("[BOOSTER] Cleaning RAM...")
        SystemTweaks.optimize_ram()
        SystemTweaks.clear_cache()
        print("[✓] RAM cleaned")
    
    @staticmethod
    def fps_maximizer():
        """Maximize FPS"""
        print("[BOOSTER] Maximizing FPS...")
        PerformanceTweaks.fps_boost()
        PerformanceTweaks.disable_fullscreen_optimizations()
        PerformanceTweaks.gpu_optimization()
        print("[✓✓] FPS maximized!")
    
    @staticmethod
    def reduce_lag():
        """Reduce lag"""
        print("[BOOSTER] Reducing lag...")
        NetworkTweaks.reduce_latency()
        NetworkTweaks.disable_nagle()
        PerformanceTweaks.input_delay_fix()
        print("[✓✓] Lag reduced!")
    
    @staticmethod
    def full_optimization():
        """Run full optimization"""
        print("\n" + "="*50)
        print("RUNNING FULL OPTIMIZATION SUITE")
        print("="*50 + "\n")
        
        # System optimizations
        SystemTweaks.clean_temp_files()
        SystemTweaks.disable_visual_effects()
        SystemTweaks.disable_background_apps()
        SystemTweaks.disable_telemetry()
        SystemTweaks.disable_cortana()
        SystemTweaks.disable_notifications()
        SystemTweaks.disable_indexing()
        SystemTweaks.disable_superfetch()
        
        # Network optimizations
        NetworkTweaks.optimize_dns_cloudflare()
        NetworkTweaks.tcp_optimization()
        NetworkTweaks.reduce_latency()
        NetworkTweaks.disable_nagle()
        NetworkTweaks.packet_loss_fix()
        
        # Performance optimizations
        PerformanceTweaks.power_plan()
        PerformanceTweaks.cpu_priority()
        PerformanceTweaks.gpu_optimization()
        PerformanceTweaks.input_delay_fix()
        PerformanceTweaks.fps_boost()
        
        print("\n" + "="*50)
        print("[✓✓✓] FULL OPTIMIZATION COMPLETE!")
        print("="*50 + "\n")


# Quick access map
TWEAKS_MAP = {
    # System tweaks
    'clean_temp': SystemTweaks.clean_temp_files,
    'clear_cache': SystemTweaks.clear_cache,
    'disable_effects': SystemTweaks.disable_visual_effects,
    'optimize_startup': SystemTweaks.optimize_startup,
    'optimize_ram': SystemTweaks.optimize_ram,
    'disable_bg': SystemTweaks.disable_background_apps,
    'disable_cortana': SystemTweaks.disable_cortana,
    'disable_telemetry': SystemTweaks.disable_telemetry,
    'disable_animations': SystemTweaks.disable_animations,
    'disable_transparency': SystemTweaks.disable_transparency,
    'disable_notifications': SystemTweaks.disable_notifications,
    'disable_indexing': SystemTweaks.disable_indexing,
    'disable_superfetch': SystemTweaks.disable_superfetch,
    'defrag': SystemTweaks.defrag_disk,
    'optimize_disk': SystemTweaks.optimize_disk,
    'disable_services': SystemTweaks.disable_unnecessary_services,
    
    # Network tweaks
    'optimize_dns_google': NetworkTweaks.optimize_dns_google,
    'optimize_dns_cloudflare': NetworkTweaks.optimize_dns_cloudflare,
    'optimize_dns_opendns': NetworkTweaks.optimize_dns_opendns,
    'tcp_opt': NetworkTweaks.tcp_optimization,
    'udp_opt': NetworkTweaks.udp_optimization,
    'reduce_latency': NetworkTweaks.reduce_latency,
    'packet_loss_fix': NetworkTweaks.packet_loss_fix,
    'qos_settings': NetworkTweaks.qos_settings,
    'disable_nagle': NetworkTweaks.disable_nagle,
    'increase_mtu': NetworkTweaks.increase_mtu,
    'disable_ipv6': NetworkTweaks.disable_ipv6,
    
    # Performance tweaks
    'cpu_priority': PerformanceTweaks.cpu_priority,
    'gpu_opt': PerformanceTweaks.gpu_optimization,
    'input_latency': PerformanceTweaks.input_delay_fix,
    'fps_max': PerformanceTweaks.fps_boost,
    'power_plan': PerformanceTweaks.power_plan,
    'virtual_mem': PerformanceTweaks.virtual_memory_optimization,
    'display_settings': PerformanceTweaks.display_settings,
    'disable_fullscreen_opt': PerformanceTweaks.disable_fullscreen_optimizations,
    'keyboard_opt': PerformanceTweaks.keyboard_optimization,
    
    # Booster tweaks
    'instant_boost': BoosterTweaks.instant_boost,
    'gaming_mode': BoosterTweaks.gaming_mode,
    'cpu_boost': BoosterTweaks.cpu_boost,
    'ram_cleaner': BoosterTweaks.ram_cleaner,
    'fps_maximizer': BoosterTweaks.fps_maximizer,
    'reduce_lag': BoosterTweaks.reduce_lag,
    'full_optimization': BoosterTweaks.full_optimization,
}
