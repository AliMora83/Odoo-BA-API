def migrate(cr, version):
    cr.execute("""
        DELETE FROM ir_module_module 
        WHERE name = 'bridging_api_account';
    """)
