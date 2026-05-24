import asyncio
import os
import sys
import time
import random
from datetime import datetime
from pystyle import Colors as _PY

def _get_theme():
    from core.display import Colorate, Theme, get_inpt
    return Colorate, Theme, get_inpt

def wallet_scanner_init():
    Colorate, Theme, get_inpt = _get_theme()
    try:
        import aiohttp
        from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator,
                                Bip44, Bip44Coins, Bip44Changes)
    except ImportError:
        import subprocess
        _cl = Theme.get_colors()
        print(Colorate.Horizontal(_cl["num"], "  [*] Installing required packages (aiohttp, bip-utils)..."))
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "aiohttp", "bip-utils", "-q"
        ])
        import aiohttp
        from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator,
                                Bip44, Bip44Coins, Bip44Changes)
    _run(aiohttp, Bip39MnemonicGenerator, Bip39SeedGenerator,
         Bip44, Bip44Coins, Bip44Changes,
         Colorate, Theme, get_inpt)
def _run(aiohttp, Bip39MnemonicGenerator, Bip39SeedGenerator,
         Bip44, Bip44Coins, Bip44Changes,
         Colorate, Theme, get_inpt):
    RED     = _PY.red
    GREEN   = _PY.green
    CYAN    = _PY.cyan
    YELLOW  = _PY.yellow
    MAGENTA = _PY.pink
    RESET   = _PY.reset
    stats        = {"generated": 0, "found": 0}
    script_start = time.time()
    semaphore  = asyncio.Semaphore(150)
    print_lock = asyncio.Lock()
    def set_title(title: str):
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f"\x1b]2;{title}\x07")
            sys.stdout.flush()
    def save_wallet(network, address, balance, mnemonic, priv_key):
        os.makedirs("found_wallets", exist_ok=True)
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"found_wallets/{network}_{ts}.txt"
        with open(filename, "w") as f:
            f.write(f"Network      : {network}\n")
            f.write(f"Address      : {address}\n")
            f.write(f"Balance      : {balance}\n\n")
            f.write(f"Mnemonic     : {mnemonic}\n")
            f.write(f"Private Key  : {priv_key}\n")
        return filename
    def generate_wallets(seed_bytes):
        def addr(coin):
            return (Bip44.FromSeed(seed_bytes, coin)
                    .Purpose().Coin().Account(0)
                    .Change(Bip44Changes.CHAIN_EXT)
                    .AddressIndex(0).PublicKey().ToAddress())
        return (
            addr(Bip44Coins.ETHEREUM),
            addr(Bip44Coins.BITCOIN),
            addr(Bip44Coins.LITECOIN),
            addr(Bip44Coins.TRON),
        )
    async def get_balance(session, address, network):
        timeout = aiohttp.ClientTimeout(total=10)
        if network == "btc":
            url = f"https://blockstream.info/api/address/{address}"
            async with semaphore:
                try:
                    async with session.get(url, timeout=timeout) as r:
                        if r.status == 200:
                            d      = await r.json()
                            chain  = d.get("chain_stats", {})
                            return str(chain.get("funded_txo_sum", 0) - chain.get("spent_txo_sum", 0))
                        if r.status == 429:
                            await asyncio.sleep(2)
                            return await get_balance(session, address, network)
                except Exception:
                    return "0"
            return "0"
        if network == "trx":
            url = f"https://api.trongrid.io/v1/accounts/{address}"
            async with semaphore:
                try:
                    async with session.get(url, timeout=timeout) as r:
                        if r.status == 200:
                            data = (await r.json()).get("data", [])
                            return str(data[0].get("balance", 0)) if data else "0"
                except Exception:
                    return "0"
            return "0"
        endpoints = {
            "eth": f"https://ethbook.guarda.co/api/v2/address/{address}",
            "bnb": f"https://bsc-nn.atomicwallet.io/api/v2/address/{address}",
            "ltc": f"https://litecoin.atomicwallet.io/api/v2/address/{address}",
        }
        async with semaphore:
            try:
                async with session.get(endpoints[network], timeout=timeout) as r:
                    if r.status == 200:
                        return str((await r.json()).get("balance", "0"))
                    if r.status == 429:
                        await asyncio.sleep(2)
                        return await get_balance(session, address, network)
            except Exception:
                return "0"
        return "0"
    async def worker(session, word_count):
        await asyncio.sleep(random.uniform(0.0, 2.0))
        while True:
            mnemonic_obj = Bip39MnemonicGenerator().FromWordsNumber(word_count)
            seed_bytes   = Bip39SeedGenerator(mnemonic_obj).Generate()
            eth_addr, btc_addr, ltc_addr, trx_addr = generate_wallets(seed_bytes)
            results = await asyncio.gather(
                get_balance(session, eth_addr, "eth"),
                get_balance(session, eth_addr, "bnb"),
                get_balance(session, btc_addr, "btc"),
                get_balance(session, ltc_addr, "ltc"),
                get_balance(session, trx_addr, "trx"),
                return_exceptions=True
            )
            stats["generated"] += 1
            def val(raw, dec):
                return 0.0 if isinstance(raw, Exception) else int(raw) / 10**dec
            e_val   = val(results[0], 18)
            b_val   = val(results[1], 18)
            btc_val = val(results[2], 8)
            ltc_val = val(results[3], 8)
            trx_val = val(results[4], 6)
            m_str = str(mnemonic_obj)
            found = any(v > 0 for v in [e_val, b_val, btc_val, ltc_val, trx_val])
            if found:
                stats["found"] += 1
                _cl = Theme.get_colors()
                fp  = ""
                if e_val   > 0: fp = save_wallet("ETH", eth_addr, e_val,   m_str, seed_bytes.hex())
                if b_val   > 0: fp = save_wallet("BNB", eth_addr, b_val,   m_str, seed_bytes.hex())
                if btc_val > 0: fp = save_wallet("BTC", btc_addr, btc_val, m_str, seed_bytes.hex())
                if ltc_val > 0: fp = save_wallet("LTC", ltc_addr, ltc_val, m_str, seed_bytes.hex())
                if trx_val > 0: fp = save_wallet("TRX", trx_addr, trx_val, m_str, seed_bytes.hex())
                async with print_lock:
                    print(Colorate.Horizontal(_cl["head"], f"\n  {'█'*68}"))
                    print(Colorate.Horizontal(_cl["head"], f"  [$$$]  WALLET WITH BALANCE FOUND  [$$$]"))
                    print(Colorate.Horizontal(_cl["sub"],  f"  {'─'*68}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  SEED    : ") + Colorate.Horizontal(_cl["txt"], m_str))
                    print(Colorate.Horizontal(_cl["num"],  f"  ETH/BNB : ") + Colorate.Horizontal(_cl["txt"], f"{eth_addr}  →  ETH:{e_val}  BNB:{b_val}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  BTC     : ") + Colorate.Horizontal(_cl["txt"], f"{btc_addr}  →  {btc_val}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  LTC     : ") + Colorate.Horizontal(_cl["txt"], f"{ltc_addr}  →  {ltc_val}"))
                    print(Colorate.Horizontal(_cl["num"],  f"  TRX     : ") + Colorate.Horizontal(_cl["txt"], f"{trx_addr}  →  {trx_val}"))
                    print(Colorate.Horizontal(_cl["inp"],  f"  Saved   : {fp}"))
                    print(Colorate.Horizontal(_cl["head"], f"  {'█'*68}\n"))
            seed_s = m_str[:12] + ".."
            e_s    = f"{eth_addr[:5]}..{eth_addr[-3:]}"
            btc_s  = f"{btc_addr[:5]}..{btc_addr[-3:]}"
            ltc_s  = f"{ltc_addr[:5]}..{ltc_addr[-3:]}"
            trx_s  = f"{trx_addr[:5]}..{trx_addr[-3:]}"
            bal = (
                f"{GREEN}E:{e_val} B:{b_val} BTC:{btc_val} LTC:{ltc_val} TRX:{trx_val}{RESET}"
                if found else "0"
            )
            line = (
                f"SEED:{MAGENTA}{seed_s:<14}{RESET}"
                f" | E/B:{CYAN}{e_s}{RESET}"
                f" BTC:{YELLOW}{btc_s}{RESET}"
                f" LTC:{CYAN}{ltc_s}{RESET}"
                f" TRX:{RED}{trx_s}{RESET}"
                f" | BAL:{bal}"
            )
            async with print_lock:
                print(line)
    async def title_loop():
        while True:
            elapsed = time.time() - script_start
            rps     = stats["generated"] / elapsed if elapsed > 0 else 0
            set_title(
                f"Scanned: {stats['generated']:,}  |  Hits: {stats['found']}  |  {rps:.1f} w/s"
            )
            await asyncio.sleep(1)
    async def _main(num_workers, word_count):
        _cl = Theme.get_colors()
        os.system("cls" if os.name == "nt" else "clear")
        print(Colorate.Horizontal(_cl["head"], f"  {'═'*50}"))
        print(Colorate.Horizontal(_cl["head"], f"  {'':^4}Crypto Wallet Scanner  v3.0"))
        print(Colorate.Horizontal(_cl["sub"],  f"  {'':^4}ETH  /  BNB  /  BTC  /  LTC  /  TRX"))
        print(Colorate.Horizontal(_cl["head"], f"  {'═'*50}\n"))
        print(
            Colorate.Horizontal(_cl["num"], "  Workers : ") +
            Colorate.Horizontal(_cl["txt"], str(num_workers)) +
            Colorate.Horizontal(_cl["num"], "   |   Seed Words : ") +
            Colorate.Horizontal(_cl["txt"], str(word_count)) + "\n"
        )
        connector = aiohttp.TCPConnector(limit=500, limit_per_host=100, ttl_dns_cache=300)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(worker(session, word_count)) for _ in range(num_workers)]
            tasks.append(asyncio.create_task(title_loop()))
            await asyncio.gather(*tasks)
    _cl = Theme.get_colors()
    os.system("cls" if os.name == "nt" else "clear")
    print(Colorate.Horizontal(_cl["head"], f"\n  ╔══════════════════════════════════════════╗"))
    print(Colorate.Horizontal(_cl["sub"],  f"  ║       ETH  BNB  BTC  LTC  TRX            ║"))
    print(Colorate.Horizontal(_cl["head"], f"  ╚══════════════════════════════════════════╝\n"))
    try:
        w = get_inpt("navi@walletbrute workers (default 50):").strip()
        num_workers = int(w) if w else 50
    except ValueError:
        num_workers = 50
    print()
    print(Colorate.Horizontal(_cl["head"], "  ┌─────────────────────────────────────────────────────────────┐"))
    print(Colorate.Horizontal(_cl["txt"],  "  │  Seed Word Count — what's the difference?                   │"))
    print(Colorate.Horizontal(_cl["sub"],  "  │                                                             │"))
    print(Colorate.Horizontal(_cl["num"],  "  │  12 words") + Colorate.Horizontal(_cl["txt"], "  →  2^128 combinations  (340 undecillion)        │"))
    print(Colorate.Horizontal(_cl["txt"],  "  │              Used by: MetaMask, TrustWallet, Coinbase       │"))
    print(Colorate.Horizontal(_cl["inp"],  "  │              Speed: faster to generate  ✓ recommended       │"))
    print(Colorate.Horizontal(_cl["sub"],  "  │                                                             │"))
    print(Colorate.Horizontal(_cl["num"],  "  │  24 words") + Colorate.Horizontal(_cl["txt"], "  →  2^256 combinations  (astronomically more)    │"))
    print(Colorate.Horizontal(_cl["txt"],  "  │              Used by: Ledger, Trezor (hardware wallets)     │"))
    print(Colorate.Horizontal(_cl["txt"],  "  │              Speed: slightly slower, fewer targets online   │"))
    print(Colorate.Horizontal(_cl["sub"],  "  │                                                             │"))
    print(Colorate.Horizontal(_cl["inp"],  "  │  → Use 12 for scanning. Most funded wallets use 12 words.  │"))
    print(Colorate.Horizontal(_cl["head"], "  └─────────────────────────────────────────────────────────────┘"))
    try:
        wc = get_inpt("navi@wallet-scanner word-count 12/24 (default 12):").strip()
        word_count = int(wc) if wc in ["12", "24"] else 12
    except ValueError:
        word_count = 12
    print()
    print(
        Colorate.Horizontal(_cl["num"], f"  [*] Starting ") +
        Colorate.Horizontal(_cl["txt"], str(num_workers)) +
        Colorate.Horizontal(_cl["num"], " workers with ") +
        Colorate.Horizontal(_cl["txt"], str(word_count)) +
        Colorate.Horizontal(_cl["num"], "-word seeds...\n")
    )
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(_main(num_workers, word_count))
    except KeyboardInterrupt:
        elapsed = time.time() - script_start
        rps     = stats["generated"] / elapsed if elapsed > 0 else 0
        mins, s = divmod(int(elapsed), 60)
        hrs, m  = divmod(mins, 60)
        _cl = Theme.get_colors()
        print()
        print(Colorate.Horizontal(_cl["head"], f"\n  {'─'*46}"))
        print(Colorate.Horizontal(_cl["head"], "    SCANNER STOPPED"))
        print(Colorate.Horizontal(_cl["head"], f"  {'─'*46}"))
        print(
            Colorate.Horizontal(_cl["num"], "  Total Scanned : ") +
            Colorate.Horizontal(_cl["txt"], f"{stats['generated']:,}")
        )
        print(
            Colorate.Horizontal(_cl["num"], "  Total Found   : ") +
            Colorate.Horizontal(_cl["txt"], str(stats["found"]))
        )
        print(
            Colorate.Horizontal(_cl["num"], "  Avg Speed     : ") +
            Colorate.Horizontal(_cl["txt"], f"{rps:.2f} wallets/sec")
        )
        print(
            Colorate.Horizontal(_cl["num"], "  Runtime       : ") +
            Colorate.Horizontal(_cl["txt"], f"{hrs:02d}h {m:02d}m {s:02d}s")
        )
        print(Colorate.Horizontal(_cl["head"], f"  {'─'*46}\n"))
        input(Colorate.Horizontal(_cl["inp"], "\n  Press Enter to return to menu..."))
