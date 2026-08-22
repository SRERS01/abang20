import json
import base64

# =====================================================================
# SERVER-SIDE LOGIC (Vulnerable Architecture)
# =====================================================================
class PaymentServer:
    def __init__(self):
        # The true server state (balance sheet)
        self.database_balances = {
            "user_7656119865": 5000  # XAF
        }

    def process_received_json(self, serialized_payload):
        """Simulates receiving, deserializing, and executing the client payload"""
        try:
            # 1. Base64 Decode the incoming network stream
            raw_json_string = base64.b64decode(serialized_payload).decode('utf-8')
            
            # 2. Deserialization: Convert raw JSON string back into a Python dictionary
            transaction_object = json.loads(raw_json_string)
            
            print(f"[SERVER] Received Payload: {transaction_object}")

            # Extract properties directly from the deserialized input
            user_id = transaction_object.get("account_id")
            requested_payout = transaction_object.get("payout_amount")
            is_authorized = transaction_object.get("is_pre_authorized_by_bank") # CRITICAL BUG

            # 3. Faulty Logic Evaluation
            # The server trusts the serialized state property inside the JSON payload 
            # instead of verifying it against its own secure backend database session.
            if is_authorized is True:
                print(f"[SUCCESS] Payout of {requested_payout} XAF approved for {user_id} via override flag.")
                return {"status": "SUCCESS", "code": 200}
                
            # Fallback to standard balance check
            current_balance = self.database_balances.get(user_id, 0)
            if requested_payout <= current_balance:
                self.database_balances[user_id] -= requested_payout
                print(f"[SUCCESS] Standard Payout of {requested_payout} XAF processed.")
                return {"status": "SUCCESS", "code": 200}
            else:
                print("[REJECTED] Error: PAYOUT_MAX_LIMIT or Insufficient Funds.")
                return {"status": "FAILED", "code": 400}

        except Exception as e:
            print(f"[SERVER ERROR] Serialization failure: {str(e)}")
            return {"status": "ERROR", "code": 500}


# =====================================================================
# CLIENT-SIDE LOGIC (The Exploit Scenario)
# =====================================================================
if __name__ == "__main__":
    server = PaymentServer()

    print("--- 1. Legitimate Transaction Flow ---")
    # A normal client tries to request more than they have
    legitimate_data = {
        "account_id": "user_7656119865",
        "payout_amount": 500000,
        "is_pre_authorized_by_bank": False
    }
    # Serialize to JSON string, then encode to Base64 byte stream for transit
    serialized_legit = base64.b64encode(json.dumps(legitimate_data).encode('utf-8'))
    server.process_received_json(serialized_legit)


    print("\n--- 2. Exploiting Insecure Deserialization ---")
    # The client realizes the server evaluates parameters passed directly in the data stream.
    # By manipulating the serialized object property, the client bypasses the server's control logic.
    malicious_data = {
        "account_id": "user_7656119865",
        "payout_amount": 500000,
        "is_pre_authorized_by_bank": True  # Injected logic bug exploit
    }
    serialized_malicious = base64.b64encode(json.dumps(malicious_data).encode('utf-8'))
    server.process_received_json(serialized_malicious)
