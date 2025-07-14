import pandas as pd
import numpy as np
import datetime
import uuid
import random

# --- 1. Generate customer_policy_data.csv ---
print("Generating customer_policy_data.csv...")
customer_data = []
# Define location probabilities and zip ranges
ny_zips = {
    'buffalo': (14201, 14228),
    'nyc': (10001, 10469),
    'other': (12007, 13905)  # Albany to Binghamton
}
other_states = ['PA', 'OH', 'CT']

# Sequential ID sequences
policy_id_seq = 10000001
customer_id_seq = 1

for i in range(1000):
    # Location Logic
    state_choice = np.random.choice(['NY', 'Other'], p=[0.6, 0.4])
    if state_choice == 'NY':
        state = 'NY'
        ny_area = np.random.choice(['buffalo', 'nyc', 'other'], p=[0.4, 0.4, 0.2])
        zip_code = np.random.randint(ny_zips[ny_area][0], ny_zips[ny_area][1] + 1)
    else:
        state = np.random.choice(other_states)
        zip_code = np.random.randint(15001, 19640)  # PA zip range example

    # Age Distribution
    age = int(np.random.normal(loc=45, scale=12))
    age = max(18, min(85, age))  # Clamp age between 18 and 85

    vehicle_year = np.random.randint(2015, 2026)
    start_date = datetime.date(2024, 1, 1) + datetime.timedelta(days=np.random.randint(0, 365))
    end_date = start_date + datetime.timedelta(days=365)

    # Premium Correlation Logic
    base_premium = random.uniform(75.50, 250.00)
    if age < 25:
        base_premium *= random.uniform(1.4, 1.6)
    if vehicle_year >= 2024:
        base_premium *= random.uniform(1.1, 1.2)
    if 10001 <= zip_code <= 10469:  # NYC zips
        base_premium *= random.uniform(1.3, 1.5)
    monthly_premium_usd = round(base_premium, 2)

    customer_data.append({
        'policy_id': policy_id_seq + i,
        'customer_id': f"CUST-{customer_id_seq + i:06d}",
        'state': state,
        'zip_code': zip_code,
        'age': age,
        'vehicle_year': vehicle_year,
        'policy_start_date': start_date,
        'policy_end_date': end_date,
        'monthly_premium_usd': monthly_premium_usd,
        'has_telematics_subscription': np.random.choice([True, False], p=[0.7, 0.3])
    })

df_customer = pd.DataFrame(customer_data)
df_customer.to_csv('customer_policy_data.csv', index=False)
print("customer_policy_data.csv generated successfully.")

# --- 2. Generate telematics_driving_data.csv ---
print("Generating telematics_driving_data.csv...")
telematics_subscribers = df_customer[df_customer['has_telematics_subscription'] == True]
# Identify 20% as risky drivers
risky_driver_policies = telematics_subscribers.sample(frac=0.2)['policy_id'].tolist()

telematics_data = []
for _ in range(1000):
    policy_row = telematics_subscribers.sample(n=1).iloc[0]
    policy_id = policy_row['policy_id']

    # Generate events based on risk profile
    if policy_id in risky_driver_policies:
        hard_braking_events = np.random.randint(3, 9)
        rapid_acceleration_events = np.random.randint(3, 9)
    else:
        hard_braking_events = np.random.randint(0, 3)
        rapid_acceleration_events = np.random.randint(0, 3)

    # Ensure trip_date is within policy dates
    policy_start = policy_row['policy_start_date']
    policy_end = policy_row['policy_end_date']
    trip_date = policy_start + datetime.timedelta(days=np.random.randint(0, 365))

    telematics_data.append({
        'trip_id': str(uuid.uuid4()),
        'policy_id': policy_id,
        'trip_date': trip_date,
        'distance_miles': round(random.uniform(1.0, 100.0), 1),
        'hard_braking_events': hard_braking_events,
        'rapid_acceleration_events': rapid_acceleration_events
    })

df_telematics = pd.DataFrame(telematics_data)
df_telematics.to_csv('telematics_driving_data.csv', index=False)
print("telematics_driving_data.csv generated successfully.")

# --- 3. Generate claims_data.csv ---
print("Generating claims_data.csv...")
# Create weighted probabilities for claims
weights = [4 if pid in risky_driver_policies else 1 for pid in df_customer['policy_id']]
probabilities = np.array(weights) / sum(weights)

claims_data = []
claim_id_seq = 1
for i in range(1000):
    # Select policy based on risk
    selected_policy_id = np.random.choice(df_customer['policy_id'], p=probabilities)
    policy_row = df_customer[df_customer['policy_id'] == selected_policy_id].iloc[0]

    incident_date = policy_row['policy_start_date'] + datetime.timedelta(days=np.random.randint(0, 365))
    claim_filed_date = incident_date + datetime.timedelta(days=np.random.randint(1, 15))
    claim_type = np.random.choice(['Collision', 'Comprehensive'])

    # Correlate cost with claim type
    if claim_type == 'Collision':
        total_claim_amount_usd = round(random.uniform(4000.00, 8000.00), 2)
    else:
        total_claim_amount_usd = round(random.uniform(1000.00, 2500.00), 2)

    claims_data.append({
        'claim_id': f"CLM-{claim_id_seq + i:07d}",
        'policy_id': selected_policy_id,
        'incident_date': incident_date,
        'claim_filed_date': claim_filed_date,
        'claim_type': claim_type,
        'claim_status': np.random.choice(['Approved', 'Pending', 'Denied'], p=[0.85, 0.10, 0.05]),
        'total_claim_amount_usd': total_claim_amount_usd
    })

df_claims = pd.DataFrame(claims_data)
df_claims.to_csv('claims_data.csv', index=False)
print("claims_data.csv generated successfully.")

# --- 4. Generate identity_protection_data.csv ---
print("Generating identity_protection_data.csv...")
# Select 300 subscribers
subscriber_ids = df_customer['customer_id'].sample(n=300, replace=False).tolist()
subscriber_map = {
    cid: datetime.date(2024, 1, 1) + datetime.timedelta(days=np.random.randint(0, 365))
    for cid in subscriber_ids
}

identity_data = []
account_id_seq = 800000000001
for i in range(1000):
    customer_id = random.choice(subscriber_ids)
    signup_date = subscriber_map[customer_id]

    # Ensure alert date is after signup date
    # Using a fixed date for 'today' to ensure reproducibility
    today_for_reproducibility = datetime.date(2025, 7, 13)
    days_after_signup = (today_for_reproducibility - signup_date).days
    alert_date = signup_date + datetime.timedelta(days=np.random.randint(1, max(2, days_after_signup)))

    identity_data.append({
        'account_id': account_id_seq + i,
        'alert_id': str(uuid.uuid4()),
        'customer_id': customer_id,
        'signup_date': signup_date,
        'alert_date': alert_date,
        'alert_type': np.random.choice(
            ['Dark Web Monitoring', 'Credit Inquiry', 'Data Breach', 'Social Media Account Takeover'],
            p=[0.60, 0.20, 0.15, 0.05]
        ),
        'alert_status': np.random.choice(['Resolved', 'Acknowledged', 'Pending'])
    })

df_identity = pd.DataFrame(identity_data)
df_identity.to_csv('identity_protection_data.csv', index=False)
print("identity_protection_data.csv generated successfully.")

print("\nAll files can be found in the directory where you run this script.")