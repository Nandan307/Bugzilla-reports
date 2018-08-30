# Bugzilla-reports

It includes Command Line Interface (CLI) tool that queries the Bugzilla API for bugs allocated to the 
given team, and further sorts them according to the individual employee bugs, stale bugs, blockers etc.; 
automated email reports; Web Application Interface with customized bug reports; and Third Party API 
named "Orgchart" (discontinued using Orgchart and implemented Team.py which retains the previous features 
while adding a few new ones) that is used for the positional hierarchy.


Getting started:

1. $ cd Bugzilla-reports

   $ ./bzreports update-team
   
 
2. Change the config settings in `app_dir/reports/config.py`
   
   Note: `manager_name` is the name of the manager who is on top of the hierarchy
   
   
   For example:     
   
                       A (manager_name)
                    /  |  \
                    B  C   D           <== direct reports
                   / \
                   E  F                <== indirect reports
                    

3. In `bzreports`, edit the arguments in `def update_team()` as per your convinience.
   Once done, add the sender's and recipients' email on line 99 and 100 respectively.
   
