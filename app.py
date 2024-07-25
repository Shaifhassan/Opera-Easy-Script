import json
from src.create import create_tc_group, create_tc_subgroup, create_tc_code, create_categories
from src.export import export_tc_groups, export_tc_subgroups, export_tc_codes


# Load the JSON payload
with open("payload.json", 'r') as file:
    data = json.load(file)

# Extract data from JSON
RESORT = data["resort"]
GROUPS = {group["code"]:group for group in data["options"]["groups"]}
IDENTIFIERS = {identifier["no"]: identifier for identifier in data["options"]["identifiers"]}
CATEGORIES = {category["code"]: category for category in data["options"]["categories"]}
SEQUENCES = data["sequences"]

# collection for export process
TC_GROUPS = {}
TC_SUBGROUPS = {}
TC_CODES = []


# add values to TC_GROUPS for transaction code creation
for group in GROUPS.values():
    tc_group = create_tc_group(group)
    TC_GROUPS[tc_group["tc_group"]] = tc_group


# Process sequences to generate transaction groups and codes
for sequence in SEQUENCES:
    # Create the list of categories based on attached category codes to sequence
    categories = create_categories(CATEGORIES, sequence)

    # Loop through list of Identifiers attached to the sequence
    for identifier_no in sequence["identifiers"]:
        identifier = IDENTIFIERS[identifier_no]

        # Create list of generates for current sequence identifier
        generates = []

        # Iterate over each category which gives the transaction set
        for category in categories:
            # Create an associated subgroup for it 00AA format
            tc_subgroup = create_tc_subgroup(GROUPS, sequence, category)
            TC_SUBGROUPS[tc_subgroup["tc_subgroup"]] = tc_subgroup


            role = category["role"]

            if role == "multiply":
                tc_group = GROUPS.get(tc_subgroup["tc_group"], None)
                # Loop through list itemizers attached to the sequence
                for itemizer in sequence["itemizers"]:
                    tc_code = create_tc_code(sequence, tc_subgroup, tc_code, category, identifier, itemizer, itemizer["description"])
                    tc_code["generates"] = generates
                    TC_CODES.append(tc_code)
            elif role == "generate":
                tc_code = GROUPS.get(category["defaultGroup"], None)
                tc_code = create_tc_code(sequence, tc_subgroup, tc_code, category, identifier, None, category["description"])
                generate = category["tax"]
                generate["trx_code"] = tc_code["trx_code"]
                generate["tc_subgroup"] = tc_code["tc_subgroup"]
                generate["tc_group"] = tc_code["tc_group"]
                generates.append(generate)
                TC_CODES.append(tc_code)
            else:
                tc_code = GROUPS.get(category["defaultGroup"], None)
                tc_code = create_tc_code(sequence, tc_subgroup, tc_code, category, identifier, None, category["description"])
                TC_CODES.append(tc_code)
"""

# export groups
# export_tc_groups(RESORT, TC_GROUPS.values())

#export subgroups 
#export_tc_subgroups(RESORT, TC_SUBGROUPS.values())

#
export_tc_codes(RESORT, TC_CODES)

"""