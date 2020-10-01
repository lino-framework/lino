{# settings.SITE.diagnostic_report_rst() #}

Plugins
=======

{% for p in settings.SITE.installed_plugins -%}
- {{p.app_label}} : {{p}}
{% endfor %}
Config directories
==================

{% for cd in settings.SITE.confdirs.config_dirs -%}
- {{cd.name}}{% if cd.writeable %} [writeable] {% endif %}
{% endfor %}
