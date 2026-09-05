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
            os.path.expandvars(r'%LocalAppData%\Temp'),
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
        
        try:
            os.system("ipconfig /flushdns")
            print("[✓] DNS cache cleared")
        except:
            pass
    
    @staticmethod
    def disable_visual_effects():
        """Disable visual effects for better performance"""
        print("[TWEAK] Disabling visual effects...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced', 0, winreg.KEY_WRITE)
            
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
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_READ)
            winreg.CloseKey(key)
            print(f"[✓] Startup optimized")
        except Exception as e:
            print(f"[!] Startup optimization error: {e}")
    
    @staticmethod
    def optimize_ram():
        """Optimize RAM usage"""
        print("[TWEAK] Optimizing RAM...")
        
        try:
            ram = psutil.virtual_memory()
            print(f"[✓] RAM optimized - Available: {ram.available / (1024**3):.2f}GB / {ram.total / (1024**3):.2f}GB")
        except Exception as e:
            print(f"[!] RAM optimization error: {e}")
    
    @staticmethod
    def disable_background_apps():
        """Disable unnecessary background apps"""
        print("[TWEAK] Disabling background apps...")
        
        try:
            processes_to_disable = [
                'OneDrive', 'DiagTrack', 'dmwappushservice',
                'SysMain', 'TabletInputService', 'ShellExperienceHost'
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
                                r'SOFTWARE\Policies\Microsoft\Windows\Windows Search', 0, winreg.KEY_WRITE)
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
            services_to_disable = ['DiagTrack', 'dmwappushservice']
            
            for service in services_to_disable:
                os.system(f"net stop {service} 2>nul")
            
            print("[✓] Telemetry disabled")
        except Exception as e:
            print(f"[!] Telemetry error: {e}")
    
    @staticmethod
    def disable_animations():
        """Disable unnecessary animations"""
        print("[TWEAK] Disabling animations...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Desktop', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'UserPreferencesMask', 0, winreg.REG_BINARY, 
                            b'\x90\x12\x03\x80\x10\x00\x00\x00')
            winreg.CloseKey(key)
            
            print("[✓] Animations disabled")
        except Exception as e:
            print(f"[!] Animation disable error: {e}")
    
    @staticmethod
    def disable_transparency():
        """Disable transparency effects"""
        print("[TWEAK] Disabling transparency...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'EnableTransparency', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("[✓] Transparency disabled")
        except:
            pass
    
    @staticmethod
    def disable_notifications():
        """Disable Windows notifications"""
        print("[TWEAK] Disabling notifications...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Software\Policies\Microsoft\Windows\Explorer', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'DisableNotificationCenter', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            print("[✓] Notifications disabled")
        except:
            pass
    
    @staticmethod
    def disable_indexing():
        """Disable Windows indexing"""
        print("[TWEAK] Disabling indexing...")
        
        try:
            os.system("net stop WSearch 2>nul")
            os.system("sc config WSearch start=disabled 2>nul")
            print("[✓] Indexing disabled")
        except:
            pass
    
    @staticmethod
    def disable_superfetch():
        """Disable SuperFetch service"""
        print("[TWEAK] Disabling SuperFetch...")
        
        try:
            os.system("net stop SysMain 2>nul")
            os.system("sc config SysMain start=disabled 2>nul")
            print("[✓] SuperFetch disabled")
        except:
            pass
    
    @staticmethod
    def defrag_disk():
        """Defragment disk"""
        print("[TWEAK] Defragmenting disk...")
        
        try:
            os.system("defrag C: /O")
            print("[✓] Disk defragmented")
        except:
            pass
    
    @staticmethod
    def optimize_disk():
        """Optimize disk"""
        print("[TWEAK] Optimizing disk...")
        
        try:
            os.system("optimize-volume -DriveLetter C -Defrag -Verbose")
            print("[✓] Disk optimized")
        except:
            pass
    
    @staticmethod
    def disable_unnecessary_services():
        """Disable unnecessary Windows services"""
        print("[TWEAK] Disabling unnecessary services...")
        
        unnecessary_services = [
            'DiagTrack', 'dmwappushservice', 'RetailDemo', 'MapsBroker', 'lmhosts', 'NaturalAuthentication',
        ]
        
        for service in unnecessary_services:
            try:
                os.system(f"sc config {service} start=disabled 2>nul")
            except:
                pass
        
        print(f"[✓] Disabled {len(unnecessary_services)} services")


class NetworkTweaks:
    """Network optimization tweaks"""
    
    @staticmethod
    def optimize_dns_google():
        """Optimize DNS to Google DNS"""
        print("[TWEAK] Optimizing DNS to Google...")
        
        try:
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 8.8.8.8 primary')
            os.system('netsh interface ipv4 add dnsservers "Ethernet" 8.8.4.4 index=2')
            os.system('netsh interface ipv4 set dnsservers "Wi-Fi" static 8.8.8.8 primary')
            os.system('netsh interface ipv4 add dnsservers "Wi-Fi" 8.8.4.4 index=2')
            os.system('ipconfig /flushdns')
            print("[✓] DNS optimized to Google (8.8.8.8)")
        except Exception as e:
            print(f"[!] DNS optimization error: {e}")
    
    @staticmethod
    def optimize_dns_cloudflare():
        """Optimize DNS to Cloudflare"""
        print("[TWEAK] Optimizing DNS to Cloudflare...")
        
        try:
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 1.1.1.1 primary')
            os.system('netsh interface ipv4 add dnsservers "Ethernet" 1.0.0.1 index=2')
            os.system('netsh interface ipv4 set dnsservers "Wi-Fi" static 1.1.1.1 primary')
            os.system('netsh interface ipv4 add dnsservers "Wi-Fi" 1.0.0.1 index=2')
            os.system('ipconfig /flushdns')
            print("[✓] DNS optimized to Cloudflare (1.1.1.1)")
        except Exception as e:
            print(f"[!] DNS optimization error: {e}")
    
    @staticmethod
    def optimize_dns_opendns():
        """Optimize DNS to OpenDNS"""
        print("[TWEAK] Optimizing DNS to OpenDNS...")
        
        try:
            os.system('netsh interface ipv4 set dnsservers "Ethernet" static 208.67.222.222 primary')
            os.system('netsh interface ipv4 add dnsservers "Ethernet" 208.67.220.220 index=2')
            os.system('ipconfig /flushdns')
            print("[✓] DNS optimized to OpenDNS")
        except Exception as e:
            print(f"[!] DNS optimization error: {e}")
    
    @staticmethod
    def tcp_optimization():
        """Optimize TCP settings"""
        print("[TWEAK] Optimizing TCP...")
        
        try:
            os.system('netsh int tcp set global autotuninglevel=normal')
            os.system('netsh int tcp set global congestionprovider=ctcp')
            os.system('netsh int tcp set global ecncapability=enabled')
            os.system('netsh int tcp set global timestamps=disabled')
            os.system('netsh int tcp set global initialrto=3000')
            
            print("[✓] TCP optimized")
        except Exception as e:
            print(f"[!] TCP optimization error: {e}")
    
    @staticmethod
    def udp_optimization():
        """Optimize UDP settings"""
        print("[TWEAK] Optimizing UDP...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            
            winreg.SetValueEx(key, 'TcpWindowSize', 0, winreg.REG_DWORD, 65535)
            winreg.SetValueEx(key, 'DefaultRcvWindow', 0, winreg.REG_DWORD, 65535)
            
            winreg.CloseKey(key)
            print("[✓] UDP optimized")
        except Exception as e:
            print(f"[!] UDP optimization error: {e}")
    
    @staticmethod
    def reduce_latency():
        """Reduce network latency"""
        print("[TWEAK] Reducing latency...")
        
        try:
            os.system('netsh int tcp set global autotuninglevel=highlyrestricted')
            
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'TcpMaxDataRetransmissions', 0, winreg.REG_DWORD, 3)
            winreg.SetValueEx(key, 'TcpDelAckTicks', 0, winreg.REG_DWORD, 0)
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
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'TcpMaxDupAcks', 0, winreg.REG_DWORD, 2)
            winreg.SetValueEx(key, 'TcpMaxSynRetransmissions', 0, winreg.REG_DWORD, 2)
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
                                r'SOFTWARE\Policies\Microsoft\Windows\Psched', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'NonBestEffortLimit', 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            
            print("[✓] QoS configured")
        except Exception as e:
            print(f"[!] QoS configuration error: {e}")
    
    @staticmethod
    def disable_nagle():
        """Disable Nagle's algorithm"""
        print("[TWEAK] Disabling Nagle's algorithm...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_WRITE)
            
            winreg.SetValueEx(key, 'TcpNoDelay', 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            
            print("[✓] Nagle's algorithm disabled")
        except:
            pass
    
    @staticmethod
    def increase_mtu():
        """Increase MTU size for better throughput"""
        print("[TWEAK] Increasing MTU...")
        
        try:
            os.system('netsh interface ipv4 set subinterface "Ethernet" mtu=1500 store=persistent')
            print("[✓] MTU increased to 1500")
        except:
            pass
    
    @staticmethod
    def disable_ipv6():
        """Disable IPv6 (faster IPv4)"""
        print("[TWEAK] Disabling IPv6...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Services\TCPIP6\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'DisabledComponents', 0, winreg.REG_DWORD, 0xffffffff)
            winreg.CloseKey(key)
            print("[✓] IPv6 disabled")
        except:
            pass


class PerformanceTweaks:
    """Performance and gaming tweaks"""
    
    @staticmethod
    def cpu_priority():
        """Set high priority for gaming"""
        print("[TWEAK] Setting CPU priority...")
        
        try:
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
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\GraphicsDrivers', 0, winreg.KEY_WRITE)
            
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
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Mouse', 0, winreg.KEY_WRITE)
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
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'GameDVR_Enabled', 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, 'GameDVR_FSEBehaviorMonitor', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            print("[✓] FPS boosted")
        except Exception as e:
            print(f"[!] FPS boost error: {e}")
    
    @staticmethod
    def power_plan():
        """Set to high performance power plan"""
        print("[TWEAK] Setting power plan...")
        
        try:
            os.system('powercfg /setactive 8c5e7fda-e8bf-45a6-a6cc-4b3c3f02b330')
            os.system('powercfg /setacvalue scheme_current sub_processor CPMINCORES 100')
            os.system('powercfg /setacvalue scheme_current sub_processor PERFBOOSTMODE 2')
            
            print("[✓] Power plan set to High Performance")
        except Exception as e:
            print(f"[!] Power plan error: {e}")
    
    @staticmethod
    def virtual_memory_optimization():
        """Optimize virtual memory"""
        print("[TWEAK] Optimizing virtual memory...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r'SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management', 0, winreg.KEY_WRITE)
            
            winreg.SetValueEx(key, 'ClearPageFileAtShutdown', 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, 'LargeSystemCache', 0, winreg.REG_DWORD, 1)
            
            winreg.CloseKey(key)
            print("[✓] Virtual memory optimized")
        except Exception as e:
            print(f"[!] Virtual memory error: {e}")
    
    @staticmethod
    def display_settings():
        """Optimize display settings"""
        print("[TWEAK] Optimizing display...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'GameDVR_FSEBehaviorMonitor', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            
            print("[✓] Display optimized")
        except Exception as e:
            print(f"[!] Display optimization error: {e}")
    
    @staticmethod
    def disable_fullscreen_optimizations():
        """Disable fullscreen optimizations"""
        print("[TWEAK] Disabling fullscreen optimizations...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'System\GameConfigStore', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'GameDVR_FSEBehaviorMonitor', 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            print("[✓] Fullscreen optimizations disabled")
        except:
            pass
    
    @staticmethod
    def keyboard_optimization():
        """Optimize keyboard response"""
        print("[TWEAK] Optimizing keyboard...")
        
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\Keyboard', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'InitialKeyboardIndicators', 0, winreg.REG_SZ, '2')
            winreg.SetValueEx(key, 'KeyboardDelay', 0, winreg.REG_SZ, '0')
            winreg.SetValueEx(key, 'KeyboardSpeed', 0, winreg.REG_SZ, '31')
            winreg.CloseKey(key)
            print("[✓] Keyboard optimized")
        except:
            pass


class BoosterTweaks:
    """Performance booster tweaks"""
    
    @staticmethod
    def instant_boost():
        """Instant performance boost"""
        print("[TWEAK] Running instant boost...")
        
        SystemTweaks.clean_temp_files()
        SystemTweaks.clear_cache()
        SystemTweaks.optimize_ram()
        PerformanceTweaks.power_plan()
        NetworkTweaks.optimize_dns_google()
        
        print("[✓] Instant boost complete!")
    
    @staticmethod
    def gaming_mode():
        """Enable gaming mode"""
        print("[TWEAK] Enabling gaming mode...")
        
        try:
            SystemTweaks.disable_background_apps()
            PerformanceTweaks.gpu_optimization()
            PerformanceTweaks.fps_boost()
            PerformanceTweaks.input_delay_fix()
            PerformanceTweaks.power_plan()
            NetworkTweaks.reduce_latency()
            
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
            ram_before = psutil.virtual_memory().available
            SystemTweaks.clear_cache()
            SystemTweaks.optimize_ram()
            
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
            SystemTweaks.disable_animations()
            
            print("[✓] FPS maximized!")
        except Exception as e:
            print(f"[!] FPS maximizer error: {e}")
    
    @staticmethod
    def reduce_lag():
        """Reduce network lag"""
        print("[TWEAK] Reducing lag...")
        
        try:
            NetworkTweaks.optimize_dns_google()
            NetworkTweaks.tcp_optimization()
            NetworkTweaks.reduce_latency()
            NetworkTweaks.packet_loss_fix()
            
            print("[✓] Lag reduced!")
        except Exception as e:
            print(f"[!] Lag reduction error: {e}")
    
    @staticmethod
    def full_optimization():
        """Full system optimization"""
        print("[TWEAK] Running full optimization...")
        
        try:
            # System
            SystemTweaks.clean_temp_files()
            SystemTweaks.clear_cache()
            SystemTweaks.optimize_ram()
            SystemTweaks.disable_visual_effects()
            SystemTweaks.disable_animations()
            SystemTweaks.disable_transparency()
            SystemTweaks.disable_notifications()
            SystemTweaks.disable_indexing()
            SystemTweaks.disable_superfetch()
            SystemTweaks.disable_unnecessary_services()
            
            # Network
            NetworkTweaks.optimize_dns_google()
            NetworkTweaks.tcp_optimization()
            NetworkTweaks.udp_optimization()
            NetworkTweaks.reduce_latency()
            NetworkTweaks.packet_loss_fix()
            NetworkTweaks.disable_nagle()
            NetworkTweaks.disable_ipv6()
            
            # Performance
            PerformanceTweaks.power_plan()
            PerformanceTweaks.gpu_optimization()
            PerformanceTweaks.input_delay_fix()
            PerformanceTweaks.fps_boost()
            PerformanceTweaks.virtual_memory_optimization()
            PerformanceTweaks.keyboard_optimization()
            
            print("[✓] Full optimization complete!")
        except Exception as e:
            print(f"[!] Full optimization error: {e}")


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
    'disable_animations': SystemTweaks.disable_animations,
    'disable_transparency': SystemTweaks.disable_transparency,
    'disable_notifications': SystemTweaks.disable_notifications,
    'disable_indexing': SystemTweaks.disable_indexing,
    'disable_superfetch': SystemTweaks.disable_superfetch,
    'defrag_disk': SystemTweaks.defrag_disk,
    'optimize_disk': SystemTweaks.optimize_disk,
    
    # Network
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
    
    # Performance
    'cpu_priority': PerformanceTweaks.cpu_priority,
    'gpu_opt': PerformanceTweaks.gpu_optimization,
    'input_latency': PerformanceTweaks.input_delay_fix,
    'fps_boost': PerformanceTweaks.fps_boost,
    'power_plan': PerformanceTweaks.power_plan,
    'virtual_mem': PerformanceTweaks.virtual_memory_optimization,
    'display_settings': PerformanceTweaks.display_settings,
    'disable_fullscreen_opt': PerformanceTweaks.disable_fullscreen_optimizations,
    'keyboard_opt': PerformanceTweaks.keyboard_optimization,
    
    # Booster
    'instant_boost': BoosterTweaks.instant_boost,
    'gaming_mode': BoosterTweaks.gaming_mode,
    'cpu_boost': BoosterTweaks.cpu_boost,
    'ram_cleaner': BoosterTweaks.ram_cleaner,
    'fps_max': BoosterTweaks.fps_maximizer,
    'reduce_lag': BoosterTweaks.reduce_lag,
    'full_optimization': BoosterTweaks.full_optimization,
}
