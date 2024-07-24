import json

# Load the JSON payload
with open("payload.json", 'r') as file:
    data = json.load(file)

# Extract data from JSON
RESORT = data["resort"]
TC_GROUPS = {group["code"]: group for group in data["options"]["groups"]}
IDENTIFIERS = {identifier["no"]: identifier for identifier in data["options"]["identifiers"]}
CATEGORIES = {category["code"]: category for category in data["options"]["categories"]}
SEQUENCES = data["sequences"]

# Function to create subgroup code
def create_tc_subgroup(sequence, category):
    group = TC_GROUPS.get(category.get("defaultGroup"), TC_GROUPS[sequence["group"]])
    sequence_num = int(str(category["seq"])[:1])
    subgroup = {
        "seq": int(f"{sequence['sequence']}{sequence_num}"),
        "code": f"{sequence['sequence']}{category['code']}",
        "description": f"{sequence['name']} {category['description']}",
        "group": group["code"],
        "type": group["type"],
        "trxType" : group["trxType"]
    }
    return subgroup

# Function to generate transaction code
def create_tc_code(sequence, tc_subgroup, group_code, category, identifier, itemizer, description):
    item_code = itemizer + category["seq"]
    trx_code_no = f'{item_code:02}'
    trx_description = f"{sequence['name']}{f' {identifier['name']}' if identifier['name'] else ''}{f' {description}' if description else ''}{f' {category['abbr']}' if category['abbr'] else ''}"

    trx_code = {
        "code": f'{sequence["sequence"]}{identifier["seq"]}{trx_code_no}',
        "description": trx_description,
        "subGroup": tc_subgroup["code"],
        "group": group_code,
        "isRevenue": category["isRevenue"],
        "isManual": category["isManual"],
        "isCash": category["isCash"],
        "isDeposit": category["isDeposit"],
        "isAr": category["isAr"],
        "isPaid": category["isPaid"],
        "type": tc_subgroup["type"],
        "trxType" : tc_subgroup["trxType"],
        "tc_code_no": category["tax"]["no"] if category.get("tax") else ""
    }

    return trx_code

# Function to generate the list of categories
def create_categories(sequence):
    categories = []
    for cat in sequence["categories"]:
        category = CATEGORIES[cat["code"]]
        category["role"] = cat["role"]
        categories.append(category)
    return categories


TC_SUBGROUPS = []
TC_CODES = []

# Process sequences to generate transaction groups and codes
for sequence in SEQUENCES:
    # Create the list of categories based on attached category codes to sequence
    categories = create_categories(sequence)

    # Loop through list of Identifiers attached to the sequence
    for identifier_no in sequence["identifiers"]:
        identifier = IDENTIFIERS[identifier_no]
        generates = []

        # Iterate over each category which gives the transaction set
        for category in categories:
            # Create an associated subgroup for it 00AA format
            tc_subgroup = create_tc_subgroup(sequence, category)
            TC_SUBGROUPS.append(tc_subgroup)

            role = category["role"]

            if role == "multiply":
                # Loop through list itemizers attached to the sequence
                for itemizer in sequence["itemizers"]:
                    tc_code = create_tc_code(sequence, tc_subgroup, tc_subgroup["group"], category, identifier, itemizer["itemizer"], itemizer["description"])
                    tc_code["generates"] = generates
                    TC_CODES.append(tc_code)
            elif role == "generate":
                tc_code = create_tc_code(sequence, tc_subgroup, category["defaultGroup"], category, identifier, 0, category["description"])
                generate = category["tax"]
                generate["tc_code"] = tc_code["code"]
                generate["tc_subgroup"] = tc_code["subGroup"]
                generate["tc_group"] = tc_code["group"]
                generates.append(generate)
                TC_CODES.append(tc_code)
            else:
                tc_code = create_tc_code(sequence, tc_subgroup, category["defaultGroup"], category, identifier, 0, category["description"])
                TC_CODES.append(tc_code)


