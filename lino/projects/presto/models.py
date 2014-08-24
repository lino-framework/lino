def site_setup(site):
    site.modules.accounts.Accounts.set_detail_layout(
        """
        ref:10 name id:5
        seqno chart group type clearable
        ledger.MovementsByAccount
        """)

    site.modules.system.SiteConfigs.set_detail_layout(
        """
        site_company next_partner_id:10
        default_build_method 
        clients_account   sales_account     sales_vat_account
        suppliers_account purchases_account purchases_vat_account
        wages_account clearings_account
        max_auto_events default_event_type site_calendar
        """)
