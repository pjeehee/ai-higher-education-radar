import csv, sqlite3, os, sys
# Candidate CSV columns should follow radar_verified_evidence.csv. This importer intentionally requires verification_status=verified.
print("Use the verified-candidate workflow before importing; production writes should preserve provenance and review gates.")
