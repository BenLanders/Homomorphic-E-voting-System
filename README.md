# e-voting
This is a simple implementation of an e-voting system. The purpose of the program is to demonstrate the homomorphic properties of the Pallier cryptosystem. Each vote is encrypted in the local database and tallied in its encrypted form. The result is decrypted after the votes have been tallied, thus preserving the privacy of each voter. 

INSTRUCTIONS
1. Run 'create_voting_database.py' to create a local sql database to store credentials and votes.
2. Run 'paillier_e_voting.py' and login to the Admin portal using the username 'Admin' and the password 'Admin'.
3. Change the Admin password in the Admin portal.
4. Add voters to the database.
5. Each voter logs into the system and casts their vote.
6. Voters can ensure their vote is encrypted by clicking the 'Validate' button.
7. Admin logs into the system and tallies the encrypted votes.
