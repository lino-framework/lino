from lino import dd
pcsw = dd.resolve_app('pcsw')
users = dd.resolve_app('users')
alicia = users.User.objects.get(username='alicia')
root = users.User.objects.get(username='root')
pg = pcsw.PersonGroup.objects.get(pk=1)

ar = pcsw.CoachingsByUser.request(master_instance=alicia)
print ar.to_rst()
print "%d rows" % ar.get_total_count()

ar = pcsw.MyClientsByGroup.request(
    user=root,subst_user=alicia,
    master_instance=pg)
print ar.to_rst('name_column national_id address_column')
print "%d rows" % ar.get_total_count()

