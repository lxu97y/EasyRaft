# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###


## TEST
Due to the unexpected operating system scheduler behavior, the expected scenario that the test script simutlates cannot always be reached. 

Our test is originally based on the specific state of some nodes. To gurantee the expected output to be observed, please check the state of each node when running test script. The following specification clarify the role each node would be. If the node fail to be the expected state, please retry the test.

test_election_one_candidate.py: None
test_election_three_candidate.py: None
test_election_two_candidate.py: None
test_election_when_leader_die.py: node 1 must be leader
test_election_old_log.py: node 1 becomes candidate

test_log_replication_append_request_from_leader.py: node 1 must be the leader
test_log_replication_remove_conflict_log.py: node 5 must not be leader
test_log_replication_leader_update_commitedIndex.py: node 1 must be leader
