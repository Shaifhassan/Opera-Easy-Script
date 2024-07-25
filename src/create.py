def create_tc_group(group):
    """
    Creates a transaction group model from the given group data.
    
    Args:
        group (dict): The group data containing options and basic information.
        
    Returns:
        dict: A dictionary representing the transaction group with merged options.
    """
    # Define allowed options for the group
    tc_option_template = {
        "tc_transaction_type": None
    }

    # Get options defined for the group model and merge valid options
    patch_options(tc_option_template, group.get("options", {}))

    # Initialize the group model with basic information and merged options
    tc_group = {
        "tc_group": group.get("code", "UNKNOWN"),
        "description": group.get("description", ""),
        "order_by": group.get("seq", 0),
    }

    tc_group.update(tc_option_template)
    return tc_group


def create_tc_subgroup(groups, sequence, category):
    """
    Creates a transaction subgroup model from the given sequence and category data.
    
    Args:
        groups (dict): The dictionary of existing groups.
        sequence (dict): The sequence data containing group and other attributes.
        category (dict): The category data containing default group and other attributes.
        
    Returns:
        dict: A dictionary representing the transaction subgroup with merged options.
    """
    group_code = category.get("defaultGroup", sequence.get("group"))
    group = groups.get(group_code, {})

    # Error handling if necessary keys are missing
    if not group:
        raise ValueError(f"Group code '{group_code}' not found in groups")

    sequence_num = int(str(category.get("seq", "0"))[:1])

    # Define allowed options for the subgroup
    tc_option_template = {
        "tc_transaction_type": None
    }

    # Merge valid options from the group
    patch_options(tc_option_template, group.get("options", {}))


    # Initialize the subgroup model with basic information and merged options
    tc_subgroup = {
        "tc_group": group.get('code', 'UNKNOWN'),
        "tc_subgroup": f"{sequence.get('sequence', '00')}{category.get('code', 'XX')}",
        "description": f"{sequence.get('name', '')} {category.get('description', '')}",
        "order_by": int(f"{sequence.get('sequence', '00')}{sequence_num}")
    }

    tc_subgroup.update(tc_option_template)
    return tc_subgroup


def create_tc_code(sequence, tc_subgroup, group, category, identifier, itemizer, description):
    """
    Creates a transaction code model from the given data.
    
    Args:
        sequence (dict): The sequence data containing necessary attributes.
        tc_subgroup (dict): The transaction subgroup data.
        group (dict): The group data.
        category (dict): The category data containing options.
        identifier (dict): The identifier data.
        itemizer (dict): The itemizer data containing options.
        description (str): The description for the transaction code.
        
    Returns:
        dict: A dictionary representing the transaction code with merged options.
    """
    # Define allowed options for the transaction code
    tc_option_template = {
        "trx_code_type": None,
        "tax_code_no": None,
        "tax_inclusive_yn": None,
        "result_included_in_sum_array": None,
        "cc_type": None,
        "cc_code": None,
        "ind_cash": None,
        "is_manual_post_allowed": None,
        "ind_billing": None,
        "ind_ar": None,
        "ind_revenue_gp": None,
        "ind_deposit_yn": None,
        "inh_deposit_yn": None,
        "include_in_deposit_rule_yn": None,
        "adj_trx_code": None
    }

    # Merge valid options from the group (Level 0)
    patch_options(tc_option_template, group.get("options", {}))

    # Merge valid options from the category (Level 2)
    patch_options(tc_option_template, category.get("options", {}))

    # Merge valid options from the itemizer if available (Level 3)
    if itemizer:
        item_code = itemizer.get("itemizer", 0) + category.get("seq", 0)
        patch_options(tc_option_template, itemizer.get("options", {}))

    else:
        item_code = category.get("seq", 0)

    trx_code_no = f'{item_code:02}'
    trx_description = f"{sequence['name'] if sequence['prefix'] else ''}{f' {identifier['name']}' if identifier['name'] else ''}{f' {description}' if description else ''}{f' {category['abbr']}' if category['abbr'] else ''}"
    # Initialize the transaction code model with basic information and merged options
    trx_code = {
        "trx_code": f'{sequence.get("sequence", "00")}{identifier.get("seq", "00")}{trx_code_no}',
        "description": trx_description.strip(),
        "tc_subgroup": tc_subgroup.get("tc_subgroup", "UNKNOWN"),
        "tc_group": tc_subgroup.get("tc_group", "UNKNOWN"),
        "tc_transaction_type": tc_subgroup.get("tc_transaction_type", "C"),
        "generates": None
    }

    trx_code.update(tc_option_template)
    return trx_code


def create_categories(categories, sequence):
    """
    Generates a list of category models from the given sequence data.
    
    Args:
        categories (dict): The dictionary of available categories.
        sequence (dict): The sequence data containing category codes.
        
    Returns:
        list: A list of dictionaries representing the categories with roles.
    """
    _categories = []
    for cat in sequence.get("categories", []):
        category = categories.get(cat["code"], {}).copy()
        if not category:
            raise ValueError(f"Category code '{cat['code']}' not found in categories")
        category["role"] = cat.get("role", "")
        _categories.append(category)
    return _categories


def create_tc_generate(group, category, trx_code):

    # Define allowed options for the generates
    tax_option_template = {
        "amount":None,
        "percentage":None,
        "percentage_base_code":None,
        "udf_function":None,
        "calculation_sequence":None,
        "result_included_in_sum_array":None
    }

    # Merge valid options from the group (Level 0)
    patch_options(tax_option_template, group.get("options", {}))

    # Merge valid options from the category (Level 2)
    patch_options(tax_option_template, category.get("options", {}))

    # create generate record
    generate = {
        "tc_group": trx_code["tc_group"],
        "tc_subgroup":trx_code["tc_subgroup"],
        "trx_code":trx_code["trx_code"]
    }

    generate.update(tax_option_template)
    return generate


def patch_options(template, options):
    patch_options = {k: v for k, v in options.items() if k in template and v is not None}
    template.update(patch_options)