

def export_tc_groups(resort, groups):

    # Base model for the TC$_GROUPS table
    base_model = {
        "resort": resort,
        "ind_revenue_gp": "N",
        "tc_group": None,
        "description": None,
        "tc_transaction_type": None,
        "class_1_mandatory_yn": "N",
        "class_2_mandatory_yn": "N",
        "insert_user": 2,
        "insert_date": "SYSDATE",
        "update_user": 2,
        "update_date": "SYSDATE",
        "order_by": None
    }

    return generate_query(base_model, groups, "TC$_GROUPS")
    # export_data(base_model, groups, "tc_groups_import.sql", "TC$_GROUPS")


def export_tc_subgroups(resort, subgroups):

    # Base model for the TC$_SUBGROUPS table
    base_model = {
        "resort": resort,
        "tc_group": None,
        "tc_subgroup": None,
        "description": None,
        "tc_transaction_type": None,
        "class_1_mandatory_yn": None,
        "class_2_mandatory_yn": None,
        "result_included_in_sum_array": None,
        "insert_user": 2,
        "insert_date": "SYSDATE",
        "update_user": 2,
        "update_date": "SYSDATE",
        "ind_revenue_gp": None,
        "tax_yn": "N",
        "sub_gp_type": None,
        "internal_yn": None,
        "order_by": None,
        "gp_points_redemption_yn": "N",
        "frequent_flyer_yn": "N"
    }
    
    return generate_query(base_model, subgroups, "TC$_SUBGROUPS")
    #export_data(base_model, subgroups, "tc_subgroups_import.sql", "TC$_SUBGROUPS")



def export_tc_codes(resort, tc_codes):

    base_model = {
        "resort": resort,
        "tc_group": None,
        "tc_subgroup": None,
        "trx_code": None,
        "tcl_code_dflt_cl1": None,
        "tcl_code_dflt_cl2": None,
        "class_1_mandatory_yn": None,
        "class_2_mandatory_yn": None,
        "description": None,
        "tc_transaction_type": "C",
        "is_manual_post_allowed": None,
        "result_included_in_sum_array": None,
        "insert_user": 2,
        "insert_date": "SYSDATE",
        "update_user": 2,
        "update_date": "SYSDATE",
        "cc_type": None,
        "commission": 0,
        "cc_code": None,
        "currency": None,
        "ind_billing": None,
        "ind_ar": None,
        "ind_revenue_gp": None,
        "adj_trx_code": None,
        "ind_cash": None,
        "arrange_code": None,
        "expense_folio": None,
        "group_folio": None,
        "deferred_yn": "N",
        "ind_deposit_yn": None,
        "rev_gp_id": None,
        "rev_bucket_id": None,
        "ar_name_id": None,
        "trx_code_type": "C",
        "frequent_flyer_yn": "N",
        "tax_inclusive_yn": "N",
        "crs_tax_desc": None,
        "tax_code_no": None,
        "export_bucket": None,
        "inh_sales_yn": "N",
        "inh_pay_yn": "N",
        "inh_deposit_yn": "N",
        "fiscal_trx_code_type": None,
        "comp_yn": "N",
        "default_price": None,
        "inactive_date": None,
        "payment_tax_invoice_yn": "N",
        "internal_yn": "N",
        "fiscal_payment_yn": "N",
        "comp_nights_yn": "N",
        "rotation_rev_yn": "N",
        "owner_rev_yn": "N",
        "check_no_mandatory_yn": "N",
        "ded_owner_rev_yn": "N",
        "non_taxable_yn": "N",
        "comp_payment_yn": "N",
        "min_amt": None,
        "max_amt": None,
        "trx_service_type": None,
        "daily_plan_folio": None,
        "trx_code_display": None,
        "include_in_deposit_rule_yn": "N",
        "include_in_8300_yn": "N",
        "manual_post_covers_yn": "N",
        "round_factor_yn": "N",
        "deposit_posting_only_yn": "N",
        "trx_tax_type_code": None,
        "deposit_type": None,
        "gp_points_redemption_yn": "N",
        "external_payment_code": None,
    }
    
    return generate_query(base_model, tc_codes, "TRX$_CODES")
    # export_data(base_model, tc_codes, "tc_codes_import.sql", "TRX$_CODES")


def export_tc_generates(resort, tc_codes):

    base_model = {
        "id": "TRX_CLASS_RELATIONSHIP_ID.NEXTVAL",
        "resort": resort,
        "tc_group": None,
        "tc_subgroup":None,
        "trx_code":None,
        "tc_group_generator":None,
        "tc_subgroup_generator":None,
        "trx_code_generator":None,
        "tcl_code_generator":None,
        "tcr_type":"A",
        "amount":None,
        "percentage":None,
        "percentage_base_code":None,
        "udf_function":None,
        "calculation_sequence":None,
        "amount_from_schedule_yn":"N",
        "currency":None,
        "result_included_in_sum_array":None,
        "generated_printed_on_folio_yn":None,
        "name_tax_type":None,
        "udf_inverse":None,
        "stop_days":None,
        "adjustment_type":"N",
        "use_tax_bracket_yn":"N",
        "insert_user":2,
        "insert_date":"SYSDATE",
        "update_user":2,
        "update_date":"SYSDATE",
    }

    generates = [gen for tc in tc_codes if tc.get("generates") for gen in tc["generates"]]

    return generate_query(base_model, generates, "TRX_CLASS_RELATIONSHIPS")
    # export_data(base_model, generates, "tc_generates_import.sql", "TRX_CLASS_RELATIONSHIPS")


def update_model(base, updates):
    model = base.copy()  # Copy the base model to avoid modifying the original
    patch_model = {k: v for k, v in updates.items() if k in model and v is not None} 
    model.update(patch_model)
    return model


def generate_sql(model, TABLE):
    # Convert all field names to uppercase
    fields = ", ".join([key.upper() for key in model.keys()])
    values = ", ".join([f"'{v}'" if v is not None and v not in ('SYSDATE','TRX_CLASS_RELATIONSHIP_ID.NEXTVAL') else "null" if v is None else v for v in model.values()])
    return f"INSERT INTO {TABLE} ({fields}) VALUES ({values});\n"



def export_data(base_model, models, file_name, table_name):
    with open(file_name,"w") as file:
        file.write("SET DEFINE OFF;\n")
        for model in models:
            updated_model = update_model(base_model, model)
            sql_query = generate_sql(updated_model, table_name)
            file.write(sql_query)  # Or write to file

        file.write("/")


def generate_query(base_model, models, table_name):
    """
    Generates a list of SQL insert queries from the base model and additional models.

    Args:
        base_model (dict): The base model with default values.
        models (list of dict): A list of additional models to update the base model.
        table_name (str): The name of the table for the SQL insert queries.

    Returns:
        list: A list of SQL insert query strings.
    """
    return [generate_sql(update_model(base_model, model), table_name) for model in models]