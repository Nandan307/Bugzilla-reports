#!/usr/bin/python3
"""
Networking Services team BZ queries
"""


# Returns bugs allocated to the NST
def bz_fetch_bugs(bz, team_obj, product_name=None):
    """
    Fetches all bugs assigned to our team, in all projects.
    Returns the bz query result itself.
    """
    team_list = team_obj.all_emails()
    query = bz.build_query(
                           product=product_name,
                           assigned_to=team_list,
                           emailtype='anywords')

    bugs = bz.bz.query(query)
    return bugs
