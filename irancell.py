from pyrancell import Client
from time import sleep
from colorama import Fore, init
import traceback

init(autoreset=True)

DELAY = 0.5  # فاصله بین درخواست‌ها

try:
    TOKEN = input("Enter token: ").strip()
    bot = Client(token=TOKEN)

    # خواندن شماره‌ها از فایل
    with open("phones.txt", "r", encoding="utf-8") as f:
        phones = [line.strip() for line in f if line.strip().isdigit()]

    print(Fore.CYAN + f"\nLoaded {len(phones)} numbers from phones.txt")
    print("-" * 40)

    plus_numbers = []
    results_all = []

    for phone in phones:
        try:
            has_app = bot.phone_has_app(phone=phone)

            if has_app:
                print(Fore.YELLOW + f"{phone} -> -")
                results_all.append(f"{phone}\t-")
            else:
                invite = bot.send_invite(phone=phone)
                if invite.get("message") == "done":
                    print(Fore.GREEN + f"{phone} -> +")
                    plus_numbers.append(phone)
                    results_all.append(f"{phone}\t+")
                else:
                    print(Fore.RED + f"{phone} -> -")
                    results_all.append(f"{phone}\t-")

        except Exception:
            print(Fore.RED + f"{phone} -> - (ERROR)")
            results_all.append(f"{phone}\t-")

        sleep(DELAY)

    # خروجی‌ها
    with open("phones_plus.txt", "w", encoding="utf-8") as f:
        for p in plus_numbers:
            f.write(p + "\n")

    with open("phones_all.txt", "w", encoding="utf-8") as f:
        for line in results_all:
            f.write(line + "\n")

    print("\nFinished.")
    print("Saved: phones_plus.txt , phones_all.txt")

except Exception:
    print("\n🔥 FATAL ERROR 🔥")
    traceback.print_exc()

finally:
    input("\nPress Enter to exit...")
