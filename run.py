"""
Cyberbullying Detection System - Launcher
Choose between Terminal mode or Web mode
"""

import os
import sys
import subprocess

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🛡️  CYBERBULLYING DETECTION SYSTEM 🛡️                 ║
    ║                                                               ║
    ║              AI-Powered Text & Image Analysis                 ║
    ║                    90.88% Accuracy                            ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_menu():
    """Print main menu"""
    menu = """
    ┌───────────────────────────────────────────────────────────────┐
    │                      SELECT MODE                              │
    ├───────────────────────────────────────────────────────────────┤
    │                                                               │
    │  1. 💻 Terminal Mode (CLI)                                    │
    │     - Interactive command-line interface                      │
    │     - Quick text detection                                    │
    │     - Image detection from file path                          │
    │     - Dataset testing                                         │
    │                                                               │
    │  2. 🌐 Website Mode (Web Interface)                           │
    │     - Beautiful web interface                                 │
    │     - User authentication                                     │
    │     - Admin dashboard                                         │
    │     - Full-featured detection system                          │
    │                                                               │
    │  3. ❌ Exit                                                    │
    │                                                               │
    └───────────────────────────────────────────────────────────────┘
    """
    print(menu)

def run_terminal_mode():
    """Run the terminal/CLI version"""
    clear_screen()
    print("\n🚀 Starting Terminal Mode...\n")
    print("="*70)
    
    try:
        # Run main.py
        subprocess.run([sys.executable, 'main.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n✋ Terminal mode stopped by user")
    except FileNotFoundError:
        print("\n❌ Error: main.py not found!")
        print("Make sure you're in the project directory.")
    except Exception as e:
        print(f"\n❌ Error running terminal mode: {e}")
    
    input("\nPress Enter to return to menu...")

def run_website_mode():
    """Run the web/Flask version"""
    clear_screen()
    print("\n🚀 Starting Website Mode...\n")
    print("="*70)
    print("Starting Flask Web Server...")
    print("="*70)
    print("\n📍 Access the website at:")
    print("   → http://127.0.0.1:5000")
    print("   → http://localhost:5000")
    print("\n👤 User Login: http://127.0.0.1:5000/login")
    print("🔐 Admin Login: http://127.0.0.1:5000/admin/login")
    print("\n⚠️  Press Ctrl+C to stop the server and return to menu")
    print("="*70)
    print()
    
    try:
        # Run app.py
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n\n✋ Web server stopped by user")
    except FileNotFoundError:
        print("\n❌ Error: app.py not found!")
        print("Make sure you're in the project directory.")
    except Exception as e:
        print(f"\n❌ Error running website mode: {e}")
    
    input("\nPress Enter to return to menu...")

def main():
    """Main launcher function"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input("    Enter your choice (1-3): ").strip()
            
            if choice == '1':
                run_terminal_mode()
            elif choice == '2':
                run_website_mode()
            elif choice == '3':
                clear_screen()
                print("\n👋 Thank you for using Cyberbullying Detection System!")
                print("   Stay safe online! 🛡️\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            clear_screen()
            print("\n\n👋 Goodbye! Stay safe online! 🛡️\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
