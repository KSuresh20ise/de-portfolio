# Functions
#==============
# Add Policy
# View All Policies
# Search Policy

# =======================
# DATABASE (Dictionary)
# =======================

from datetime import datetime


policies = {}
claims = {}

# ======================
# POLICY FUNCTIONS
# ======================

def add_policy():
    print("\n--- ADD NEW POLICY ---")
    pol_id = input("Policy ID: ")
    if pol_id in policies:
        print("Policy already exists!")
        return
    holder = input("Holder Name: ")
    ptype = input("Type (Health/Auto/Propery/Cyber): ")
    premium = float(input("Premium Amount: "))
    status = input("Status (Active/Inactive): ")
    state = input("State: ")

    policies[pol_id] = {
        "holder": holder,
        "type": ptype,
        "premium": premium,
        "status": status,
        "state": state,
        "created": datetime.now().strftime("%Y-%m-%d")
    }

def view_all_policies():
    print("\n--- ALL POLICIES ---")
    if not policies:
        print(" No Policies Found!")
        return
    for i, (pol_id, det) in enumerate(policies.items(),1):
        print(f"\n{i}. {pol_id}")
        for key, val in det.items():
            print(f"  {key:10}: {val}")

def search_policy():
    print("\n--- SEARCH POLICY ---")
    pol_id = input("Enter Policy ID: ")
    if pol_id in policies:
        print(f"\n Policy: {pol_id}")
        for key, val in policies[pol_id].items():
            print(f"  {key:10}: {val}")
    else:
        print(" Policy Not Found!")

def update_premium():
    print("\n--- UPDATE PREMIUM ---")
    pol_id = input("Enter Policy ID: ")
    if pol_id not in policies:
        print("Policy Not Found!")
        return
    old = policies[pol_id]["premium"]
    new = float(input(f"curent: ₹{old} -> New Premium: "))
    policies[pol_id]["premium"] = new
    print(f" Premium Updated: ₹{old} -> ${new}")

def delete_policy():
     print("\n--- DELETE POLICY ---")
     pol_id = input("Enter Policy ID: ")
     if pol_id not in policies:
        print("Policy Not Found!")
        return
     confirm = input(f"Delete {pol_id}? (yes/no): ")
     if confirm.lower() == "yes":
         policies.pop(pol_id)
         print(f"Policy {pol_id} deleted!")
     else:
         print("Cancelled!")

def filter_policies():
    print("\n--- FILTER POLICIES ---")
    print("1 By Status")
    print("2. By Type")
    print("3. By State")
    choice = input("Choose: ")
    if choice == "1":
        status = input("Status (Active/Inactive/Renewed): ")
        filtered = {
            k:v for k,v in policies.items()
            if v["status"] == status
        }
    elif choice == "2":
        ptype = input("Type (Health/Auto/Cyber): ")
        filtered = {
            k:v for k,v in policies.items()
            if v["type"] == ptype
        }
    elif choice == "3":
        state = input("State: ")
        filtered = {
            k:v for k,v in policies.items()
            if v["state"] == state
        }
    else:
        print("Invalid")
        return
    if not filtered:
        print("No Policies Found!")
        return
    print(f"\nFound {len(filtered)} Policies")
    for pol_id, det in filtered.items():
        print(f" {pol_id}: {det['holder']}"
              f"-> ₹{det['premium']}"
              f"({det['status']})"
              )

# ========================
# CLAIMS FUNCTIONS
# ========================

def add_claims():
    print("\n--- ADD CLAIM ---")
    claim_id = input("Enter Claim ID: ")
    pol_id = input("Enter Policy ID: ")

    if pol_id not in policies:
        print("Policy not found!")
        return
    amount = float(input("Claim Amount: "))
    status = input("Status (Pending/Approved/Rejected): ")
    claims[claim_id] = {
        "policy_id": pol_id,
        "holder": policies[pol_id]["holder"],
        "claim_amount": amount,
        "status": status,
        "claim_date": datetime.now.strftime("%Y-%m-%d")
    }
    print(f"Claim {claim_id} added!")

def view_all_claims():
    print("\n--- ALL CLAIMS ---")
    if not claims:
        print("No Claims Found")
        return
    for i, (claim_id,det) in enumerate(claims.items(),1):
        print(f"\n{i}. {claim_id}")
        for key, val in det.items():
            print(f"  {key:15}: {val}")

def load_sample_data():
    global policies, claims
    policies = {
        "POL001": {"holder": "Suresh Kumar",
                   "type": "Health", "premium": 4500,
                   "status": "Active",
                   "state": "Karnataka",
                   "created": "2024-01-15"},
        "POL002": {"holder": "Raj Patel",
                   "type": "Auto", "premium": 2300,
                   "status": "Inactive",
                   "state": "Maharashtra",
                   "created": "2024-02-20"},
        "POL003": {"holder": "Priya Singh",
                   "type": "Cyber", "premium": 5600,
                   "status": "Active",
                   "state": "Tamil Nadu",
                   "created": "2024-03-10"},
        "POL004": {"holder": "Ankit Shah",
                   "type": "Health", "premium": 1800,
                   "status": "Active",
                   "state": "Gujarat",
                   "created": "2024-04-05"},
        "POL005": {"holder": "Sneha Reddy",
                   "type": "Auto", "premium": 3200,
                   "status": "Renewed",
                   "state": "Telangana",
                   "created": "2024-05-12"}
    }
    claims = {
        "CLM001": {"policy_id": "POL001",
                   "holder": "Suresh Kumar",
                   "claim_amount": 15000,
                   "status": "Approved",
                   "claim_date": "2024-03-10"},
        "CLM002": {"policy_id": "POL002",
                   "holder": "Raj Patel",
                   "claim_amount": 8500,
                   "status": "Pending",
                   "claim_date": "2024-04-15"},
        "CLM003": {"policy_id": "POL003",
                   "holder": "Priya Singh",
                   "claim_amount": 22000,
                   "status": "Rejected",
                   "claim_date": "2024-05-20"}
    }
    print("✅ Sample data loaded!")

# ===========================
# MAIN MENU
#============================

def main():
    load_sample_data()
    print("\n WELCOME TO INSURANCE MANAGER")

    while True:
        print("\n" + "="*40)
        print("         MAIN MENU")
        print("="*40)
        print("POLICIES:")
        print("  1. Add Policy")
        print("  2. View All Policies")
        print("  3. Search Policy")
        print("  4. Update Premium")
        print("  5. Delete Policy")
        print("  6. Filter Policies")
        print("\nCLAIMS:")
        print("  7. Add Claim")
        print("  8. View All Claims")
        print("  0. Exit")
        print("="*40)

        choice = input("\n Enter Choice: ")
        if choice == "1":   add_policy()
        elif choice == "2": view_all_policies()
        elif choice == "3": search_policy()
        elif choice == "4": update_premium()
        elif choice == "5": delete_policy()
        elif choice == "6": filter_policies()
        elif choice == "7": add_claims()
        elif choice == "8": view_all_claims()
        else:
            print("Invalid choice!")
if __name__ == "__main__":
    main()