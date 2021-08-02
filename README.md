# e-voting
This is a simple implementation of an e-voting system that uses the Pallier homomorphic cryptosystem.

INSTRUCTIONS
1. Run 'create_voting_database.py' to create a local sql database to store credentials and votes.
2. Run 'paillier_e_voting.py' and login to the Admin portal using the username 'Admin' and the password 'Admin'.
3. Change the Admin password in the Admin portal.
4. Add voters to the database.
5. Each voter logs into the system and casts their vote.
6. Voters can ensure their vote is encrypted by clicking the 'Validate' button.
7. Admin logs into the system and tallies the encrypted votes.
