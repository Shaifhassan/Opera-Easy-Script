
def create_tc_group(group):
    options = group.get("options", {})

    #default Value
    group = {
        "tc_group":group["code"],
        "description":group["description"],
        "order_by": group["seq"],
        "tc_transaction_type":"C",
    }

    #update model with options
    group.update(options)
    return group


# Function to create a transaction subgroup
def create_tc_subgroup(tc_groups, sequence, category):
    # Load the group based on the group defined in category or sequence
    group_code = category.get("defaultGroup", sequence.get("group"))
    group = tc_groups.get(group_code, {})

    # Get the first digit of the sequence number defined in the category
    sequence_num = int(str(category["seq"])[:1])

    # Get Options from Category
    options = category.get("options", {})

    # Define subgroup template
    subgroup = {
        "tc_subgroup":None,
        "description":None,
        "tc_group":None,
        "tc_transaction_type":None,
        "order_by":None
        }
    
    # Apply Group options
    subgroup.update(group)

    # Apply Category options
    subgroup.update(options)

    # Update the subgroup with new values
    subgroup.update({
        "tc_subgroup": f"{sequence['sequence']}{category['code']}",
        "description": f"{sequence['name']} {category['description']}",
        "order_by": int(f"{sequence['sequence']}{sequence_num}")
    })

    return subgroup


# Function to generate transaction code
def create_tc_code(sequence, tc_subgroup, group_code, category, identifier, itemizer, description):
    # get transaction code option based on itemizer definitions
    if itemizer:
        item_code = itemizer.get("itemizer", 0) + category["seq"]
        options = itemizer.get("options", {})
    else:
        item_code = category["seq"]
        options = {}

    # variables
    trx_code_no = f'{item_code:02}'
    trx_description = f"{sequence['name'] if sequence['prefix'] else ''}{f' {identifier['name']}' if identifier['name'] else ''}{f' {description}' if description else ''}{f' {category['abbr']}' if category['abbr'] else ''}"

    #transaction code default template 
    trx_code = {
        "trx_code":None,
        "description":None,
        "tc_subgroup":None,
        "tc_group":None,
        "tc_transaction_type":None,
        "trx_code_type":None,
        "tax_code_no":None,
        "tax_inclusive_yn":None,
        "result_included_in_sum_array":None,
        "cc_type":None,
        "cc_code":None,
        "ind_cash":None,
        "is_manual_post_allowed":None,
        "ind_billing":None,
        "ind_ar": None,
        "ind_revenue_gp":None,
        "ind_deposit_yn":None,
        "inh_deposit_yn":None,
        "include_in_deposit_rule_yn":None,
        "adj_trx_code":None
    }

    # apply changes from subgroup
    trx_code.update(tc_subgroup)

    # Merge options into trx_code dictionary
    trx_code.update(options)

    trx_code.update({
        "trx_code": f'{sequence["sequence"]}{identifier["seq"]}{trx_code_no}',
        "description": trx_description.strip(),
        "generates": None
    })

    return trx_code


# Function to generate the list of categories
def create_categories(categories, sequence):
    _categories = []
    for cat in sequence["categories"]:
        category = categories[cat["code"]]
        category["role"] = cat["role"]
        _categories.append(category)
    return _categories