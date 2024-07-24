def export_tc_groups(resort, groups):
    with open("tc_groups_import.sql","w") as file:
        file.write("SET DEFINE OFF;\n")
        for t in groups:
            query = f"Insert into TC$_GROUPS (RESORT,IND_REVENUE_GP,TC_GROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,ORDER_BY) values ('{resort}','N','{t["tc_group"]}','{t["description"]}','{t["tc_transaction_type"]}','N','N',2,SYSDATE,2,SYSDATE,{t["order_by"]});\n"
            file.write(query)

        file.write("/")


def export_tc_subgroups(resort, subgroups):
    
    with open("tc_subgroups_import.sql","w") as file:
        file.write("SET DEFINE OFF;\n")

        for t in subgroups:
            query = f"Insert into TC$_SUBGROUPS (RESORT,TC_GROUP,TC_SUBGROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,IND_REVENUE_GP,TAX_YN,SUB_GP_TYPE,INTERNAL_YN,ORDER_BY,GP_POINTS_REDEMPTION_YN,FREQUENT_FLYER_YN) values ('{resort}','{t["tc_group"]}','{t["tc_subgroup"]}','{t["description"]}','{t["tc_transaction_type"]}',null,null,null,2,SYSDATE,2,SYSDATE,null,'N',null,null,{t["order_by"]},'N','N');\n"
            file.write(query)

        file.write("/")



def export_tc_codes(resort, tc_codes):

    base_model = {
        "resort": resort,
        "tc_group": "x",
        "tc_subgroup": "x",
        "trx_code": "x",
        "tcl_code_dflt_cl1": None,
        "tcl_code_dflt_cl2": None,
        "class_1_mandatory_yn": None,
        "class_2_mandatory_yn": None,
        "description": "x",
        "tc_transaction_type": "c",
        "is_manual_post_allowed": None,
        "result_included_in_sum_array": None,
        "insert_user": 2,
        "insert_date": "sysdate",
        "update_user": 2,
        "update_date": "sysdate",
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
        "trx_code_type": "c",
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
    
    with open("tc_codes_import.sql", "w") as file:
        file.write("SET DEFINE OFF;\n")
        for tc in tc_codes:
            updated_model = update_model(base_model, tc)
            sql_query = generate_sql(updated_model, "TRX$_CODES")
            file.write(sql_query)  # Or write to file
        file.write("/")


def update_model(base, updates):
    model = base.copy()  # Copy the base model to avoid modifying the original
    patch_model = {k: v for k, v in updates.items() if k in model and v is not None} 
    model.update(patch_model)
    return model


def generate_sql(model, TABLE):
    # Convert all field names to uppercase
    fields = ", ".join([key.upper() for key in model.keys()])
    values = ", ".join([f"'{v}'" if v is not None and v != 'SYSDATE' else "null" if v is None else v for v in model.values()])
    return f"INSERT INTO {TABLE} ({fields}) VALUES ({values});\n"