with open("query.sql","w") as file:
    file.write("SET DEFINE OFF;\n")
    for tc_group in TC_GROUPS.values():
        query = f"Insert into TC$_GROUPS (RESORT,IND_REVENUE_GP,TC_GROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,ORDER_BY) values ('{RESORT}','{tc_group["isRevenue"]}','{tc_group["code"]}','{tc_group["description"]}','{tc_group["type"]}','N','N',2,SYSDATE,2,SYSDATE,{tc_group["seq"]});\n"
        file.write(query)

    for tc_subgroup in TC_SUBGROUPS:
        query = f"Insert into TC$_SUBGROUPS (RESORT,TC_GROUP,TC_SUBGROUP,DESCRIPTION,TC_TRANSACTION_TYPE,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,IND_REVENUE_GP,TAX_YN,SUB_GP_TYPE,INTERNAL_YN,ORDER_BY,GP_POINTS_REDEMPTION_YN,FREQUENT_FLYER_YN) values ('{RESORT}','{tc_subgroup["group"]}','{tc_subgroup["code"]}','{tc_subgroup["description"]}','{tc_subgroup["type"]}',null,null,null,2,SYSDATE,2,SYSDATE,null,'N',null,null,{tc_subgroup["seq"]},'N','N');\n"
        file.write(query)

    for tc_code in TC_CODES:
        query = f"""Insert into TRX$_CODES (RESORT,TC_GROUP,TC_SUBGROUP,TRX_CODE,TCL_CODE_DFLT_CL1,TCL_CODE_DFLT_CL2,CLASS_1_MANDATORY_YN,CLASS_2_MANDATORY_YN,DESCRIPTION,TC_TRANSACTION_TYPE,IS_MANUAL_POST_ALLOWED,RESULT_INCLUDED_IN_SUM_ARRAY,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE,CC_TYPE,COMMISSION,CC_CODE,CURRENCY,IND_BILLING,IND_AR,IND_REVENUE_GP,ADJ_TRX_CODE,IND_CASH,ARRANGE_CODE,EXPENSE_FOLIO,GROUP_FOLIO,DEFERRED_YN,IND_DEPOSIT_YN,REV_GP_ID,REV_BUCKET_ID,AR_NAME_ID,TRX_CODE_TYPE,FREQUENT_FLYER_YN,TAX_INCLUSIVE_YN,CRS_TAX_DESC,TAX_CODE_NO,EXPORT_BUCKET,INH_SALES_YN,INH_PAY_YN,INH_DEPOSIT_YN,FISCAL_TRX_CODE_TYPE,COMP_YN,DEFAULT_PRICE,INACTIVE_DATE,PAYMENT_TAX_INVOICE_YN,INTERNAL_YN,FISCAL_PAYMENT_YN,COMP_NIGHTS_YN,ROTATION_REV_YN,OWNER_REV_YN,CHECK_NO_MANDATORY_YN,DED_OWNER_REV_YN,NON_TAXABLE_YN,COMP_PAYMENT_YN,MIN_AMT,MAX_AMT,TRX_SERVICE_TYPE,DAILY_PLAN_FOLIO,TRX_CODE_DISPLAY,INCLUDE_IN_DEPOSIT_RULE_YN,INCLUDE_IN_8300_YN,MANUAL_POST_COVERS_YN,ROUND_FACTOR_YN,DEPOSIT_POSTING_ONLY_YN,TRX_TAX_TYPE_CODE,DEPOSIT_TYPE,GP_POINTS_REDEMPTION_YN,EXTERNAL_PAYMENT_CODE) values ('{RESORT}','{tc_code["group"]}','{tc_code["subGroup"]}','{tc_code["code"]}',null,null,null,null,'{tc_code["description"]}','{tc_code["type"]}','{tc_code["isManual"]}',null,2,SYSDATE,2,SYSDATE,null,0,null,null,'N','N','Y',null,'N',null,null,null,'N','N',null,null,null,'{tc_code["trxType"]}','N','N',null,'',null,'N','N','N',null,'N',null,null,'N',null,'N','N',null,null,'N',null,'N','N',null,null,null,null,null,'Y',null,null,'N',null,null,null,'N',null);\n"""
        file.write(query)

    
    query = f"Insert into TRX_CLASS_RELATIONSHIPS (ID,RESORT,TC_GROUP,TC_SUBGROUP,TRX_CODE,TC_GROUP_GENERATOR,TC_SUBGROUP_GENERATOR,TRX_CODE_GENERATOR,TCL_CODE_GENERATOR,TCR_TYPE,AMOUNT,PERCENTAGE,PERCENTAGE_BASE_CODE,UDF_FUNCTION,CALCULATION_SEQUENCE,AMOUNT_FROM_SCHEDULE_YN,CURRENCY,RESULT_INCLUDED_IN_SUM_ARRAY,GENERATED_PRINTED_ON_FOLIO_YN,NAME_TAX_TYPE,UDF_INVERSE,STOP_DAYS,ADJUSTMENT_TYPE,USE_TAX_BRACKET_YN,INSERT_USER,INSERT_DATE,UPDATE_USER,UPDATE_DATE) values (TRX_CLASS_RELATIONSHIP_ID.nextval,'{RESORT}','SVC','20SC','20170','F&B','20RV','20101',null,'A',null,10,0,null,1,'N',null,'100',null,null,null,null,'N','N',2,SYSDATE,2,SYSDATE);"