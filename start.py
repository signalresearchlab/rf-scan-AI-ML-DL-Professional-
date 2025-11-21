#!/usr/bin/env python3
# start.py - Fixed main entry point
import sys

def main():
    print("🚀 Advanced RF Scanning System")
    print("=" * 40)
    
    print("1. Real-time Spectrum Monitoring")
    print("2. Frequency Analysis") 
    print("3. ML Signal Classification")
    print("4. CNN Modulation Recognition")
    print("5. Full System Scan")
    
    try:
        choice = input("\nSelect mode (1-5): ").strip()
        
        if choice == "1":
            from monitor import main
            main()
        elif choice == "2":
            from spectrum import main  
            main()
        elif choice == "3":
            from ml import main
            main()
        elif choice == "4":
            from cnn import main
            main()
        elif choice == "5":
            print("Starting full system scan...")
            from monitor import main as monitor_main
            monitor_main()
        else:
            print("Invalid choice. Starting default monitoring...")
            from monitor import main
            main()
            
    except KeyboardInterrupt:
        print("\n👋 Exiting RF Scanner")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
