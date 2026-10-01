def simulate_momo_p2p_trade(trade_amount, action_sequence):
    # Initial Balances
    buyer_momo = trade_amount
    buyer_crypto = 0
    seller_momo = 0
    seller_crypto = trade_amount
    escrow_crypto = 0
    seller_cash_in_hand = 0
    
    print(f"--- STARTING P2P TRADE ({trade_amount} Value) ---")
    
    # 1. Seller opens trade, crypto goes to escrow holding
    seller_crypto -= trade_amount
    escrow_crypto += trade_amount
    print(f"[P2P Engine] Seller locks {trade_amount} USDT into Escrow.")
    
    # 2. Buyer transfers MoMo XAF
    buyer_momo -= trade_amount
    seller_momo += trade_amount
    print(f"[MTN Network] Buyer transfers {trade_amount} XAF to Seller's MoMo number.")
    
    if action_sequence == "scammer_wins":
        # 3. Platform forces release or Seller prematurely releases
        escrow_crypto -= trade_amount
        buyer_crypto += trade_amount
        print("[P2P Engine] Crypto is released from Escrow to Buyer.")
        
        # 4. Scammer calls MTN and triggers reversal before seller moves money
        seller_momo -= trade_amount
        buyer_momo += trade_amount
        print("[CRITICAL SCAM] Buyer calls MTN support for a 'Wrong Number Reversal'.")
        print(f"RESULT -> Seller Final Balance: {seller_momo} XAF | {seller_crypto} USDT. (TOTAL LOSS)")
        
    elif action_sequence == "seller_protected":
        # 3. Seller instantly pulls cash out of the mobile money system
        seller_cash_in_hand += trade_amount
        seller_momo -= trade_amount
        print("[DEFENSE] Seller instantly cash-out at kiosk or moves funds to a 2nd phone network.")
        
        # 4. Seller safely releases crypto
        escrow_crypto -= trade_amount
        buyer_crypto += trade_amount
        print("[P2P Engine] Seller safely clicks 'Release Crypto' to Buyer.")
        
        # 5. Scammer tries to reverse from empty wallet
        print("[CRITICAL SCAM FAILED] Buyer calls MTN to reverse. MTN system rejects it because balance is 0!")
        print(f"RESULT -> Seller Final Balance: {seller_cash_in_hand} XAF Cash in hand. (SAFE)")

# --- EXECUTE THE SIMULATIONS ---
print("\n=== SCENARIO A: Leaving money in your wallet ===")
simulate_momo_p2p_trade(5000, "scammer_wins")

print("\n=== SCENARIO B: Defending with immediate withdrawal ===")
simulate_momo_p2p_trade(5000, "seller_protected")
```

### The Code Output Explanation:
* *Scenario A (The Scam Works):* Because the seller_momo balance was still holding the money, MTN's system is legally and technically capable of pulling the funds back out of your account balance during a "Wrong Number Transfer" claim. The scammer walks away with both the crypto and their original cash.
* *Scenario B (The Shield):* By running the function that transfers seller_momo into seller_cash_in_hand before the crypto release event, you break the MTN system’s capability. MTN customer support agents *cannot reverse money that is no longer inside the mobile wallet balance*. 

<FollowUp>
Would you like help writing a small *Python script* to calculate and track your local P2P *trading profits and network cash-out fees* automatically? Let me know *which local currencies* or platforms you want to include!
</FollowUp>
