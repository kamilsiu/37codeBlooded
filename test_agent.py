from nlp_classifier.process_email import process_email

# Simulated email input
subject = "Need urgent help"
body = "Our entire locality in Dasarahalli hasn't had any water since yesterday evening."

# Call the AI agent
result = process_email(subject, body)

# Print the result
print("---- ANALYSIS RESULT ----")
print(f"Category      : {result['category']}")
print(f"Constituency  : {result['constituency']}")
print(f"Department    : {result['department']}")
print(f"Confidence    : {result['confidence']}")

from data_storage.store_complaint import store_complaint

store_complaint(subject, body, result)
