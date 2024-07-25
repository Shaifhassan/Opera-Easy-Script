import json
from src.create import create_tc_group, create_tc_subgroup, create_tc_code, create_categories, create_tc_generate
from src.export import export_to_sql, export_to_json_file


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
TC_CODES = {}


# add values to TC_GROUPS for transaction code creation
for group in GROUPS.values():
    grp = create_tc_group(group)
    TC_GROUPS[grp["tc_group"]] = grp


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
                    # Create a transaction code
                    tc_code = create_tc_code(sequence, tc_subgroup, tc_group, category, identifier, itemizer, itemizer["description"])

                    # Assign generates with updated generator fields
                    tc_code["generates"] = [{**gen, 
                            "tc_group_generator": tc_code["tc_group"], 
                            "tc_subgroup_generator": tc_code["tc_subgroup"], 
                            "trx_code_generator": tc_code["trx_code"]
                            } for gen in generates ]

                    # Add the transaction code to the TC_CODES dictionary
                    TC_CODES[tc_code["trx_code"]] = tc_code
            elif role == "generate":
                tc_group = GROUPS.get(category["defaultGroup"], None)
                tc_code = create_tc_code(sequence, tc_subgroup, tc_group, category, identifier, None, category["description"])
                generate = create_tc_generate(tc_group, category, tc_code)  
                generates.append(generate)
                TC_CODES[tc_code["trx_code"]]=tc_code
            else:
                tc_group = GROUPS.get(category["defaultGroup"], None)
                tc_code = create_tc_code(sequence, tc_subgroup, tc_group, category, identifier, None, category["description"])
                TC_CODES[tc_code["trx_code"]]=tc_code



# Usage example
# file_path = "trx_import.sql"
# export_to_sql(file_path, RESORT, TC_GROUPS.values(), TC_SUBGROUPS.values(), TC_CODES.values())


# Export transaction code groups
# export_to_json_file(TC_GROUPS, 'tc_groups.json')

# Export transaction code subgroups
# export_to_json_file(TC_SUBGROUPS, 'tc_subgroups.json')

# Export transaction codes
export_to_json_file(TC_CODES, 'tc_codes.json')