
from query import export_tc_groups, export_tc_subgroups, export_tc_codes,export_tc_generates

def export_to_sql(file_path, resort, tc_groups, tc_subgroups, tc_codes):
    """
    Exports SQL scripts to a file for transaction code groups, subgroups, codes, and generates.

    Args:
        file_path (str): The path to the output SQL file.
        resort (str): The resort name or identifier.
        tc_groups (iterable): An iterable of transaction code groups.
        tc_subgroups (iterable): An iterable of transaction code subgroups.
        tc_codes (iterable): An iterable of transaction codes.
    """
    header = """\
/***************
THIS IS AN AUTO GENERATED FILE,
DEVELOPED AND CREATED BY : MOHAMED SHAIF HASSAN
COMPANY : XKYERON 

***************/

"""

    set_define_off = "SET DEFINE OFF;\n"
    section_headers = {
        "groups": "-- Transaction Code Groups Import Scripts \n",
        "subgroups": "-- Transaction Code Subgroups Import Scripts \n",
        "codes": "-- Transaction Code Import Scripts \n",
        "generates": "-- Transaction Code Generates Import Scripts \n"
    }

    with open(file_path, "w") as file:
        # Write header and initial setup
        file.write(header)
        file.write(set_define_off)

        # Write Transaction Code Groups
        file.write(section_headers["groups"])
        for query in export_tc_groups(resort, tc_groups):
            file.write(query)

        # Write Transaction Code Subgroups
        file.write(section_headers["subgroups"])
        for query in export_tc_subgroups(resort, tc_subgroups):
            file.write(query)

        # Write Transaction Codes
        file.write(section_headers["codes"])
        for query in export_tc_codes(resort, tc_codes):
            file.write(query)

        # Write Transaction Code Generates
        file.write(section_headers["generates"])
        for query in export_tc_generates(resort, tc_codes):
            file.write(query)

        # Finalize file with a termination symbol
        file.write("/")

