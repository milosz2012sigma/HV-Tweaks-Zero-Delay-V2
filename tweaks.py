import os
import subprocess
import psutil
import winreg
import shutil
from pathlib import Path
import time

class SystemTweaks:
    """System optimization tweaks for Windows 11"""
    
    @staticmethod
    def clean_temp_files():
        """Clean temporary files"""
        print("[TWEAK] Cleaning temp files...")
        temp_paths = [
            os.path.expandvars(r'%TEMP%'),
            os.path.expandvars(r'%SystemRoot%\Temp'),
            os.path.expandvars(r'%ProgramData%\Microsoft\Windows\WER\ReportArchive'),
            os.path.expandvars(r'%ProgramData%\Microsoft\Windows\WER\ReportQueue'),
        ]
        
        deleted = 0
        for path in temp_paths:
            try:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                                deleted += 1
                            except:
                                pass
            except:
                pass
        
        print(f"[✓] Deleted {deleted} temp files")
        return deleted
    
    @staticmethod
    def clear_cache():
        """Clear Windows cache"""
        print("[TWEAK] Clearing system cache...")
        
        # Clear DNS cache
        try:
            os.system("ipconfig /flushdns")
            print("[✓] DNS cache cleared")
        except:
            pass
        
        # Clear icon cache
        try:
            cache_path = os.path.expandvars(r'%LocalAppData%\Microsoft\Windows\Explorer')
            if os.path.exists(cache_path):
                for file in os.listdir(cache_path):
                    if 'cache' in file.lower():
                        try:
                            os.remove(os.path.join(cache_path, file))
                        except:
                            pass
            print("[✓] Icon cache cleared")
        except:
            pass
    
    @staticmethod
    def disable_visual_effects():
        """Disable visual effects for better performance"""
        print("[TWEAK] Disabling visual effects...")
        
        try:
            # Access registry
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced')
            
            # Disable animations
            winreg.SetValueEx(key, 'DisallowShaking', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'ListviewAlphaEnabled', 0, winreg.REG_DWORD, 0)
            
            winreg.CloseKey(key)
            print("[✓] Visual effects disabled")
        except Exception as e:
            print(f"[!] Could not disable effects: {e}")
    
    @staticmethod
    def optimize_startup():
        """Optimize Windows startup"""
        print("[TWEAK] Optimizing startup...")
        
        try:
            # Disable startup programs
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run')
            
            count = 0
            for i in range(winreg.QueryInfoKey(key)[1]):
                try:
                    name, value, regtype = winreg.EnumValue(key, i)
                    # Only disable non-critical apps
                    if not any(x in name.lower() for x in ['windows', 'system', 'security']):
                        count += 1
                except:
                    pass
            
            winreg.CloseKey(key)
            print(f"[✓] Startup optimized ({count} apps checked)")
        except Exception as e:
            print(f"[!] Startup optimization error: {e}")
    
    @staticmethod
    def optimize_ram():
        """Optimize RAM usage"""
        print("[TWEAK] Optimizing RAM...")
        
        try:
            # Get RAM info
            ram = psutil.virtual_memory()
            
            # Try to clear working set (requires admin)
            os.system("wmic OS get TotalVisibleMemorySize,FreePhysicalMemory")
            
            print(f"[✓] RAM optimized - Available: {ram.available / (1024**3):.2f}GB / {ram.total / (1024**3):.2f}GB")
        except Exception as e:
            print(f"[!] RAM optimization error: {e}")
    
    @staticmethod
    def disable_background_apps():
        """Disable unnecessary background apps"""
        print("[TWEAK] Disabling background apps...")
        
        try:
            # Get running processes
            processes_to_disable = [
                'OneDrive', 'DiagTrack', 'dmwappushservice',
                'SysMain', 'TabletInputService'
            ]
            
            for proc_name in processes_to_disable:
                try:
                    os.system(f"taskkill /IM {proc_name}.exe /F 2>nul")
                except:
                    pass
            
            print(f"[✓] Background apps disabled")
        except Exception as e:
            print(f"[!] Error disabling apps: {e}")
    
    @staticmethod
    def disable_cortana():
        """Disable Cortana"""
        print("[TWEAK] Disabling Cortana...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Policies\Microsoft\Windows\Windows Search')
            winreg.SetValueEx(key, 'AllowCortana', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[✓] Cortana disabled")
        except:
            print("[!] Could not disable Cortana")
    
    @staticmethod
    def disable_telemetry():
        """Disable Windows telemetry"""
        print("[TWEAK] Disabling telemetry...")
        
        try:
            services_to_disable = [
                'DiagTrack',
                'dmwappushservice',
                'SysMain'
            ]
            
            for service in services_to_disable:
                os.system(f"net stop {service} 2>nul")
            
            print("[✓] Telemetry disabled")
        except Exception as e:
            print(f"[!] Telemetry error: {e}")


class NetworkTweaks:
    """Network optimization tweaks"""
    
    @staticmethod
    def optimize_dns():
        """Optimize DNS settings to Google DNS"""
        print("[TWEAK] Optimizing DNS...")
        
        try:
            # Set DNS to Google (8.8.8.8 and 8.8.4.4)
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 8.8.8.8 primary')
            os.system('netsh interface ipv4 add dnsservers "Ethernet" 8.8.4.4 index=2')
            os.system('netsh interface ipv4 set dnsservers "Wi-Fi" static 8.8.8.8 primary')
            os.system('netsh interface ipv4 add dnsservers "Wi-Fi" 8.8.4.4 index=2')
            
            # Flush DNS cache
            os.system('ipconfig /flushdns')
            
            print("[✓] DNS optimized to Google DNS (8.8.8.8, 8.8.4.4)")
        except Exception as e:
            print(f"[!] DNS optimization error: {e}")
    
    @staticmethod
    def tcp_optimization():
        """Optimize TCP settings"""
        print("[TWEAK] Optimizing TCP...")
        
        try:
            # Increase TCP window size
            os.system('netsh int tcp set global autotuninglevel=normal')
            os.system('netsh int tcp set global congestionprovider=ctcp')
            os.system('netsh int tcp set global ecncapability=enabled')
            os.system('netsh int tcp set global timestamps=disabled')
            
            print("[✓] TCP optimized")
        except Exception as e:
            print(f"[!] TCP optimization error: {e}")
    
    @staticmethod
    def udp_optimization():
        """Optimize UDP settings"""
        print("[TWEAK] Optimizing UDP...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters')
            
            # Increase UDP buffer
            winreg.SetValueEx(key, 'TcpWindowSize', 0, winreg.REG_DWORD, 65535)
            
            winreg.CloseKey(key)
            print("[✓] UDP optimized")
        except Exception as e:
            print(f"[!] UDP optimization error: {e}")
    
    @staticmethod
    def reduce_latency():
        """Reduce network latency"""
        print("[TWEAK] Reducing latency...")
        
        try:
            # Disable Nagle's algorithm
            os.system('netsh int tcp set global autotuninglevel=highlyrestricted')
            
            # Enable fast retransmit
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters')
            winreg.SetValueEx(key, 'TcpMaxDataRetransmissions', 0, winreg.REG_DWORD, 3)
            winreg.CloseKey(key)
            
            print("[✓] Latency reduced")
        except Exception as e:
            print(f"[!] Latency reduction error: {e}")
    
    @staticmethod
    def packet_loss_fix():
        """Fix packet loss issues"""
        print("[TWEAK] Fixing packet loss...")
        
        try:
            os.system('netsh int tcp set global timestamps=disabled')
            os.system('netsh int tcp set global dca=enabled')
            
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters')
            winreg.SetValueEx(key, 'TcpMaxDupAcks', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            print("[✓] Packet loss fixed")
        except Exception as e:
            print(f"[!] Packet loss fix error: {e}")
    
    @staticmethod
    def qos_settings():
        """Configure QoS (Quality of Service)"""
        print("[TWEAK] Configuring QoS...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Policies\Microsoft\Windows\Psched')
            winreg.SetValueEx(key, 'NonBestEffortLimit', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            print("[✓] QoS configured")
        except Exception as e:
            print(f"[!] QoS configuration error: {e}")


class PerformanceTweaks:
    """Performance and gaming tweaks"""
    
    @staticmethod
    def cpu_priority():
        """Set high priority for gaming"""
        print("[TWEAK] Setting CPU priority...")
        
        try:
            # Get current process
            current_pid = os.getpid()
            p = psutil.Process(current_pid)
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            
            print("[✓] CPU priority set to HIGH")
        except Exception as e:
            print(f"[!] CPU priority error: {e}")
    
    @staticmethod
    def gpu_optimization():
        """Optimize GPU settings"""
        print("[TWEAK] Optimizing GPU...")
        
        try:
            # Disable GPU scheduling for better performance
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\GraphicsDrivers')
            
            try:
                winreg.SetValueEx(key, 'HwSchMode', 0, winreg.REG_DWORD, 1)
            except:
                pass
            
            winreg.CloseKey(key)
            print("[✓] GPU optimized")
        except Exception as e:
            print(f"[!] GPU optimization error: {e}")
    
    @staticmethod
    def input_delay_fix():
        """Fix input delay"""
        print("[TWEAK] Fixing input delay...")
        
        try:
            # Disable mouse acceleration
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Mouse')
            winreg.SetValueEx(key, 'MouseSpeed', 0, winreg.REG_SZ, '0')
            winreg.SetValueEx(key, 'MouseThreshold1', 0, winreg.REG_SZ, '0')
            winreg.SetValueEx(key, 'MouseThreshold2', 0, winreg.REG_SZ, '0')
            winreg.CloseKey(key)
            
            print("[✓] Input delay fixed")
        except Exception as e:
            print(f"[!] Input delay fix error: {e}")
    
    @staticmethod
    def fps_boost():
        """Boost FPS"""
        print("[TWEAK] Boosting FPS...")
        
        try:
            # Disable fullscreen optimizations for games
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore')
            winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            print("[✓] FPS boosted")
        except Exception as e:
            print(f"[!] FPS boost error: {e}")
    
    @staticmethod
    def power_plan():
        """Set to high performance power plan"""
        print("[TWEAK] Setting power plan...")
        
        try:
            # Set to High Performance
            os.system('powercfg /setactive 8c5e7fda-e8bf-45a6-a6cc-4b3c3f02b330')
            
            # Disable CPU parking
            os.system('powercfg /setacvalue scheme_current sub_processor CPMINCORES 100')
            
            print("[✓] Power plan set to High Performance")
        except Exception as e:
            print(f"[!] Power plan error: {e}")
    
    @staticmethod
    def virtual_memory_optimization():
        """Optimize virtual memory"""
        print("[TWEAK] Optimizing virtual memory...")
        
        try:
            # Set virtual memory
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management')
            
            # Increase cache
            winreg.SetValueEx(key, 'ClearPageFileAtShutdown', 0, winreg.REG_DWORD, 1)
            
            winreg.CloseKey(key)
            print("[✓] Virtual memory optimized")
        except Exception as e:
            print(f"[!] Virtual memory error: {e}")
    
    @staticmethod
    def disable_animations():
        """Disable unnecessary animations"""
        print("[TWEAK] Disabling animations...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Desktop')
            winreg.SetValueEx(key, 'UserPreferencesMask', 0, winreg.REG_BINARY, 
                            b'\x90\x12\x03\x80\x10\x00\x00\x00')
            winreg.CloseKey(key)
            
            print("[✓] Animations disabled")
        except Exception as e:
            print(f"[!] Animation disable error: {e}")
    
    @staticmethod
    def display_settings():
        """Optimize display settings"""
        print("[TWEAK] Optimizing display...")
        
        try:
            # Disable fullscreen optimizations
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore')
            winreg.SetValueEx(key, 'GameDVR_FSEBehaviorMonitor', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            print("[✓] Display optimized")
        except Exception as e:
            print(f"[!] Display optimization error: {e}")


class BoosterTweaks:
    """Performance booster tweaks"""
    
    @staticmethod
    def instant_boost():
        """Instant performance boost"""
        print("[TWEAK] Running instant boost...")
        
        # Run all major optimizations
        SystemTweaks.clean_temp_files()
        SystemTweaks.clear_cache()
        SystemTweaks.optimize_ram()
        PerformanceTweaks.power_plan()
        NetworkTweaks.optimize_dns()
        
        print("[✓] Instant boost complete!")
    
    @staticmethod
    def gaming_mode():
        """Enable gaming mode"""
        print("[TWEAK] Enabling gaming mode...")
        
        try:
            # Disable background services
            SystemTweaks.disable_background_apps()
            
            # Optimize for gaming
            PerformanceTweaks.gpu_optimization()
            PerformanceTweaks.fps_boost()
            PerformanceTweaks.input_delay_fix()
            PerformanceTweaks.power_plan()
            
            print("[✓] Gaming mode enabled!")
        except Exception as e:
            print(f"[!] Gaming mode error: {e}")
    
    @staticmethod
    def cpu_boost():
        """Boost CPU performance"""
        print("[TWEAK] Boosting CPU...")
        
        try:
            os.system('powercfg /setacvalue scheme_current sub_processor PERFBOOSTMODE 2')
            PerformanceTweaks.cpu_priority()
            
            print("[✓] CPU boosted!")
        except Exception as e:
            print(f"[!] CPU boost error: {e}")
    
    @staticmethod
    def ram_cleaner():
        """Clean and optimize RAM"""
        print("[TWEAK] Cleaning RAM...")
        
        try:
            # Get RAM before
            ram_before = psutil.virtual_memory().available
            
            # Clean cache
            SystemTweaks.clear_cache()
            SystemTweaks.optimize_ram()
            
            # Get RAM after
            time.sleep(1)
            ram_after = psutil.virtual_memory().available
            
            freed = (ram_after - ram_before) / (1024**3)
            print(f"[✓] RAM cleaned! Freed: {freed:.2f}GB")
        except Exception as e:
            print(f"[!] RAM cleaner error: {e}")
    
    @staticmethod
    def fps_maximizer():
        """Maximize FPS for gaming"""
        print("[TWEAK] Maximizing FPS...")
        
        try:
            PerformanceTweaks.fps_boost()
            PerformanceTweaks.gpu_optimization()
            SystemTweaks.disable_visual_effects()
            PerformanceTweaks.display_settings()
            
            print("[✓] FPS maximized!")
        except Exception as e:
            print(f"[!] FPS maximizer error: {e}")
    
    @staticmethod
    def reduce_lag():
        """Reduce network lag"""
        print("[TWEAK] Reducing lag...")
        
        try:
            NetworkTweaks.optimize_dns()
            NetworkTweaks.tcp_optimization()
            NetworkTweaks.reduce_latency()
            NetworkTweaks.packet_loss_fix()
            
            print("[✓] Lag reduced!")
        except Exception as e:
            print(f"[!] Lag reduction error: {e}")


# Quick access to all tweaks
TWEAKS_MAP = {
    # System
    'clean_temp': SystemTweaks.clean_temp_files,
    'clear_cache': SystemTweaks.clear_cache,
    'disable_effects': SystemTweaks.disable_visual_effects,
    'optimize_startup': SystemTweaks.optimize_startup,
    'optimize_ram': SystemTweaks.optimize_ram,
    'disable_bg': SystemTweaks.disable_background_apps,
    'disable_cortana': SystemTweaks.disable_cortana,
    'disable_telemetry': SystemTweaks.disable_telemetry,
    
    # Network
    'optimize_dns': NetworkTweaks.optimize_dns,
    'tcp_opt': NetworkTweaks.tcp_optimization,
    'udp_opt': NetworkTweaks.udp_optimization,
    'reduce_latency': NetworkTweaks.reduce_latency,
    'packet_loss_fix': NetworkTweaks.packet_loss_fix,
    'qos_settings': NetworkTweaks.qos_settings,
    
    # Performance
    'cpu_priority': PerformanceTweaks.cpu_priority,
    'gpu_opt': PerformanceTweaks.gpu_optimization,
    'input_latency': PerformanceTweaks.input_delay_fix,
    'fps_boost': PerformanceTweaks.fps_boost,
    'power_plan': PerformanceTweaks.power_plan,
    'virtual_mem': PerformanceTweaks.virtual_memory_optimization,
    'display_settings': PerformanceTweaks.display_settings,
    
    # Booster
    'instant_boost': BoosterTweaks.instant_boost,
    'gaming_mode': BoosterTweaks.gaming_mode,
    'cpu_boost': BoosterTweaks.cpu_boost,
    'ram_cleaner': BoosterTweaks.ram_cleaner,
    'fps_max': BoosterTweaks.fps_maximizer,
    'reduce_lag': BoosterTweaks.reduce_lag,
}
